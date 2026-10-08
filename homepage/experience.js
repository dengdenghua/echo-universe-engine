/* ECHO site experience layer: soundtrack controls, echo ripples, scroll reveals and
 * live signal visuals. Shared by the homepage and /universe/.
 *
 * Progressive enhancement under the site's strict CSP: no inline style attributes
 * (only CSSOM), no network requests, and every piece of content stays readable
 * without it. Motion respects prefers-reduced-motion and the page's motion toggle.
 */
(() => {
  "use strict";
  const audio = window.EchoAudio || null;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)");
  const fine = matchMedia("(hover: hover) and (pointer: fine)");
  const body = document.body;
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $all = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const still = () => reduce.matches || body.classList.contains("motion-paused");

  const COPY = {
    zh: {
      sound: "声音",
      soundOn: "配乐开启",
      soundOff: "配乐关闭",
      soundResume: "轻触任意处恢复配乐",
      toggle: "切换配乐（快捷键 M）",
      inviteKicker: "GENERATIVE SCORE · 生成式配乐",
      inviteTitle: "《记忆海》",
      inviteBody: "为这一页实时合成的配乐。轻触记忆环，它会回响。",
      accept: "开启声音",
      decline: "保持安静",
      toastOn: "配乐已开启 · 按 M 静音",
      toastOff: "配乐已关闭 · 按 M 重新开启",
      ringHint: "开启声音，聆听记忆环的回响",
    },
    en: {
      sound: "SOUND",
      soundOn: "Soundtrack on",
      soundOff: "Soundtrack off",
      soundResume: "Tap anywhere to resume the soundtrack",
      toggle: "Toggle soundtrack (M)",
      inviteKicker: "GENERATIVE SCORE",
      inviteTitle: "Memory Sea",
      inviteBody: "A score synthesised live for this page. Touch the memory ring and it will echo.",
      accept: "Turn sound on",
      decline: "Stay silent",
      toastOn: "Soundtrack on · press M to mute",
      toastOff: "Soundtrack off · press M to bring it back",
      ringHint: "Turn sound on to hear the ring echo",
    },
  };
  const locale = () => (document.documentElement.lang.startsWith("en") ? "en" : "zh");
  const t = (key) => COPY[locale()][key];

  function make(tag, className, attributes = {}) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    for (const [name, value] of Object.entries(attributes)) element.setAttribute(name, value);
    return element;
  }

  function restart(element, className) {
    element.classList.remove(className);
    void element.offsetWidth;
    element.classList.add(className);
  }

  /* ---------- toast ---------- */

  const toast = make("div", "echo-toast", { role: "status", "aria-live": "polite" });
  body.append(toast);
  let toastTimer = 0;
  function say(message) {
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2200);
  }

  /* ---------- sound controls ---------- */

  let soundSwitch = null;
  let invite = null;

  function syncSound() {
    if (!audio || !soundSwitch) return;
    const on = audio.music;
    const live = on && audio.running;
    soundSwitch.setAttribute("aria-pressed", String(on));
    soundSwitch.setAttribute("aria-label", `${t("toggle")} · ${on ? t("soundOn") : t("soundOff")}`);
    soundSwitch.title = live || !on ? t("toggle") : t("soundResume");
    soundSwitch.classList.toggle("is-on", live);
    soundSwitch.classList.toggle("is-armed", on && !live);
    $(".sound-word", soundSwitch).textContent = t("sound");
  }

  function setSound(on, announce = true) {
    if (!audio) return;
    if (on && audio.music && !audio.running) audio.unlock();
    else audio.setMusic(on);
    if (on) setTimeout(() => audio.sfx("awake"), 120);
    if (announce) say(on ? t("toastOn") : t("toastOff"));
    closeInvite();
  }

  function buildInvite() {
    invite = make("aside", "sound-invite", { "aria-label": t("inviteTitle") });
    const wave = make("div", "sound-invite-wave", { "aria-hidden": "true" });
    for (let i = 0; i < 5; i += 1) wave.append(make("i"));
    const copy = make("div", "sound-invite-copy");
    const kicker = make("span", "sound-invite-kicker");
    const title = make("strong");
    const text = make("p");
    copy.append(kicker, title, text);
    const actions = make("div", "sound-invite-actions");
    const accept = make("button", "sound-accept", { type: "button", "data-audio-control": "" });
    const decline = make("button", "sound-decline", { type: "button", "data-audio-control": "" });
    actions.append(accept, decline);
    invite.append(wave, copy, actions);
    const fill = () => {
      kicker.textContent = t("inviteKicker");
      title.textContent = t("inviteTitle");
      text.textContent = t("inviteBody");
      accept.textContent = t("accept");
      decline.textContent = t("decline");
      invite.setAttribute("aria-label", t("inviteTitle"));
    };
    fill();
    invite.fill = fill;
    accept.addEventListener("click", () => setSound(true));
    decline.addEventListener("click", () => {
      audio.setMusic(false);
      closeInvite();
    });
    body.append(invite);
    requestAnimationFrame(() => requestAnimationFrame(() => invite.classList.add("show")));
  }

  function closeInvite() {
    if (!invite) return;
    const leaving = invite;
    invite = null;
    leaving.classList.remove("show");
    setTimeout(() => leaving.remove(), 600);
  }

  function installSound() {
    if (!audio) return;
    const host = $(".header-actions") || $(".universe-actions");
    if (!host) return;
    soundSwitch = make("button", "sound-switch", { type: "button", "aria-pressed": "false", "data-audio-control": "" });
    const bars = make("span", "sound-bars", { "aria-hidden": "true" });
    for (let i = 0; i < 4; i += 1) bars.append(make("i"));
    soundSwitch.append(bars, make("span", "sound-word"));
    host.prepend(soundSwitch);
    soundSwitch.addEventListener("click", () => setSound(!audio.music || !audio.running));

    document.addEventListener("keydown", (event) => {
      if ((event.key || "").toLowerCase() !== "m" || event.ctrlKey || event.metaKey || event.altKey || event.repeat) return;
      if (event.target.closest?.("input, textarea, select, [contenteditable]")) return;
      setSound(!audio.music || !audio.running);
    });

    // Each new chapter of the dive rings a soft chime (only when sound is on).
    let chimed = 0;
    document.addEventListener("echo:dive", (event) => {
      const now = performance.now();
      if (now - chimed < 900) return;
      chimed = now;
      audio.sfx("chapter", { index: event.detail.index, pan: 0.5 });
    });

    // Tapping the ring in silence nudges the visitor towards the sound switch, once.
    let hinted = false;
    document.addEventListener("echo:ring", () => {
      if (audio.music || hinted) return;
      hinted = true;
      restart(soundSwitch, "nudge");
      say(t("ringHint"));
    });

    audio.on((event) => {
      if (event.type === "state") syncSound();
    });
    new MutationObserver(() => {
      syncSound();
      invite?.fill();
    }).observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });

    if (!audio.decided) setTimeout(() => !audio.decided && buildInvite(), 2600);

    // The score gathers density as the visitor travels deeper into the site.
    let scrollFrame = 0;
    addEventListener(
      "scroll",
      () => {
        if (scrollFrame) return;
        scrollFrame = requestAnimationFrame(() => {
          scrollFrame = 0;
          const depth = scrollY / Math.max(1, document.documentElement.scrollHeight - innerHeight);
          audio.setIntensity(0.25 + clamp(depth, 0, 1) * 0.55);
        });
      },
      { passive: true },
    );
    syncSound();
  }

  /* ---------- echo ripples and cursor glow ---------- */

  const TAP_TARGETS = "a, button";

  function installPointer() {
    addEventListener(
      "pointerdown",
      (event) => {
        if (event.button !== 0) return;
        const target = event.target;
        const pan = clamp((event.clientX / innerWidth) * 2 - 1, -0.8, 0.8);
        if (!target.closest?.(".future-hero")) {
          if (target.closest?.(TAP_TARGETS)) audio?.sfx("tap", { pan });
          else audio?.sfx("echo", { pan });
        }
        if (still()) return;
        for (const late of [false, true]) {
          const ring = make("span", late ? "echo-ring late" : "echo-ring", { "aria-hidden": "true" });
          ring.style.left = `${event.clientX}px`;
          ring.style.top = `${event.clientY}px`;
          ring.addEventListener("animationend", () => ring.remove());
          body.append(ring);
        }
      },
      { passive: true },
    );

    if (!fine.matches) return;
    const halo = make("div", "cursor-halo", { "aria-hidden": "true" });
    body.append(halo);
    const pos = { x: innerWidth / 2, y: innerHeight / 2, tx: innerWidth / 2, ty: innerHeight / 2 };
    let frame = 0;
    const follow = () => {
      pos.x += (pos.tx - pos.x) * 0.16;
      pos.y += (pos.ty - pos.y) * 0.16;
      halo.style.transform = `translate3d(${pos.x.toFixed(1)}px, ${pos.y.toFixed(1)}px, 0)`;
      frame = Math.abs(pos.tx - pos.x) + Math.abs(pos.ty - pos.y) > 0.5 ? requestAnimationFrame(follow) : 0;
    };
    addEventListener(
      "pointermove",
      (event) => {
        pos.tx = event.clientX;
        pos.ty = event.clientY;
        halo.classList.add("show");
        if (!frame) frame = requestAnimationFrame(follow);
      },
      { passive: true },
    );
    document.documentElement.addEventListener("pointerleave", () => halo.classList.remove("show"));

    // Primary actions lean gently towards the pointer.
    $all(".future-primary, .future-secondary, .outline-link, .enter-panel > a, .gateway").forEach((element) => {
      const pull = element.classList.contains("gateway") ? 0.04 : 0.22;
      element.addEventListener("pointermove", (event) => {
        if (still()) return;
        const rect = element.getBoundingClientRect();
        const dx = event.clientX - (rect.left + rect.width / 2);
        const dy = event.clientY - (rect.top + rect.height / 2);
        element.style.setProperty("translate", `${(dx * pull).toFixed(1)}px ${(dy * pull * 1.4).toFixed(1)}px`);
      });
      element.addEventListener("pointerleave", () => element.style.removeProperty("translate"));
    });

    // Spotlight that follows the pointer across cards.
    $all(".system-card, .capability-card, .roadmap-stages article, .gateway, .universe-feature, .ecosystem-node").forEach((card) => {
      card.classList.add("has-spotlight");
      card.prepend(make("i", "spot", { "aria-hidden": "true" }));
      card.addEventListener(
        "pointermove",
        (event) => {
          const rect = card.getBoundingClientRect();
          card.style.setProperty("--spot-x", `${Math.round(event.clientX - rect.left)}px`);
          card.style.setProperty("--spot-y", `${Math.round(event.clientY - rect.top)}px`);
        },
        { passive: true },
      );
    });
  }

  /* ---------- scroll reveals ---------- */

  const GLYPHS = "▓▒░<>/\\|=+*#01";

  function decode(element, duration = 700) {
    const final = element.dataset.final || element.textContent;
    element.dataset.final = final;
    const start = performance.now();
    const step = (now) => {
      const progress = Math.min(1, (now - start) / duration);
      const shown = Math.floor(progress * final.length);
      let text = final.slice(0, shown);
      for (let i = shown; i < final.length; i += 1) text += final[i] === " " ? " " : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      element.textContent = text;
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  const REVEAL = [
    ".gateway",
    ".epoch-divider",
    ".section-copy",
    ".heading-detail",
    ".product-card",
    ".product-backplane",
    ".capability-card",
    ".capability-core",
    ".capability-identity",
    ".agent-card",
    ".flow-board",
    ".ecosystem-map",
    ".universe-visual",
    ".roadmap-stages article",
    ".enter-panel",
  ].join(", ");

  // Wrap each <br>-separated line of a headline so it can slide up through a mask.
  // <i> wrappers, not <span>: the stylesheets style `h2 span` for the secondary lines.
  function splitLines(heading) {
    if (heading.dataset.split) return;
    heading.dataset.split = "1";
    const lines = [[]];
    for (const node of Array.from(heading.childNodes)) {
      if (node.nodeName === "BR") lines.push([]);
      else lines[lines.length - 1].push(node);
    }
    heading.textContent = "";
    lines.forEach((nodes, index) => {
      const line = make("i", "line");
      const inner = make("i", "line-inner");
      inner.style.setProperty("--line", index);
      nodes.forEach((node) => inner.append(node));
      line.append(inner);
      heading.append(line);
    });
  }

  function installReveals() {
    if (reduce.matches || !("IntersectionObserver" in window)) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          const element = entry.target;
          element.classList.add("in-view");
          observer.unobserve(element);
          $all(".kicker", element).forEach((kicker) => decode(kicker));
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" },
    );
    const siblings = new Map();
    $all(REVEAL).forEach((element) => {
      // Only content below the fold animates in, so nothing already visible flickers.
      if (element.getBoundingClientRect().top < innerHeight) return;
      const index = siblings.get(element.parentElement) || 0;
      siblings.set(element.parentElement, index + 1);
      element.style.setProperty("--reveal-delay", `${Math.min(index, 6) * 80}ms`);
      element.classList.add("reveal");
      $all("h2", element).forEach(splitLines);
      observer.observe(element);
    });
  }

  /* ---------- epoch divider marquee ---------- */

  function installMarquee() {
    const divider = $(".epoch-divider");
    if (!divider || reduce.matches) return;
    const track = make("div", "marquee-track");
    const items = Array.from(divider.childNodes);
    const half = make("div", "marquee-half");
    items.forEach((node) => half.append(node));
    track.append(half, half.cloneNode(true), half.cloneNode(true));
    divider.append(track);
    divider.classList.add("is-marquee");
  }

  /* ---------- live signal map ---------- */

  // Signals travel between the Memory Sea core and each civilisation node.
  function installSignalMap() {
    const map = $(".ecosystem-map");
    const core = map && $(".ecosystem-core", map);
    if (!map || !core) return;
    const canvas = make("canvas", "signal-canvas", { "aria-hidden": "true" });
    map.append(canvas);
    const ctx = canvas.getContext("2d");
    let links = [];
    let width = 0;
    let height = 0;
    let visible = false;
    let frame = 0;
    let last = 0;
    let surge = 0;

    function layout() {
      const box = map.getBoundingClientRect();
      const ratio = Math.min(devicePixelRatio || 1, 2);
      width = box.width;
      height = box.height;
      canvas.width = Math.round(width * ratio);
      canvas.height = Math.round(height * ratio);
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      const coreBox = core.getBoundingClientRect();
      const cx = coreBox.left - box.left + coreBox.width / 2;
      const cy = coreBox.top - box.top + coreBox.height / 2;
      links = $all(".ecosystem-node", map).map((node, index) => {
        const nodeBox = node.getBoundingClientRect();
        const nx = nodeBox.left - box.left + nodeBox.width / 2;
        const ny = nodeBox.top - box.top + nodeBox.height / 2;
        const bend = index % 2 ? 0.22 : -0.22;
        return {
          a: { x: cx, y: cy },
          b: { x: nx, y: ny },
          c: { x: (cx + nx) / 2 - (ny - cy) * bend, y: (cy + ny) / 2 + (nx - cx) * bend },
          pulses: [Math.random(), Math.random()],
          speed: 0.12 + Math.random() * 0.1,
        };
      });
      paint(0);
    }

    function point(link, s) {
      const k = 1 - s;
      return {
        x: k * k * link.a.x + 2 * k * s * link.c.x + s * s * link.b.x,
        y: k * k * link.a.y + 2 * k * s * link.c.y + s * s * link.b.y,
      };
    }

    function paint(dt) {
      ctx.clearRect(0, 0, width, height);
      const energy = 1 + surge + (audio ? audio.level() * 1.5 : 0);
      surge *= 0.94;
      for (const link of links) {
        ctx.setLineDash([2, 6]);
        ctx.lineWidth = 1;
        ctx.strokeStyle = `rgba(197, 255, 178, ${0.16 * Math.min(energy, 2)})`;
        ctx.beginPath();
        ctx.moveTo(link.a.x, link.a.y);
        ctx.quadraticCurveTo(link.c.x, link.c.y, link.b.x, link.b.y);
        ctx.stroke();
        ctx.setLineDash([]);
        link.pulses = link.pulses.map((s) => (s + dt * link.speed * energy) % 1);
        for (const s of link.pulses) {
          const head = point(link, s);
          const tail = point(link, Math.max(0, s - 0.08));
          const trail = ctx.createLinearGradient(tail.x, tail.y, head.x, head.y);
          trail.addColorStop(0, "rgba(197, 255, 178, 0)");
          trail.addColorStop(1, "rgba(220, 255, 205, 0.9)");
          ctx.strokeStyle = trail;
          ctx.lineWidth = 1.6;
          ctx.beginPath();
          ctx.moveTo(tail.x, tail.y);
          ctx.lineTo(head.x, head.y);
          ctx.stroke();
          ctx.fillStyle = "rgba(236, 255, 214, 0.95)";
          ctx.fillRect(head.x - 1.2, head.y - 1.2, 2.4, 2.4);
        }
      }
    }

    function tick(now) {
      frame = 0;
      if (!visible || still() || document.hidden) {
        last = 0;
        return;
      }
      const dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
      last = now;
      paint(dt);
      frame = requestAnimationFrame(tick);
    }

    const wake = () => {
      if (!frame && visible && !still()) frame = requestAnimationFrame(tick);
    };
    new ResizeObserver(layout).observe(map);
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      wake();
    }).observe(map);
    new MutationObserver(wake).observe(body, { attributes: true, attributeFilter: ["class"] });
    document.addEventListener("visibilitychange", wake);
    audio?.on((event) => {
      if (event.type === "beat") surge = Math.max(surge, 1.2);
    });
  }

  /* ---------- music-driven details ---------- */

  function installMusicVisuals() {
    if (!audio) return;
    const wordmark = $(".echo-wordmark");
    if (wordmark) {
      wordmark.setAttribute("data-echo", wordmark.firstChild?.textContent?.trim() || "ECHO");
      audio.on((event) => {
        if (event.type === "beat" && !still()) restart(wordmark, "beat");
      });
    }

    // The hero frequency bars become a real spectrum while the score plays.
    const frequency = $(".hero-frequency");
    const bars = frequency ? $all("i", frequency) : [];
    const meter = soundSwitch ? $all(".sound-bars i", soundSwitch) : [];
    let frame = 0;
    const draw = () => {
      frame = 0;
      const live = audio.music && audio.running && !document.hidden;
      frequency?.classList.toggle("is-live", live);
      if (!live) {
        bars.forEach((bar) => bar.style.removeProperty("transform"));
        meter.forEach((bar) => bar.style.removeProperty("transform"));
        // Sound is on but the audio context is still waking: check back shortly.
        if (audio.music && !document.hidden) setTimeout(wake, 400);
        return;
      }
      const spectrum = audio.bands(Math.max(bars.length, 1));
      bars.forEach((bar, index) => bar.style.setProperty("transform", `scaleY(${(0.2 + spectrum[index] * 0.8).toFixed(3)})`));
      const small = audio.bands(meter.length || 1);
      meter.forEach((bar, index) => bar.style.setProperty("transform", `scaleY(${(0.2 + small[index] * 0.8).toFixed(3)})`));
      frame = requestAnimationFrame(draw);
    };
    const wake = () => {
      if (!frame) frame = requestAnimationFrame(draw);
    };
    audio.on((event) => event.type === "state" && wake());
    document.addEventListener("visibilitychange", wake);
    wake();
  }

  /* ---------- start ---------- */

  installSound();
  installPointer();
  installReveals();
  installMarquee();
  installSignalMap();
  installMusicVisuals();
})();
