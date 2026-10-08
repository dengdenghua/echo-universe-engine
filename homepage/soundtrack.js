/* ECHO site score: "Memory Sea / 记忆海", a generative ambient soundtrack.
 *
 * Synthesised live with the Web Audio API: no audio files, no network requests
 * (it runs under the site's strict CSP). Sound is strictly opt-in: nothing is
 * created until the visitor turns it on, and the choice is remembered.
 *
 * A slow D-major progression (glass pads, sub bass, music-box chimes) floats on
 * filtered-noise swells, the Memory Sea. Density follows an intensity value the
 * page raises as the visitor travels deeper into the site.
 *
 * Public surface: window.EchoAudio (see the bottom of this file).
 */
(() => {
  "use strict";
  const PREFS = { music: "echo.site.sound", sfx: "echo.site.sfx", volume: "echo.site.volume" };
  const BPM = 66;
  const STEP = 60 / BPM / 4; // one sixteenth note, in seconds
  const STEPS_PER_BAR = 16;
  const STEPS_PER_CHORD = STEPS_PER_BAR * 2;
  const LOOKAHEAD = 0.2;
  const IDLE_INTENSITY = 0.25;

  // Chimes only ever pick from the chord's own set, so every interface sound,
  // including notes strummed on the memory ring, stays in key with the score.
  const PROGRESSION = [
    { name: "Dmaj9", bass: 38, pad: [50, 57, 61, 64, 66], bell: [66, 69, 73, 74, 76, 78, 81] },
    { name: "Bm11", bass: 35, pad: [47, 54, 57, 62, 64], bell: [64, 66, 69, 71, 74, 76, 78] },
    { name: "Gmaj7#11", bass: 31, pad: [43, 50, 54, 57, 61], bell: [66, 67, 69, 71, 73, 74, 78] },
    { name: "Asus4", bass: 33, pad: [45, 52, 57, 62, 64], bell: [64, 69, 71, 74, 76, 81, 83] },
  ];

  const mtof = (midi) => 440 * 2 ** ((midi - 69) / 12);
  const rand = (min, max) => min + Math.random() * (max - min);
  const pick = (list) => list[Math.floor(Math.random() * list.length)];
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

  function readPref(key, fallback) {
    try {
      const value = localStorage.getItem(key);
      return value === null ? fallback : value;
    } catch (_) {
      return fallback;
    }
  }

  function writePref(key, value) {
    try {
      localStorage.setItem(key, String(value));
    } catch (_) {
      // Storage unavailable: the choice holds for this page only.
    }
  }

  const storedVolume = Number(readPref(PREFS.volume, "0.55"));
  const state = {
    music: readPref(PREFS.music, "off") === "on",
    decided: readPref(PREFS.music, null) !== null,
    sfx: readPref(PREFS.sfx, "on") === "on",
    volume: Number.isFinite(storedVolume) ? clamp(storedVolume, 0, 1) : 0.55,
    intensity: IDLE_INTENSITY,
    targetIntensity: IDLE_INTENSITY,
    chordIndex: 0,
    step: 0,
    nextTime: 0,
    timer: null,
    suspendTimer: null,
    lastBell: null,
  };

  const listeners = new Set();
  let ctx = null;
  let graph = null;

  function emit(event) {
    listeners.forEach((listener) => {
      try {
        listener(event);
      } catch (error) {
        console.error(error);
      }
    });
  }

  function emitAt(time, event) {
    setTimeout(() => emit(event), Math.max(0, (time - ctx.currentTime) * 1000));
  }

  /* ---------- graph ---------- */

  function gain(value, ...targets) {
    const node = ctx.createGain();
    node.gain.value = value;
    targets.forEach((target) => node.connect(target));
    return node;
  }

  function filter(type, frequency, q = 0.7) {
    const node = ctx.createBiquadFilter();
    node.type = type;
    node.frequency.value = frequency;
    node.Q.value = q;
    return node;
  }

  function panner(value) {
    const node = ctx.createStereoPanner();
    node.pan.value = clamp(value, -1, 1);
    return node;
  }

  function noise(seconds) {
    const length = Math.floor(ctx.sampleRate * seconds);
    const buffer = ctx.createBuffer(1, length, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < length; i += 1) data[i] = Math.random() * 2 - 1;
    return buffer;
  }

  function impulse(seconds, decay) {
    const length = Math.floor(ctx.sampleRate * seconds);
    const buffer = ctx.createBuffer(2, length, ctx.sampleRate);
    for (let channel = 0; channel < 2; channel += 1) {
      const data = buffer.getChannelData(channel);
      for (let i = 0; i < length; i += 1) data[i] = (Math.random() * 2 - 1) * (1 - i / length) ** decay;
    }
    return buffer;
  }

  function buildGraph() {
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -20;
    compressor.knee.value = 16;
    compressor.ratio.value = 3;
    compressor.attack.value = 0.02;
    compressor.release.value = 0.35;

    // The analyser taps the mix before the volume knob so visuals respond at any level.
    const analyser = ctx.createAnalyser();
    analyser.fftSize = 512;
    analyser.smoothingTimeConstant = 0.8;
    const master = gain(state.volume, ctx.destination);
    compressor.connect(analyser);
    compressor.connect(master);

    const mix = gain(1, compressor);
    const musicOut = gain(0, mix);
    const sfxOut = gain(state.sfx ? 1 : 0, mix);

    const room = impulse(5.2, 2.2);
    const reverb = ctx.createConvolver();
    reverb.buffer = room;
    reverb.connect(gain(0.9, musicOut));
    const reverbIn = gain(1, reverb);

    const delay = ctx.createDelay(2);
    delay.delayTime.value = STEP * 3;
    const darken = filter("lowpass", 2600);
    delay.connect(darken);
    darken.connect(gain(0.42, delay));
    delay.connect(gain(0.5, musicOut, reverbIn));
    const delayIn = gain(1, delay);

    const bus = (dry, wet, echo = 0) => {
      const input = ctx.createGain();
      input.connect(gain(dry, musicOut));
      if (wet) input.connect(gain(wet, reverbIn));
      if (echo) input.connect(gain(echo, delayIn));
      return input;
    };

    const sfxReverb = ctx.createConvolver();
    sfxReverb.buffer = room;
    sfxReverb.connect(gain(0.6, sfxOut));
    const sfx = ctx.createGain();
    sfx.connect(sfxOut);
    sfx.connect(gain(0.5, sfxReverb));

    const padLfo = ctx.createOscillator();
    padLfo.frequency.value = 0.04;
    const padLfoDepth = gain(420);
    padLfo.connect(padLfoDepth);
    padLfo.start();

    return {
      analyser,
      master,
      musicOut,
      sfxOut,
      pad: bus(0.55, 0.8),
      bass: bus(0.9, 0.12),
      bell: bus(0.4, 0.6, 0.5),
      pulse: bus(0.9, 0.2),
      air: bus(0.6, 0.35),
      sfx,
      padLfoDepth,
      noise: noise(4),
      sea: null,
      timeData: new Float32Array(analyser.fftSize),
      freqData: new Uint8Array(analyser.frequencyBinCount),
    };
  }

  /* ---------- voices ---------- */

  function padChord(chord, time, duration) {
    const attack = 3;
    const release = 4.5;
    const level = 0.03;
    const end = time + duration + release + 0.1;
    chord.pad.forEach((midi, index) => {
      const tone = filter("lowpass", 560 + state.intensity * 1100 + index * 80, 0.6);
      graph.padLfoDepth.connect(tone.frequency);
      const amp = ctx.createGain();
      amp.gain.setValueAtTime(0, time);
      amp.gain.linearRampToValueAtTime(level, time + attack);
      amp.gain.setValueAtTime(level, time + duration);
      amp.gain.linearRampToValueAtTime(0, time + duration + release);
      tone.connect(amp).connect(panner((index / (chord.pad.length - 1)) * 1.4 - 0.7)).connect(graph.pad);
      for (const [type, detune] of [
        ["sawtooth", -7],
        ["triangle", 6],
      ]) {
        const osc = ctx.createOscillator();
        osc.type = type;
        osc.frequency.value = mtof(midi);
        osc.detune.value = detune + rand(-3, 3);
        osc.connect(tone);
        osc.start(time);
        osc.stop(end);
      }
      setTimeout(() => graph.padLfoDepth.disconnect(tone.frequency), (end - ctx.currentTime) * 1000 + 250);
    });
  }

  function bassNote(midi, time, duration) {
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0, time);
    amp.gain.linearRampToValueAtTime(0.15, time + 1.6);
    amp.gain.setValueAtTime(0.15, time + duration);
    amp.gain.linearRampToValueAtTime(0, time + duration + 2.4);
    amp.connect(filter("lowpass", 280)).connect(graph.bass);
    const root = ctx.createOscillator();
    root.frequency.value = mtof(midi);
    const body = ctx.createOscillator();
    body.type = "triangle";
    body.frequency.value = mtof(midi + 12);
    root.connect(amp);
    body.connect(gain(0.26, amp));
    for (const osc of [root, body]) {
      osc.start(time);
      osc.stop(time + duration + 2.6);
    }
  }

  function swell(time, peak, destination) {
    const osc = ctx.createOscillator();
    osc.frequency.setValueAtTime(82, time);
    osc.frequency.exponentialRampToValueAtTime(44, time + 0.3);
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0.0001, time);
    amp.gain.exponentialRampToValueAtTime(peak, time + 0.03);
    amp.gain.exponentialRampToValueAtTime(0.0001, time + 0.7);
    osc.connect(amp).connect(destination);
    osc.start(time);
    osc.stop(time + 0.75);
  }

  // FM chime: ratio 2 is a soft music box, 3.5 a colder glass bell.
  function bell(midi, time, { velocity = 0.07, pan = 0, decay = 2.8, ratio = 2, destination = graph.bell } = {}) {
    const frequency = mtof(midi);
    const carrier = ctx.createOscillator();
    carrier.frequency.value = frequency;
    const modulator = ctx.createOscillator();
    modulator.frequency.value = frequency * ratio;
    const index = ctx.createGain();
    index.gain.setValueAtTime(frequency * 1.4, time);
    index.gain.exponentialRampToValueAtTime(frequency * 0.03, time + decay * 0.6);
    modulator.connect(index).connect(carrier.frequency);
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0.0001, time);
    amp.gain.exponentialRampToValueAtTime(velocity, time + 0.008);
    amp.gain.exponentialRampToValueAtTime(0.0001, time + decay);
    carrier.connect(amp).connect(panner(pan)).connect(destination);
    for (const osc of [carrier, modulator]) {
      osc.start(time);
      osc.stop(time + decay + 0.05);
    }
  }

  // The Memory Sea: low filtered noise that rises and falls like slow surf.
  function startSea(time) {
    if (graph.sea) return;
    const source = ctx.createBufferSource();
    source.buffer = graph.noise;
    source.loop = true;
    const amp = gain(0.03);
    const tide = ctx.createOscillator();
    tide.frequency.value = 0.085;
    tide.connect(gain(0.026, amp.gain));
    const shore = filter("lowpass", 520, 0.4);
    const drift = ctx.createOscillator();
    drift.frequency.value = 0.031;
    drift.connect(gain(240, shore.frequency));
    source.connect(shore).connect(amp).connect(panner(0)).connect(graph.air);
    source.start(time);
    tide.start(time);
    drift.start(time);
    graph.sea = { source, tide, drift };
  }

  function stopSea(time) {
    if (!graph.sea) return;
    for (const node of Object.values(graph.sea)) node.stop(time);
    graph.sea = null;
  }

  function breath(time) {
    const source = ctx.createBufferSource();
    source.buffer = graph.noise;
    source.loop = true;
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0, time);
    amp.gain.linearRampToValueAtTime(0.08, time + 2.4);
    amp.gain.linearRampToValueAtTime(0, time + 5.6);
    amp.connect(panner(rand(-0.7, 0.7))).connect(graph.air);
    for (const [from, to, q] of [
      [620, 900, 10],
      [1120, 1500, 12],
    ]) {
      const formant = filter("bandpass", from, q);
      formant.frequency.setValueAtTime(from, time);
      formant.frequency.linearRampToValueAtTime(to, time + 5.4);
      source.connect(formant).connect(amp);
    }
    source.start(time, rand(0, 1), 5.8);
  }

  /* ---------- sequencer ---------- */

  function pickBell(chord) {
    let midi = pick(chord.bell);
    if (midi === state.lastBell) midi = pick(chord.bell);
    state.lastBell = midi;
    return midi;
  }

  function playStep(step, time) {
    const stepInChord = step % STEPS_PER_CHORD;
    const stepInBar = step % STEPS_PER_BAR;
    const bar = Math.floor(step / STEPS_PER_BAR);
    state.intensity += (state.targetIntensity - state.intensity) * 0.04;
    const energy = state.intensity;

    if (stepInChord === 0) {
      state.chordIndex = Math.floor(step / STEPS_PER_CHORD) % PROGRESSION.length;
      const chord = PROGRESSION[state.chordIndex];
      const seconds = STEPS_PER_CHORD * STEP;
      padChord(chord, time, seconds - 0.4);
      bassNote(chord.bass, time, seconds - 0.8);
      emitAt(time, { type: "chord", name: chord.name, index: state.chordIndex });
      if (Math.random() < 0.18) breath(time + rand(1, 4));
    }
    const chord = PROGRESSION[state.chordIndex];

    if (stepInBar === 0 && (energy > 0.45 || bar % 2 === 0)) {
      swell(time, 0.18 + energy * 0.2, graph.pulse);
      emitAt(time, { type: "beat", strength: 0.5 + energy * 0.5 });
    }

    if (stepInBar % 2 === 0) {
      const weight = stepInBar % 8 === 0 ? 1.7 : 1;
      if (Math.random() < (0.07 + energy * 0.2) * weight) {
        const midi = pickBell(chord);
        const pan = rand(-0.75, 0.75);
        const velocity = rand(0.04, 0.09);
        bell(midi, time, { velocity, pan, ratio: Math.random() < 0.25 ? 3.5 : 2 });
        emitAt(time, { type: "note", midi, pan, velocity });
      }
    }

    // Deeper in the site: a quiet rising arpeggio joins.
    if (energy > 0.55 && stepInBar % 4 === 2) {
      const midi = chord.bell[(step / 2) % chord.bell.length] + 12;
      const pan = Math.sin(step * 0.5) * 0.6;
      bell(midi, time, { velocity: 0.018 * energy, pan, decay: 1, ratio: 2 });
      emitAt(time, { type: "note", midi, pan, velocity: 0.02, soft: true });
    }
  }

  function scheduler() {
    const horizon = document.hidden ? 1.2 : LOOKAHEAD;
    while (state.nextTime < ctx.currentTime + horizon) {
      playStep(state.step, state.nextTime);
      state.nextTime += STEP;
      state.step += 1;
    }
  }

  /* ---------- transport ---------- */

  function ensureContext() {
    if (!ctx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return null;
      ctx = new AudioContextClass({ latencyHint: "playback" });
      graph = buildGraph();
      ctx.addEventListener?.("statechange", () => emit({ type: "state" }));
    }
    clearTimeout(state.suspendTimer);
    if (ctx.state === "suspended") ctx.resume().catch(() => {});
    return ctx;
  }

  function fade(param, value, seconds) {
    const now = ctx.currentTime;
    param.cancelScheduledValues(now);
    param.setValueAtTime(param.value, now);
    param.linearRampToValueAtTime(value, now + seconds);
  }

  function startMusic() {
    if (!ensureContext()) return;
    fade(graph.musicOut.gain, 1, 3);
    if (state.timer) return;
    state.step = Math.ceil(state.step / STEPS_PER_CHORD) * STEPS_PER_CHORD;
    state.nextTime = ctx.currentTime + 0.08;
    startSea(state.nextTime);
    state.timer = setInterval(scheduler, 30);
    scheduler();
  }

  function stopMusic() {
    if (!ctx) return;
    fade(graph.musicOut.gain, 0, 1.2);
    clearInterval(state.timer);
    state.timer = null;
    stopSea(ctx.currentTime + 1.3);
    clearTimeout(state.suspendTimer);
    state.suspendTimer = setTimeout(() => {
      if (ctx && !state.music) ctx.suspend().catch(() => {});
    }, 1800);
  }

  /* ---------- interface sounds ---------- */

  // Interface sounds belong to the opt-in too: silent until sound is switched on.
  function sfx(name, { pan = 0, index = null } = {}) {
    if (!state.music || !state.sfx || !ctx || ctx.state !== "running") return;
    const t = ctx.currentTime + 0.01;
    const chord = PROGRESSION[state.chordIndex];
    const destination = graph.sfx;
    switch (name) {
      case "hover":
        bell(pick(chord.bell) + 12, t, { velocity: 0.01, decay: 0.3, pan, destination });
        break;
      case "tap":
        bell(pick(chord.bell) + 12, t, { velocity: 0.035, decay: 0.9, pan, destination });
        break;
      case "echo":
        bell(pick(chord.bell), t, { velocity: 0.05, decay: 2.4, pan, ratio: 3.5, destination });
        swell(t, 0.1, destination);
        break;
      case "ring": {
        // A note on the memory ring: its position picks the pitch.
        const notes = chord.bell;
        const slot = index === null ? Math.floor(Math.random() * notes.length) : index;
        const octave = Math.floor(slot / notes.length) * 12;
        bell(notes[((slot % notes.length) + notes.length) % notes.length] + octave, t, { velocity: 0.06, decay: 2.6, pan, destination });
        break;
      }
      case "chapter": {
        // Crossing into a new chapter of the dive: a rising pair over a soft swell.
        const step = index === null ? 0 : index % 3;
        bell(chord.bell[step], t, { velocity: 0.04, decay: 2.8, pan: pan - 0.25, destination });
        bell(chord.bell[step + 2] + 12, t + 0.16, { velocity: 0.03, decay: 3.2, pan: pan + 0.25, ratio: 3.5, destination });
        swell(t, 0.12, destination);
        break;
      }
      case "awake":
        PROGRESSION[0].bell.slice(0, 5).forEach((midi, i) => {
          bell(midi, t + i * 0.12, { velocity: 0.045, decay: 2.6, pan: (i - 2) * 0.3, destination });
        });
        swell(t, 0.2, destination);
        break;
      default:
        break;
    }
  }

  /* ---------- analysis ---------- */

  function level() {
    if (!ctx || ctx.state !== "running" || !state.music) return 0;
    graph.analyser.getFloatTimeDomainData(graph.timeData);
    let sum = 0;
    for (const sample of graph.timeData) sum += sample * sample;
    return clamp(Math.sqrt(sum / graph.timeData.length) * 2.5, 0, 1);
  }

  function bands(count) {
    const result = new Array(count).fill(0);
    if (!ctx || ctx.state !== "running" || !state.music) return result;
    graph.analyser.getByteFrequencyData(graph.freqData);
    const bins = graph.freqData.length;
    for (let band = 0; band < count; band += 1) {
      const from = Math.floor(2 * (bins / 2) ** (band / count));
      const to = Math.max(from + 1, Math.floor(2 * (bins / 2) ** ((band + 1) / count)));
      let peak = 0;
      for (let i = from; i < to && i < bins; i += 1) peak = Math.max(peak, graph.freqData[i]);
      result[band] = peak / 255;
    }
    return result;
  }

  // A returning visitor who left sound on gets it back on their first gesture,
  // unless that gesture is on a sound control, which decides for itself.
  if (state.music) {
    const unlock = (event) => {
      if (event.target?.closest?.("[data-audio-control]")) return;
      window.removeEventListener("pointerdown", unlock, true);
      window.removeEventListener("keydown", unlock, true);
      if (state.music) startMusic();
      emit({ type: "state" });
    };
    window.addEventListener("pointerdown", unlock, true);
    window.addEventListener("keydown", unlock, true);
  }

  window.EchoAudio = {
    get music() {
      return state.music;
    },
    get decided() {
      return state.decided;
    },
    get sfxEnabled() {
      return state.sfx;
    },
    get volume() {
      return state.volume;
    },
    get running() {
      return Boolean(ctx && ctx.state === "running");
    },
    get chord() {
      return PROGRESSION[state.chordIndex].name;
    },
    setMusic(on) {
      state.music = Boolean(on);
      state.decided = true;
      writePref(PREFS.music, state.music ? "on" : "off");
      if (state.music) startMusic();
      else stopMusic();
      emit({ type: "state" });
    },
    toggleMusic() {
      this.setMusic(!state.music);
    },
    setSfx(on) {
      state.sfx = Boolean(on);
      writePref(PREFS.sfx, state.sfx ? "on" : "off");
      if (graph) fade(graph.sfxOut.gain, state.sfx ? 1 : 0, 0.2);
      emit({ type: "state" });
    },
    setVolume(value) {
      state.volume = clamp(Number(value) || 0, 0, 1);
      writePref(PREFS.volume, state.volume.toFixed(2));
      if (graph) graph.master.gain.setTargetAtTime(state.volume, ctx.currentTime, 0.05);
      emit({ type: "state" });
    },
    setIntensity(value) {
      state.targetIntensity = clamp(value, 0, 1);
    },
    unlock() {
      if (state.music) startMusic();
    },
    sfx,
    level,
    bands,
    on(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
  };
})();
