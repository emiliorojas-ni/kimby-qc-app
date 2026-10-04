// Main Application Controller for Embutidos Kimby In-Line QC & Traceability System

document.addEventListener('DOMContentLoaded', async () => {
    // DOM Elements
    const videoElem = document.getElementById('cameraFeed');
    const cameraPlaceholder = document.getElementById('cameraPlaceholder');
    const startCameraBtn = document.getElementById('btnStartCamera');
    const stopCameraBtn = document.getElementById('btnStopCamera');
    const captureBtn = document.getElementById('btnCapture');
    const fileInput = document.getElementById('fileInput');
    const btnUpload = document.getElementById('btnUpload');
    
    // Sample buttons
    const sampleButtonsContainer = document.getElementById('sampleButtons');
    
    // Previews & Canvases
    const rawPreviewCanvas = document.getElementById('rawPreviewCanvas');
    const processedPreviewCanvas = document.getElementById('processedPreviewCanvas');
    const filterSelect = document.getElementById('filterSelect');
    
    // Status & Pneumatic Arm Indicators
    const statusBanner = document.getElementById('statusBanner');
    const statusIcon = document.getElementById('statusIcon');
    const statusTitle = document.getElementById('statusTitle');
    const statusSubtitle = document.getElementById('statusSubtitle');
    const pneumaticArmBox = document.getElementById('pneumaticArmBox');
    const pneumaticArmStatus = document.getElementById('pneumaticArmStatus');
    const strobeAlert = document.getElementById('strobeAlert');

    // Metrics & Readouts
    const readoutLote = document.getElementById('readoutLote');
    const readoutVenc = document.getElementById('readoutVenc');
    const readoutConfidence = document.getElementById('readoutConfidence');
    const readoutTimestamp = document.getElementById('readoutTimestamp');
    const confidenceBar = document.getElementById('confidenceBar');

    // Counters
    const statTotal = document.getElementById('statTotal');
    const statPassed = document.getElementById('statPassed');
    const statRejected = document.getElementById('statRejected');
    const statRejectRate = document.getElementById('statRejectRate');

    // Log Table & Export
    const logTableBody = document.getElementById('logTableBody');
    const btnExportCSV = document.getElementById('btnExportCSV');
    const btnClearLogs = document.getElementById('btnClearLogs');

    // Config Inputs (Sensibilidad)
    const cfgThreshold = document.getElementById('cfgThreshold');
    const thresholdValDisplay = document.getElementById('thresholdValDisplay');
    const roiSelect = document.getElementById('roiSelect');

    // State Variables
    let mediaStream = null;
    let currentSourceImage = null;
    let currentSourceSample = null;
    let inspectionHistory = [];
    let stats = { total: 0, passed: 0, rejected: 0 };
    let lastDetectedLote = null;
    let lastDetectedVenc = null;

    // Initialize OCR
    window.qcOCREngine.init();

    // Threshold Slider Display
    if (cfgThreshold && thresholdValDisplay) {
        cfgThreshold.addEventListener('input', (e) => {
            thresholdValDisplay.textContent = e.target.value + '%';
            window.qcOCREngine.minConfidence = Number(e.target.value);
        });
    }

    // Setup Synthetic Samples
    const samples = window.kimbySampleGenerator.getSamples();
    sampleButtonsContainer.innerHTML = '';
    samples.forEach((sample, idx) => {
        const btn = document.createElement('button');
        btn.className = 'sample-chip';
        btn.innerHTML = `<strong>${sample.name}</strong><span>${sample.description}</span>`;
        btn.addEventListener('click', () => {
            loadSyntheticSample(sample);
        });
        sampleButtonsContainer.appendChild(btn);
    });

    function loadSyntheticSample(sample) {
        currentSourceSample = sample;
        const canvas = window.kimbySampleGenerator.generateCanvas(sample);
        currentSourceImage = canvas;
        
        // Show in raw canvas
        drawToRawCanvas(canvas);
        updateProcessedPreview();

        // Automatically trigger inspection for rapid testing
        runInspection();
    }

    // Camera Controls
    async function startCamera() {
        try {
            if (mediaStream) {
                stopCamera();
            }
            const constraints = {
                video: {
                    facingMode: { ideal: 'environment' },
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: false
            };
            mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
            videoElem.srcObject = mediaStream;
            videoElem.style.display = 'block';
            cameraPlaceholder.style.display = 'none';
            startCameraBtn.style.display = 'none';
            stopCameraBtn.style.display = 'inline-flex';
            captureBtn.disabled = false;
        } catch (err) {
            console.warn('getUserMedia failed:', err);
            alert('No se pudo acceder a la cámara en vivo (requiere HTTPS o permiso de navegador). Usa el botón "Tomar/Subir Foto" para usar la cámara nativa.');
        }
    }

    function stopCamera() {
        if (mediaStream) {
            mediaStream.getTracks().forEach(t => t.stop());
            mediaStream = null;
        }
        videoElem.style.display = 'none';
        cameraPlaceholder.style.display = 'flex';
        startCameraBtn.style.display = 'inline-flex';
        stopCameraBtn.style.display = 'none';
        captureBtn.disabled = true;
    }

    if (startCameraBtn) startCameraBtn.addEventListener('click', startCamera);
    if (stopCameraBtn) stopCameraBtn.addEventListener('click', stopCamera);

    // Native file input / mobile camera capture
    if (btnUpload) {
        btnUpload.addEventListener('click', () => fileInput.click());
    }

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const img = new Image();
        const url = URL.createObjectURL(file);
        img.onload = () => {
            currentSourceSample = null;
            currentSourceImage = img;
            drawToRawCanvas(img);
            updateProcessedPreview();
            runInspection();
            URL.revokeObjectURL(url);
        };
        img.src = url;
    });

    // Capture from Live Video
    if (captureBtn) {
        captureBtn.addEventListener('click', () => {
            if (!videoElem.srcObject) return;
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = videoElem.videoWidth || 640;
            tempCanvas.height = videoElem.videoHeight || 480;
            const tCtx = tempCanvas.getContext('2d');
            tCtx.drawImage(videoElem, 0, 0, tempCanvas.width, tempCanvas.height);
            
            currentSourceSample = null;
            currentSourceImage = tempCanvas;
            drawToRawCanvas(tempCanvas);
            updateProcessedPreview();
            runInspection();
        });
    }

    function getSelectedRoi() {
        if (roiSelect && roiSelect.value === 'full') {
            return null; // Search entire image
        }
        return { x: 0.05, y: 0.15, w: 0.9, h: 0.75 };
    }

    // Filter or ROI Change
    if (filterSelect) {
        filterSelect.addEventListener('change', () => {
            if (currentSourceImage) {
                updateProcessedPreview();
            }
        });
    }

    if (roiSelect) {
        roiSelect.addEventListener('change', () => {
            if (currentSourceImage) {
                drawToRawCanvas(currentSourceImage);
                updateProcessedPreview();
            }
        });
    }

    function drawToRawCanvas(source) {
        const sw = source.videoWidth || source.naturalWidth || source.width;
        const sh = source.videoHeight || source.naturalHeight || source.height;
        rawPreviewCanvas.width = sw;
        rawPreviewCanvas.height = sh;
        const ctx = rawPreviewCanvas.getContext('2d');
        ctx.drawImage(source, 0, 0);

        const roi = getSelectedRoi();
        if (roi) {
            ctx.strokeStyle = '#00ffcc';
            ctx.lineWidth = 4;
            ctx.strokeRect(sw * roi.x, sh * roi.y, sw * roi.w, sh * roi.h);
            ctx.fillStyle = '#00ffcc';
            ctx.font = 'bold 16px sans-serif';
            ctx.fillText('ZONA ROI (LOTE & CADUCIDAD)', sw * roi.x + 8, sh * roi.y - 8);
        } else {
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 3;
            ctx.strokeRect(4, 4, sw - 8, sh - 8);
            ctx.fillStyle = '#38bdf8';
            ctx.font = 'bold 14px sans-serif';
            ctx.fillText('ENCUADRE: FOTO COMPLETA (MODO CELULAR)', 12, 24);
        }
    }

    function updateProcessedPreview() {
        if (!currentSourceImage) return;
        const filter = filterSelect ? filterSelect.value : 'binarized';
        const roi = getSelectedRoi();
        const processed = window.visionProcessor.process(currentSourceImage, filter, roi);
        
        if (processed) {
            processedPreviewCanvas.width = processed.width;
            processedPreviewCanvas.height = processed.height;
            const ctx = processedPreviewCanvas.getContext('2d');
            ctx.drawImage(processed, 0, 0);
        }
    }

    // Inspection Pipeline
    async function runInspection() {
        if (!currentSourceImage) return;

        // Visual loading state
        setStatusLoading();

        // 1. Preprocess using Otsu binarization for the OCR engine
        const roi = getSelectedRoi();
        const ocrCanvas = window.visionProcessor.process(currentSourceImage, 'binarized', roi);

        // 2. Perform OCR recognition and Rule Evaluation
        const result = await window.qcOCREngine.recognize(ocrCanvas, currentSourceSample);

        // Cache last detected values
        lastDetectedLote = result.detectedLote;
        lastDetectedVenc = result.detectedVenc;

        // 3. Render Output
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0]; // HH:MM:SS
        const dateStr = now.toLocaleDateString();
        const fullTimestamp = `${dateStr} ${timeStr}`;

        readoutLote.textContent = result.detectedLote || 'NO DETECTADO';
        readoutVenc.textContent = result.detectedVenc || 'NO DETECTADO';
        readoutConfidence.textContent = `${result.confidence}%`;
        confidenceBar.style.width = `${result.confidence}%`;
        readoutTimestamp.textContent = fullTimestamp;

        // Telemetry readouts for real OCR verification
        const ocrEngineName = document.getElementById('ocrEngineName');
        const ocrTime = document.getElementById('ocrTime');
        const rawOcrText = document.getElementById('rawOcrText');
        if (ocrEngineName && result.engine) ocrEngineName.textContent = result.engine;
        if (ocrTime && result.inferenceTimeMs !== undefined) ocrTime.textContent = `Latencia: ${result.inferenceTimeMs} ms`;
        if (rawOcrText) rawOcrText.textContent = result.rawText.trim() || '(Ningún carácter alfanumérico detectado)';

        // Color confidence bar
        if (result.confidence >= 85) {
            confidenceBar.style.backgroundColor = '#10b981'; // Green
        } else if (result.confidence >= 60) {
            confidenceBar.style.backgroundColor = '#f59e0b'; // Amber
        } else {
            confidenceBar.style.backgroundColor = '#ef4444'; // Red
        }

        const isApproved = result.evaluation.status === 'APPROVED';

        if (isApproved) {
            handleApproved(result, fullTimestamp);
        } else {
            handleRejected(result, fullTimestamp);
        }

        // Update statistics
        stats.total++;
        if (isApproved) stats.passed++;
        else stats.rejected++;
        updateStats();

        // Add to history log table
        addLogEntry({
            timestamp: fullTimestamp,
            status: isApproved ? 'APROBADO' : 'RECHAZADO',
            lote: result.detectedLote || 'N/A',
            venc: result.detectedVenc || 'N/A',
            confidence: result.confidence,
            reason: result.evaluation.reasonMsg,
            actuator: isApproved ? 'Cinta continua' : 'Brazo neumático'
        });
    }

    function setStatusLoading() {
        statusBanner.className = 'status-banner loading';
        statusIcon.innerHTML = '<div class="spinner"></div>';
        statusTitle.textContent = 'PROCESANDO INSPECCIÓN...';
        statusSubtitle.textContent = 'Analizando matriz de caracteres térmicos y contraste en film plástico...';
        pneumaticArmBox.className = 'actuator-box idle';
        pneumaticArmStatus.textContent = 'LISTO (STANDBY)';
    }

    function handleApproved(result, timestamp) {
        statusBanner.className = 'status-banner approved';
        statusIcon.innerHTML = '✔';
        statusTitle.textContent = 'PRODUCTO APROBADO (100% LEGIBLE)';
        statusSubtitle.textContent = result.evaluation.reasonMsg;

        pneumaticArmBox.className = 'actuator-box idle';
        pneumaticArmStatus.innerHTML = '<strong>PASO LIBRE:</strong> Cinta transportadora activa (Sin descarte).';

        window.industrialAudio.playPass();
        if (window.innerWidth < 992) {
            statusBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    function handleRejected(result, timestamp) {
        statusBanner.className = 'status-banner rejected';
        statusIcon.innerHTML = '✖';
        statusTitle.textContent = '¡PRODUCTO DESCARTADO!';
        statusSubtitle.textContent = `[${timestamp}] - MOTIVO: ${result.evaluation.reasonMsg}`;

        // Activate pneumatic arm actuator alert
        pneumaticArmBox.className = 'actuator-box active';
        pneumaticArmStatus.innerHTML = `
            <strong>SEÑAL DE DISPARO AL BRAZO NEUMÁTICO:</strong><br>
            <span class="pulse-code">Pulso PLC 24V DC activado a las ${timestamp.split(' ')[1]}</span><br>
            <em>Producto eyectado hacia el contenedor de rechazo de calidad Kimby.</em>
        `;

        // Industrial buzzer
        window.industrialAudio.playReject();

        // Strobe alert effect
        triggerStrobe();

        if (window.innerWidth < 992) {
            statusBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }

    function triggerStrobe() {
        strobeAlert.classList.add('flash');
        setTimeout(() => {
            strobeAlert.classList.remove('flash');
        }, 1200);
    }

    function updateStats() {
        statTotal.textContent = stats.total;
        statPassed.textContent = stats.passed;
        statRejected.textContent = stats.rejected;
        const rate = stats.total > 0 ? ((stats.rejected / stats.total) * 100).toFixed(1) : '0.0';
        statRejectRate.textContent = `${rate}%`;
    }

    function addLogEntry(entry) {
        inspectionHistory.unshift(entry);
        renderLogs();
    }

    function renderLogs() {
        logTableBody.innerHTML = '';
        inspectionHistory.slice(0, 50).forEach(item => {
            const tr = document.createElement('tr');
            const badgeClass = item.status === 'APROBADO' ? 'badge-pass' : 'badge-reject';
            tr.innerHTML = `
                <td>${item.timestamp}</td>
                <td><span class="badge ${badgeClass}">${item.status}</span></td>
                <td><code>${item.lote}</code></td>
                <td><code>${item.venc}</code></td>
                <td><strong>${item.confidence}%</strong></td>
                <td>${item.reason}</td>
                <td>${item.actuator}</td>
            `;
            logTableBody.appendChild(tr);
        });
    }

    // Export to CSV
    if (btnExportCSV) {
        btnExportCSV.addEventListener('click', () => {
            if (inspectionHistory.length === 0) {
                alert('No hay registros en la bitácora para exportar.');
                return;
            }
            const headers = ['Fecha y Hora', 'Estado', 'Lote Detectado', 'Caducidad Detectada', 'Legibilidad (%)', 'Motivo', 'Actuador'];
            const rows = inspectionHistory.map(h => [
                `"${h.timestamp}"`,
                `"${h.status}"`,
                `"${h.lote}"`,
                `"${h.venc}"`,
                `"${h.confidence}%"`,
                `"${h.reason.replace(/"/g, '""')}"`,
                `"${h.actuator}"`
            ]);
            const csvContent = 'data:text/csv;charset=utf-8,\uFEFF' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', encodedUri);
            link.setAttribute('download', `Kimby_Control_Calidad_${Date.now()}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }

    if (btnClearLogs) {
        btnClearLogs.addEventListener('click', () => {
            if (confirm('¿Deseas reiniciar la bitácora de inspección y los contadores?')) {
                inspectionHistory = [];
                stats = { total: 0, passed: 0, rejected: 0 };
                updateStats();
                renderLogs();
            }
        });
    }

    function showToast(msg) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }

    // Auto-load first sample on start so user sees interface populated!
    setTimeout(() => {
        loadSyntheticSample(samples[0]);
    }, 600);
});
