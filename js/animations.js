/**
 * ============================================================
 * ANIMATIONS — CountUp · Typewriter · Particles · Sparkline
 * Premium Financial Information Platform
 * ============================================================
 */

(function () {
  'use strict';

  /* ──────────────────────────────────────────────────────────
   *  1.  countUp  — animate a number from 0 → target
   * ────────────────────────────────────────────────────────── */
  const countUp = (element, target, duration = 2000) => {
    if (!element) return;

    const isFloat = String(target).includes('.');
    const decimals = isFloat ? (String(target).split('.')[1] || '').length : 0;
    const start = 0;
    const startTime = performance.now();
    const prefix = element.dataset.prefix || '';
    const suffix = element.dataset.suffix || '';

    const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);

    const tick = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeOutQuart(progress);
      const current = start + (target - start) * eased;

      if (isFloat) {
        element.textContent = prefix + current.toFixed(decimals) + suffix;
      } else {
        element.textContent =
          prefix + Math.round(current).toLocaleString('en-IN') + suffix;
      }

      if (progress < 1) {
        requestAnimationFrame(tick);
      }
    };

    requestAnimationFrame(tick);
  };

  /* ──────────────────────────────────────────────────────────
   *  2.  typewriter  — rotate through words with typing effect
   * ────────────────────────────────────────────────────────── */
  const typewriter = (
    element,
    words = [],
    typingSpeed = 100,
    deletingSpeed = 60,
    pauseTime = 1800
  ) => {
    if (!element || !words.length) return;

    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    const type = () => {
      const currentWord = words[wordIndex];
      let delay;

      if (isDeleting) {
        charIndex--;
        element.textContent = currentWord.substring(0, charIndex);
        delay = deletingSpeed;

        if (charIndex === 0) {
          isDeleting = false;
          wordIndex = (wordIndex + 1) % words.length;
          delay = 400; // short pause before next word
        }
      } else {
        charIndex++;
        element.textContent = currentWord.substring(0, charIndex);
        delay = typingSpeed;

        if (charIndex === currentWord.length) {
          isDeleting = true;
          delay = pauseTime;
        }
      }

      setTimeout(type, delay);
    };

    type();
  };

  /* ──────────────────────────────────────────────────────────
   *  3.  initParticles  — constellation / node-link animation
   * ────────────────────────────────────────────────────────── */
  const initParticles = (canvasId) => {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let width, height, particles, animId;
    const PARTICLE_COUNT = 60;
    const CONNECTION_DIST = 140;
    const MOUSE_DIST = 180;
    const mouse = { x: -9999, y: -9999 };

    const resize = () => {
      width = canvas.width = canvas.parentElement?.offsetWidth || window.innerWidth;
      height = canvas.height = canvas.parentElement?.offsetHeight || window.innerHeight;
    };

    class Particle {
      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.6;
        this.vy = (Math.random() - 0.5) * 0.6;
        this.radius = Math.random() * 2 + 1;
        this.opacity = Math.random() * 0.5 + 0.3;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;

        // gentle mouse repulsion
        const dx = this.x - mouse.x;
        const dy = this.y - mouse.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < MOUSE_DIST && dist > 0) {
          const force = (MOUSE_DIST - dist) / MOUSE_DIST * 0.02;
          this.vx += (dx / dist) * force;
          this.vy += (dy / dist) * force;
        }

        // dampen velocity
        this.vx *= 0.999;
        this.vy *= 0.999;
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(99, 102, 241, ${this.opacity})`;
        ctx.fill();
      }
    }

    const init = () => {
      particles = [];
      for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push(new Particle());
      }
    };

    const drawConnections = () => {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < CONNECTION_DIST) {
            const opacity = (1 - dist / CONNECTION_DIST) * 0.25;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = `rgba(99, 102, 241, ${opacity})`;
            ctx.lineWidth = 0.6;
            ctx.stroke();
          }
        }
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, width, height);
      particles.forEach((p) => {
        p.update();
        p.draw();
      });
      drawConnections();
      animId = requestAnimationFrame(animate);
    };

    canvas.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    });

    canvas.addEventListener('mouseleave', () => {
      mouse.x = -9999;
      mouse.y = -9999;
    });

    window.addEventListener('resize', () => {
      resize();
      // re-initialise particles to fit new dimensions
      init();
    });

    resize();
    init();
    animate();

    // return a cleanup fn
    return () => {
      if (animId) cancelAnimationFrame(animId);
    };
  };

  /* ──────────────────────────────────────────────────────────
   *  4.  generateSparkline  — returns an inline SVG string
   *      with a smooth gradient-filled area + stroke line
   * ────────────────────────────────────────────────────────── */
  const generateSparkline = (data, width = 120, height = 40, color = '#10b981') => {
    if (!data || data.length < 2) {
      return `<svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg"></svg>`;
    }

    const padding = 2;
    const w = width - padding * 2;
    const h = height - padding * 2;
    const min = Math.min(...data);
    const max = Math.max(...data);
    const range = max - min || 1;

    // Determine colour from trend
    const isUp = data[data.length - 1] >= data[0];
    const strokeColor = color || (isUp ? '#10b981' : '#ef4444');
    const gradId = 'sg_' + Math.random().toString(36).substring(2, 9);

    // Build points
    const points = data.map((val, i) => {
      const x = padding + (i / (data.length - 1)) * w;
      const y = padding + h - ((val - min) / range) * h;
      return { x, y };
    });

    // Smooth curve using cardinal spline (Catmull-Rom → cubic Bezier)
    const catmullRomToBezier = (pts) => {
      const d = [`M ${pts[0].x.toFixed(2)},${pts[0].y.toFixed(2)}`];
      for (let i = 0; i < pts.length - 1; i++) {
        const p0 = pts[Math.max(i - 1, 0)];
        const p1 = pts[i];
        const p2 = pts[i + 1];
        const p3 = pts[Math.min(i + 2, pts.length - 1)];

        const cp1x = p1.x + (p2.x - p0.x) / 6;
        const cp1y = p1.y + (p2.y - p0.y) / 6;
        const cp2x = p2.x - (p3.x - p1.x) / 6;
        const cp2y = p2.y - (p3.y - p1.y) / 6;

        d.push(
          `C ${cp1x.toFixed(2)},${cp1y.toFixed(2)} ${cp2x.toFixed(2)},${cp2y.toFixed(2)} ${p2.x.toFixed(2)},${p2.y.toFixed(2)}`
        );
      }
      return d.join(' ');
    };

    const linePath = catmullRomToBezier(points);

    // Area fill path (line path + close to bottom)
    const areaPath =
      linePath +
      ` L ${points[points.length - 1].x.toFixed(2)},${height} L ${points[0].x.toFixed(2)},${height} Z`;

    return `<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg" class="sparkline-svg">
  <defs>
    <linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="${strokeColor}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="${strokeColor}" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <path d="${areaPath}" fill="url(#${gradId})" stroke="none"/>
  <path d="${linePath}" fill="none" stroke="${strokeColor}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;
  };

  /* ── Expose globally ────────────────────────────────────── */
  window.Animations = {
    countUp,
    typewriter,
    initParticles,
    generateSparkline
  };
})();
