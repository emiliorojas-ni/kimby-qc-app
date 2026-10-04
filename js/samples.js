// Realistic Kimby Packaging Samples Generator
// Generates synthetic test labels simulating conveyor belt products

class KimbySampleGenerator {
    constructor() {
        this.samples = [
            {
                id: 'sample_ok',
                name: '1. Etiqueta Conforme (100% Legible)',
                description: 'Impresión térmica nítida. Lote y caducidad válidos.',
                expected: 'PASS',
                loteText: 'LOTE: KMB-2026-A01',
                vencText: 'VENC: 15/12/2026',
                blur: 0,
                noise: false,
                glare: false,
                missingPixels: 0
            },
            {
                id: 'sample_blurry',
                name: '2. Falla Cabezal Térmico (Ilegible / Borroso)',
                description: 'Cabezal con pines quemados o sucios: tinta corrida y texto desvanecido.',
                expected: 'REJECT_ILLEGIBLE',
                loteText: 'LOTE: KMB-2026-A01',
                vencText: 'VENC: 15/12/2026',
                blur: 7.5,
                noise: true,
                glare: false,
                missingPixels: 0.65
            },
            {
                id: 'sample_wrong_date',
                name: '3. Lote/Fecha Discrepante (Expirada)',
                description: 'Texto nítido pero el lote o fecha no corresponden al turno actual.',
                expected: 'REJECT_MISMATCH',
                loteText: 'LOTE: KMB-2023-Z88',
                vencText: 'VENC: 10/02/2024',
                blur: 0,
                noise: false,
                glare: false,
                missingPixels: 0
            },
            {
                id: 'sample_wrinkle',
                name: '4. Arruga en Film Plástico y Reflejo',
                description: 'Deformación física de la envoltura plástica que oculta dígitos.',
                expected: 'REJECT_CONFIDENCE',
                loteText: 'LOTE: KMB-2026-A01',
                vencText: 'VENC: 15/12/2026',
                blur: 2,
                noise: true,
                glare: true,
                missingPixels: 0.35
            }
        ];
    }

    getSamples() {
        return this.samples;
    }

    generateCanvas(sampleConfig, width = 640, height = 480) {
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');

        // Background: Plastic sausage casing (red/amber packaging with glossy highlights)
        const bgGrad = ctx.createLinearGradient(0, 0, width, height);
        bgGrad.addColorStop(0, '#8c1616');
        bgGrad.addColorStop(0.5, '#ab1d1d');
        bgGrad.addColorStop(1, '#660e0e');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, width, height);

        // Kimby Branding Header
        ctx.save();
        ctx.fillStyle = '#f6d32d'; // Yellow ribbon
        ctx.fillRect(20, 20, width - 40, 70);

        ctx.fillStyle = '#b71c1c';
        ctx.font = 'bold 36px "Segoe UI", Arial, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('EMBUTIDOS KIMBY', width / 2, 60);

        ctx.fillStyle = '#ffffff';
        ctx.font = '16px "Segoe UI", Arial, sans-serif';
        ctx.fillText('SALCHICHAS TRADICIONALES - CALIDAD SUPREMA 500g', width / 2, 82);
        ctx.restore();

        // White thermal print area / label box
        const lx = 80;
        const ly = 130;
        const lw = width - 160;
        const lh = 280;

        ctx.save();
        ctx.fillStyle = '#f8f9fa';
        ctx.shadowColor = 'rgba(0,0,0,0.35)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 4;
        ctx.shadowOffsetY = 4;
        ctx.fillRect(lx, ly, lw, lh);
        ctx.restore();

        // Subtitle inside label
        ctx.fillStyle = '#333333';
        ctx.font = '600 15px "Segoe UI", Arial, sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText('CONTROL DE CALIDAD & TRAZABILIDAD (LÍNEA 02)', lx + 20, ly + 35);

        // Barcode decorative simulation
        ctx.fillStyle = '#111111';
        let barX = lx + 20;
        for (let b = 0; b < 40; b++) {
            const bw = (b % 3 === 0) ? 4 : (b % 2 === 0 ? 2 : 1);
            ctx.fillRect(barX, ly + 55, bw, 35);
            barX += bw + 3;
        }

        // Dedicated Thermal Jet Ink Area
        const inkBoxX = lx + 20;
        const inkBoxY = ly + 110;
        const inkBoxW = lw - 40;
        const inkBoxH = 140;

        ctx.strokeStyle = '#cccccc';
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 4]);
        ctx.strokeRect(inkBoxX, inkBoxY, inkBoxW, inkBoxH);
        ctx.setLineDash([]);

        ctx.fillStyle = '#888888';
        ctx.font = '11px monospace';
        ctx.fillText('ZONA DE IMPRESIÓN TÉRMICA EN LÍNEA', inkBoxX + 10, inkBoxY + 20);

        // Render Thermal Inkjet / Dot-Matrix Text
        ctx.save();
        if (sampleConfig.blur > 0) {
            ctx.filter = `blur(${sampleConfig.blur}px)`;
        }

        ctx.fillStyle = '#0a0a0a';
        ctx.font = 'bold 32px "Courier New", monospace';
        ctx.letterSpacing = '3px';

        const textX = inkBoxX + 25;
        const loteY = inkBoxY + 65;
        const vencY = inkBoxY + 115;

        ctx.fillText(sampleConfig.loteText, textX, loteY);
        ctx.fillText(sampleConfig.vencText, textX, vencY);
        ctx.restore();

        // Simulate defective thermal print head (missing vertical pin lines)
        if (sampleConfig.missingPixels > 0) {
            ctx.save();
            ctx.fillStyle = '#f8f9fa';
            const missingP = Math.floor(sampleConfig.missingPixels * 10);
            for (let m = 0; m < missingP; m++) {
                const mx = inkBoxX + 30 + m * 40;
                ctx.fillRect(mx, inkBoxY + 30, 18, 100);
            }
            ctx.restore();
        }

        // Simulate wrinkle and specular glare reflection on packaging
        if (sampleConfig.glare) {
            ctx.save();
            const glareGrad = ctx.createLinearGradient(0, ly, width, ly + lh);
            glareGrad.addColorStop(0.3, 'rgba(255,255,255,0)');
            glareGrad.addColorStop(0.5, 'rgba(255,255,255,0.85)');
            glareGrad.addColorStop(0.7, 'rgba(255,255,255,0)');
            ctx.fillStyle = glareGrad;
            ctx.beginPath();
            ctx.moveTo(lx, ly + 80);
            ctx.lineTo(lx + lw, ly + 20);
            ctx.lineTo(lx + lw, ly + 70);
            ctx.lineTo(lx, ly + 130);
            ctx.closePath();
            ctx.fill();

            // Wrinkle distortion line
            ctx.strokeStyle = 'rgba(0,0,0,0.5)';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(lx + 40, ly + 60);
            ctx.bezierCurveTo(lx + 120, ly + 140, lx + 200, ly + 90, lx + 300, ly + 160);
            ctx.stroke();
            ctx.restore();
        }

        return canvas;
    }
}

window.kimbySampleGenerator = new KimbySampleGenerator();
