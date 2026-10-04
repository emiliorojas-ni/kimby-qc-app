// Vision Preprocessing Module for In-Line Industrial Packaging
// Prepares video frames or photos for fast, accurate OCR on shiny plastic films.

class VisionProcessor {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });
    }

    // Process an image source (Image, Video, Canvas) into a preprocessed canvas
    process(source, mode = 'binarized', roi = null) {
        let sw = source.videoWidth || source.naturalWidth || source.width;
        let sh = source.videoHeight || source.naturalHeight || source.height;

        if (!sw || !sh) {
            console.error('Invalid source dimensions', sw, sh);
            return null;
        }

        // If ROI is defined (normalized 0-1 coords: {x, y, w, h})
        let sx = 0, sy = 0, sWidth = sw, sHeight = sh;
        if (roi) {
            sx = Math.round(roi.x * sw);
            sy = Math.round(roi.y * sh);
            sWidth = Math.round(roi.w * sw);
            sHeight = Math.round(roi.h * sh);
        }

        // Resize canvas to ROI
        this.canvas.width = sWidth;
        this.canvas.height = sHeight;

        // Draw source to canvas
        this.ctx.drawImage(source, sx, sy, sWidth, sHeight, 0, 0, sWidth, sHeight);

        if (mode === 'original') {
            return this.canvas;
        }

        const imgData = this.ctx.getImageData(0, 0, sWidth, sHeight);
        const data = imgData.data;
        const totalPixels = sWidth * sHeight;

        // 1. Grayscale conversion + find min/max for auto-contrast
        let minL = 255;
        let maxL = 0;
        const gray = new Uint8Array(totalPixels);

        for (let i = 0; i < totalPixels; i++) {
            const idx = i * 4;
            // Standard luminance weights
            const lum = Math.round(0.299 * data[idx] + 0.587 * data[idx + 1] + 0.114 * data[idx + 2]);
            gray[i] = lum;
            if (lum < minL) minL = lum;
            if (lum > maxL) maxL = lum;
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

        // 2. Contrast Stretching / Normalization (Crucial for eliminating plastic glare)
        const range = maxL - minL || 1;
        const contrast = new Uint8Array(totalPixels);
        for (let i = 0; i < totalPixels; i++) {
            contrast[i] = Math.min(255, Math.max(0, Math.round(((gray[i] - minL) / range) * 255)));
        }

        if (mode === 'contrast') {
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

        // 3. Fast Otsu-like Global Threshold Binarization
        // Computes histogram
        const histogram = new Int32Array(256);
        for (let i = 0; i < totalPixels; i++) {
            histogram[contrast[i]]++;
        }

        let sum = 0;
        for (let t = 0; t < 256; t++) sum += t * histogram[t];

        let sumB = 0;
        let wB = 0;
        let wF = 0;
        let varMax = 0;
        let threshold = 128;

        for (let t = 0; t < 256; t++) {
            wB += histogram[t];
            if (wB === 0) continue;
            wF = totalPixels - wB;
            if (wF === 0) break;

            sumB += t * histogram[t];
            const mB = sumB / wB;
            const mF = (sum - sumB) / wF;

            const varBetween = wB * wF * (mB - mF) * (mB - mF);
            if (varBetween > varMax) {
                varMax = varBetween;
                threshold = t;
            }
        }

        // Apply thresholding (Text is dark on light background -> make text 0/black, background 255/white)
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
