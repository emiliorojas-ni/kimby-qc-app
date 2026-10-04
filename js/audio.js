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
}

window.industrialAudio = new IndustrialAudio();
