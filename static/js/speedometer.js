/* Speedometer — 0 (left, green) → 1 (right, red) */
class Speedometer {
    constructor(canvasId, cw = 380, ch = 220, radius = 150) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');

        const dpr = window.devicePixelRatio || 1;
        this.canvas.width  = cw * dpr;
        this.canvas.height = ch * dpr;
        this.canvas.style.width  = cw + 'px';
        this.canvas.style.height = ch + 'px';
        this.ctx.scale(dpr, dpr);

        this.W = cw; this.H = ch;
        this.cx = cw / 2;
        this.cy = ch * 0.80;
        this.r = radius;
        this.cur = 0; this.target = 0; this.raf = null;

        this.draw(0);
    }

    draw(v) {
        const { ctx, cx, cy, r, W, H } = this;
        ctx.clearRect(0, 0, W * 3, H * 3);

        const LW = Math.max(16, r * 0.18);

        // colour zones
        const zones = [
            [0.00, 0.33, '#22c55e'],
            [0.33, 0.66, '#f59e0b'],
            [0.66, 1.00, '#ef4444'],
        ];
        zones.forEach(([s, e, col]) => {
            ctx.beginPath();
            ctx.arc(cx, cy, r, Math.PI + s * Math.PI, Math.PI + e * Math.PI, false);
            ctx.strokeStyle = col;
            ctx.lineWidth = LW;
            ctx.lineCap = 'round';
            ctx.stroke();
        });

        // ticks
        ctx.strokeStyle = 'rgba(255,255,255,.5)';
        for (let i = 0; i <= 10; i++) {
            const a = Math.PI + (i / 10) * Math.PI;
            const inner = r - LW / 2;
            const outer = r + LW / 2;
            ctx.beginPath();
            ctx.moveTo(cx + Math.cos(a) * inner, cy + Math.sin(a) * inner);
            ctx.lineTo(cx + Math.cos(a) * outer, cy + Math.sin(a) * outer);
            ctx.lineWidth = i % 5 === 0 ? 2 : 1;
            ctx.stroke();
        }

        // needle
        const ang = Math.PI + v * Math.PI;
        const len = r - LW / 2;
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(ang);
        ctx.beginPath();
        ctx.moveTo(-12, 0);
        ctx.lineTo(len, -3);
        ctx.lineTo(len, 3);
        ctx.closePath();
        ctx.fillStyle = '#1e293b';
        ctx.fill();
        ctx.restore();

        // hub
        ctx.beginPath();
        ctx.arc(cx, cy, 11, 0, Math.PI * 2);
        ctx.fillStyle = '#1e293b';
        ctx.fill();

        // end labels
        const fs = Math.max(11, r * 0.09);
        ctx.fillStyle = '#94a3b8';
        ctx.font = `700 ${fs}px Inter, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('0', cx - r, cy + LW);
        ctx.fillText('1', cx + r, cy + LW);
    }

    animate(target) {
        this.target = Math.max(0, Math.min(1, target));
        if (this.raf) cancelAnimationFrame(this.raf);
        const start = performance.now();
        const dur = 1500;
        const from = this.cur;
        const tick = (now) => {
            const t = Math.min((now - start) / dur, 1);
            const e = 1 - Math.pow(1 - t, 3);
            this.cur = from + (this.target - from) * e;
            this.draw(this.cur);
            if (t < 1) this.raf = requestAnimationFrame(tick);
            else this.cur = this.target;
        };
        this.raf = requestAnimationFrame(tick);
    }
}