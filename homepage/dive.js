/* ECHO site: "Memory Dive / 记忆潜航".
 *
 * Below the hero the whole page becomes one continuous dive through the Memory Sea.
 * A single WebGL particle field sits behind every section and re-forms as the visitor
 * scrolls: the sea surface, a civilisation globe, six embodiments, a continuity knot,
 * a helix of life, a stream of context, a spiral universe and, at the end, the ECHO
 * mark rising on the horizon. A depth gauge on the right doubles as chapter navigation.
 *
 * WebGL 1 only, no eval and no network, so it runs under the site's strict CSP. The
 * particle layer never renders while the hero covers it, while the page is hidden or
 * paused, or for reduced-motion visitors; the gauge works for everyone.
 */
(() => {
  "use strict";
  const main = document.querySelector("main");
  const hero = document.querySelector(".future-hero");
  if (!main) return;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)");
  const audio = window.EchoAudio || null;
  const tau = Math.PI * 2;
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const smooth = (edge0, edge1, x) => {
    const t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
    return t * t * (3 - 2 * t);
  };

  /* ---------- chapters ---------- */

  // Which formation each chapter dives into (homepage and /universe/ ids).
  const CHAPTERS = {
    gateways: "sea",
    ecosystem: "globe",
    products: "six",
    capabilities: "knot",
    labs: "helix",
    "system-flow": "stream",
    universe: "galaxy",
    roadmap: "symbol",
    canon: "sea",
    story: "stream",
    atlas: "globe",
    media: "galaxy",
    community: "six",
    "canon-notes": "symbol",
  };
  const ORDER = ["sea", "globe", "six", "knot", "helix", "stream", "galaxy", "symbol"];
  const NAMES = {
    sea: ["海面", "THE SURFACE"],
    globe: ["文明", "CIVILIZATION"],
    six: ["化身", "EMBODIMENTS"],
    knot: ["连续", "CONTINUITY"],
    helix: ["生命", "LIFE"],
    stream: ["语境", "CONTEXT"],
    galaxy: ["宇宙", "UNIVERSE"],
    symbol: ["地平线", "HORIZON"],
  };
  const english = () => document.documentElement.lang.startsWith("en");

  const chapters = Array.from(main.children)
    .filter((element) => element.tagName === "SECTION" && !element.classList.contains("future-hero"))
    .map((element, index) => ({ element, formation: CHAPTERS[element.id] || ORDER[index % ORDER.length], anchor: 0 }));
  if (!chapters.length) return;

  function measure() {
    for (const chapter of chapters) {
      const rect = chapter.element.getBoundingClientRect();
      chapter.anchor = rect.top + scrollY + Math.min(rect.height, innerHeight * 1.4) / 2 - innerHeight / 2;
    }
  }

  // Scroll position -> the two formations being blended and how far between them.
  function locate(position) {
    if (position <= chapters[0].anchor) return { from: 0, to: 0, mix: 0, active: 0 };
    const last = chapters.length - 1;
    if (position >= chapters[last].anchor) return { from: last, to: last, mix: 0, active: last };
    let i = 0;
    while (i < last && position >= chapters[i + 1].anchor) i += 1;
    const t = (position - chapters[i].anchor) / Math.max(1, chapters[i + 1].anchor - chapters[i].anchor);
    const mix = smooth(0.18, 0.82, t);
    return { from: i, to: i + 1, mix, active: mix < 0.5 ? i : i + 1 };
  }

  /* ---------- depth gauge ---------- */

  const gauge = document.createElement("nav");
  gauge.className = "dive-gauge";
  const readout = document.createElement("div");
  readout.className = "dive-readout";
  const depthText = document.createElement("span");
  depthText.className = "dive-depth";
  const nameText = document.createElement("strong");
  nameText.className = "dive-name";
  const countText = document.createElement("small");
  countText.className = "dive-count";
  readout.append(depthText, nameText, countText);
  const rail = document.createElement("ol");
  rail.className = "dive-rail";
  const fill = document.createElement("span");
  fill.className = "dive-fill";
  fill.setAttribute("aria-hidden", "true");
  rail.append(fill);
  const buttons = chapters.map((chapter, index) => {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.append(document.createElement("i"));
    button.addEventListener("click", () => {
      chapter.element.scrollIntoView({ behavior: reduce.matches ? "auto" : "smooth", block: "start" });
    });
    item.append(button);
    rail.append(item);
    return button;
  });
  gauge.append(readout, rail);
  document.body.append(gauge);

  let active = -1;
  function labelGauge() {
    const lang = english() ? 1 : 0;
    gauge.setAttribute("aria-label", english() ? "Dive depth and chapters" : "潜航深度与章节");
    buttons.forEach((button, index) => {
      const label = NAMES[chapters[index].formation][lang];
      button.setAttribute("aria-label", `${String(index + 1).padStart(2, "0")} · ${label}`);
      button.dataset.label = label;
    });
    if (active >= 0) nameText.textContent = NAMES[chapters[active].formation][lang];
  }

  function updateGauge(state) {
    const depth = clamp(scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight), 0, 1);
    const reading = `${english() ? "DEPTH" : "深度"} ${Math.round(depth * 2147).toString().padStart(4, "0")} m`;
    if (depthText.textContent !== reading) depthText.textContent = reading;
    fill.style.setProperty("transform", `scaleY(${depth.toFixed(3)})`);
    const heroBottom = hero ? hero.offsetTop + hero.offsetHeight : 0;
    gauge.classList.toggle("show", scrollY > heroBottom * 0.55);
    if (state.active === active) return;
    const first = active < 0;
    active = state.active;
    buttons.forEach((button, index) => {
      button.classList.toggle("active", index === active);
      if (index === active) button.setAttribute("aria-current", "step");
      else button.removeAttribute("aria-current");
    });
    nameText.textContent = NAMES[chapters[active].formation][english() ? 1 : 0];
    countText.textContent = `${String(active + 1).padStart(2, "0")} / ${String(chapters.length).padStart(2, "0")}`;
    if (!first) {
      gauge.classList.remove("ping");
      void gauge.offsetWidth;
      gauge.classList.add("ping");
      document.dispatchEvent(new CustomEvent("echo:dive", { detail: { index: active, formation: chapters[active].formation } }));
    }
  }

  new MutationObserver(labelGauge).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
  labelGauge();

  /* ---------- particle formations ---------- */

  const canvas = document.createElement("canvas");
  canvas.className = "memory-dive";
  canvas.setAttribute("aria-hidden", "true");
  const gl = reduce.matches ? null : canvas.getContext("webgl", { alpha: true, antialias: false, premultipliedAlpha: true, powerPreference: "low-power" });

  const compact = innerWidth < 760;
  const COUNT = compact ? 6500 : 14000;
  let seed = 2147;
  const random = () => {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  };
  const gauss = () => {
    let u = 0;
    while (!u) u = random();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(tau * random());
  };

  function build(place) {
    const out = new Float32Array(COUNT * 3);
    for (let i = 0; i < COUNT; i += 1) {
      const p = place(i, i / COUNT);
      out[i * 3] = p[0];
      out[i * 3 + 1] = p[1];
      out[i * 3 + 2] = p[2];
    }
    return out;
  }

  function onSphere(radius) {
    const z = random() * 2 - 1;
    const a = random() * tau;
    const r = Math.sqrt(1 - z * z);
    return [Math.cos(a) * r * radius, z * radius, Math.sin(a) * r * radius];
  }

  const cities = Array.from({ length: 14 }, () => onSphere(1));

  const FORMATIONS = {
    // The Memory Sea: a vast surface receding to the horizon.
    sea: () =>
      build(() => {
        const z = -1 + 6 * Math.sqrt(random());
        return [(random() * 2 - 1) * (2.2 + z * 1.1), -0.62 + gauss() * 0.012, z];
      }),
    // A signal became civilisation: a planet of household cores, cities and arcs.
    globe: () =>
      build((i, f) => {
        if (f < 0.66) return onSphere(1.12 + gauss() * 0.006);
        if (f < 0.84) {
          const c = cities[i % cities.length];
          const p = [c[0] + gauss() * 0.06, c[1] + gauss() * 0.06, c[2] + gauss() * 0.06];
          const l = Math.hypot(...p) || 1;
          return p.map((v) => (v / l) * 1.13);
        }
        const a = cities[i % cities.length];
        const b = cities[(i * 7 + 3) % cities.length];
        const s = random();
        const p = [a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s, a[2] + (b[2] - a[2]) * s];
        const l = Math.hypot(...p) || 1;
        const lift = 1.13 + Math.sin(Math.PI * s) * 0.32;
        return p.map((v) => (v / l) * lift);
      }),
    // One intelligence, six embodiments orbiting a shared core.
    six: () =>
      build((i, f) => {
        if (f < 0.14) return [gauss() * 0.13, gauss() * 0.13, gauss() * 0.13];
        if (f < 0.38) {
          const a = random() * tau;
          return [Math.cos(a) * 1.3 + gauss() * 0.01, gauss() * 0.01, Math.sin(a) * 1.3 + gauss() * 0.01];
        }
        const k = i % 6;
        const a = (k / 6) * tau;
        const body = onSphere(0.17 + gauss() * 0.012);
        return [Math.cos(a) * 1.3 + body[0], body[1], Math.sin(a) * 1.3 + body[2]];
      }),
    // The same Echo wherever you are: one unbroken trefoil of continuity.
    knot: () =>
      build(() => {
        const t = random() * tau;
        const r = Math.cos(3 * t) + 2.2;
        const tube = 0.06;
        return [r * Math.cos(2 * t) * 0.42 + gauss() * tube, r * Math.sin(2 * t) * 0.42 + gauss() * tube, -Math.sin(3 * t) * 0.42 + gauss() * tube];
      }),
    // Life agents and companions: a double helix that turns on its own axis.
    helix: () =>
      build((i, f) => {
        const x = (random() * 2 - 1) * 1.9;
        const a = x * 3.1;
        if (f < 0.8) {
          const strand = i % 2 ? Math.PI : 0;
          return [x + gauss() * 0.01, Math.cos(a + strand) * 0.46 + gauss() * 0.025, Math.sin(a + strand) * 0.46 + gauss() * 0.025];
        }
        const rung = Math.round(x * 4) / 4;
        const ra = rung * 3.1;
        const s = random() * 2 - 1;
        return [rung + gauss() * 0.008, Math.cos(ra) * 0.46 * s, Math.sin(ra) * 0.46 * s];
      }),
    // Context moves, understanding stays: a ribbon that carries a travelling wave.
    stream: () =>
      build(() => {
        const x = (random() * 2 - 1) * 2.7;
        const w = (random() - 0.5) * 0.7;
        return [x, Math.sin(x * 1.25) * 0.32 + gauss() * 0.035, Math.cos(x * 0.8) * 0.45 + w];
      }),
    // The universe: a three-armed spiral galaxy.
    galaxy: () =>
      build((i, f) => {
        if (f < 0.16) return [gauss() * 0.2, gauss() * 0.07, gauss() * 0.2];
        const arm = (i % 3) * (tau / 3);
        const t = 0.12 + random() ** 0.75 * 1.55;
        const a = arm + t * 2.5 + gauss() * (0.16 / (t + 0.25));
        return [Math.cos(a) * t, gauss() * 0.045 * (1.4 - t * 0.5), Math.sin(a) * t];
      }),
    // The horizon: the ECHO mark, an open ring with an inner arc and a signal dot.
    symbol: () =>
      build((i, f) => {
        const turn = 0.75;
        if (f < 0.5) {
          const a = turn + 0.42 + random() * (tau - 0.84);
          const r = 1.05 + gauss() * 0.03;
          return [Math.cos(a) * r, Math.sin(a) * r, gauss() * 0.03];
        }
        if (f < 0.78) {
          const a = turn + Math.PI + 0.55 + random() * (tau - 1.1);
          const r = 0.64 + gauss() * 0.02;
          return [Math.cos(a) * r, Math.sin(a) * r, gauss() * 0.02];
        }
        if (f < 0.88) return [Math.cos(turn) * 1.24 + gauss() * 0.045, Math.sin(turn) * 1.24 + gauss() * 0.045, gauss() * 0.04];
        const a = random() * tau;
        const r = 1.55 + gauss() * 0.1;
        return [Math.cos(a) * r, Math.sin(a) * r, gauss() * 0.06];
      }),
  };

  // Camera behaviour and colour for each formation:
  // params = [rotate with camera, sea swell, travelling wave, spin on own axis].
  // Formations with speed 0 hold a fixed heading so they always face the visitor the same way.
  const LOOK = {
    sea: { params: [0, 1, 0, 0], speed: 0, pitch: 0, a: [0.62, 0.88, 0.77], b: [0.77, 1, 0.7] },
    globe: { params: [1, 0, 0, 0], speed: 0.12, pitch: 0.38, a: [0.77, 1, 0.7], b: [0.94, 1, 0.9] },
    six: { params: [1, 0, 0, 0], speed: 0.16, pitch: 0.55, a: [0.72, 1, 0.86], b: [0.9, 1, 0.82] },
    knot: { params: [1, 0, 0, 0], speed: 0.2, pitch: 0.3, a: [0.65, 0.8, 0.76], b: [0.82, 1, 0.75] },
    helix: { params: [1, 0, 0, 1], speed: 0, pitch: 0.12, a: [0.77, 1, 0.7], b: [1, 0.86, 0.66] },
    stream: { params: [1, 0, 1, 0], speed: 0, pitch: 0.28, a: [0.62, 0.88, 0.94], b: [0.77, 1, 0.7] },
    galaxy: { params: [1, 0, 0, 0], speed: 0.07, pitch: 0.62, a: [0.78, 0.72, 1], b: [0.77, 1, 0.7] },
    symbol: { params: [0, 0, 0, 0], speed: 0, pitch: 0, a: [1, 0.95, 0.84], b: [0.77, 1, 0.7] },
  };

  const VERTEX = `
    attribute vec3 aFrom;
    attribute vec3 aTo;
    attribute vec4 aSeed;
    uniform float uMix;
    uniform float uTime;
    uniform mat3 uRot;
    uniform vec4 uFromParams;
    uniform vec4 uToParams;
    uniform vec3 uFromA;
    uniform vec3 uFromB;
    uniform vec3 uToA;
    uniform vec3 uToB;
    uniform vec2 uView;
    uniform vec2 uIso;
    uniform float uPixel;
    uniform float uLevel;
    uniform float uBeat;
    uniform vec2 uPointer;
    uniform vec3 uClick;
    varying vec3 vColor;
    varying float vAlpha;
    void main() {
      float m = clamp((uMix - aSeed.x * 0.3) / 0.7, 0.0, 1.0);
      m = m * m * (3.0 - 2.0 * m);
      vec4 params = mix(uFromParams, uToParams, m);
      vec3 p = mix(aFrom, aTo, m);
      float phase = aSeed.w * 6.2831;
      p += sin(3.14159 * m) * 0.3 * vec3(sin(phase + uTime * 0.9), cos(phase * 1.3 + uTime * 0.7), sin(phase * 0.7 - uTime * 0.8));
      p += 0.016 * vec3(sin(uTime * 0.6 + phase * 7.0), cos(uTime * 0.5 + phase * 5.0), sin(uTime * 0.4 + phase * 3.0));
      p.y += params.y * (sin(p.x * 1.6 + uTime * 0.55) * 0.07 + cos(p.z * 2.1 - uTime * 0.42) * 0.05);
      p.y += params.z * sin(p.x * 2.3 - uTime * 1.4) * 0.12;
      float spin = params.w * uTime * 0.45;
      p.yz = mat2(cos(spin), sin(spin), -sin(spin), cos(spin)) * p.yz;
      p *= 1.0 + uLevel * 0.045 + uBeat * 0.03;
      vec3 r = mix(p, uRot * p, params.x);
      float depth = r.z + 3.4;
      if (depth < 0.5) {
        gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
        gl_PointSize = 0.0;
        return;
      }
      float persp = 3.4 / depth;
      vec2 ndc = r.xy * persp * uView;
      vec2 fromPointer = (ndc - uPointer) / uIso;
      float near = 1.0 - smoothstep(0.0, 0.32, length(fromPointer));
      ndc += normalize(fromPointer + 0.0001) * near * 0.07 * uIso;
      vec2 fromClick = (ndc - uClick.xy) / uIso;
      float ring = (1.0 - smoothstep(0.0, 0.1, abs(length(fromClick) - uClick.z * 1.5))) * clamp(1.0 - uClick.z / 1.7, 0.0, 1.0);
      ndc += normalize(fromClick + 0.0001) * ring * 0.06 * uIso;
      gl_Position = vec4(ndc, 0.0, 1.0);
      gl_PointSize = clamp((1.2 + aSeed.y * 6.5) * persp * uPixel * (1.0 + uBeat * 0.35 + ring), 0.0, 16.0 * uPixel);
      vColor = mix(mix(uFromA, uFromB, aSeed.z), mix(uToA, uToB, aSeed.z), m);
      vAlpha = clamp(0.34 + 0.4 * persp, 0.0, 1.0) * (0.45 + 0.55 * fract(aSeed.w * 13.7)) * (1.0 - aSeed.y * 0.62) * (1.0 + near * 1.4 + ring * 2.5);
    }
  `;
  const FRAGMENT = `
    precision mediump float;
    uniform float uFade;
    varying vec3 vColor;
    varying float vAlpha;
    void main() {
      vec2 c = gl_PointCoord - 0.5;
      float d = dot(c, c);
      if (d > 0.25) discard;
      float a = 1.0 - d * 4.0;
      a = a * a * vAlpha * uFade;
      gl_FragColor = vec4(vColor * a, a);
    }
  `;

  function compile(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(shader) || "shader");
    return shader;
  }

  let program = null;
  let uniforms = {};
  let attributes = {};
  const buffers = {};

  function setupGl() {
    program = gl.createProgram();
    gl.attachShader(program, compile(gl.VERTEX_SHADER, VERTEX));
    gl.attachShader(program, compile(gl.FRAGMENT_SHADER, FRAGMENT));
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program) || "link");
    gl.useProgram(program);
    for (const name of ["uMix", "uTime", "uRot", "uFromParams", "uToParams", "uFromA", "uFromB", "uToA", "uToB", "uView", "uIso", "uPixel", "uLevel", "uBeat", "uPointer", "uClick", "uFade"]) {
      uniforms[name] = gl.getUniformLocation(program, name);
    }
    attributes = { from: gl.getAttribLocation(program, "aFrom"), to: gl.getAttribLocation(program, "aTo"), seed: gl.getAttribLocation(program, "aSeed") };
    const needed = new Set(chapters.map((chapter) => chapter.formation));
    for (const name of needed) {
      buffers[name] = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buffers[name]);
      gl.bufferData(gl.ARRAY_BUFFER, FORMATIONS[name](), gl.STATIC_DRAW);
    }
    const seeds = new Float32Array(COUNT * 4);
    for (let i = 0; i < COUNT; i += 1) {
      seeds[i * 4] = random();
      seeds[i * 4 + 1] = random() ** 3;
      seeds[i * 4 + 2] = random() < 0.22 ? 1 : random() * 0.35;
      seeds[i * 4 + 3] = random();
    }
    buffers.seed = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.seed);
    gl.bufferData(gl.ARRAY_BUFFER, seeds, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(attributes.seed);
    gl.vertexAttribPointer(attributes.seed, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(attributes.from);
    gl.enableVertexAttribArray(attributes.to);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE);
    gl.disable(gl.DEPTH_TEST);
    gl.clearColor(0, 0, 0, 0);
  }

  /* ---------- render loop ---------- */

  const view = { width: 1, height: 1, ratio: 1 };
  const pointer = { x: 9, y: 9, tx: 9, ty: 9, px: 0, py: 0 };
  const click = { x: 0, y: 0, age: 9 };
  let glReady = false;
  let frame = 0;
  let last = 0;
  let time = 0;
  let level = 0;
  let beat = 0;
  let scrollSmooth = scrollY;
  let lastFormation = "";

  function resize() {
    view.width = innerWidth;
    view.height = innerHeight;
    view.ratio = Math.min(devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(view.width * view.ratio);
    canvas.height = Math.round(view.height * view.ratio);
    if (glReady) gl.viewport(0, 0, canvas.width, canvas.height);
    measure();
  }

  function fadeAmount() {
    if (!hero) return 1;
    const heroBottom = hero.offsetTop + hero.offsetHeight;
    return smooth(heroBottom * 0.35, heroBottom * 0.95, scrollY);
  }

  function render(dt) {
    const state = locate(scrollSmooth);
    const from = chapters[state.from].formation;
    const to = chapters[state.to].formation;
    const lookFrom = LOOK[from];
    const lookTo = LOOK[to];
    const m = state.mix;
    pointer.px += (clamp(pointer.tx, -1, 1) - pointer.px) * 0.05;
    pointer.py += (clamp(pointer.ty, -1, 1) - pointer.py) * 0.05;
    const heading = (look) => (look.speed ? (time * look.speed) % tau : 0);
    const start = heading(lookFrom);
    const turn = ((((heading(lookTo) - start + Math.PI) % tau) + tau) % tau) - Math.PI;
    const yawNow = start + turn * m + pointer.px * 0.35;
    const pitch = lookFrom.pitch + (lookTo.pitch - lookFrom.pitch) * m - pointer.py * 0.18;
    const cy = Math.cos(yawNow);
    const sy = Math.sin(yawNow);
    const cx = Math.cos(pitch);
    const sx = Math.sin(pitch);

    const shortest = Math.min(view.width, view.height);
    const scale = compact ? 0.78 : 0.6;
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform1f(uniforms.uMix, m);
    gl.uniform1f(uniforms.uTime, time);
    gl.uniformMatrix3fv(uniforms.uRot, false, [cy, sx * sy, -cx * sy, 0, cx, sx, sy, -sx * cy, cx * cy]);
    gl.uniform4fv(uniforms.uFromParams, lookFrom.params);
    gl.uniform4fv(uniforms.uToParams, lookTo.params);
    gl.uniform3fv(uniforms.uFromA, lookFrom.a);
    gl.uniform3fv(uniforms.uFromB, lookFrom.b);
    gl.uniform3fv(uniforms.uToA, lookTo.a);
    gl.uniform3fv(uniforms.uToB, lookTo.b);
    gl.uniform2f(uniforms.uView, (scale * shortest) / view.width, (scale * shortest) / view.height);
    gl.uniform2f(uniforms.uIso, shortest / view.width, shortest / view.height);
    gl.uniform1f(uniforms.uPixel, view.ratio);
    gl.uniform1f(uniforms.uLevel, level);
    gl.uniform1f(uniforms.uBeat, beat);
    gl.uniform2f(uniforms.uPointer, pointer.x, pointer.y);
    gl.uniform3f(uniforms.uClick, click.x, click.y, click.age);
    gl.uniform1f(uniforms.uFade, fadeAmount() * (compact ? 0.75 : 0.9));
    if (from !== lastFormation || to !== lastFormation) {
      gl.bindBuffer(gl.ARRAY_BUFFER, buffers[from]);
      gl.vertexAttribPointer(attributes.from, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, buffers[to]);
      gl.vertexAttribPointer(attributes.to, 3, gl.FLOAT, false, 0, 0);
      lastFormation = from === to ? from : "";
    }
    gl.drawArrays(gl.POINTS, 0, COUNT);
  }

  function visible() {
    return !document.hidden && !document.body.classList.contains("motion-paused") && fadeAmount() > 0.001;
  }

  function tick(now) {
    frame = 0;
    const dt = last ? Math.min(0.05, (now - last) / 1000) : 0.016;
    last = now;
    scrollSmooth += (scrollY - scrollSmooth) * Math.min(1, dt * 6);
    updateGauge(locate(scrollY));
    if (!glReady || !visible()) {
      last = 0;
      if (glReady) gl.clear(gl.COLOR_BUFFER_BIT);
      return;
    }
    time += dt;
    level += ((audio ? audio.level() : 0) - level) * 0.2;
    beat *= Math.pow(0.04, dt);
    click.age += dt;
    render(dt);
    frame = requestAnimationFrame(tick);
  }

  function wake() {
    if (!frame) frame = requestAnimationFrame(tick);
  }

  if (gl) {
    try {
      setupGl();
      main.prepend(canvas);
      glReady = true;
    } catch (error) {
      console.warn("Memory dive disabled:", error);
    }
  }

  canvas.addEventListener("webglcontextlost", (event) => {
    event.preventDefault();
    glReady = false;
    canvas.remove();
  });

  addEventListener("scroll", wake, { passive: true });
  addEventListener("resize", () => {
    resize();
    wake();
  });
  new ResizeObserver(() => {
    measure();
    wake();
  }).observe(main);
  document.addEventListener("visibilitychange", wake);
  new MutationObserver(wake).observe(document.body, { attributes: true, attributeFilter: ["class"] });
  addEventListener(
    "pointermove",
    (event) => {
      pointer.tx = (event.clientX / view.width) * 2 - 1;
      pointer.ty = 1 - (event.clientY / view.height) * 2;
      pointer.x = pointer.tx;
      pointer.y = pointer.ty;
    },
    { passive: true },
  );
  document.documentElement.addEventListener("pointerleave", () => {
    pointer.x = 9;
    pointer.y = 9;
    pointer.tx = 0;
    pointer.ty = 0;
  });
  addEventListener(
    "pointerdown",
    (event) => {
      if (event.target.closest?.(".future-hero")) return;
      click.x = (event.clientX / view.width) * 2 - 1;
      click.y = 1 - (event.clientY / view.height) * 2;
      click.age = 0;
      wake();
    },
    { passive: true },
  );
  audio?.on((event) => {
    if (event.type === "beat") beat = Math.max(beat, event.strength);
  });

  resize();
  wake();
})();
