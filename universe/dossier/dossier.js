/* ECHO character dossier: a code-rendered motion trailer built from the locked reference sheets.
 *
 * Every frame is drawn on one 1280x720 canvas from a deterministic timeline, so the same code
 * plays live in the browser and records itself to WebM (MediaRecorder, no ffmpeg needed).
 * The characters stay the approved 2D art; the motion comes from camera work, cuts, light,
 * a surveillance HUD and kinetic type, i.e. ECHO's "monitored world" turned into film grammar.
 *
 *   ?id=001 … 009   which White Ghost Team member
 *   ?record=1        record one pass and expose it as window.__video (data URL)
 */
(() => {
  "use strict";
  const W = 1280;
  const H = 720;
  const BAR = 62;
  const FPS = 30;
  const DURATION = 15;
  const MONO = "Consolas, 'SFMono-Regular', 'Liberation Mono', monospace";
  const DISPLAY = "Inter, 'Segoe UI', sans-serif";

  // Canon facts from characters/*.md and colours from bible/visual_system_v1.md.
  const CHARACTERS = {
    "001": { dir: "001_zero", name: "ZERO", codename: "WHITE GHOST", role: "CAPTAIN", rank: "S", core: "NEURAL SYNC", shell: "IRIDESCENT WHITE", accent: "#bff4ff", accent2: "#f5a8ca", line: "Memory is evidence." },
    "002": { dir: "002_kane", name: "KANE", codename: "PALADIN", role: "VICE CAPTAIN", rank: "A", core: "COMBAT DOWNLOAD", shell: "BLACK COAT / VIOLET", accent: "#9479ff", accent2: "#e3c27a", line: "Ten seconds to learn." },
    "003": { dir: "003_eve", name: "EVE", codename: "SIREN", role: "EMOTION HACKER", rank: "A", core: "EMOTION HACK", shell: "SILVER / ROSE SIGNAL", accent: "#f49ac1", accent2: "#e9ecf4", line: "Every feeling has a port." },
    "004": { dir: "004_leon", name: "LEON", codename: "CHRONOS", role: "SWORDSMAN", rank: "A", core: "TIME ECHO", shell: "WHITE STEEL / COLD BLUE", accent: "#98bfff", accent2: "#eef4ff", line: "Three seconds ahead." },
    "005": { dir: "005_raven", name: "RAVEN", codename: "NIGHT CROW", role: "ASSASSIN", rank: "A", core: "SHADOW LINK", shell: "BLACK / WHITE EDGE", accent: "#a993f2", accent2: "#f3c873", line: "Blind spots are doors." },
    "006": { dir: "006_shion", name: "SHION", codename: "VIRUS QUEEN", role: "HACKER", rank: "A", core: "NANO SWARM", shell: "WHITE / VIOLET NANOLIGHT", accent: "#c693ff", accent2: "#f5a8ca", line: "The supply chain is a stage." },
    "007": { dir: "007_noah", name: "NOAH", codename: "PROBABILITY", role: "STRATEGIST", rank: "A", core: "PROBABILITY ENGINE", shell: "WHITE FIELD COAT / AMBER", accent: "#f3c873", accent2: "#f4f9fb", line: "The odds are a language." },
    "008": { dir: "008_luna", name: "LUNA", codename: "DREAM WALKER", role: "DREAM WALKER", rank: "A", core: "DREAM DIVE", shell: "WHITE SUIT / LUNAR PINK", accent: "#ffb6d3", accent2: "#d9d0ff", line: "Dreams leave residue." },
    "009": { dir: "009_mira_voss", name: "MIRA VOSS", codename: "GLASS VEIN", role: "FORENSIC MEDIC", rank: "A", core: "MEMORY SUTURING", shell: "GLASS / PALE TELEMETRY", accent: "#a8dcff", accent2: "#f4f9fb", line: "Every repair leaves a seam.", face: [0.4, 0.07, 0.61, 0.29], faceScale: 0.56 },
  };
  const TICKER = [
    "ECHO CORE SYNC 99.2%",
    "GHOST REGISTRY +3",
    "CHASER · 7TH MOBILE SQUAD",
    "MEMORY BANK ▲2.4%",
    "WHITE HARBOR 03:12",
    "NO MAGIC · EVERY POWER IS TECHNOLOGICAL",
    "IDENTITY BREACH 0",
    "SEASON 01 · GHOST AWAKENING",
    "ATLAS CIVIC GLASS · NOMINAL",
  ];
  const SHOTS = [
    { name: "BOOT", start: 0, end: 0.8 },
    { name: "SUBJECT", start: 0.8, end: 4.0 },
    { name: "LOOK", start: 4.0, end: 7.6 },
    { name: "TURN", start: 7.6, end: 10.6 },
    { name: "TICKET", start: 10.6, end: 13.0 },
    { name: "TITLE", start: 13.0, end: DURATION },
  ];

  const params = new URLSearchParams(location.search);
  const id = CHARACTERS[params.get("id")] ? params.get("id") : "001";
  const who = CHARACTERS[id];
  const canvas = document.querySelector("#dossier");
  const ctx = canvas.getContext("2d");
  canvas.width = W;
  canvas.height = H;

  /* ---------- helpers ---------- */

  const clamp01 = (v) => Math.min(1, Math.max(0, v));
  const seg = (t, a, b) => clamp01((t - a) / (b - a));
  const easeOut = (t) => 1 - (1 - t) ** 3;
  const easeInOut = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);
  const easeBack = (t) => 1 + 2.7 * (t - 1) ** 3 + 1.7 * (t - 1) ** 2;
  const lerp = (a, b, t) => a + (b - a) * t;

  function seeded(seed) {
    let a = seed >>> 0;
    return () => {
      a = (a + 0x6d2b79f5) >>> 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function hexToRgb(hex) {
    const n = parseInt(hex.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  const rgba = (hex, a) => `rgba(${hexToRgb(hex).join(", ")}, ${a})`;

  function loadImage(src) {
    return new Promise((resolve) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = () => resolve(null);
      img.src = src;
    });
  }

  function mono(size, weight = 500) {
    ctx.font = `${weight} ${size}px ${MONO}`;
  }

  function display(size, weight = 600) {
    ctx.font = `${weight} ${size}px ${DISPLAY}`;
  }

  // Draw an image so that its fractional point (fx, fy) lands on canvas (x, y).
  function place(img, fx, fy, x, y, scale, { flip = false, alpha = 1 } = {}) {
    if (!img) return null;
    const w = img.naturalWidth * scale;
    const h = img.naturalHeight * scale;
    const left = flip ? x - (1 - fx) * w : x - fx * w;
    const top = y - fy * h;
    ctx.save();
    ctx.globalAlpha = alpha;
    if (flip) {
      ctx.translate(left + w, top);
      ctx.scale(-1, 1);
      ctx.drawImage(img, 0, 0, w, h);
    } else {
      ctx.drawImage(img, left, top, w, h);
    }
    ctx.restore();
    return { left, top, w, h, at: (px, py) => [flip ? left + (1 - px) * w : left + px * w, top + py * h] };
  }

  // The holographic sheen that sweeps across the figure, masked to its silhouette.
  const sheen = document.createElement("canvas");
  const sheenCtx = sheen.getContext("2d");
  function placeWithSheen(img, fx, fy, x, y, scale, phase, options = {}) {
    if (!img) return null;
    const w = Math.round(img.naturalWidth * scale);
    const h = Math.round(img.naturalHeight * scale);
    sheen.width = w;
    sheen.height = h;
    sheenCtx.globalCompositeOperation = "source-over";
    if (options.flip) {
      sheenCtx.save();
      sheenCtx.translate(w, 0);
      sheenCtx.scale(-1, 1);
      sheenCtx.drawImage(img, 0, 0, w, h);
      sheenCtx.restore();
    } else {
      sheenCtx.drawImage(img, 0, 0, w, h);
    }
    sheenCtx.globalCompositeOperation = "source-atop";
    const band = sheenCtx.createLinearGradient(w * (phase - 0.2), 0, w * (phase + 0.02), h * 0.5);
    band.addColorStop(0, rgba(who.accent, 0));
    band.addColorStop(0.45, rgba(who.accent, 0.2));
    band.addColorStop(0.55, rgba(who.accent2, 0.16));
    band.addColorStop(1, rgba(who.accent2, 0));
    sheenCtx.fillStyle = band;
    sheenCtx.fillRect(0, 0, w, h);
    // Crops (head shots) end abruptly at the image border: feather them into the set.
    if (options.feather) {
      sheenCtx.globalCompositeOperation = "destination-in";
      const across = sheenCtx.createLinearGradient(0, 0, w, 0);
      across.addColorStop(0, "rgba(0, 0, 0, 0)");
      across.addColorStop(0.12, "#000");
      across.addColorStop(0.82, "#000");
      across.addColorStop(1, "rgba(0, 0, 0, 0)");
      sheenCtx.fillStyle = across;
      sheenCtx.fillRect(0, 0, w, h);
      const down = sheenCtx.createLinearGradient(0, 0, 0, h);
      down.addColorStop(0, "#000");
      down.addColorStop(0.8, "#000");
      down.addColorStop(1, "rgba(0, 0, 0, 0)");
      sheenCtx.fillStyle = down;
      sheenCtx.fillRect(0, 0, w, h);
    }
    const left = options.flip ? x - (1 - fx) * w : x - fx * w;
    const top = y - fy * h;
    ctx.save();
    ctx.globalAlpha = options.alpha ?? 1;
    ctx.drawImage(sheen, left, top);
    ctx.restore();
    return { left, top, w, h, at: (px, py) => [options.flip ? left + (1 - px) * w : left + px * w, top + py * h] };
  }

  // Where the figure actually sits in a reference sheet (its non-transparent bounds), so sheets
  // cropped at different scales (Kane's side view is much larger than Zero's) frame identically.
  function silhouette(img) {
    const height = 220;
    const width = Math.max(1, Math.round((img.naturalWidth / img.naturalHeight) * height));
    const probe = document.createElement("canvas");
    probe.width = width;
    probe.height = height;
    const g = probe.getContext("2d", { willReadFrequently: true });
    g.drawImage(img, 0, 0, width, height);
    const { data } = g.getImageData(0, 0, width, height);
    let x0 = width;
    let y0 = height;
    let x1 = -1;
    let y1 = -1;
    for (let y = 0; y < height; y += 1) {
      for (let x = 0; x < width; x += 1) {
        if (data[(y * width + x) * 4 + 3] <= 24) continue;
        if (x < x0) x0 = x;
        if (x > x1) x1 = x;
        if (y < y0) y0 = y;
        if (y > y1) y1 = y;
      }
    }
    if (x1 < 0) return { x0: 0, y0: 0, x1: 1, y1: 1 };
    return { x0: x0 / width, y0: y0 / height, x1: (x1 + 1) / width, y1: (y1 + 1) / height };
  }

  // Place a full-body sheet by its silhouette: (u, v) are fractions of the figure itself and
  // `height` is the figure's on-screen height. frame.fig(u, v) maps figure fractions to canvas.
  function figure(img, u, v, x, y, height, phase, options = {}) {
    if (!img) return null;
    const box = img.box || { x0: 0, y0: 0, x1: 1, y1: 1 };
    const bw = box.x1 - box.x0;
    const bh = box.y1 - box.y0;
    const scale = height / (bh * img.naturalHeight);
    const frame = placeWithSheen(img, box.x0 + u * bw, box.y0 + v * bh, x, y, scale, phase, options);
    frame.fig = (pu, pv) => frame.at(box.x0 + pu * bw, box.y0 + pv * bh);
    return frame;
  }

  /* ---------- sets ---------- */

  const bokeh = (() => {
    const random = seeded(2147);
    return Array.from({ length: 26 }, () => ({ x: random() * W, y: BAR + random() * (H - BAR * 2), r: 20 + random() * 70, warm: random() < 0.3, speed: 4 + random() * 10, a: 0.05 + random() * 0.12 }));
  })();

  function drawBokeh(t, drift = 1) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    for (const b of bokeh) {
      const x = (b.x - t * b.speed * drift + W * 2) % (W + 200) - 100;
      const g = ctx.createRadialGradient(x, b.y, 0, x, b.y, b.r);
      const color = b.warm ? who.accent2 : who.accent;
      g.addColorStop(0, rgba(color, b.a));
      g.addColorStop(0.7, rgba(color, b.a * 0.4));
      g.addColorStop(1, rgba(color, 0));
      ctx.fillStyle = g;
      ctx.fillRect(x - b.r, b.y - b.r, b.r * 2, b.r * 2);
    }
    ctx.restore();
  }

  // A white-industrial corridor: light strips receding to a vanishing point.
  function drawCorridor(t, vx, vy) {
    const bg = ctx.createLinearGradient(0, 0, 0, H);
    bg.addColorStop(0, "#0b1216");
    bg.addColorStop(0.6, "#070b0e");
    bg.addColorStop(1, "#030506");
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, W, H);
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < 14; i += 1) {
      const depth = ((i / 14 + t * 0.05) % 1) ** 1.6;
      const spread = lerp(40, 760, depth);
      const alpha = 0.04 + depth * 0.22;
      for (const side of [-1, 1]) {
        const x = vx + side * spread;
        const top = vy - lerp(10, 300, depth);
        const bottom = vy + lerp(8, 260, depth);
        ctx.strokeStyle = `rgba(220, 240, 246, ${alpha})`;
        ctx.lineWidth = lerp(0.5, 3, depth);
        ctx.beginPath();
        ctx.moveTo(x, top);
        ctx.lineTo(x, bottom);
        ctx.stroke();
      }
      ctx.strokeStyle = `rgba(220, 240, 246, ${alpha * 0.6})`;
      ctx.beginPath();
      ctx.moveTo(vx - spread, vy - lerp(10, 300, depth));
      ctx.lineTo(vx + spread, vy - lerp(10, 300, depth));
      ctx.stroke();
    }
    const beam = ctx.createRadialGradient(vx, vy, 0, vx, vy, 520);
    beam.addColorStop(0, rgba(who.accent, 0.16));
    beam.addColorStop(1, rgba(who.accent, 0));
    ctx.fillStyle = beam;
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
  }

  function drawFloorGlow(x, y, width) {
    const g = ctx.createRadialGradient(x, y, 0, x, y, width);
    g.addColorStop(0, rgba(who.accent, 0.28));
    g.addColorStop(1, rgba(who.accent, 0));
    ctx.save();
    ctx.scale(1, 0.22);
    ctx.fillStyle = g;
    ctx.fillRect(x - width, y / 0.22 - width, width * 2, width * 2);
    ctx.restore();
  }

  /* ---------- HUD primitives ---------- */

  function brackets(x, y, w, h, color, size = 14, progress = 1) {
    const s = size * progress;
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (const [cx, cy, dx, dy] of [
      [x, y, 1, 1],
      [x + w, y, -1, 1],
      [x, y + h, 1, -1],
      [x + w, y + h, -1, -1],
    ]) {
      ctx.moveTo(cx + dx * s, cy);
      ctx.lineTo(cx, cy);
      ctx.lineTo(cx, cy + dy * s);
    }
    ctx.stroke();
  }

  function chip(x, y, text, { color = "#eef6f8", background = "rgba(4, 7, 9, 0.82)", size = 12, border = null } = {}) {
    mono(size, 600);
    const width = ctx.measureText(text).width + 14;
    ctx.fillStyle = background;
    ctx.fillRect(x, y, width, size + 10);
    if (border) {
      ctx.strokeStyle = border;
      ctx.lineWidth = 1;
      ctx.strokeRect(x + 0.5, y + 0.5, width - 1, size + 9);
    }
    ctx.fillStyle = color;
    ctx.textBaseline = "middle";
    ctx.fillText(text, x + 7, y + (size + 10) / 2 + 1);
    return width;
  }

  // A tracking box that grows in, with a label chip and a confidence readout.
  function track(x, y, w, h, progress, label, value) {
    if (progress <= 0) return;
    const p = easeOut(progress);
    const cx = x + w / 2;
    const cy = y + h / 2;
    const bw = w * lerp(0.6, 1, p);
    const bh = h * lerp(0.6, 1, p);
    ctx.save();
    ctx.globalAlpha = Math.min(1, progress * 3);
    ctx.strokeStyle = "rgba(238, 246, 248, 0.22)";
    ctx.lineWidth = 1;
    ctx.strokeRect(cx - bw / 2, cy - bh / 2, bw, bh);
    brackets(cx - bw / 2, cy - bh / 2, bw, bh, "#eef6f8", 12, p);
    if (progress > 0.35) {
      const width = chip(cx - bw / 2, cy - bh / 2 - 24, label, { color: "#05080a", background: "#eef6f8", size: 11 });
      if (value) chip(cx - bw / 2 + width + 4, cy - bh / 2 - 24, value, { color: who.accent, size: 11 });
    }
    ctx.restore();
  }

  function ruler(x, top, bottom, t) {
    ctx.strokeStyle = "rgba(238, 246, 248, 0.35)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    const offset = (t * 40) % 20;
    for (let y = top + offset; y < bottom; y += 20) {
      const long = Math.round((y - offset) / 20) % 5 === 0;
      ctx.moveTo(x, y);
      ctx.lineTo(x + (long ? 12 : 6), y);
    }
    ctx.stroke();
  }

  function typed(text, progress) {
    return text.slice(0, Math.floor(text.length * clamp01(progress)));
  }

  /* ---------- shots ---------- */

  const art = {};

  function shotBoot(t) {
    ctx.fillStyle = "#030506";
    ctx.fillRect(0, 0, W, H);
    mono(14, 600);
    ctx.fillStyle = "#eef6f8";
    ctx.textBaseline = "middle";
    ctx.fillText(typed(`ECHO // SUBJECT FILE ${id}`, t / 0.5), 96, H / 2 - 10);
    mono(11);
    ctx.fillStyle = rgba(who.accent, 0.8);
    ctx.fillText(typed("DECRYPTING CANON LOCK …", (t - 0.25) / 0.4), 96, H / 2 + 14);
  }

  // Face close-up: the identity system acquires the subject.
  function shotSubject(t, p) {
    ctx.fillStyle = "#04070a";
    ctx.fillRect(0, 0, W, H);
    drawBokeh(t, 1.4);
    const img = art.head || art.avatar;
    if (!img) return;
    const [u0, v0, u1, v1] = who.face || [0.31, 0.33, 0.75, 0.75];
    const faceHeight = lerp(318, 366, easeInOut(p)) * (who.faceScale || 1) * (1 + Math.sin(t * 2.3) * 0.004);
    const scale = faceHeight / ((v1 - v0) * img.naturalHeight);
    const frame = placeWithSheen(img, (u0 + u1) / 2, (v0 + v1) / 2, W * 0.4 + Math.sin(t * 0.7) * 6, H * 0.5, scale, lerp(-0.2, 1.3, p), { feather: true });
    const [fx1, fy1] = frame.at(u0, v0);
    const [fx2, fy2] = frame.at(u1, v1);
    track(fx1, fy1, fx2 - fx1, fy2 - fy1, seg(t, 0.25, 1.0), `SUBJECT ${id} · ${who.name}`, `MATCH ${(0.8 + 0.19 * easeOut(seg(t, 0.5, 2.2))).toFixed(2)}`);
    // Facial landmarks blink in once the box is locked.
    // Eyes, nose, mouth and temples as fractions of the face box.
    const marks = [
      [0.25, 0.45],
      [0.7, 0.44],
      [0.47, 0.64],
      [0.5, 0.81],
      [0.11, 0.4],
      [0.84, 0.4],
    ];
    marks.forEach(([mx, my], i) => {
      const a = seg(t, 1.0 + i * 0.08, 1.2 + i * 0.08) * (0.6 + 0.4 * Math.sin(t * 9 + i));
      if (a <= 0) return;
      const [x, y] = frame.at(u0 + mx * (u1 - u0), v0 + my * (v1 - v0));
      ctx.fillStyle = rgba(who.accent, a);
      ctx.fillRect(x - 2, y - 2, 4, 4);
      ctx.strokeStyle = rgba(who.accent, a * 0.5);
      ctx.strokeRect(x - 6, y - 6, 12, 12);
    });
    // Scan line sweeping the face once.
    const scanY = lerp(fy1 - 40, fy2 + 40, seg(t, 0.3, 1.6));
    if (t > 0.3 && t < 1.6) {
      const g = ctx.createLinearGradient(0, scanY - 40, 0, scanY);
      g.addColorStop(0, rgba(who.accent, 0));
      g.addColorStop(1, rgba(who.accent, 0.35));
      ctx.fillStyle = g;
      ctx.fillRect(fx1 - 30, scanY - 40, fx2 - fx1 + 60, 40);
    }
    // Readout column.
    const lines = [
      ["IDENTITY CHECKSUM", "VERIFIED"],
      ["ECHO CORE", who.core],
      ["SYNC", `${(88 + 11 * easeOut(seg(t, 0.8, 2.6))).toFixed(1)}%`],
      ["GHOST CONTAMINATION", "0.00"],
      ["CANON STATUS", "LOCKED"],
    ];
    lines.forEach(([k, v], i) => {
      const a = seg(t, 1.2 + i * 0.15, 1.5 + i * 0.15);
      if (!a) return;
      ctx.globalAlpha = a;
      mono(11);
      ctx.fillStyle = "rgba(238, 246, 248, 0.55)";
      ctx.fillText(k, W - 330, 170 + i * 46);
      mono(15, 600);
      ctx.fillStyle = i === 3 ? "#96e0aa" : "#eef6f8";
      ctx.fillText(v, W - 330, 188 + i * 46);
      ctx.globalAlpha = 1;
    });
    ruler(60, BAR + 30, H - BAR - 30, t);
  }

  // Full body: the camera tilts from boots to visor while gear gets tagged.
  function shotLook(t, p) {
    drawCorridor(t, W * 0.38, H * 0.46);
    const img = art.front;
    const focus = lerp(0.84, 0.15, easeInOut(seg(p, 0, 0.75)));
    const height = lerp(880, 770, easeInOut(p)) * (1 + Math.sin(t * 2.1) * 0.003);
    const frame = figure(img, 0.5, focus, W * 0.36, H * 0.5, height, lerp(-0.3, 1.2, p));
    if (!frame) return;
    const [footX, footY] = frame.fig(0.5, 1);
    drawFloorGlow(footX, footY, 260);
    // Head, sleeve, waist and boots as fractions of the figure's own bounds.
    const tags = [
      [0.29, 0, 0.82, 0.13, "VISOR", "0.98", 0.2],
      [0, 0.25, 0.42, 0.49, "SHELL · HOLO", "0.97", 0.7],
      [0.32, 0.28, 0.88, 0.38, "HARNESS", "OK", 1.2],
      [0.14, 0.8, 1, 1, "STRIDE", "LOCK", 0.0],
    ];
    for (const [x1, y1, x2, y2, label, value, at] of tags) {
      const [ax, ay] = frame.fig(x1, y1);
      const [bx, by] = frame.fig(x2, y2);
      if (by < BAR || ay > H - BAR) continue;
      track(ax, ay, bx - ax, by - ay, seg(t, at, at + 0.7), label, value);
    }
    // Lookbook tag card.
    const card = easeBack(seg(t, 0.9, 1.6));
    if (card > 0) {
      const x = lerp(W + 20, W * 0.64, card);
      const y = BAR + 48;
      ctx.fillStyle = "rgba(244, 249, 251, 0.94)";
      ctx.fillRect(x, y, 340, 352);
      ctx.fillStyle = "#05080a";
      mono(11, 600);
      ctx.fillText(`LOOK ${id.slice(1)} / 09`, x + 20, y + 26);
      ctx.fillText("ECHO · 2147", x + 240, y + 26);
      display(30, 700);
      ctx.fillText(who.codename, x + 20, y + 68);
      ctx.fillRect(x + 20, y + 88, 300, 2);
      const rows = [
        ["MODEL", who.name],
        ["SHELL", who.shell],
        ["CORE", who.core],
        ["RANK", who.rank],
        ["ROLE", who.role],
        ["UNIT", "CHASER · 7TH"],
        ["MADE IN", "WHITE HARBOR"],
      ];
      rows.forEach(([k, v], i) => {
        const a = seg(t, 1.3 + i * 0.09, 1.5 + i * 0.09);
        ctx.globalAlpha = a;
        mono(12, 500);
        ctx.fillStyle = "rgba(5, 8, 10, 0.55)";
        ctx.fillText(k, x + 20, y + 114 + i * 28);
        mono(12, 700);
        ctx.fillStyle = "#05080a";
        ctx.fillText(v, x + 110, y + 114 + i * 28);
        ctx.globalAlpha = 1;
      });
      // Care-label glyphs, ECHO style: no magic, no copy, consent, no ghost.
      ctx.strokeStyle = "#05080a";
      ctx.lineWidth = 1.6;
      const gy = y + 318;
      ctx.strokeRect(x + 20, gy - 10, 20, 20);
      ctx.beginPath();
      ctx.moveTo(x + 52, gy + 10);
      ctx.lineTo(x + 62, gy - 10);
      ctx.lineTo(x + 72, gy + 10);
      ctx.closePath();
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(x + 94, gy, 10, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x + 116, gy - 10);
      ctx.lineTo(x + 136, gy + 10);
      ctx.moveTo(x + 136, gy - 10);
      ctx.lineTo(x + 116, gy + 10);
      ctx.stroke();
      mono(10, 600);
      ctx.fillStyle = "#05080a";
      ctx.fillText("NO MAGIC · NO COPY", x + 152, gy + 1);
    }
  }

  // Turnaround: quick cuts as the subject rotates, then kinetic type.
  function shotTurn(t, p) {
    drawCorridor(t + 3, W * 0.3, H * 0.48);
    const views = [art.front, art.side, art.back, art.side, art.front];
    const cut = Math.min(views.length - 1, Math.floor(t / 0.3));
    const hold = t > 1.5;
    const img = hold ? art.side : views[cut];
    const flip = !hold && cut === 3;
    const height = (hold ? lerp(500, 530, seg(t, 1.5, 3)) : 500) * (1 + Math.sin(t * 2.1) * 0.003);
    const frame = figure(img || art.front, 0.5, 1, W * 0.3, H - BAR - 46, height, (t * 0.6) % 1.6 - 0.3, { flip });
    if (frame) {
      const [fx, fy] = frame.fig(0.5, 1);
      drawFloorGlow(fx, fy, 200);
    }
    if (!hold && t % 0.3 < 0.05) {
      ctx.fillStyle = "rgba(238, 246, 248, 0.18)";
      ctx.fillRect(0, 0, W, H);
    }
    mono(12, 600);
    ctx.fillStyle = rgba(who.accent, 0.9);
    ctx.fillText(`ROTATION ${String(Math.min(4, cut) * 90).padStart(3, "0")}°`, 70, BAR + 40);
    // Kinetic type, line by line.
    const x = W * 0.54;
    const lines = [
      { text: `Look ${id.slice(1)}.`, size: 76, weight: 700, at: 1.2 },
      { text: who.line, size: 40, weight: 400, at: 1.7 },
      { text: "Not a ghost story.", size: 40, weight: 400, at: 2.2, mark: true },
    ];
    let y = H * 0.36;
    for (const line of lines) {
      const a = easeOut(seg(t, line.at, line.at + 0.35));
      if (a > 0) {
        display(line.size, line.weight);
        const width = ctx.measureText(line.text).width;
        ctx.save();
        ctx.beginPath();
        ctx.rect(x - 10, y - line.size, width + 30, line.size * 1.3);
        ctx.clip();
        if (line.mark) {
          ctx.fillStyle = rgba(who.accent2, 0.9);
          ctx.fillRect(x - 6, y - line.size * 0.78 + (1 - a) * line.size, width * a + 12, line.size * 0.98);
        }
        ctx.fillStyle = line.mark ? "#05080a" : "#f4f9fb";
        ctx.textBaseline = "alphabetic";
        ctx.fillText(line.text, x, y + (1 - a) * line.size);
        ctx.restore();
      }
      y += line.size * 1.25;
    }
  }

  // A boarding-pass ticket: the dossier's thesis, stamped as canon.
  function shotTicket(t) {
    ctx.fillStyle = "#04070a";
    ctx.fillRect(0, 0, W, H);
    ctx.save();
    ctx.filter = "blur(14px) brightness(0.45)";
    place(art.head || art.avatar || art.front, 0.5, 0.5, W * 0.5 + t * 12, H * 0.5, art.head ? 1.6 : 0.9);
    ctx.restore();
    drawBokeh(t + 6, 0.6);
    const drop = easeBack(seg(t, 0.05, 0.75));
    const x = W * 0.5 - 220;
    const y = lerp(-420, H * 0.5 - 170, drop);
    ctx.save();
    ctx.translate(x + 220, y + 170);
    ctx.rotate(lerp(-0.2, -0.045, drop));
    ctx.translate(-220, -170);
    ctx.shadowColor = "rgba(0, 0, 0, 0.6)";
    ctx.shadowBlur = 40;
    ctx.fillStyle = "#f4f9fb";
    ctx.fillRect(0, 0, 440, 340);
    ctx.shadowBlur = 0;
    ctx.fillStyle = "#05080a";
    mono(11, 600);
    ctx.fillText(`ADMIT ONE · SUBJECT ${id}`, 24, 30);
    ctx.fillText("2147", 380, 30);
    ctx.fillRect(24, 44, 392, 1);
    display(46, 800);
    ctx.fillText("NO MAGIC.", 24, 104);
    ctx.fillText("ONLY MEMORY.", 24, 156);
    const rows = [
      ["ECHO CORE", who.core],
      ["RANK", who.rank],
      ["UNIT", "CHASER 7TH"],
      ["STATUS", "CANON"],
    ];
    rows.forEach(([k, v], i) => {
      mono(11, 500);
      ctx.fillStyle = "rgba(5, 8, 10, 0.55)";
      ctx.fillText(k, 24 + (i % 2) * 200, 196 + Math.floor(i / 2) * 40);
      mono(13, 700);
      ctx.fillStyle = "#05080a";
      ctx.fillText(v, 24 + (i % 2) * 200, 214 + Math.floor(i / 2) * 40);
    });
    const bars = seeded(Number(id) * 97);
    let bx = 24;
    while (bx < 300) {
      const w = 1 + Math.floor(bars() * 4);
      if (bars() > 0.35) ctx.fillRect(bx, 270, w, 46);
      bx += w + 1;
    }
    mono(10, 600);
    ctx.fillText(`ECHO-${id}-${who.name.replace(/\s+/g, "")}`, 24, 330);
    // Stamp.
    const stamp = seg(t, 1.0, 1.25);
    if (stamp > 0) {
      const s = lerp(1.8, 1, easeOut(stamp));
      ctx.save();
      ctx.translate(352, 260);
      ctx.rotate(-0.3);
      ctx.scale(s, s);
      ctx.globalAlpha = stamp;
      ctx.strokeStyle = rgba(who.accent2 === "#f4f9fb" ? who.accent : who.accent2, 0.95);
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(0, 0, 48, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(0, 0, 40, 0, Math.PI * 2);
      ctx.stroke();
      mono(12, 800);
      ctx.fillStyle = ctx.strokeStyle;
      ctx.textAlign = "center";
      ctx.fillText("CANON", 0, -4);
      ctx.fillText("LOCKED", 0, 12);
      ctx.textAlign = "left";
      ctx.restore();
    }
    ctx.restore();
  }

  // Title: the name, echoing outward.
  function shotTitle(t, p) {
    drawCorridor(t + 6, W * 0.7, H * 0.5);
    figure(art.front, 0.5, 1, W * 0.74, H - BAR - 36, 520, (t * 0.5) % 1.4 - 0.2, { alpha: 0.85 });
    const reveal = easeOut(seg(t, 0, 0.6));
    display(170, 800);
    display(Math.min(170, Math.floor((170 * 600) / ctx.measureText(who.name).width)), 800);
    ctx.textBaseline = "alphabetic";
    const x = 90;
    const y = H * 0.56;
    for (let i = 4; i >= 1; i -= 1) {
      const offset = i * 26 * easeOut(seg(t, 0.2, 1.4));
      ctx.strokeStyle = rgba(who.accent, (0.5 - i * 0.1) * reveal);
      ctx.lineWidth = 1.2;
      ctx.strokeText(who.name, x + offset, y);
    }
    ctx.fillStyle = `rgba(244, 249, 251, ${reveal})`;
    ctx.fillText(who.name, x, y);
    mono(14, 600);
    ctx.fillStyle = rgba(who.accent, reveal);
    ctx.fillText(`${who.codename} · ${id} · ${who.role}`, x + 6, y + 44);
    mono(12, 500);
    ctx.fillStyle = `rgba(238, 246, 248, ${0.6 * seg(t, 0.6, 1.2)})`;
    ctx.fillText("ECHO: 回响纪元 · SEASON 01 · GHOST AWAKENING", x + 6, y + 72);
    // ECHO mark.
    const m = seg(t, 0.8, 1.6);
    if (m > 0) {
      ctx.save();
      ctx.translate(x + 26, BAR + 70);
      ctx.strokeStyle = `rgba(244, 249, 251, ${m})`;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(0, 0, 18, 0.5, 0.5 + Math.PI * 1.6 * m);
      ctx.stroke();
      ctx.fillStyle = rgba(who.accent, m);
      ctx.beginPath();
      ctx.arc(22, 0, 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  const DRAW = { BOOT: shotBoot, SUBJECT: shotSubject, LOOK: shotLook, TURN: shotTurn, TICKET: shotTicket, TITLE: shotTitle };

  /* ---------- finishing: HUD, grain, letterbox, glitch ---------- */

  const grains = Array.from({ length: 4 }, (_, k) => {
    const tile = document.createElement("canvas");
    tile.width = 160;
    tile.height = 160;
    const g = tile.getContext("2d");
    const data = g.createImageData(160, 160);
    const random = seeded(31 + k);
    for (let i = 0; i < data.data.length; i += 4) {
      const v = random() * 255;
      data.data[i] = v;
      data.data[i + 1] = v;
      data.data[i + 2] = v;
      data.data[i + 3] = 255;
    }
    g.putImageData(data, 0, 0);
    return ctx.createPattern(tile, "repeat");
  });

  const tickerText = TICKER.join("   ◆   ") + "   ◆   ";

  function finish(t) {
    const frame = Math.floor(t * FPS);
    // Grain and vignette.
    ctx.save();
    ctx.globalCompositeOperation = "overlay";
    ctx.globalAlpha = 0.09;
    ctx.fillStyle = grains[frame % grains.length];
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    const vignette = ctx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.75);
    vignette.addColorStop(0, "rgba(0, 0, 0, 0)");
    vignette.addColorStop(1, "rgba(0, 0, 0, 0.55)");
    ctx.fillStyle = vignette;
    ctx.fillRect(0, 0, W, H);

    // Glitch tears at every cut: Ghost contamination as an edit.
    const nearest = SHOTS.reduce((best, s) => (Math.abs(t - s.start) < Math.abs(t - best) ? s.start : best), -9);
    const gap = Math.abs(t - nearest);
    if (nearest > 0 && gap < 0.1) {
      const amount = 1 - gap / 0.1;
      const random = seeded(frame * 13 + 7);
      for (let i = 0; i < 9; i += 1) {
        const y = random() * H;
        const h = 4 + random() * 36;
        const dx = (random() - 0.5) * 90 * amount;
        ctx.drawImage(canvas, 0, y, W, h, dx, y, W, h);
      }
      ctx.fillStyle = rgba(who.accent2, 0.12 * amount);
      ctx.fillRect(0, random() * H, W, 2);
    }

    // Letterbox and frame furniture.
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, W, BAR);
    ctx.fillRect(0, H - BAR, W, BAR);
    mono(11, 600);
    ctx.textBaseline = "middle";
    ctx.fillStyle = "#eef6f8";
    ctx.fillText(`ECHO // SUBJECT FILE ${id} · ${who.name}`, 40, BAR / 2);
    const seconds = Math.floor(t);
    ctx.fillText(`TC 00:00:${String(seconds).padStart(2, "0")}:${String(frame % FPS).padStart(2, "0")}`, W - 210, BAR / 2);
    if (frame % 30 < 18) {
      ctx.fillStyle = "#ff6f7d";
      ctx.beginPath();
      ctx.arc(W - 64, BAR / 2, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#eef6f8";
      ctx.fillText("REC", W - 54, BAR / 2);
    }
    // Scrubber with shot markers.
    const sx = 420;
    const sw = 420;
    ctx.fillStyle = "rgba(238, 246, 248, 0.25)";
    ctx.fillRect(sx, BAR / 2, sw, 1);
    for (const s of SHOTS) {
      const mx = sx + (s.start / DURATION) * sw;
      ctx.fillRect(mx, BAR / 2 - 4, 1, 9);
    }
    ctx.fillStyle = who.accent;
    ctx.fillRect(sx, BAR / 2 - 1, (t / DURATION) * sw, 3);
    const current = SHOTS.find((s) => t >= s.start && t < s.end) || SHOTS[SHOTS.length - 1];
    mono(10, 600);
    ctx.fillText(current.name, sx + sw + 14, BAR / 2);
    // Ticker.
    mono(12, 500);
    ctx.fillStyle = "rgba(238, 246, 248, 0.75)";
    const width = ctx.measureText(tickerText).width;
    const offset = (t * 70) % width;
    ctx.save();
    ctx.beginPath();
    ctx.rect(40, H - BAR, W - 80, BAR);
    ctx.clip();
    ctx.fillText(tickerText + tickerText, 40 - offset, H - BAR / 2);
    ctx.restore();
    // Corner brackets of the camera frame.
    brackets(24, BAR + 14, W - 48, H - BAR * 2 - 28, "rgba(238, 246, 248, 0.4)", 18);
  }

  function render(t) {
    const shot = SHOTS.find((s) => t >= s.start && t < s.end) || SHOTS[SHOTS.length - 1];
    const local = t - shot.start;
    const progress = clamp01(local / (shot.end - shot.start));
    ctx.save();
    DRAW[shot.name](local, progress);
    ctx.restore();
    finish(t);
  }

  /* ---------- playback and recording ---------- */

  function pickMime() {
    for (const type of ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"]) {
      if (window.MediaRecorder && MediaRecorder.isTypeSupported(type)) return type;
    }
    return "";
  }

  // MediaRecorder writes WebM without a Duration, so players show no length and some editors
  // refuse the file. Insert Segment > Info > Duration (float64, in TimecodeScale units = ms).
  async function withDuration(blob, milliseconds) {
    const bytes = new Uint8Array(await blob.arrayBuffer());
    const vint = (at) => {
      let length = 1;
      while (length <= 8 && !(bytes[at] & (0x80 >> (length - 1)))) length += 1;
      let value = bytes[at] & (0xff >> length);
      let unknown = value === 0xff >> length;
      for (let i = 1; i < length; i += 1) {
        value = value * 256 + bytes[at + i];
        unknown = unknown && bytes[at + i] === 0xff;
      }
      return { length, value, unknown };
    };
    const idLength = (at) => {
      let length = 1;
      while (length <= 4 && !(bytes[at] & (0x80 >> (length - 1)))) length += 1;
      return length;
    };
    const idAt = (at, length) => Array.from(bytes.subarray(at, at + length), (b) => b.toString(16).padStart(2, "0")).join("");
    const size8 = (value) => {
      const out = new Uint8Array(8);
      out[0] = 0x01;
      for (let i = 7; i >= 1; i -= 1) {
        out[i] = value % 256;
        value = Math.floor(value / 256);
      }
      return out;
    };
    let at = 0;
    const headerId = idLength(at);
    const header = vint(at + headerId);
    at += headerId + header.length + header.value;
    const segmentId = idLength(at);
    if (idAt(at, segmentId) !== "18538067") return blob;
    const segmentSizeAt = at + segmentId;
    const segment = vint(segmentSizeAt);
    let child = segmentSizeAt + segment.length;
    while (child < bytes.length) {
      const length = idLength(child);
      const size = vint(child + length);
      if (idAt(child, length) === "1549a966") {
        const dataStart = child + length + size.length;
        const duration = new Uint8Array(11);
        duration.set([0x44, 0x89, 0x88]);
        new DataView(duration.buffer).setFloat64(3, milliseconds);
        const parts = [
          bytes.subarray(0, segmentSizeAt),
          segment.unknown ? bytes.subarray(segmentSizeAt, segmentSizeAt + segment.length) : size8(segment.value + 11 + 8 - size.length),
          bytes.subarray(segmentSizeAt + segment.length, child + length),
          size8(size.value + 11),
          bytes.subarray(dataStart, dataStart + size.value),
          duration,
          bytes.subarray(dataStart + size.value),
        ];
        return new Blob(parts, { type: blob.type });
      }
      if (size.unknown) break;
      child += length + size.length + size.value;
    }
    return blob;
  }

  async function record() {
    const stream = canvas.captureStream(FPS);
    const recorder = new MediaRecorder(stream, { mimeType: pickMime(), videoBitsPerSecond: 10_000_000 });
    const chunks = [];
    recorder.ondataavailable = (event) => event.data.size && chunks.push(event.data);
    const stopped = new Promise((resolve) => {
      recorder.onstop = resolve;
    });
    recorder.start(250);
    const start = performance.now();
    await new Promise((resolve) => {
      const step = (now) => {
        const t = (now - start) / 1000;
        render(Math.min(t, DURATION - 0.001));
        if (t < DURATION) requestAnimationFrame(step);
        else resolve();
      };
      requestAnimationFrame(step);
    });
    recorder.stop();
    await stopped;
    return withDuration(new Blob(chunks, { type: recorder.mimeType || "video/webm" }), DURATION * 1000);
  }

  let playing = true;
  let recording = false;
  let clock = 0;
  let last = 0;
  function loop(now) {
    if (playing) clock = (clock + (last ? (now - last) / 1000 : 0)) % DURATION;
    last = now;
    if (!recording) render(clock);
    requestAnimationFrame(loop);
  }

  // The reference sheets are large; show the file loading instead of a black frame.
  function drawLoading(done, total) {
    ctx.fillStyle = "#030506";
    ctx.fillRect(0, 0, W, H);
    mono(14, 600);
    ctx.textBaseline = "middle";
    ctx.fillStyle = "#eef6f8";
    ctx.fillText(`ECHO // LOADING SUBJECT FILE ${id} · ${who.name}`, 96, H / 2 - 18);
    ctx.fillStyle = "rgba(238, 246, 248, 0.18)";
    ctx.fillRect(96, H / 2 + 8, 420, 2);
    ctx.fillStyle = who.accent;
    ctx.fillRect(96, H / 2 + 8, (420 * done) / total, 2);
    mono(11);
    ctx.fillStyle = rgba(who.accent, 0.85);
    ctx.fillText(`REFERENCE SHEETS ${done} / ${total}`, 96, H / 2 + 30);
  }

  async function boot() {
    const base = `/universe/dossier/assets/${who.dir}/`;
    const sheets = ["front", "side", "back", "head", "avatar"];
    let loaded = 0;
    drawLoading(0, sheets.length);
    const [front, side, back, head, avatar] = await Promise.all(
      sheets.map((name) =>
        loadImage(`${base}${name}.webp`).then((img) => {
          loaded += 1;
          drawLoading(loaded, sheets.length);
          return img;
        }),
      ),
    );
    for (const sheet of [front, side, back]) if (sheet) sheet.box = silhouette(sheet);
    Object.assign(art, { front, side: side || front, back: back || front, head, avatar });
    try {
      await document.fonts.load(`700 76px ${DISPLAY}`);
    } catch (_) {
      // System fonts are an acceptable fallback.
    }
    // Tooling hook: ?t=<seconds> freezes on one frame; EchoDossier.render(t) draws any other.
    window.EchoDossier = { render, duration: DURATION };
    if (params.has("t")) {
      render(Math.min(DURATION - 0.001, Number(params.get("t")) || 0));
      return;
    }
    if (params.get("record") === "1") {
      const blob = await record();
      const reader = new FileReader();
      reader.onload = () => {
        window.__video = reader.result;
      };
      reader.readAsDataURL(blob);
      return;
    }
    requestAnimationFrame(loop);
    wireControls();
  }

  function wireControls() {
    const select = document.querySelector("#dossier-character");
    const toggle = document.querySelector("#dossier-play");
    const save = document.querySelector("#dossier-record");
    if (!select) return;
    for (const [key, value] of Object.entries(CHARACTERS)) {
      const option = document.createElement("option");
      option.value = key;
      option.textContent = `${key} · ${value.name} / ${value.codename}`;
      option.selected = key === id;
      select.append(option);
    }
    select.addEventListener("change", () => {
      location.search = `?id=${select.value}`;
    });
    toggle.addEventListener("click", () => {
      playing = !playing;
      toggle.textContent = playing ? "暂停 Pause" : "播放 Play";
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === " ") {
        event.preventDefault();
        toggle.click();
      }
    });
    save.addEventListener("click", async () => {
      save.disabled = true;
      save.textContent = "录制中… Recording";
      recording = true;
      const blob = await record();
      recording = false;
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `echo-dossier-${id}-${who.name.toLowerCase().replace(/\s+/g, "-")}.webm`;
      link.click();
      save.disabled = false;
      save.textContent = "录制 WebM";
    });
  }

  boot();
})();
