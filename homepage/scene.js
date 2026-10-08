/* Procedural memory ring. Shared by the homepage and universe; no network or GPU dependency. */
(() => {
  "use strict";
  const canvas = document.querySelector("#echo-singularity");
  const ctx = canvas?.getContext("2d", { alpha: false });
  const hero = canvas?.closest(".future-hero");
  const toggle = document.querySelector("#motion-toggle");
  const preference = matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = matchMedia("(hover: hover) and (pointer: fine)");
  const tau = Math.PI * 2;
  let paused = preference.matches;
  let manuallyChosen = false;
  let visible = true;
  let frame = 0;
  let previousTime = 0;
  let elapsed = 0;
  let width = 1;
  let height = 1;
  let compact = false;
  let pointerX = 0;
  let pointerY = 0;
  let smoothX = 0;
  let smoothY = 0;
  let particles = [];
  let stars = [];
  let background;
  let coreImage;
  let progressFrame = 0;

  function rng(seed) {
    let state = seed;
    return () => { state = (state * 1664525 + 1013904223) >>> 0; return state / 4294967296; };
  }

  function syncToggle() {
    const english = document.documentElement.lang.startsWith("en");
    document.body.classList.toggle("motion-paused", paused);
    if (!toggle) return;
    toggle.setAttribute("aria-pressed", String(!paused));
    toggle.setAttribute("aria-label", english ? (paused ? "Play animation" : "Pause animation") : (paused ? "播放动效" : "暂停动效"));
    const label = toggle.querySelector("[data-motion-label]");
    if (label) label.textContent = english ? (paused ? "MOTION OFF" : "MOTION ON") : (paused ? "动效暂停" : "动效开启");
  }

  function stop() {
    cancelAnimationFrame(frame);
    frame = 0;
    previousTime = 0;
  }

  function start() {
    if (ctx && !frame && !paused && visible && !document.hidden) frame = requestAnimationFrame(tick);
  }

  function tick(time) {
    frame = 0;
    if (paused || !visible || document.hidden) { previousTime = 0; return; }
    if (!previousTime || time - previousTime >= 32) {
      elapsed += previousTime ? Math.min(time - previousTime, 70) : 0;
      previousTime = time;
      smoothX += (pointerX - smoothX) * .055;
      smoothY += (pointerY - smoothY) * .055;
      draw();
    }
    frame = requestAnimationFrame(tick);
  }

  function size() {
    if (!ctx || !hero) return;
    width = hero.clientWidth;
    height = hero.clientHeight;
    compact = width <= 600;
    const ratio = Math.min(devicePixelRatio || 1, compact ? 1.6 : 1.5);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    const random = rng(2147);
    stars = Array.from({ length: compact ? 95 : 210 }, () => ({ x: random() * width, y: random() * height, a: .12 + random() * .48, r: .3 + random() * .7 }));
    // Sample the surface of a torus, with fine filaments between its edges.
    particles = Array.from({ length: compact ? 2800 : 6800 }, () => {
      const u = random() * tau;
      const v = random() * tau;
      const tube = .16 + random() * .025;
      const radius = 1 + tube * Math.cos(v);
      return { x: Math.cos(u) * radius, y: Math.sin(u) * radius, z: tube * Math.sin(v), a: .2 + random() * .8, light: random() > .72 };
    });
    background = ctx.createRadialGradient(width * .72, height * .45, 0, width * .72, height * .45, width * .68);
    background.addColorStop(0, "#12221c");
    background.addColorStop(.32, "#0b1511");
    background.addColorStop(.72, "#060b09");
    background.addColorStop(1, "#060909");
    // Cache the small planetary core instead of rebuilding its texture each frame.
    coreImage = document.createElement("canvas");
    coreImage.width = 600;
    coreImage.height = 600;
    const core = coreImage.getContext("2d");
    if (core) {
      const surface = core.createRadialGradient(395, 130, 15, 220, 380, 350);
      surface.addColorStop(0, "#293e31");
      surface.addColorStop(.4, "#101e17");
      surface.addColorStop(.75, "#080e0b");
      surface.addColorStop(1, "#030706");
      core.beginPath(); core.arc(300, 300, 246, 0, tau); core.fillStyle = surface; core.fill();
      core.save(); core.clip();
      for (let i = 0; i < 9500; i++) {
        const x = random() * 492 - 246;
        const y = random() * 492 - 246;
        if (x * x + y * y > 246 * 246) continue;
        const terrain = Math.sin(x * .038 + Math.sin(y * .02) * 3) * Math.cos(y * .033 + x * .012);
        const light = Math.max(0, (x - y + 246) / 738);
        core.fillStyle = terrain > .26 ? `rgba(160,188,129,${light * .28})` : `rgba(0,5,2,${.08 + light * .1})`;
        const radius = terrain > .54 ? 1.2 : .6;
        core.fillRect(x + 300, y + 300, radius, radius);
      }
      core.restore();
      core.strokeStyle = "#c6f8bd55"; core.lineWidth = 1;
      core.beginPath(); core.arc(300, 300, 246, -1.85, .24); core.stroke();
      core.shadowColor = "#b0ffc9"; core.shadowBlur = 14;
      core.strokeStyle = "#c6f8bd77"; core.lineWidth = 1.5;
      core.beginPath(); core.arc(300, 300, 247, -1.45, -.45); core.stroke();
    }
    draw();
    document.body.classList.add("scene-ready");
    start();
  }

  function draw() {
    if (!ctx) return;
    ctx.fillStyle = background || "#060909";
    ctx.fillRect(0, 0, width, height);
    for (const star of stars) {
      ctx.globalAlpha = star.a;
      ctx.fillStyle = "#cee8d9";
      ctx.fillRect(star.x, star.y, star.r, star.r);
    }
    ctx.globalAlpha = 1;
    const cx = compact ? width * .55 : width * .745 + smoothX * 14;
    const cy = compact ? 510 : height * .48 + smoothY * 12;
    const scale = compact ? width * .345 : Math.min(width * .285, height * .435);
    const turn = elapsed * .000055;
    const tilt = .66 + Math.sin(elapsed * .0001) * .05 + smoothY * .03;
    const angle = -.57 + smoothX * .035;
    const ca = Math.cos(angle), sa = Math.sin(angle);
    const ct = Math.cos(tilt), st = Math.sin(tilt);
    const cr = Math.cos(turn), sr = Math.sin(turn);

    function project(x, y, z) {
      const tx = x * cr - y * sr;
      const ty = x * sr + y * cr;
      const yy = ty * ct - z * st;
      const zz = ty * st + z * ct;
      const perspective = 3.8 / (3.8 - zz);
      return { x: cx + (tx * ca - yy * sa) * scale * perspective, y: cy + (tx * sa + yy * ca) * scale * perspective, z: zz, p: perspective };
    }

    // Soft scattered light surrounding an open, dark centre.
    const glow = ctx.createRadialGradient(cx, cy, scale * .2, cx, cy, scale * 1.65);
    glow.addColorStop(0, "#06090900");
    glow.addColorStop(.48, "#a0e4ac03");
    glow.addColorStop(.62, "#90e8b40d");
    glow.addColorStop(.77, "#8bc5a307");
    glow.addColorStop(1, "#00000000");
    ctx.fillStyle = glow;
    ctx.fillRect(cx - scale * 2, cy - scale * 2, scale * 4, scale * 4);
    if (coreImage) {
      const diameter = scale * 1.65;
      ctx.drawImage(coreImage, cx - diameter / 2, cy - diameter / 2, diameter, diameter);
    }

    // Thin orbital guide marks retain scale without competing with the object.
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(angle);
    ctx.strokeStyle = "#bce1c323";
    ctx.lineWidth = .65;
    ctx.beginPath(); ctx.ellipse(0, 0, scale * 1.52, scale * .88, 0, -.8, 4.7); ctx.stroke();
    ctx.setLineDash([2, 7]);
    ctx.strokeStyle = "#bce1c328";
    ctx.beginPath(); ctx.ellipse(0, 0, scale * 1.39, scale * .86, 0, 0, tau); ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();

    // Thirty longitudinal filaments form a luminous, sculptural memory ring.
    ctx.globalCompositeOperation = "lighter";
    for (let band = 0; band < 30; band++) {
      const v = band / 30 * tau;
      const radius = 1 + .18 * Math.cos(v);
      const z = .18 * Math.sin(v);
      ctx.beginPath();
      for (let i = 0; i <= 160; i++) {
        const u = i / 160 * tau;
        const p = project(Math.cos(u) * radius, Math.sin(u) * radius, z);
        if (i === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
      }
      ctx.strokeStyle = band % 5 === 0 ? "#c0ffb9a0" : "#a3d9c246";
      ctx.lineWidth = band % 5 === 0 ? 1 : .6;
      ctx.stroke();
    }
    // Cross sections describe the volume and rotate slowly through the light.
    for (let i = 0; i < 84; i++) {
      const u = i / 84 * tau;
      ctx.beginPath();
      for (let j = 0; j <= 28; j++) {
        const v = j / 28 * tau;
        const p = project(Math.cos(u) * (1 + .18 * Math.cos(v)), Math.sin(u) * (1 + .18 * Math.cos(v)), .18 * Math.sin(v));
        if (!j) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y);
      }
      ctx.strokeStyle = i % 7 === 0 ? "#c6ffd47a" : "#9bbf9f29";
      ctx.lineWidth = .55;
      ctx.stroke();
    }
    for (const particle of particles) {
      const p = project(particle.x, particle.y, particle.z);
      const light = .32 + .68 * Math.max(0, (particle.x + particle.z + 1) / 2);
      ctx.globalAlpha = particle.a * light * (p.z > 0 ? .9 : .37);
      ctx.fillStyle = particle.light ? "#eaffc7" : "#86cbb6";
      const r = (particle.light ? 1.15 : .7) * p.p;
      ctx.fillRect(p.x, p.y, r, r);
    }
    ctx.globalAlpha = 1;
    // Traveling glints are deliberately slow; no flashes or strobing.
    for (let i = 0; i < 4; i++) {
      const u = i * 1.55 - turn * 1.2;
      const p = project(Math.cos(u), Math.sin(u), .185);
      const flare = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 25);
      flare.addColorStop(0, "#e4ffbfaa"); flare.addColorStop(.1, "#caffc14d"); flare.addColorStop(1, "#a6ffc000");
      ctx.fillStyle = flare; ctx.fillRect(p.x - 25, p.y - 25, 50, 50);
      ctx.fillStyle = "#e8ffd9"; ctx.fillRect(p.x - 1, p.y - 1, 2, 2);
    }
    ctx.globalCompositeOperation = "source-over";
    // The central reticle identifies the shared memory anchor.
    ctx.strokeStyle = "#bdd5bc57"; ctx.lineWidth = .7;
    ctx.beginPath(); ctx.moveTo(cx - 7, cy); ctx.lineTo(cx + 7, cy); ctx.moveTo(cx, cy - 7); ctx.lineTo(cx, cy + 7); ctx.stroke();
    ctx.fillStyle = "#93ac9680";
    ctx.font = "7px monospace";
    ctx.textAlign = "center";
    ctx.fillText("E C H O  /  2 1 4 7", cx, cy + 24);
    if (!compact) {
      ctx.textAlign = "left";
      ctx.fillText("CONTINUITY FIELD", cx + scale * .62, cy - scale * .9);
      ctx.fillText("01 : ∞", cx - scale * 1.1, cy + scale * .5);
    }
  }

  toggle?.addEventListener("click", () => {
    paused = !paused;
    manuallyChosen = true;
    syncToggle();
    if (paused) stop(); else start();
  });
  preference.addEventListener("change", () => {
    if (!manuallyChosen) paused = preference.matches;
    syncToggle();
    if (paused) stop(); else start();
  });
  document.addEventListener("visibilitychange", () => document.hidden ? stop() : start());
  new MutationObserver(syncToggle).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  if (ctx && hero) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      if (visible) start(); else stop();
    }, { threshold: 0 }).observe(hero);
    new ResizeObserver(size).observe(hero);
    hero.addEventListener("pointermove", event => {
      if (!finePointer.matches || paused) return;
      const rect = hero.getBoundingClientRect();
      pointerX = (event.clientX - rect.left) / width - .5;
      pointerY = (event.clientY - rect.top) / height - .5;
    }, { passive: true });
    hero.addEventListener("pointerleave", () => { pointerX = 0; pointerY = 0; });
    size();
  } else if (toggle) {
    toggle.hidden = true;
  }
  syncToggle();

  const progress = document.querySelector(".reading-progress");
  function updateProgress() {
    progressFrame = 0;
    const remaining = document.documentElement.scrollHeight - innerHeight;
    const value = remaining > 0 ? Math.min(1, Math.max(0, scrollY / remaining)) : 0;
    if (progress) progress.style.transform = `scaleX(${value})`;
  }
  addEventListener("scroll", () => { if (!progressFrame) progressFrame = requestAnimationFrame(updateProgress); }, { passive: true });
  addEventListener("resize", updateProgress, { passive: true });
  updateProgress();
})();
