// Web Audio API Synthesizer for Industrial Feedback
class IndustrialAudio {
    constructor() {
        this.ctx = null;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playPass() {
        try {
            this.init();
            if (!this.ctx) return;
            const now = this.ctx.currentTime;
            
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            
            osc.type = 'sine';
            osc.frequency.setValueAtTime(784, now); // G5
            osc.frequency.setValueAtTime(1046.5, now + 0.1); // C6
            
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
            
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            
            osc.start(now);
            osc.stop(now + 0.35);
        } catch (e) {
            console.warn('Audio playPass error:', e);
        }
    }

    playReject() {
        try {
            this.init();
            if (!this.ctx) return;
            const now = this.ctx.currentTime;
            
            // Industrial alarm buzzer (harsh dual pulse)
            [0, 0.18].forEach(offset => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(220, now + offset);
                osc.frequency.exponentialRampToValueAtTime(140, now + offset + 0.14);
                
                gain.gain.setValueAtTime(0.3, now + offset);
                gain.gain.exponentialRampToValueAtTime(0.01, now + offset + 0.14);
                
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                
                osc.start(now + offset);
                osc.stop(now + offset + 0.14);
            });
        } catch (e) {
            console.warn('Audio playReject error:', e);
        }
    }

    playPneumatic() {
        try {
            this.init();
            if (!this.ctx) return;
            const now = this.ctx.currentTime;
            
            // White noise burst simulating pressurized pneumatic air exhaust (FESTO cylinder)
            const bufferSize = Math.floor(this.ctx.sampleRate * 0.16);
            const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            
            const noise = this.ctx.createBufferSource();
            noise.buffer = buffer;
            
            const filter = this.ctx.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.setValueAtTime(1200, now);
            filter.frequency.exponentialRampToValueAtTime(350, now + 0.16);
            
            const gain = this.ctx.createGain();
            gain.gain.setValueAtTime(0.35, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.16);
            
            noise.connect(filter);
            filter.connect(gain);
            gain.connect(this.ctx.destination);
            
            noise.start(now);
        } catch (e) {
            console.warn('Audio playPneumatic error:', e);
        }
    }

    playCameraShutter() {
        try {
            this.init();
            if (!this.ctx) return;
            const now = this.ctx.currentTime;
            
            // Quick high-frequency opto-mechanical click
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(2200, now);
            osc.frequency.exponentialRampToValueAtTime(400, now + 0.045);
            
            gain.gain.setValueAtTime(0.25, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.045);
            
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            
            osc.start(now);
            osc.stop(now + 0.045);
        } catch (e) {
            console.warn('Audio playCameraShutter error:', e);
        }
    }
}

window.industrialAudio = new IndustrialAudio();
