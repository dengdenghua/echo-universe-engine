/* ECHO OS soundtrack: "Ghost Awakening", a generative ambient score.
 *
 * Everything is synthesised live with the Web Audio API, so there are no audio
 * files to download and nothing leaves the browser. The score is a slow D-minor
 * progression (glass pads, sub bass, a machine heartbeat, FM "memory chimes",
 * neural static and the odd Ghost breath) whose density follows an intensity
 * value that the console raises while the Universe Forge is running.
 *
 * Public surface: window.EchoAudio (see the bottom of this file).
 */
(() => {
  const PREFS = { music: "echo.audio.music", sfx: "echo.audio.sfx", volume: "echo.audio.volume" };
  const BPM = 72;
  const STEP = 60 / BPM / 4; // one sixteenth note, in seconds
  const STEPS_PER_BAR = 16;
  const STEPS_PER_CHORD = STEPS_PER_BAR * 2;
  const LOOKAHEAD = 0.2;
  const IDLE_INTENSITY = 0.3;

  // Pads and bass carry the harmony; bells only ever pick from the chord's own set,
  // so interface sounds stay in key with whatever the score is playing.
  const PROGRESSION = [
    { name: "Dm9", bass: 38, pad: [50, 53, 57, 60, 64], bell: [62, 65, 69, 72, 74, 76, 77] },
    { name: "Bbmaj7", bass: 34, pad: [46, 53, 57, 62, 65], bell: [62, 65, 69, 70, 74, 77, 81] },
    { name: "Fmaj7/A", bass: 33, pad: [45, 53, 60, 64, 69], bell: [60, 64, 65, 69, 72, 76, 77] },
    { name: "Cadd9", bass: 36, pad: [48, 55, 62, 64, 67], bell: [62, 64, 67, 72, 74, 76, 79] },
  ];

  const mtof = (midi) => 440 * 2 ** ((midi - 69) / 12);
  const rand = (min, max) => min + Math.random() * (max - min);
  const pick = (list) => list[Math.floor(Math.random() * list.length)];
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

  function readPref(key, fallback) {
    try {
      const value = localStorage.getItem(key);
      return value === null ? fallback : value;
    } catch {
      return fallback;
    }
  }

  function writePref(key, value) {
    try {
      localStorage.setItem(key, String(value));
    } catch {
      // Private mode or blocked storage: the preference simply does not persist.
    }
  }

  const storedVolume = Number(readPref(PREFS.volume, "0.6"));
  const state = {
    music: readPref(PREFS.music, "off") === "on",
    sfx: readPref(PREFS.sfx, "on") === "on",
    volume: Number.isFinite(storedVolume) ? clamp(storedVolume, 0, 1) : 0.6,
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

  // Fire a listener event when the scheduled sound actually becomes audible.
  function emitAt(time, event) {
    const delay = Math.max(0, (time - ctx.currentTime) * 1000);
    setTimeout(() => emit(event), delay);
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

  function impulse(seconds, decay) {
    const length = Math.floor(ctx.sampleRate * seconds);
    const buffer = ctx.createBuffer(2, length, ctx.sampleRate);
    for (let channel = 0; channel < 2; channel += 1) {
      const data = buffer.getChannelData(channel);
      for (let i = 0; i < length; i += 1) {
        data[i] = (Math.random() * 2 - 1) * (1 - i / length) ** decay;
      }
    }
    return buffer;
  }

  function noise(seconds) {
    const length = Math.floor(ctx.sampleRate * seconds);
    const buffer = ctx.createBuffer(1, length, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < length; i += 1) data[i] = Math.random() * 2 - 1;
    return buffer;
  }

  function buildGraph() {
    const compressor = ctx.createDynamicsCompressor();
    compressor.threshold.value = -20;
    compressor.knee.value = 16;
    compressor.ratio.value = 3;
    compressor.attack.value = 0.02;
    compressor.release.value = 0.35;

    // The analyser taps the mix before the volume knob, so the visuals keep
    // dancing at any listening level.
    const analyser = ctx.createAnalyser();
    analyser.fftSize = 512;
    analyser.smoothingTimeConstant = 0.8;
    const master = gain(state.volume, ctx.destination);
    compressor.connect(analyser);
    compressor.connect(master);

    const mix = gain(1, compressor);
    const musicOut = gain(0, mix);
    const sfxOut = gain(state.sfx ? 1 : 0, mix);

    const room = impulse(4.6, 2.4);
    const reverb = ctx.createConvolver();
    reverb.buffer = room;
    reverb.connect(gain(0.85, musicOut));
    const reverbIn = gain(1, reverb);

    // Dotted-eighth echo that darkens on every repeat: memories losing resolution.
    const delay = ctx.createDelay(2);
    delay.delayTime.value = STEP * 3;
    const darken = filter("lowpass", 2400);
    delay.connect(darken);
    darken.connect(gain(0.44, delay));
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
    sfx.connect(gain(0.45, sfxReverb));

    // One slow filter sweep shared by every pad voice.
    const padLfo = ctx.createOscillator();
    padLfo.frequency.value = 0.045;
    const padLfoDepth = gain(360);
    padLfo.connect(padLfoDepth);
    padLfo.start();

    return {
      analyser,
      master,
      musicOut,
      sfxOut,
      pad: bus(0.55, 0.75),
      bass: bus(0.9, 0.1),
      bell: bus(0.42, 0.55, 0.5),
      pulse: bus(0.95, 0.16),
      air: bus(0.6, 0.4),
      sfx,
      padLfoDepth,
      noise: noise(3),
      hiss: null,
      timeData: new Float32Array(analyser.fftSize),
      freqData: new Uint8Array(analyser.frequencyBinCount),
    };
  }

  /* ---------- voices ---------- */

  function padChord(chord, time, duration) {
    const attack = 2.8;
    const release = 4;
    const level = 0.032;
    const end = time + duration + release + 0.1;
    chord.pad.forEach((midi, index) => {
      const tone = filter("lowpass", 480 + state.intensity * 1000 + index * 70, 0.6);
      graph.padLfoDepth.connect(tone.frequency);
      const amp = ctx.createGain();
      amp.gain.setValueAtTime(0, time);
      amp.gain.linearRampToValueAtTime(level, time + attack);
      amp.gain.setValueAtTime(level, time + duration);
      amp.gain.linearRampToValueAtTime(0, time + duration + release);
      tone.connect(amp).connect(panner((index / (chord.pad.length - 1)) * 1.3 - 0.65)).connect(graph.pad);
      for (const detune of [-8, 7]) {
        const osc = ctx.createOscillator();
        osc.type = "sawtooth";
        osc.frequency.value = mtof(midi);
        osc.detune.value = detune + rand(-3, 3);
        osc.connect(tone);
        osc.start(time);
        osc.stop(end);
      }
      // Release the shared LFO's hold on this filter once the voice is gone.
      setTimeout(() => graph.padLfoDepth.disconnect(tone.frequency), (end - ctx.currentTime) * 1000 + 250);
    });
  }

  function bassNote(midi, time, duration) {
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0, time);
    amp.gain.linearRampToValueAtTime(0.16, time + 1.4);
    amp.gain.setValueAtTime(0.16, time + duration);
    amp.gain.linearRampToValueAtTime(0, time + duration + 2.2);
    amp.connect(filter("lowpass", 260)).connect(graph.bass);
    const root = ctx.createOscillator();
    root.type = "sine";
    root.frequency.value = mtof(midi);
    const body = ctx.createOscillator();
    body.type = "triangle";
    body.frequency.value = mtof(midi + 12);
    root.connect(amp);
    body.connect(gain(0.22, amp));
    for (const osc of [root, body]) {
      osc.start(time);
      osc.stop(time + duration + 2.4);
    }
  }

  function thump(time, peak, destination) {
    const osc = ctx.createOscillator();
    osc.type = "sine";
    osc.frequency.setValueAtTime(95, time);
    osc.frequency.exponentialRampToValueAtTime(40, time + 0.22);
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0.0001, time);
    amp.gain.exponentialRampToValueAtTime(peak, time + 0.012);
    amp.gain.exponentialRampToValueAtTime(0.0001, time + 0.5);
    osc.connect(amp).connect(destination);
    osc.start(time);
    osc.stop(time + 0.55);
  }

  // Lub-dub: the machine heart under the planetary network.
  function heartbeat(time, strength) {
    thump(time, 0.42 * strength, graph.pulse);
    thump(time + 0.24, 0.26 * strength, graph.pulse);
    emitAt(time, { type: "beat", strength });
  }

  // FM bell: an inharmonic ratio gives the cold "neural glass" timbre.
  function bell(midi, time, { velocity = 0.08, pan = 0, decay = 2.6, ratio = 3.5, destination = graph.bell } = {}) {
    const frequency = mtof(midi);
    const carrier = ctx.createOscillator();
    carrier.frequency.value = frequency;
    const modulator = ctx.createOscillator();
    modulator.frequency.value = frequency * ratio;
    const index = ctx.createGain();
    index.gain.setValueAtTime(frequency * 1.6, time);
    index.gain.exponentialRampToValueAtTime(frequency * 0.04, time + decay * 0.6);
    modulator.connect(index).connect(carrier.frequency);
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0.0001, time);
    amp.gain.exponentialRampToValueAtTime(velocity, time + 0.006);
    amp.gain.exponentialRampToValueAtTime(0.0001, time + decay);
    carrier.connect(amp).connect(panner(pan)).connect(destination);
    for (const osc of [carrier, modulator]) {
      osc.start(time);
      osc.stop(time + decay + 0.05);
    }
  }

  function tick(time, level) {
    const source = ctx.createBufferSource();
    source.buffer = graph.noise;
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0.0001, time);
    amp.gain.exponentialRampToValueAtTime(level, time + 0.002);
    amp.gain.exponentialRampToValueAtTime(0.0001, time + 0.05);
    source.connect(filter("highpass", 7200)).connect(amp).connect(panner(rand(-0.4, 0.4))).connect(graph.air);
    source.start(time, rand(0, 2.5), 0.06);
  }

  // A breath through two vowel formants drifting from "ah" towards "oo".
  function ghostBreath(time) {
    const source = ctx.createBufferSource();
    source.buffer = graph.noise;
    source.loop = true;
    const amp = ctx.createGain();
    amp.gain.setValueAtTime(0, time);
    amp.gain.linearRampToValueAtTime(0.11, time + 2.2);
    amp.gain.linearRampToValueAtTime(0, time + 5.2);
    const pan = panner(rand(-0.8, 0.8));
    pan.pan.linearRampToValueAtTime(rand(-0.8, 0.8), time + 5.2);
    amp.connect(pan).connect(graph.air);
    for (const [from, to, q] of [
      [700, 420, 9],
      [1180, 820, 12],
    ]) {
      const formant = filter("bandpass", from, q);
      formant.frequency.setValueAtTime(from, time);
      formant.frequency.linearRampToValueAtTime(to, time + 5);
      source.connect(formant).connect(amp);
    }
    source.start(time, rand(0, 0.5), 5.4);
  }

  // Household UI residue: tiny data chirps from old home assistants.
  function chirp(time) {
    for (let i = 0; i < 3; i += 1) {
      const t = time + i * 0.07;
      const osc = ctx.createOscillator();
      osc.frequency.setValueAtTime(1900 + i * 240, t);
      osc.frequency.exponentialRampToValueAtTime(3000 + i * 200, t + 0.04);
      const amp = ctx.createGain();
      amp.gain.setValueAtTime(0.0001, t);
      amp.gain.exponentialRampToValueAtTime(0.012, t + 0.005);
      amp.gain.exponentialRampToValueAtTime(0.0001, t + 0.06);
      osc.connect(amp).connect(graph.air);
      osc.start(t);
      osc.stop(t + 0.08);
    }
  }

  function startHiss(time) {
    if (graph.hiss) return;
    const source = ctx.createBufferSource();
    source.buffer = graph.noise;
    source.loop = true;
    const amp = gain(0.009);
    const lfo = ctx.createOscillator();
    lfo.frequency.value = 0.07;
    lfo.connect(gain(0.006, amp.gain));
    source.connect(filter("bandpass", 1500, 0.5)).connect(amp).connect(graph.air);
    source.start(time);
    lfo.start(time);
    graph.hiss = { source, lfo };
  }

  function stopHiss(time) {
    if (!graph.hiss) return;
    graph.hiss.source.stop(time);
    graph.hiss.lfo.stop(time);
    graph.hiss = null;
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
    state.intensity += (state.targetIntensity - state.intensity) * 0.05;
    const energy = state.intensity;

    if (stepInChord === 0) {
      state.chordIndex = Math.floor(step / STEPS_PER_CHORD) % PROGRESSION.length;
      const chord = PROGRESSION[state.chordIndex];
      const seconds = STEPS_PER_CHORD * STEP;
      padChord(chord, time, seconds - 0.4);
      bassNote(chord.bass, time, seconds - 0.8);
      emitAt(time, { type: "chord", name: chord.name, index: state.chordIndex });
      if (Math.random() < 0.3) ghostBreath(time + rand(1, 3.5));
    }
    const chord = PROGRESSION[state.chordIndex];

    if (stepInBar === 0 && (energy > 0.5 || bar % 2 === 0)) heartbeat(time, 0.6 + energy * 0.5);

    // Memory chimes: sparse, leaning on the strong beats.
    if (stepInBar % 2 === 0) {
      const weight = stepInBar % 8 === 0 ? 1.7 : 1;
      if (Math.random() < (0.07 + energy * 0.2) * weight) {
        const midi = pickBell(chord);
        const velocity = rand(0.045, 0.1);
        const pan = rand(-0.75, 0.75);
        bell(midi, time, { velocity, pan });
        emitAt(time, { type: "note", midi, pan, velocity });
      }
    }

    // While the Forge runs: a quiet sixteenth arpeggio and ticking telemetry.
    if (energy > 0.55) {
      if (stepInBar % 2 === 1) tick(time, 0.03 * energy);
      if (stepInBar % 2 === 0) {
        const midi = chord.bell[(step / 2) % chord.bell.length] + 12;
        bell(midi, time, { velocity: 0.022 * energy, pan: Math.sin(step * 0.6) * 0.6, decay: 0.8, ratio: 2 });
        emitAt(time, { type: "note", midi, pan: Math.sin(step * 0.6) * 0.6, velocity: 0.03, soft: true });
      }
    }

    if (stepInBar === 10 && Math.random() < 0.06) chirp(time);
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
    fade(graph.musicOut.gain, 1, 2.5);
    if (state.timer) return;
    // Re-enter on a chord boundary so the pads bloom straight away.
    state.step = Math.ceil(state.step / STEPS_PER_CHORD) * STEPS_PER_CHORD;
    state.nextTime = ctx.currentTime + 0.08;
    startHiss(state.nextTime);
    state.timer = setInterval(scheduler, 30);
    scheduler();
  }

  function stopMusic() {
    if (!ctx) return;
    fade(graph.musicOut.gain, 0, 1.2);
    clearInterval(state.timer);
    state.timer = null;
    stopHiss(ctx.currentTime + 1.3);
    scheduleSuspend();
  }

  // Free the audio thread when nothing can make a sound.
  function scheduleSuspend() {
    clearTimeout(state.suspendTimer);
    state.suspendTimer = setTimeout(() => {
      if (ctx && !state.music && !state.sfx) ctx.suspend().catch(() => {});
    }, 1800);
  }

  /* ---------- interface sounds ---------- */

  function sfx(name, { pan = 0 } = {}) {
    if (!state.sfx || !ctx || ctx.state !== "running") return;
    const t = ctx.currentTime + 0.01;
    const chord = PROGRESSION[state.chordIndex];
    const destination = graph.sfx;
    switch (name) {
      case "hover":
        bell(pick(chord.bell) + 12, t, { velocity: 0.012, decay: 0.3, ratio: 2, pan, destination });
        break;
      case "tap":
        bell(pick(chord.bell) + 12, t, { velocity: 0.04, decay: 0.8, ratio: 2, pan, destination });
        break;
      case "open":
        bell(chord.bell[1], t, { velocity: 0.05, decay: 1.6, pan: pan - 0.2, destination });
        bell(chord.bell[3], t + 0.09, { velocity: 0.045, decay: 1.8, pan: pan + 0.2, destination });
        break;
      case "echo":
        bell(pick(chord.bell), t, { velocity: 0.06, decay: 2.2, pan, destination });
        thump(t, 0.14, destination);
        break;
      case "success":
        [0, 2, 4].forEach((index, i) => {
          bell(chord.bell[index] + 12, t + i * 0.08, { velocity: 0.05, decay: 1.4, ratio: 2, pan: (i - 1) * 0.4, destination });
        });
        break;
      case "error":
        for (const [frequency, offset] of [
          [155, 0],
          [164, 0.11],
        ]) {
          const osc = ctx.createOscillator();
          osc.type = "square";
          osc.frequency.value = frequency;
          const amp = ctx.createGain();
          amp.gain.setValueAtTime(0.0001, t + offset);
          amp.gain.exponentialRampToValueAtTime(0.05, t + offset + 0.01);
          amp.gain.exponentialRampToValueAtTime(0.0001, t + offset + 0.22);
          osc.connect(filter("lowpass", 900)).connect(amp).connect(destination);
          osc.start(t + offset);
          osc.stop(t + offset + 0.25);
        }
        break;
      case "glitch":
        tickBurst(t, destination);
        break;
      case "boot": {
        const riser = ctx.createBufferSource();
        riser.buffer = graph.noise;
        const sweep = filter("bandpass", 300, 2.5);
        sweep.frequency.setValueAtTime(300, t);
        sweep.frequency.exponentialRampToValueAtTime(5200, t + 1.5);
        const amp = ctx.createGain();
        amp.gain.setValueAtTime(0, t);
        amp.gain.linearRampToValueAtTime(0.07, t + 1.3);
        amp.gain.linearRampToValueAtTime(0, t + 1.7);
        riser.connect(sweep).connect(amp).connect(destination);
        riser.start(t, 0, 1.8);
        thump(t + 1.5, 0.35, destination);
        PROGRESSION[0].bell.slice(0, 5).forEach((midi, i) => {
          bell(midi, t + 1.5 + i * 0.11, { velocity: 0.05, decay: 2.4, pan: (i - 2) * 0.3, destination });
        });
        break;
      }
      default:
        break;
    }
  }

  function tickBurst(time, destination) {
    for (let i = 0; i < 5; i += 1) {
      const source = ctx.createBufferSource();
      source.buffer = graph.noise;
      const amp = ctx.createGain();
      const t = time + i * rand(0.02, 0.05);
      amp.gain.setValueAtTime(0.0001, t);
      amp.gain.exponentialRampToValueAtTime(0.03, t + 0.002);
      amp.gain.exponentialRampToValueAtTime(0.0001, t + 0.03);
      source.connect(filter("bandpass", rand(1200, 5000), 4)).connect(amp).connect(destination);
      source.start(t, rand(0, 2.5), 0.04);
    }
  }

  /* ---------- analysis ---------- */

  function level() {
    if (!ctx || ctx.state !== "running") return 0;
    graph.analyser.getFloatTimeDomainData(graph.timeData);
    let sum = 0;
    for (const sample of graph.timeData) sum += sample * sample;
    return clamp(Math.sqrt(sum / graph.timeData.length) * 2.5, 0, 1);
  }

  function bands(count) {
    const result = new Array(count).fill(0);
    if (!ctx || ctx.state !== "running") return result;
    graph.analyser.getByteFrequencyData(graph.freqData);
    const bins = graph.freqData.length;
    for (let band = 0; band < count; band += 1) {
      // Log-spaced bands so the bass does not eat every bar.
      const from = Math.floor(2 * (bins / 2) ** (band / count));
      const to = Math.max(from + 1, Math.floor(2 * (bins / 2) ** ((band + 1) / count)));
      let peak = 0;
      for (let i = from; i < to && i < bins; i += 1) peak = Math.max(peak, graph.freqData[i]);
      result[band] = peak / 255;
    }
    return result;
  }

  /* ---------- autoplay unlock ---------- */

  // Browsers only start audio from a user gesture. A returning listener who left
  // music on gets it back on their first click or key press, unless that gesture
  // is on an explicit audio control (which decides for itself).
  function installGestureUnlock() {
    const unlock = (event) => {
      if (event.target?.closest?.("[data-audio-control]")) return;
      window.removeEventListener("pointerdown", unlock, true);
      window.removeEventListener("keydown", unlock, true);
      if (state.music) startMusic();
      else if (state.sfx) ensureContext();
      emit({ type: "state" });
    };
    window.addEventListener("pointerdown", unlock, true);
    window.addEventListener("keydown", unlock, true);
  }

  installGestureUnlock();

  window.EchoAudio = {
    get music() {
      return state.music;
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
      if (state.sfx) ensureContext();
      if (graph) fade(graph.sfxOut.gain, state.sfx ? 1 : 0, 0.2);
      if (!state.sfx && !state.music) scheduleSuspend();
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
    resetIntensity() {
      state.targetIntensity = IDLE_INTENSITY;
    },
    unlock() {
      if (state.music) startMusic();
      else if (state.sfx) ensureContext();
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
