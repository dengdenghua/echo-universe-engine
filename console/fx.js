/* ECHO OS visual layer.
 *
 * Purely presentational: the living neural sky behind the desktop, the planetary
 * World Brain globe, the boot sequence, echo ripples, Ghost whispers, holographic
 * card tilt and the soundtrack controls. It decorates the DOM that app.js renders
 * and listens for the echo:forge events app.js dispatches; it never calls the API.
 */
(() => {
  const audio = window.EchoAudio || null;
  const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const BOOT_PREF = "echo.boot.seen";
  const TAU = Math.PI * 2;

  const rand = (min, max) => min + Math.random() * (max - min);
  const pick = (list) => list[Math.floor(Math.random() * list.length)];
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const lerp = (a, b, t) => a + (b - a) * t;
  const $ = (selector) => document.querySelector(selector);
  const $all = (selector) => Array.from(document.querySelectorAll(selector));

  // Echo Core light language (bible/visual_system_v1.md).
  const LIGHT = {
    snow: [236, 246, 250],
    cyan: [127, 230, 242],
    signal: [159, 200, 255],
    pink: [245, 168, 202],
    violet: [185, 162, 255],
    amber: [243, 200, 115],
    green: [150, 224, 170],
    red: [255, 111, 125],
  };
  const NODE_COLORS = ["snow", "snow", "snow", "cyan", "cyan", "cyan", "signal", "signal", "pink", "pink", "violet", "amber"];
  // Pitch class of a soundtrack note -> the light it fires through the network.
  const NOTE_COLORS = { 0: "signal", 2: "cyan", 4: "violet", 5: "pink", 7: "green", 9: "snow", 10: "amber" };
  const rgba = ([r, g, b], alpha) => `rgba(${r}, ${g}, ${b}, ${alpha})`;

  function readPref(key) {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  }

  function writePref(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch {
      // Storage blocked: the boot sequence will simply play in full next time.
    }
  }

  function panAt(x) {
    return clamp((x / window.innerWidth) * 2 - 1, -0.8, 0.8);
  }

  function panFor(element) {
    const rect = element.getBoundingClientRect();
    return panAt(rect.left + rect.width / 2);
  }

  /* ---------- text effects ---------- */

  const GLYPHS = "▓▒░<>/\\|=+*#ΞΣΔ01";

  function decode(element, duration = 650) {
    if (!element) return;
    const final = element.dataset.final || element.textContent;
    element.dataset.final = final;
    if (motion.matches) {
      element.textContent = final;
      return;
    }
    cancelAnimationFrame(element.decodeFrame);
    const start = performance.now();
    const step = (now) => {
      const progress = Math.min(1, (now - start) / duration);
      const revealed = Math.floor(progress * final.length);
      let text = final.slice(0, revealed);
      for (let i = revealed; i < final.length; i += 1) {
        text += final[i] === " " ? " " : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      }
      element.textContent = text;
      if (progress < 1) element.decodeFrame = requestAnimationFrame(step);
    };
    element.decodeFrame = requestAnimationFrame(step);
  }

  function typeText(element, text, speed = 32) {
    return new Promise((resolve) => {
      if (motion.matches) {
        element.textContent = text;
        resolve();
        return;
      }
      let index = 0;
      const step = () => {
        index += 1;
        element.textContent = text.slice(0, index);
        if (index < text.length) setTimeout(step, speed + Math.random() * speed);
        else resolve();
      };
      step();
    });
  }

  function countUp(element, from, to, duration = 1400) {
    if (motion.matches || from === to) {
      element.textContent = to;
      return;
    }
    const start = performance.now();
    const step = (now) => {
      const progress = Math.min(1, (now - start) / duration);
      const eased = 1 - (1 - progress) ** 3;
      element.textContent = Math.round(from + (to - from) * eased);
      if (progress < 1) requestAnimationFrame(step);
    };
    element.textContent = from;
    requestAnimationFrame(step);
  }

  let toastTimer = null;
  function toast(message) {
    const element = $("#echo-toast");
    if (!element) return;
    element.textContent = message;
    element.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => element.classList.remove("show"), 1800);
  }

  /* ---------- neural sky ---------- */

  // Household AI cores drifting in depth, wired by synapses. Pulses travel the
  // wiring, clicks send echo rings through it, and soundtrack notes fire it.
  function createSky(canvas) {
    if (!canvas) return { resize() {}, draw() {}, ring() {}, note() {}, pointer() {}, leave() {}, burst() {} };
    const ctx = canvas.getContext("2d");
    const sprites = new Map();
    const pointer = { x: 0, y: 0, active: false, px: 0, py: 0, tx: 0, ty: 0 };
    let width = 0;
    let height = 0;
    let nodes = [];
    let pulses = [];
    let rings = [];
    let spawnIn = 0.6;
    let slowFrames = 0;
    let lowPower = false;

    function sprite(color) {
      if (sprites.has(color)) return sprites.get(color);
      const size = 64;
      const image = document.createElement("canvas");
      image.width = size;
      image.height = size;
      const g = image.getContext("2d");
      const gradient = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
      gradient.addColorStop(0, rgba(LIGHT[color], 1));
      gradient.addColorStop(0.16, rgba(LIGHT[color], 0.6));
      gradient.addColorStop(0.42, rgba(LIGHT[color], 0.12));
      gradient.addColorStop(1, rgba(LIGHT[color], 0));
      g.fillStyle = gradient;
      g.fillRect(0, 0, size, size);
      sprites.set(color, image);
      return image;
    }

    function makeNode() {
      const z = 0.25 + Math.random() ** 1.5 * 0.75;
      return {
        x: rand(0, width),
        y: rand(0, height),
        z,
        vx: rand(-1, 1) * 7 * z,
        vy: rand(-1, 1) * 5 * z,
        color: pick(NODE_COLORS),
        phase: rand(0, TAU),
        flash: 0,
        sx: 0,
        sy: 0,
      };
    }

    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.round(clamp((width * height) / 12000, 36, lowPower ? 70 : 140));
      nodes = Array.from({ length: count }, makeNode);
      for (const node of nodes) {
        node.sx = node.x;
        node.sy = node.y;
      }
      pulses = [];
    }

    function neighbours(node, exclude, limit) {
      const reach = 70 + 120 * node.z;
      return nodes
        .filter((other) => other !== node && other !== exclude && Math.abs(other.z - node.z) < 0.25)
        .map((other) => ({ other, d: Math.hypot(other.sx - node.sx, other.sy - node.sy) }))
        .filter((entry) => entry.d < reach)
        .sort((a, b) => a.d - b.d)
        .slice(0, limit)
        .map((entry) => entry.other);
    }

    function launch(from, to, color, depth) {
      if (pulses.length > 110) return;
      pulses.push({ from, to, t: 0, duration: rand(0.45, 0.9), color, depth, done: false });
    }

    function fire(node, color = node.color, depth = 2) {
      node.flash = 1;
      for (const target of neighbours(node, null, 2)) launch(node, target, color, depth);
    }

    function ring(x, y, strength = 1, color = "cyan") {
      rings.push({ x, y, r: 0, life: 0, strength, color, hit: new Set() });
    }

    function note(event) {
      if (!nodes.length) return;
      const x = ((event.pan + 1) / 2) * width;
      const candidates = nodes.filter((node) => Math.abs(node.sx - x) < width * 0.18);
      const node = pick(candidates.length ? candidates : nodes);
      const color = NOTE_COLORS[((event.midi % 12) + 12) % 12] || "cyan";
      fire(node, color, event.soft ? 1 : 3);
    }

    function burst(x, y, color = "cyan") {
      ring(x, y, 1.5, color);
      setTimeout(() => ring(x, y, 1, color), 180);
    }

    function setPointer(x, y) {
      pointer.x = x;
      pointer.y = y;
      pointer.active = true;
      pointer.tx = x / width - 0.5;
      pointer.ty = y / height - 0.5;
    }

    function leave() {
      pointer.active = false;
      pointer.tx = 0;
      pointer.ty = 0;
    }

    function draw(frame) {
      const dt = frame.dt;
      // Drop to a lighter network if the machine is struggling.
      slowFrames = frame.dt > 0.03 ? slowFrames + 1 : Math.max(0, slowFrames - 1);
      if (!lowPower && slowFrames > 90) {
        lowPower = true;
        resize();
      }

      pointer.px = lerp(pointer.px, pointer.tx, Math.min(1, dt * 2.5));
      pointer.py = lerp(pointer.py, pointer.ty, Math.min(1, dt * 2.5));
      const fade = Math.pow(0.04, dt);
      for (const node of nodes) {
        node.x += node.vx * dt;
        node.y += node.vy * dt;
        if (node.x < -40) node.x = width + 40;
        else if (node.x > width + 40) node.x = -40;
        if (node.y < -40) node.y = height + 40;
        else if (node.y > height + 40) node.y = -40;
        node.flash *= fade;
        node.sx = node.x - pointer.px * node.z * 34;
        node.sy = node.y - pointer.py * node.z * 24;
      }

      ctx.clearRect(0, 0, width, height);
      ctx.globalCompositeOperation = "lighter";
      ctx.lineWidth = 1;

      // Synapses.
      const breathe = 1 + frame.beat * 0.9 + frame.level * 0.8 + frame.energy * 0.5;
      for (let i = 0; i < nodes.length; i += 1) {
        const a = nodes[i];
        const reach = 70 + 120 * a.z;
        for (let j = i + 1; j < nodes.length; j += 1) {
          const b = nodes[j];
          if (Math.abs(a.z - b.z) > 0.22) continue;
          const dx = a.sx - b.sx;
          const dy = a.sy - b.sy;
          if (dx > reach || dx < -reach || dy > reach || dy < -reach) continue;
          const d = Math.sqrt(dx * dx + dy * dy);
          if (d > reach) continue;
          const alpha = (1 - d / reach) * (0.04 + 0.11 * a.z) * breathe + (a.flash + b.flash) * 0.16;
          ctx.strokeStyle = `rgba(150, 215, 232, ${Math.min(alpha, 0.7)})`;
          ctx.beginPath();
          ctx.moveTo(a.sx, a.sy);
          ctx.lineTo(b.sx, b.sy);
          ctx.stroke();
        }
      }

      // The visitor is a node too.
      if (pointer.active) {
        for (const node of nodes) {
          const d = Math.hypot(node.sx - pointer.x, node.sy - pointer.y);
          if (d > 190) continue;
          const k = 1 - d / 190;
          node.flash = Math.max(node.flash, k * 0.3);
          ctx.strokeStyle = rgba(LIGHT.snow, k * 0.2 * node.z);
          ctx.beginPath();
          ctx.moveTo(node.sx, node.sy);
          ctx.lineTo(pointer.x, pointer.y);
          ctx.stroke();
        }
      }

      // Echo rings wake every node on their wavefront.
      for (const echo of rings) {
        echo.life += dt;
        echo.r += dt * (360 + 140 * echo.strength);
        const remaining = 1 - echo.life / 1.9;
        if (remaining <= 0) continue;
        ctx.lineWidth = 1.4;
        ctx.strokeStyle = rgba(LIGHT[echo.color], 0.5 * remaining * Math.min(1, echo.strength));
        ctx.beginPath();
        ctx.arc(echo.x, echo.y, echo.r, 0, TAU);
        ctx.stroke();
        ctx.lineWidth = 1;
        ctx.strokeStyle = rgba(LIGHT.pink, 0.22 * remaining * Math.min(1, echo.strength));
        ctx.beginPath();
        ctx.arc(echo.x, echo.y, echo.r * 0.7, 0, TAU);
        ctx.stroke();
        for (const node of nodes) {
          if (echo.hit.has(node)) continue;
          if (Math.abs(Math.hypot(node.sx - echo.x, node.sy - echo.y) - echo.r) > 14) continue;
          echo.hit.add(node);
          node.flash = 1;
          if (Math.random() < 0.07 * echo.strength) fire(node, echo.color, 1);
        }
      }
      rings = rings.filter((echo) => echo.life < 1.9);

      // Synaptic pulses.
      ctx.lineWidth = 1.6;
      for (const pulse of pulses) {
        pulse.t += dt / pulse.duration;
        const head = Math.min(1, pulse.t);
        const tail = Math.max(0, head - 0.3);
        const hx = lerp(pulse.from.sx, pulse.to.sx, head);
        const hy = lerp(pulse.from.sy, pulse.to.sy, head);
        const tx = lerp(pulse.from.sx, pulse.to.sx, tail);
        const ty = lerp(pulse.from.sy, pulse.to.sy, tail);
        const trail = ctx.createLinearGradient(tx, ty, hx, hy);
        trail.addColorStop(0, rgba(LIGHT[pulse.color], 0));
        trail.addColorStop(1, rgba(LIGHT[pulse.color], 0.85));
        ctx.strokeStyle = trail;
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(hx, hy);
        ctx.stroke();
        ctx.drawImage(sprite(pulse.color), hx - 8, hy - 8, 16, 16);
        if (pulse.t >= 1) {
          pulse.done = true;
          pulse.to.flash = 1;
          if (pulse.depth > 0) {
            for (const next of neighbours(pulse.to, pulse.from, Math.random() < 0.35 ? 2 : 1)) {
              launch(pulse.to, next, pulse.color, pulse.depth - 1);
            }
          }
        }
      }
      pulses = pulses.filter((pulse) => !pulse.done);

      // Cores.
      const t = frame.now / 1000;
      for (const node of nodes) {
        const twinkle = 0.75 + 0.25 * Math.sin(t * (0.6 + node.z) + node.phase);
        const size = (5 + 12 * node.z) * (twinkle + node.flash * 1.4) * (1 + frame.level * 0.6);
        ctx.globalAlpha = clamp((0.22 + 0.55 * node.z) * twinkle + node.flash * 0.6, 0, 1);
        ctx.drawImage(sprite(node.color), node.sx - size / 2, node.sy - size / 2, size, size);
      }
      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation = "source-over";

      if (frame.still) return;
      spawnIn -= dt;
      if (spawnIn <= 0 && nodes.length) {
        spawnIn = rand(0.5, 1.4) / (1 + frame.energy * 2.5);
        fire(pick(nodes), undefined, 2 + Math.round(frame.energy * 2));
      }
    }

    resize();
    return { resize, draw, ring, note, burst, pointer: setPointer, leave };
  }

  /* ---------- World Brain globe ---------- */

  // ECHO as a planet: a dotted sphere of household cores, memory arcs leaping
  // between cities, three orbital rings and a latitude scan that never stops.
  function createGlobe(canvas) {
    if (!canvas) return { draw() {} };
    const host = canvas.parentElement;
    const ctx = canvas.getContext("2d");
    const longitude = $("#core-longitude");
    const sync = $("#core-sync");
    const COUNT = 640;
    const golden = Math.PI * (3 - Math.sqrt(5));
    const points = Array.from({ length: COUNT }, (_, i) => {
      const y = 1 - (i / (COUNT - 1)) * 2;
      const r = Math.sqrt(1 - y * y);
      return { x: Math.cos(golden * i) * r, y, z: Math.sin(golden * i) * r, city: Math.random() < 0.09, phase: rand(0, TAU) };
    });
    const orbits = [
      { radius: 1.3, incline: 1.18, yaw: 0.3, speed: 0.5, color: "cyan", dash: [3, 5] },
      { radius: 1.47, incline: 1.92, yaw: -0.6, speed: -0.32, color: "pink", dash: [12, 7] },
      { radius: 1.64, incline: 1.42, yaw: 1.2, speed: 0.22, color: "green", dash: [1, 6] },
    ];
    let arcs = [];
    let width = 0;
    let height = 0;
    let radius = 0;
    let cx = 0;
    let cy = 0;
    let rotation = rand(0, TAU);
    let velocity = 0;
    let tilt = 0.42;
    let tiltTarget = 0.42;
    let drag = null;
    let visible = true;
    let hudIn = 0;
    let lastFrame = null;

    function makeArc() {
      const a = pick(points);
      let b = pick(points);
      for (let tries = 0; tries < 20; tries += 1) {
        const dot = a.x * b.x + a.y * b.y + a.z * b.z;
        if (dot < 0.85 && dot > -0.2) break;
        b = pick(points);
      }
      return { a, b, head: Math.random(), speed: rand(0.25, 0.55), lift: rand(0.14, 0.32), color: pick(["cyan", "pink", "snow", "signal"]), age: 0, life: rand(3, 7) };
    }
    arcs = Array.from({ length: 14 }, makeArc);

    function resize() {
      const rect = host.getBoundingClientRect();
      if (!rect.width || !rect.height) return;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = rect.width;
      height = rect.height;
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      radius = Math.min(width, height) * 0.27;
      cx = width / 2;
      cy = height / 2 + 6;
      if (lastFrame?.still) draw(lastFrame);
    }

    function view(x, y, z, spin) {
      const cos = Math.cos(spin);
      const sin = Math.sin(spin);
      const rx = x * cos + z * sin;
      const rz = -x * sin + z * cos;
      const ct = Math.cos(tilt);
      const st = Math.sin(tilt);
      return { x: rx, y: y * ct - rz * st, z: y * st + rz * ct };
    }

    function project(v, scale) {
      const depth = 3.2 / (3.2 - v.z);
      return { x: cx + v.x * scale * depth, y: cy - v.y * scale * depth, z: v.z, depth };
    }

    function draw(frame) {
      lastFrame = frame;
      if (!visible || !width) return;
      const dt = frame.dt;
      const t = frame.now / 1000;
      if (!drag) {
        rotation += (0.16 + velocity) * dt;
        velocity *= Math.pow(0.15, dt);
      }
      tilt = lerp(tilt, tiltTarget, Math.min(1, dt * 3));
      const r = radius * (1 + frame.level * 0.05 + frame.beat * 0.025);

      ctx.clearRect(0, 0, width, height);

      const glow = ctx.createRadialGradient(cx, cy, r * 0.2, cx, cy, r * 1.9);
      glow.addColorStop(0, `rgba(127, 230, 242, ${0.16 + frame.level * 0.25 + frame.beat * 0.1})`);
      glow.addColorStop(0.5, "rgba(127, 230, 242, 0.04)");
      glow.addColorStop(1, "rgba(127, 230, 242, 0)");
      ctx.fillStyle = glow;
      ctx.fillRect(0, 0, width, height);

      const orbitPaths = orbits.map((orbit) => {
        const path = [];
        for (let i = 0; i <= 72; i += 1) {
          const angle = (i / 72) * TAU;
          const ox = Math.cos(angle) * orbit.radius;
          const oz = Math.sin(angle) * orbit.radius;
          path.push(project(view(ox, -oz * Math.sin(orbit.incline), oz * Math.cos(orbit.incline), orbit.yaw + t * 0.05), r));
        }
        return path;
      });

      const drawOrbits = (front) => {
        orbits.forEach((orbit, index) => {
          const path = orbitPaths[index];
          ctx.setLineDash(orbit.dash);
          ctx.lineWidth = 1;
          ctx.strokeStyle = rgba(LIGHT[orbit.color], front ? 0.55 : 0.16);
          ctx.beginPath();
          let pen = false;
          for (const p of path) {
            if (p.z >= 0 === front) {
              if (pen) ctx.lineTo(p.x, p.y);
              else ctx.moveTo(p.x, p.y);
              pen = true;
            } else pen = false;
          }
          ctx.stroke();
          ctx.setLineDash([]);
          const angle = (t * orbit.speed) % TAU;
          const sx = Math.cos(angle) * orbit.radius;
          const sz = Math.sin(angle) * orbit.radius;
          const sat = project(view(sx, -sz * Math.sin(orbit.incline), sz * Math.cos(orbit.incline), orbit.yaw + t * 0.05), r);
          if (sat.z >= 0 === front) {
            ctx.fillStyle = rgba(LIGHT[orbit.color], front ? 1 : 0.35);
            ctx.shadowColor = rgba(LIGHT[orbit.color], 1);
            ctx.shadowBlur = front ? 12 : 0;
            ctx.beginPath();
            ctx.arc(sat.x, sat.y, front ? 2.6 : 1.8, 0, TAU);
            ctx.fill();
            ctx.shadowBlur = 0;
          }
        });
      };

      drawOrbits(false);

      // Surface: household cores, with a latitude scan sweeping the planet.
      const scan = Math.sin(t * 0.45) * 0.92;
      for (const point of points) {
        const p = project(view(point.x, point.y, point.z, rotation), r);
        const front = p.z > 0;
        const scanned = Math.abs(point.y - scan) < 0.05;
        if (point.city && front) {
          const pulse = 0.6 + 0.4 * Math.sin(t * 2 + point.phase) + frame.beat * 0.6;
          ctx.fillStyle = `rgba(245, 168, 202, ${clamp(0.35 + pulse * 0.45, 0, 1)})`;
          ctx.beginPath();
          ctx.arc(p.x, p.y, 1.6 + pulse * 0.9, 0, TAU);
          ctx.fill();
          continue;
        }
        const alpha = front ? 0.22 + 0.7 * p.z : 0.07 + 0.08 * (1 + p.z);
        const size = front ? 1 + p.z * 1.3 : 0.8;
        ctx.fillStyle = scanned && front ? `rgba(127, 230, 242, ${Math.min(1, alpha + 0.5)})` : `rgba(222, 240, 246, ${alpha})`;
        ctx.fillRect(p.x - size / 2, p.y - size / 2, size, size);
      }

      // Atmosphere rim.
      ctx.lineWidth = 1;
      ctx.strokeStyle = `rgba(201, 247, 255, ${0.18 + frame.level * 0.3})`;
      ctx.beginPath();
      ctx.arc(cx, cy, r * 1.02, 0, TAU);
      ctx.stroke();

      // Memory arcs leaping between cities.
      for (const arc of arcs) {
        arc.age += dt;
        arc.head = (arc.head + dt * arc.speed) % 1.25;
        const envelope = Math.min(1, arc.age / 0.8, Math.max(0, (arc.life - arc.age) / 0.8));
        let previous = null;
        for (let i = 0; i <= 28; i += 1) {
          const s = i / 28;
          let x = lerp(arc.a.x, arc.b.x, s);
          let y = lerp(arc.a.y, arc.b.y, s);
          let z = lerp(arc.a.z, arc.b.z, s);
          const length = Math.hypot(x, y, z) || 1;
          const lift = 1 + arc.lift * Math.sin(Math.PI * s);
          x = (x / length) * lift;
          y = (y / length) * lift;
          z = (z / length) * lift;
          const p = project(view(x, y, z, rotation), r);
          if (previous) {
            const near = Math.abs(s - arc.head);
            const lit = near < 0.12 ? 1 - near / 0.12 : 0;
            const depth = p.z > -0.1 ? 1 : 0.2;
            ctx.strokeStyle = rgba(LIGHT[arc.color], (0.12 + lit * 0.85) * depth * envelope);
            ctx.lineWidth = 1 + lit * 1.2;
            ctx.beginPath();
            ctx.moveTo(previous.x, previous.y);
            ctx.lineTo(p.x, p.y);
            ctx.stroke();
          }
          previous = p;
        }
      }
      arcs = arcs.map((arc) => (arc.age > arc.life ? makeArc() : arc));

      drawOrbits(true);

      hudIn -= dt;
      if (hudIn <= 0 && !frame.still) {
        hudIn = 0.15;
        const degrees = ((((rotation * 180) / Math.PI) % 360) + 360) % 360;
        if (longitude) {
          longitude.textContent = degrees > 180 ? `LON ${(360 - degrees).toFixed(1)}°W` : `LON ${degrees.toFixed(1)}°E`;
        }
        if (sync) sync.textContent = `${(99.1 + frame.level * 0.8 + Math.random() * 0.08).toFixed(2)}%`;
      }
    }

    // Grab the planet and spin it.
    canvas.addEventListener("pointerdown", (event) => {
      if (event.button !== 0) return;
      drag = { x: event.clientX, y: event.clientY, rotation, tilt: tiltTarget, last: event.clientX, time: performance.now() };
      canvas.setPointerCapture(event.pointerId);
      canvas.classList.add("grabbing");
    });
    canvas.addEventListener("pointermove", (event) => {
      if (!drag) return;
      rotation = drag.rotation + (event.clientX - drag.x) * 0.01;
      tiltTarget = clamp(drag.tilt + (event.clientY - drag.y) * 0.006, -0.3, 1.1);
      const now = performance.now();
      velocity = ((event.clientX - drag.last) * 0.01) / Math.max(0.016, (now - drag.time) / 1000) - 0.16;
      drag.last = event.clientX;
      drag.time = now;
    });
    const release = () => {
      if (!drag) return;
      drag = null;
      velocity = clamp(velocity, -4, 4);
      tiltTarget = lerp(tiltTarget, 0.42, 0.5);
      canvas.classList.remove("grabbing");
    };
    canvas.addEventListener("pointerup", release);
    canvas.addEventListener("pointercancel", release);

    new ResizeObserver(resize).observe(host);
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
    }).observe(host);
    resize();
    return { draw, resize };
  }

  /* ---------- frame loop ---------- */

  const frame = { now: 0, dt: 0.016, level: 0, beat: 0, energy: 0, still: false };
  const renderers = [];
  let rafId = 0;
  let forgeRunning = false;

  function loop(now) {
    frame.dt = frame.now ? Math.min(0.05, (now - frame.now) / 1000) : 0.016;
    frame.now = now;
    frame.level = lerp(frame.level, audio ? audio.level() : 0, 0.2);
    frame.beat *= Math.pow(0.03, frame.dt);
    frame.energy = lerp(frame.energy, forgeRunning ? 1 : 0, Math.min(1, frame.dt * 2));
    for (const render of renderers) render(frame);
    rafId = requestAnimationFrame(loop);
  }

  function startLoop() {
    if (!rafId && !motion.matches) rafId = requestAnimationFrame(loop);
  }

  function stopLoop() {
    cancelAnimationFrame(rafId);
    rafId = 0;
    frame.now = 0;
  }

  function renderStill() {
    const still = { now: performance.now(), dt: 0, level: 0, beat: 0, energy: 0, still: true };
    for (const render of renderers) render(still);
  }

  /* ---------- boot sequence ---------- */

  const BOOT_LINES = [
    ["echo core", "cold start"],
    ["household cores", "2,147,000,000 linked"],
    ["white ghost network", "handshake ok"],
    ["canon bible", "mounted read-only"],
    ["ghost registry", "monitored"],
    ["laws 01-04", "no magic · tech only"],
    ["identity check", "is this you?", "warn"],
  ];
  const QUESTIONS = [
    "If memory can be copied, what is a human?",
    "If consciousness can be uploaded, what is death?",
    "If a perfect copy of you exists, which one is real?",
  ];

  let booted = false;
  const afterBoot = [];

  function whenBooted(callback) {
    if (booted) callback();
    else afterBoot.push(callback);
  }

  function revealDesktop() {
    if (booted) return;
    booted = true;
    document.body.classList.remove("is-booting");
    document.body.classList.add("booted");
    $all(".window.active .titlebar h1, .window.active .titlebar h2").forEach((title, index) => {
      setTimeout(() => decode(title, 700), 180 + index * 110);
    });
    afterBoot.splice(0).forEach((callback) => callback());
  }

  function runBoot() {
    const boot = $("#boot");
    const log = $("#boot-log");
    if (!boot || !log) {
      revealDesktop();
      return;
    }
    const full = new URLSearchParams(window.location.search).has("boot") || readPref(BOOT_PREF) !== "1";
    const fast = !full || motion.matches;
    let finished = false;
    let timer = null;
    let index = 0;

    const finish = (choice) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      document.removeEventListener("keydown", onKey);
      if (choice && audio) {
        const withSound = choice === "sound";
        audio.setSfx(withSound);
        audio.setMusic(withSound);
        if (withSound) setTimeout(() => audio.sfx("boot"), 80);
        toast(withSound ? "Soundtrack · on — press M to mute" : "Silent mode — press M for music");
      }
      writePref(BOOT_PREF, "1");
      boot.classList.add("leaving");
      revealDesktop();
      setTimeout(() => {
        boot.hidden = true;
      }, motion.matches ? 0 : 1100);
    };

    const ready = async () => {
      if (!full) {
        timer = setTimeout(() => finish(null), motion.matches ? 0 : 420);
        return;
      }
      await typeText($("#boot-question"), pick(QUESTIONS), 30);
      boot.classList.add("ready");
      boot.querySelector(".boot-enter.primary")?.focus({ preventScroll: true });
    };

    const addLine = () => {
      if (index >= BOOT_LINES.length) {
        ready();
        return;
      }
      const [key, value, tone] = BOOT_LINES[index];
      const line = document.createElement("li");
      line.innerHTML = `<span class="t">[${(0.117 * index + 0.003 * index * index).toFixed(3)}]</span><span class="k"></span><span class="dots"></span><span class="v"></span>`;
      line.querySelector(".k").textContent = key;
      const result = line.querySelector(".v");
      result.textContent = value;
      if (tone) result.classList.add(tone);
      log.append(line);
      decode(result, fast ? 200 : 420);
      index += 1;
      timer = setTimeout(addLine, fast ? 70 : rand(170, 300));
    };

    // Skip the typing on a click; the choice buttons still decide about sound.
    const rush = () => {
      if (index >= BOOT_LINES.length || finished) return;
      clearTimeout(timer);
      while (index < BOOT_LINES.length) {
        const [key, value, tone] = BOOT_LINES[index];
        const line = document.createElement("li");
        line.innerHTML = `<span class="t">[${(0.117 * index).toFixed(3)}]</span><span class="k"></span><span class="dots"></span><span class="v"></span>`;
        line.querySelector(".k").textContent = key;
        line.querySelector(".v").textContent = value;
        if (tone) line.querySelector(".v").classList.add(tone);
        log.append(line);
        index += 1;
      }
      ready();
    };

    function onKey(event) {
      // A focused choice button answers Enter itself.
      if (event.key === "Enter" && !event.target.closest?.("[data-enter]")) {
        event.preventDefault();
        finish("sound");
      } else if (event.key === "Escape") {
        finish("silent");
      }
    }

    if (!full) boot.classList.add("quick");
    boot.querySelectorAll("[data-enter]").forEach((button) => {
      button.addEventListener("click", () => finish(button.dataset.enter));
    });
    boot.addEventListener("pointerdown", (event) => {
      if (!event.target.closest("button")) rush();
    });
    if (full) document.addEventListener("keydown", onKey);
    timer = setTimeout(addLine, fast ? 0 : 500);
  }

  /* ---------- ambient events ---------- */

  const WHISPERS = [
    "If memory can be copied, what is a human?",
    "If consciousness can be uploaded, what is death?",
    "If a perfect copy of you exists, which one is real?",
    "回响纪元 · ECHO: Echo Age",
    "幽灵觉醒 · Ghost Awakening",
    "identity registry · checksum mismatch",
    "memory afterimage detected · sector 7",
    "whose birthday was it?",
    "the household core is still listening",
    "voice waveform halo · unregistered",
    "consent key rotated · 00:00:03 ago",
  ];

  function startWhispers() {
    const layer = $("#ghost-layer");
    if (!layer) return;
    const spawn = () => {
      if (!document.hidden && booted && layer.childElementCount < 3) {
        const whisper = document.createElement("div");
        whisper.className = "whisper";
        whisper.textContent = pick(WHISPERS);
        whisper.style.left = `${rand(4, 66)}%`;
        whisper.style.top = `${rand(10, 92)}%`;
        whisper.addEventListener("animationend", () => whisper.remove());
        layer.append(whisper);
      }
      setTimeout(spawn, rand(6000, 12000));
    };
    setTimeout(spawn, 3000);
  }

  // Ghost contamination: once in a while a window flickers like black glass.
  function startContamination() {
    const strike = () => {
      const windows = $all(".window.active:not(.dragging)");
      if (!document.hidden && booted && windows.length) {
        const target = pick(windows);
        target.classList.add("ghost-glitch");
        audio?.sfx("glitch", { pan: panFor(target) });
        setTimeout(() => target.classList.remove("ghost-glitch"), 450);
      }
      setTimeout(strike, rand(40000, 75000));
    };
    setTimeout(strike, rand(22000, 32000));
  }

  /* ---------- interaction ---------- */

  const TILT_TARGETS = ".agent-tile, .asset-card, .forge-command, .metric";
  const TAP_TARGETS = ".dock-item, .forge-command, .window-actions button, .candidate-actions button, .asset-links a";

  function installPointer(sky) {
    let tilted = null;
    const resetTilt = (card) => {
      for (const name of ["--rx", "--ry"]) card.style.removeProperty(name);
    };

    window.addEventListener(
      "pointermove",
      (event) => {
        sky.pointer(event.clientX, event.clientY);
        if (motion.matches || event.pointerType === "touch") return;
        const card = event.target.closest?.(TILT_TARGETS) || null;
        if (tilted && tilted !== card) resetTilt(tilted);
        tilted = card;
        if (card) {
          const rect = card.getBoundingClientRect();
          const px = (event.clientX - rect.left) / rect.width;
          const py = (event.clientY - rect.top) / rect.height;
          const strength = card.classList.contains("agent-tile") ? 5 : 10;
          card.style.setProperty("--ry", `${((px - 0.5) * strength).toFixed(2)}deg`);
          card.style.setProperty("--rx", `${((0.5 - py) * strength).toFixed(2)}deg`);
          card.style.setProperty("--gx", `${(px * 100).toFixed(1)}%`);
          card.style.setProperty("--gy", `${(py * 100).toFixed(1)}%`);
        }
        const panel = event.target.closest?.(".window");
        if (panel) {
          const rect = panel.getBoundingClientRect();
          panel.style.setProperty("--mx", `${Math.round(event.clientX - rect.left)}px`);
          panel.style.setProperty("--my", `${Math.round(event.clientY - rect.top)}px`);
        }
      },
      { passive: true },
    );

    document.documentElement.addEventListener("pointerleave", () => {
      sky.leave();
      if (tilted) resetTilt(tilted);
      tilted = null;
    });

    window.addEventListener(
      "pointerdown",
      (event) => {
        const inside = event.target.closest?.(".window, .dock, .system-bar, .boot, .sound-panel");
        sky.ring(event.clientX, event.clientY, inside ? 0.5 : 1);
        if (!inside) audio?.sfx("echo", { pan: panAt(event.clientX) });
        else if (event.target.closest?.(TAP_TARGETS)) audio?.sfx("tap", { pan: panAt(event.clientX) });
      },
      { passive: true },
    );

    $all(".dock-item").forEach((item) => {
      item.addEventListener("pointerenter", () => audio?.sfx("hover", { pan: -0.7 }));
      item.addEventListener("click", () => {
        const panel = $(`[data-window-panel="${item.dataset.window}"]`);
        if (!panel) return;
        panel.classList.remove("summoned");
        void panel.offsetWidth;
        panel.classList.add("summoned");
        setTimeout(() => panel.classList.remove("summoned"), 950);
      });
    });
  }

  function watchWindows() {
    const observer = new MutationObserver((records) => {
      for (const record of records) {
        const panel = record.target;
        const wasActive = (record.oldValue || "").split(/\s+/).includes("active");
        if (!wasActive && panel.classList.contains("active") && booted) {
          audio?.sfx("open", { pan: panFor(panel) });
          decode(panel.querySelector(".titlebar h1, .titlebar h2"), 600);
        }
      }
    });
    $all(".window").forEach((panel) => {
      observer.observe(panel, { attributes: true, attributeFilter: ["class"], attributeOldValue: true });
    });
  }

  function watchContent() {
    const shown = new Map();
    const metrics = $("#metrics");
    if (metrics) {
      new MutationObserver(() => {
        const cards = $all("#metrics .metric");
        const values = cards.map((card) => Number(card.querySelector("strong")?.textContent));
        const max = Math.max(1, ...values.filter(Number.isFinite));
        cards.forEach((card, index) => {
          const value = values[index];
          const strong = card.querySelector("strong");
          if (!strong || !Number.isFinite(value)) return;
          const label = card.querySelector("span")?.textContent || String(index);
          const from = shown.get(label) ?? 0;
          shown.set(label, value);
          strong.textContent = from;
          whenBooted(() => {
            countUp(strong, from, value);
            requestAnimationFrame(() =>
              requestAnimationFrame(() => card.style.setProperty("--fill", (value / max).toFixed(3))),
            );
          });
        });
      }).observe(metrics, { childList: true });
    }

    const stream = $("#memory-stream");
    if (stream) {
      const stagger = () => $all("#memory-stream li").forEach((item, index) => item.style.setProperty("--n", index));
      new MutationObserver(stagger).observe(stream, { childList: true });
      stagger();
    }

    const output = $("#factory-output");
    const terminal = $("#factory-terminal");
    if (output && terminal) {
      new MutationObserver(() => {
        terminal.classList.remove("signal");
        void terminal.offsetWidth;
        terminal.classList.add("signal");
      }).observe(output, { childList: true, characterData: true, subtree: true });
    }
  }

  function installForge(sky) {
    let pressed = null;
    document.addEventListener(
      "click",
      (event) => {
        const button = event.target.closest?.(".forge-command");
        if (button) pressed = button;
      },
      true,
    );
    document.addEventListener("echo:forge", (event) => {
      const phase = event.detail?.phase;
      const forge = $('[data-window-panel="factory"]');
      const rect = forge?.getBoundingClientRect();
      const x = rect ? rect.left + rect.width / 2 : window.innerWidth / 2;
      const y = rect ? rect.top + rect.height / 2 : window.innerHeight / 2;
      if (phase === "start") {
        forgeRunning = true;
        document.body.classList.add("forge-running");
        pressed?.classList.add("running");
        audio?.setIntensity(0.92);
        return;
      }
      forgeRunning = false;
      document.body.classList.remove("forge-running");
      $all(".forge-command.running").forEach((button) => button.classList.remove("running"));
      audio?.resetIntensity();
      if (phase === "done") {
        audio?.sfx("success", { pan: panAt(x) });
        sky.burst(x, y, "cyan");
      } else {
        audio?.sfx("error", { pan: panAt(x) });
        sky.burst(x, y, "red");
        document.body.classList.add("breach");
        setTimeout(() => document.body.classList.remove("breach"), 900);
      }
    });
  }

  /* ---------- sound controls ---------- */

  function installSoundControls() {
    const control = $("#sound-control");
    const toggle = $("#sound-toggle");
    const label = $("#sound-label");
    const more = $("#sound-more");
    const panel = $("#sound-panel");
    const volume = $("#sound-volume");
    const sfx = $("#sound-sfx");
    const chord = $("#sound-chord");
    const bars = $all("#sound-eq i");
    if (!control || !toggle) return;
    if (!audio) {
      control.hidden = true;
      return;
    }

    const sync = () => {
      const on = audio.music;
      const live = on && audio.running;
      toggle.setAttribute("aria-pressed", String(on));
      toggle.classList.toggle("on", live);
      toggle.classList.toggle("armed", on && !live);
      label.textContent = !on ? "Sound off" : live ? "Sound on" : "Tap to resume";
      volume.value = String(Math.round(audio.volume * 100));
      sfx.checked = audio.sfxEnabled;
    };

    const toggleSound = () => {
      if (audio.music && !audio.running) {
        audio.unlock();
        toast("Soundtrack · resumed");
        return;
      }
      audio.toggleMusic();
      toast(audio.music ? "Soundtrack · on" : "Soundtrack · off");
    };

    const setPanel = (open) => {
      panel.hidden = !open;
      more.setAttribute("aria-expanded", String(open));
    };

    toggle.addEventListener("click", toggleSound);
    more.addEventListener("click", () => setPanel(panel.hidden));
    volume.addEventListener("input", () => {
      audio.setVolume(Number(volume.value) / 100);
      audio.unlock();
    });
    sfx.addEventListener("change", () => {
      audio.setSfx(sfx.checked);
      if (sfx.checked) setTimeout(() => audio.sfx("tap"), 60);
    });
    document.addEventListener("pointerdown", (event) => {
      if (!panel.hidden && !event.target.closest("#sound-control")) setPanel(false);
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !panel.hidden) {
        setPanel(false);
        more.focus();
        return;
      }
      if ((event.key || "").toLowerCase() !== "m" || event.ctrlKey || event.metaKey || event.altKey || event.repeat) return;
      if (event.target.closest?.("input, textarea, select, [contenteditable]") || !booted) return;
      toggleSound();
    });

    audio.on((event) => {
      if (event.type === "state") sync();
      else if (event.type === "chord" && chord) chord.textContent = `generative score · ${event.name}`;
    });

    let eqLive = false;
    renderers.push(() => {
      const live = audio.music && audio.running;
      if (live) {
        const levels = audio.bands(bars.length);
        bars.forEach((bar, index) => {
          bar.style.transform = `scaleY(${(0.18 + levels[index] * 0.82).toFixed(3)})`;
        });
        eqLive = true;
      } else if (eqLive) {
        bars.forEach((bar) => bar.style.removeProperty("transform"));
        eqLive = false;
      }
    });

    sync();
  }

  /* ---------- start ---------- */

  const sky = createSky($("#neural-sky"));
  const globe = createGlobe($("#core-canvas"));
  renderers.push(sky.draw, globe.draw);

  installSoundControls();
  installPointer(sky);
  installForge(sky);
  watchWindows();
  watchContent();

  audio?.on((event) => {
    if (event.type === "note") sky.note(event);
    else if (event.type === "beat") frame.beat = Math.max(frame.beat, event.strength);
  });

  window.addEventListener("resize", () => {
    sky.resize();
    if (motion.matches) renderStill();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopLoop();
    else startLoop();
  });

  runBoot();
  if (motion.matches) {
    renderStill();
  } else {
    startLoop();
    startWhispers();
    startContamination();
  }
})();
