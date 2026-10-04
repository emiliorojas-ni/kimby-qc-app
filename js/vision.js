// Vision Preprocessing Module for In-Line Industrial Packaging & Real-World Camera Photos
// Prepares video frames, smartphone captures, and physical printed labels for robust OCR.

class VisionProcessor {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });
    }

    // Helper to rotate a canvas by 90, 180, or 270 degrees
    rotateCanvas(sourceCanvas, degrees) {
        const rad = (degrees * Math.PI) / 180;
        const rotated = document.createElement('canvas');
        const rCtx = rotated.getContext('2d', { willReadFrequently: true });

        if (degrees === 90 || degrees === 270) {
            rotated.width = sourceCanvas.height;
            rotated.height = sourceCanvas.width;
        } else {
            rotated.width = sourceCanvas.width;
            rotated.height = sourceCanvas.height;
        }

        rCtx.save();
        rCtx.translate(rotated.width / 2, rotated.height / 2);
        rCtx.rotate(rad);
        rCtx.drawImage(sourceCanvas, -sourceCanvas.width / 2, -sourceCanvas.height / 2);
        rCtx.restore();

        return rotated;
    }

    // Process an image source (Image, Video, Canvas) into a preprocessed canvas
    process(source, mode = 'contrast', roi = null) {
        let sw = source.videoWidth || source.naturalWidth || source.width;
        let sh = source.videoHeight || source.naturalHeight || source.height;

        if (!sw || !sh) {
            console.error('Invalid source dimensions', sw, sh);
            return null;
        }

        // 1. Calculate ROI in original coordinates
        let sx = 0, sy = 0, sWidth = sw, sHeight = sh;
        if (roi) {
            sx = Math.round(roi.x * sw);
            sy = Math.round(roi.y * sh);
            sWidth = Math.round(roi.w * sw);
            sHeight = Math.round(roi.h * sh);
        }

        // 2. Intelligent Auto-Scaling:
        // High-res phone captures (3000-4000px) degrade OCR accuracy (character height > 150px)
        // and cause memory pressure. Scale down to optimal sweet spot (max 1400px).
        const maxDim = 1400;
        let scale = 1;
        if (Math.max(sWidth, sHeight) > maxDim) {
            scale = maxDim / Math.max(sWidth, sHeight);
        }
        const destW = Math.round(sWidth * scale);
        const destH = Math.round(sHeight * scale);

        this.canvas.width = destW;
        this.canvas.height = destH;

        // Draw and scale to destination canvas
        this.ctx.drawImage(source, sx, sy, sWidth, sHeight, 0, 0, destW, destH);

        if (mode === 'original') {
            return this.canvas;
        }

        const imgData = this.ctx.getImageData(0, 0, destW, destH);
        const data = imgData.data;
        const totalPixels = destW * destH;

        // 3. Grayscale conversion + Histogram for Percentile Contrast Stretching
        const gray = new Uint8Array(totalPixels);
        const hist = new Int32Array(256);

        for (let i = 0; i < totalPixels; i++) {
            const idx = i * 4;
            // Standard luminance weights
            const lum = Math.round(0.299 * data[idx] + 0.587 * data[idx + 1] + 0.114 * data[idx + 2]);
            gray[i] = lum;
            hist[lum]++;
        }

        // Robust percentile boundaries (2% and 98%) to eliminate hot glare and deep shadows
        let p2 = 0, p98 = 255;
        const targetP2 = totalPixels * 0.02;
        const targetP98 = totalPixels * 0.98;
        let cum = 0;
        for (let t = 0; t < 256; t++) {
            cum += hist[t];
            if (cum >= targetP2 && p2 === 0) p2 = t;
            if (cum >= targetP98) {
                p98 = t;
                break;
            }
        }
        if (p98 <= p2) {
            p2 = 0;
            p98 = 255;
        }

        const range = p98 - p2 || 1;
        const contrast = new Uint8Array(totalPixels);
        for (let i = 0; i < totalPixels; i++) {
            const val = ((gray[i] - p2) / range) * 255;
            contrast[i] = Math.min(255, Math.max(0, Math.round(val)));
        }

        if (mode === 'grayscale') {
            for (let i = 0; i < totalPixels; i++) {
                const idx = i * 4;
                const g = gray[i];
                data[idx] = g;
                data[idx + 1] = g;
                data[idx + 2] = g;
            }
            this.ctx.putImageData(imgData, 0, 0);
            return this.canvas;
        }

        if (mode === 'contrast') {
            // High-Contrast Grayscale (Optimal for Tesseract LSTM Engine on Real Paper)
            for (let i = 0; i < totalPixels; i++) {
                const idx = i * 4;
                const c = contrast[i];
                data[idx] = c;
                data[idx + 1] = c;
                data[idx + 2] = c;
            }
            this.ctx.putImageData(imgData, 0, 0);
            return this.canvas;
        }

        // 4. Otsu Global Threshold Binarization
        const contrastHist = new Int32Array(256);
        for (let i = 0; i < totalPixels; i++) {
            contrastHist[contrast[i]]++;
        }

        let sum = 0;
        for (let t = 0; t < 256; t++) sum += t * contrastHist[t];

        let sumB = 0;
        let wB = 0;
        let varMax = 0;
        let threshold = 128;

        for (let t = 0; t < 256; t++) {
            wB += contrastHist[t];
            if (wB === 0) continue;
            const wF = totalPixels - wB;
            if (wF === 0) break;

            sumB += t * contrastHist[t];
            const mB = sumB / wB;
            const mF = (sum - sumB) / wF;

            const varBetween = wB * wF * (mB - mF) * (mB - mF);
            if (varBetween > varMax) {
                varMax = varBetween;
                threshold = t;
            }
        }

        // Apply thresholding (Dark text on light background -> text 0, background 255)
        for (let i = 0; i < totalPixels; i++) {
            const idx = i * 4;
            const val = contrast[i] < threshold ? 0 : 255;
            data[idx] = val;
            data[idx + 1] = val;
            data[idx + 2] = val;
            data[idx + 3] = 255;
        }

        this.ctx.putImageData(imgData, 0, 0);
        return this.canvas;
    }
}

window.visionProcessor = new VisionProcessor();

