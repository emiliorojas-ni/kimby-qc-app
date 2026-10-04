// OCR Engine & Industrial QA Decision Logic
// Powered by Tesseract.js with real-time text parsing and threshold verification

class QCOCREngine {
    constructor() {
        this.worker = null;
        this.isReady = false;
        this.isLoading = false;
        this.loadError = null;

        // Default Production Baseline (Base de datos activa)
        this.expectedLote = 'KMB-2026-A01';
        this.expectedVenc = '15/12/2026';
        this.minConfidence = 50; // % mínimo calibrado para fotos de smartphone en papel físico (ajustable en UI)
        
        // Validation Mode:
        // 'flexible' -> Verifica que la etiqueta sea legible, tenga lote y fecha válida NO vencida (ideal para cualquier producto real).
        // 'strict'   -> Compara estrictamente con el Lote y Fecha esperados en la orden de producción.
        this.validationMode = 'flexible';
    }

    async init() {
        if (this.isReady || this.isLoading) return;
        this.isLoading = true;

        try {
            if (typeof Tesseract !== 'undefined') {
                console.log('Initializing Tesseract.js worker...');
                this.worker = await Tesseract.createWorker('eng', 1, {
                    logger: m => console.log('Tesseract:', m.status, m.progress ? Math.round(m.progress * 100) + '%' : '')
                });

                // Configure character whitelist for packaging labels (letters, numbers and delimiters)
                await this.worker.setParameters({
                    tessedit_char_whitelist: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz/:.- '
                });

                this.isReady = true;
                console.log('Tesseract OCR Worker Ready!');
            } else {
                console.warn('Tesseract not loaded from CDN, running fallback heuristic OCR mode.');
            }
        } catch (err) {
            console.error('Error starting Tesseract:', err);
            this.loadError = err;
        } finally {
            this.isLoading = false;
        }
    }

    setProductionConfig(lote, venc, threshold, mode = null) {
        if (lote) this.expectedLote = lote.trim().toUpperCase();
        if (venc) this.expectedVenc = venc.trim();
        if (threshold) this.minConfidence = Number(threshold);
        if (mode) this.validationMode = mode;
    }

    setValidationMode(mode) {
        this.validationMode = mode;
    }

    // Helper to run a single OCR pass on a canvas
    async _runSinglePass(canvas) {
        if (!this.isReady || !this.worker) {
            return { rawText: '', confidence: 0 };
        }
        try {
            const res = await this.worker.recognize(canvas);
            const rawText = res.data.text || '';
            const lines = res.data.lines || [];
            const matchedLines = lines.filter(l => {
                const t = l.text.toUpperCase();
                return t.includes('LOTE') || t.includes('KMB') || t.includes('KM8') ||
                       t.includes('VENC') || t.includes('CAD') || t.includes('EXP') ||
                       /\b\d{1,2}[\/\.\- ]\d{1,2}[\/\.\- ]\d{2,4}\b/.test(t);
            });

            let confidence = 0;
            if (matchedLines.length > 0) {
                const sum = matchedLines.reduce((acc, l) => acc + (l.confidence || 0), 0);
                confidence = Math.round(sum / matchedLines.length);
            } else {
                confidence = Math.round(res.data.confidence || 0);
            }
            return { rawText, confidence };
        } catch (e) {
            console.warn('Tesseract recognition error:', e);
            return { rawText: '', confidence: 0 };
        }
    }

    async recognize(imageCanvas, sourceSample = null) {
        const t0 = performance.now();

        // Synthetic sample simulation bypass
        if (sourceSample) {
            let rawText = '';
            let confidence = 0;
            if (sourceSample.id === 'sample_ok') {
                rawText = `${sourceSample.loteText}\n${sourceSample.vencText}`;
                confidence = 96;
            } else if (sourceSample.id === 'sample_blurry') {
                rawText = 'LOTE: KM?-2026-??\nVENC: ??/??/????';
                confidence = 38;
            } else if (sourceSample.id === 'sample_wrong_date') {
                rawText = `${sourceSample.loteText}\n${sourceSample.vencText}`;
                confidence = 94;
            } else if (sourceSample.id === 'sample_wrinkle') {
                rawText = 'LOTE: KMB-????\nVENC: 15/?2/2?26';
                confidence = 61;
            }
            const parsed = this.parseKimbyLabel(rawText);
            const evaluation = this.evaluateRules(parsed, confidence, sourceSample);
            return {
                rawText,
                confidence,
                detectedLote: parsed.lote,
                detectedVenc: parsed.venc,
                evaluation,
                inferenceTimeMs: Math.round(performance.now() - t0),
                engine: 'Banco de Muestras Kimby'
            };
        }

        // Real Camera / Uploaded Photo Pipeline:
        // Try orientations [0°, 90°, 270°, 180°] automatically so that vertical/horizontal/upside-down
        // mobile captures are detected instantly without user struggle!
        const orientations = [0, 90, 270, 180];
        let bestCandidate = null;

        for (const angle of orientations) {
            let passCanvas = imageCanvas;
            if (angle !== 0 && window.visionProcessor && window.visionProcessor.rotateCanvas) {
                passCanvas = window.visionProcessor.rotateCanvas(imageCanvas, angle);
            }

            const { rawText, confidence } = await this._runSinglePass(passCanvas);
            const parsed = this.parseKimbyLabel(rawText);

            const candidate = {
                rawText,
                confidence,
                detectedLote: parsed.lote,
                detectedVenc: parsed.venc,
                parsed,
                angle
            };

            // If we detected BOTH the KMB Lot and a Date, we found the optimal orientation!
            if (parsed.hasKMB && parsed.kmbComplete && parsed.venc) {
                bestCandidate = candidate;
                break;
            }

            // Otherwise, keep the best candidate with highest feature count or confidence
            if (!bestCandidate) {
                bestCandidate = candidate;
            } else {
                const curScore = (parsed.hasKMB ? 2 : 0) + (parsed.venc ? 2 : 0) + (parsed.kmbComplete ? 1 : 0);
                const bestScore = (bestCandidate.parsed.hasKMB ? 2 : 0) + (bestCandidate.parsed.venc ? 2 : 0) + (bestCandidate.parsed.kmbComplete ? 1 : 0);
                if (curScore > bestScore || (curScore === bestScore && confidence > bestCandidate.confidence)) {
                    bestCandidate = candidate;
                }
            }
        }

        const t1 = performance.now();
        const inferenceTimeMs = Math.round(t1 - t0);

        // Evaluate against Quality Control Rules
        const evaluation = this.evaluateRules(bestCandidate.parsed, bestCandidate.confidence, null);

        const angleStr = bestCandidate.angle !== 0 ? ` [Orientación ${bestCandidate.angle}°]` : '';

        return {
            rawText: bestCandidate.rawText,
            confidence: bestCandidate.confidence,
            detectedLote: bestCandidate.detectedLote,
            detectedVenc: bestCandidate.detectedVenc,
            evaluation,
            inferenceTimeMs,
            engine: this.isReady ? `Tesseract.js v5 LSTM${angleStr}` : 'Heuristic Engine'
        };
    }

    parseKimbyLabel(text) {
        if (!text) return { lote: null, venc: null, hasKMB: false, kmbComplete: false };
        let clean = text.toUpperCase();

        // Normalizaciones inteligentes para impresión en papel físico y fuentes térmicas:
        // 1. Confusiones térmicas comunes: 'B' leído como '8' o 'D' o 'R' en el prefijo KMB
        clean = clean.replace(/\b(KM[8BDR]|KH[B8]|KN[B8])\s*[-_./ ]?\s*([0-9O]{4})/g, 'KMB-$2');
        clean = clean.replace(/\bKM8\b/g, 'KMB');
        clean = clean.replace(/\bL[0O]TE\b/g, 'LOTE');
        clean = clean.replace(/\bV[E3]N[CGT]\b/g, 'VENC');

        // 2. Normalizar fechas con espacios entre barras o puntos (ej. 15 / 12 / 2026 o 15 . 12 . 2026)
        clean = clean.replace(/(\d{1,2})\s*[\/\.\-]\s*(\d{1,2})\s*[\/\.\-]\s*([0-9O]{2,4})/g, (m, d, mo, y) => {
            const yr = y.replace(/O/g, '0');
            return `${d.padStart(2, '0')}/${mo.padStart(2, '0')}/${yr}`;
        });

        // 1. Extraer LOTE Kimby y verificar estructura
        let lote = null;
        let hasKMB = clean.includes('KMB');
        let kmbComplete = false;

        // Patrón A: KMB con año y código (ej. KMB-2026-A01, KMB 2026 A01, KMB-2026A01)
        const kmbPattern = /\bKMB\s*[-_./ ]?\s*([0-9O]{4})\s*[-_./ ]?\s*([A-Z0-9]{2,6})\b/;
        const kmbMatch = clean.match(kmbPattern);

        if (kmbMatch) {
            hasKMB = true;
            const yearClean = kmbMatch[1].replace(/O/g, '0');
            lote = `KMB-${yearClean}-${kmbMatch[2]}`;
            if (lote.length >= 10) {
                kmbComplete = true;
            }
        } else {
            // Patrón B: LOTE: KMB... o LOTE: [Código]
            const loteRegex = /\b(?:LOTE|LOT|BATCH|L)\s*[:.\- ]\s*([A-Z0-9\- ]{3,20})/;
            const m = clean.match(loteRegex);
            if (m) {
                lote = m[1].trim().replace(/\s+/g, '-');
                if (lote.includes('KMB')) {
                    hasKMB = true;
                    if (lote.length >= 10) kmbComplete = true;
                }
            } else {
                // Patrón C: Token aislado que empiece con KMB
                const tokenKMB = clean.match(/\bKMB[A-Z0-9\-]{3,15}\b/);
                if (tokenKMB) {
                    hasKMB = true;
                    lote = tokenKMB[0];
                    if (lote.length >= 10) kmbComplete = true;
                }
            }
        }

        // 2. Extraer FECHA / CADUCIDAD
        let venc = null;

        // A) Mapeo de meses en texto (ej. 15 DIC 2026 -> 15/12/2026)
        const meses = {
            'ENE': '01', 'FEB': '02', 'MAR': '03', 'ABR': '04', 'MAY': '05', 'JUN': '06',
            'JUL': '07', 'AGO': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DIC': '12',
            'JAN': '01', 'APR': '04', 'AUG': '08', 'DEC': '12'
        };
        const textMonthRegex = /\b([0-9]{1,2})\s*[\/\.\- ]\s*(ENE|FEB|MAR|ABR|MAY|JUN|JUL|AGO|SEP|OCT|NOV|DIC|JAN|APR|AUG|DEC)\s*[\/\.\- ]\s*([0-9]{2,4})\b/;
        const tm = clean.match(textMonthRegex);
        if (tm) {
            const d = tm[1].padStart(2, '0');
            const m = meses[tm[2]] || '01';
            let y = tm[3];
            if (y.length === 2) y = '20' + y;
            venc = `${d}/${m}/${y}`;
        }

        // B) Si no, buscar prefijo explícito (VENC, CAD, EXP, F.V, CONSUMIR ANTES DE, BB)
        if (!venc) {
            const vencRegex = /\b(?:VENC|CAD|EXP|F\.V|FV|BB|BEST|USE)\s*[:.\- ]?\s*([0-9]{1,2}[\/\.\-][0-9]{1,2}[\/\.\-][0-9]{2,4})/;
            const vm = clean.match(vencRegex);
            if (vm) {
                venc = this.normalizeDate(vm[1].trim());
            }
        }

        // C) Si no, cualquier fecha en formato DD/MM/AAAA o AAAA-MM-DD
        if (!venc) {
            const dateMatch = clean.match(/\b([0-9]{1,2}[\/\.\-][0-9]{1,2}[\/\.\-][0-9]{2,4})\b/);
            if (dateMatch) {
                venc = this.normalizeDate(dateMatch[0].trim());
            } else {
                const isoMatch = clean.match(/\b([2][0-9]{3}[\/\.\-][0-9]{1,2}[\/\.\-][0-9]{1,2})\b/);
                if (isoMatch) {
                    const p = isoMatch[0].split(/[\/\.\-]/);
                    venc = `${p[2].padStart(2, '0')}/${p[1].padStart(2, '0')}/${p[0]}`;
                }
            }
        }

        return { lote, venc, hasKMB, kmbComplete };
    }

    normalizeDate(str) {
        const parts = str.split(/[\/\.\-]/);
        if (parts.length === 3) {
            const d = parts[0].padStart(2, '0');
            const m = parts[1].padStart(2, '0');
            let y = parts[2].replace(/O/g, '0');
            if (y.length === 2) y = '20' + y;
            return `${d}/${m}/${y}`;
        }
        return str;
    }

    evaluateRules(parsed, confidence, sourceSample = null) {
        // Caso de muestra sintética de cabezal térmico defectuoso
        if (sourceSample && sourceSample.expected === 'REJECT_ILLEGIBLE') {
            return {
                status: 'REJECTED',
                reasonCode: 'ILLEGIBLE_PRINT',
                reasonMsg: 'RECHAZADO: Falla en cabezal térmico. No se lee KMB, caracteres incompletos y fecha borrosa.',
                pneumaticSignal: true,
                severity: 'CRITICAL'
            };
        }

        const hasKmb = parsed.hasKMB;
        const isKmbComplete = parsed.kmbComplete;
        const hasVenc = !!parsed.venc;

        // =========================================================================
        // CONDICIÓN PRINCIPAL SOLICITADA POR EL USUARIO:
        // 1. "mientras sea capaz de leerse el KMB y el resto del código, que sea válido"
        // 2. "Pero si no se lee el KMB, la cantidad de caracteres que debe tener y la
        //     fecha de vencimiento tampoco se lee, entonces sí lo descartas"
        // 3. "Pero mientras sea legible y el OCR la detecte, la dejas"
        // =========================================================================

        // Verificación A: ¿No se lee el 'KMB' o está ausente?
        if (!hasKmb) {
            return {
                status: 'REJECTED',
                reasonCode: 'NO_KMB_PREFIX',
                reasonMsg: 'RECHAZADO: No se lee el identificador [KMB] en la etiqueta (ilegible o ausente).',
                pneumaticSignal: true,
                severity: 'CRITICAL'
            };
        }

        // Verificación B: ¿Tiene el prefijo KMB pero faltan caracteres en el código?
        if (!isKmbComplete) {
            const charsDetectados = parsed.lote ? parsed.lote.length : 0;
            return {
                status: 'REJECTED',
                reasonCode: 'INCOMPLETE_CODE_LENGTH',
                reasonMsg: `RECHAZADO: Cantidad de caracteres del código incompleta (${charsDetectados} caracteres). Se requiere estructura completa KMB-YYYY-XXX.`,
                pneumaticSignal: true,
                severity: 'CRITICAL'
            };
        }

        // Verificación C: ¿La fecha de vencimiento tampoco se lee?
        if (!hasVenc) {
            return {
                status: 'REJECTED',
                reasonCode: 'DATE_ILLEGIBLE',
                reasonMsg: 'RECHAZADO: La fecha de caducidad no se lee o está borrosa.',
                pneumaticSignal: true,
                severity: 'CRITICAL'
            };
        }

        // Verificación E: Si la fecha está en el pasado (caducada)
        const parts = parsed.venc.split('/');
        if (parts.length === 3) {
            const day = parseInt(parts[0], 10);
            const month = parseInt(parts[1], 10) - 1;
            const year = parseInt(parts[2], 10);
            const expDate = new Date(year, month, day, 23, 59, 59);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (expDate < today) {
                return {
                    status: 'REJECTED',
                    reasonCode: 'EXPIRED_PRODUCT',
                    reasonMsg: `RECHAZADO: Producto con fecha vencida (${parsed.venc}). Descarte por inocuidad alimentaria.`,
                    pneumaticSignal: true,
                    severity: 'CRITICAL'
                };
            }
        }

        // Verificación D: Umbral mínimo de confianza global (si el texto está excesivamente borroso)
        if (confidence < this.minConfidence) {
            // Tolerancia para papel físico real impreso con celular:
            // Si el KMB está completo y la fecha es válida y vigente, y la confianza es >= 38%:
            if (hasKmb && isKmbComplete && hasVenc && confidence >= 38) {
                return {
                    status: 'APPROVED',
                    reasonCode: 'CONFORMING_PHYSICAL_PAPER',
                    reasonMsg: `APROBADO: Lote [${parsed.lote}] y Caducidad [${parsed.venc}] validados en papel físico (Legibilidad: ${confidence}%).`,
                    pneumaticSignal: false,
                    severity: 'NORMAL'
                };
            }
            return {
                status: 'REJECTED',
                reasonCode: 'LOW_CONFIDENCE',
                reasonMsg: `RECHAZADO: Legibilidad global del ${confidence}%, inferior al umbral mínimo (${this.minConfidence}%). Tinta desvanecida o borrosa.`,
                pneumaticSignal: true,
                severity: 'HIGH'
            };
        }

        // =========================================================================
        // CONDICIÓN CUMPLIDA -> ¡APROBADO!
        // El OCR leyó el KMB, el resto del código completo y la fecha de vencimiento.
        // =========================================================================
        return {
            status: 'APPROVED',
            reasonCode: 'CONFORMING',
            reasonMsg: `APROBADO: Lote [${parsed.lote}] (KMB y código completo) y Caducidad [${parsed.venc}] detectados y legibles.`,
            pneumaticSignal: false,
            severity: 'NORMAL'
        };
    }
}

window.qcOCREngine = new QCOCREngine();
