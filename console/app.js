const state = {
  status: null,
  characters: [],
  assets: null,
  candidates: [],
  governanceCandidates: [],
  events: [],
  engineState: { key: "connecting", params: {}, ok: false },
  outputModeKey: "idle",
  outputContentKey: "awaitingSignal",
  octopusStatusKey: "adapter",
  octopusPlanKey: "loadingRuntime",
  runtimeVisible: new URLSearchParams(window.location.search).get("runtime") === "1",
};

const i18n = window.EchoI18n;
const t = (key, params, fallback) => i18n.t(key, params, fallback);

function $(selector) {
  return document.querySelector(selector);
}

function $all(selector) {
  return Array.from(document.querySelectorAll(selector));
}

function truncate(value, size = 150) {
  if (!value) return "";
  return value.length > size ? `${value.slice(0, size)}...` : value;
}

async function requestJson(url, options = {}) {
  const headers = new Headers(options.headers || {});
  try {
    const token = sessionStorage.getItem("echo.admin.token") || localStorage.getItem("echo.auth.token");
    if (token && !headers.has("Authorization")) headers.set("Authorization", `Bearer ${token}`);
  } catch (_) {
    // A trusted reverse proxy may provide authentication when browser storage is unavailable.
  }
  const response = await fetch(url, { ...options, headers });
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      message = body.detail || body.error || message;
    } catch {
      // Keep the HTTP status fallback when the server did not return JSON.
    }
    throw new Error(message);
  }
  return response.json();
}

function setEngineState(key, ok = false, params = {}) {
  state.engineState = { key, params, ok };
  const target = $("#engine-state");
  target.textContent = t(key, params);
  target.classList.toggle("online", ok);
}

function setOutputMode(key) {
  state.outputModeKey = key;
  $("#output-mode").textContent = t(key);
}

function setOutputModeRaw(value) {
  state.outputModeKey = null;
  $("#output-mode").textContent = value;
}

function setOutputContent(key) {
  state.outputContentKey = key;
  $("#factory-output").textContent = t(key);
}

function setOutputContentRaw(value) {
  state.outputContentKey = null;
  $("#factory-output").textContent = value;
}

function openWindow(name) {
  const panel = document.querySelector(`[data-window-panel="${name}"]`);
  if (!panel) return;
  $all(".window").forEach((item) => item.classList.remove("active", "focused"));
  panel.classList.add("active", "focused");
  $all(".dock-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.window === name);
  });
}

function closeWindow(panel) {
  if (!panel) return;
  const name = panel.dataset.windowPanel;
  panel.classList.remove("active", "focused");
  $all(".dock-item").forEach((item) => {
    if (item.dataset.window === name) item.classList.remove("active");
  });
}

function installRuntimeVisibility() {
  document.body.classList.toggle("show-runtime", state.runtimeVisible);
  if (!state.runtimeVisible) {
    const panel = document.querySelector('[data-window-panel="octopus"]');
    panel?.classList.remove("active");
  }
}

function renderMetrics(status) {
  const metrics = [
    ["metricBible", status.bible_files],
    ["metricCharacters", status.characters],
    ["metricFactions", status.factions],
    ["metricLocations", status.locations],
    ["metricTech", status.technologies],
    ["metricTimeline", status.timeline_files],
    ["metricRelations", status.relationship_files],
    ["metricStories", status.stories],
  ];
  $("#metrics").innerHTML = metrics
    .map(
      ([labelKey, value]) => `
        <div class="metric">
          <strong>${value}</strong>
          <span>${t(labelKey)}</span>
        </div>
      `,
    )
    .join("");
}

function renderCharacters(cards) {
  $("#character-count").textContent = t("onlineCount", { count: cards.length });
  $("#character-grid").innerHTML = cards
    .map(
      (card) => `
        <article class="agent-tile">
          <div class="agent-head">
            <span>${card.id}</span>
            <strong>${card.name}</strong>
          </div>
          <div class="agent-code">${card.codename || card.name}</div>
          <p>${truncate(card.description)}</p>
          <div class="agent-tags">
            <span>${card.role || t("unassigned")}</span>
            <span>${card.rank || t("noRank")}</span>
            ${(card.abilities || []).slice(0, 1).map((ability) => `<span>${ability}</span>`).join("")}
          </div>
        </article>
      `,
    )
    .join("");
}

function renderAssets(index) {
  const characters = Object.entries(index?.characters || {});
  $("#asset-count").textContent = t("lockedCount", { count: characters.length });
  $("#asset-grid").innerHTML = characters
    .map(([id, item]) => {
      const urls = item.urls || {};
      const portrait = urls.front || urls.avatar;
      return `
        <article class="asset-card">
          <div class="asset-preview">
            ${portrait ? `<img src="${portrait}" alt="${t("frontReference", { name: item.name })}" />` : ""}
          </div>
          <div class="asset-info">
            <div class="asset-title">
              <span>${id}</span>
              <strong>${item.name}</strong>
            </div>
            <p>${item.codename || t("whiteGhostTeam")}</p>
            <div class="asset-links">
              ${["front", "side", "back", "avatar", "source_turnaround"]
                .filter((key) => urls[key])
                .map((key) => `<a href="${urls[key]}" target="_blank" rel="noreferrer">${t(`link${key.split("_").map((part) => part[0].toUpperCase() + part.slice(1)).join("")}`, {}, key)}</a>`)
                .join("")}
            </div>
          </div>
        </article>
      `;
    })
    .join("");
}

function renderMemory(result) {
  if (!result?.content) return;
  const lines = result.content
    .split("\n")
    .filter((line) => line.startsWith("### ") || line.startsWith("- Activity:"))
    .slice(0, 16);
  $("#memory-stream").innerHTML = lines
    .map((line) => {
      const isName = line.startsWith("### ");
      return isName
        ? `<li class="stream-name"><strong>${line.replace("### ", "")}</strong><span>${t("agentPulse")}</span></li>`
        : `<li><strong>${t("log")}</strong><span>${line.replace("- Activity: ", "")}</span></li>`;
    })
    .join("");
}

function renderJournal(events) {
  if (!events?.length) {
    $("#memory-stream").innerHTML = `<li><strong>${t("queue")}</strong><span>${t("noJournalEvents")}</span></li>`;
    return;
  }
  $("#memory-stream").innerHTML = events
    .slice(-16)
    .reverse()
    .map(
      (event) => `
        <li>
          <strong>${i18n.translateMode(event.mode)}</strong>
          <span>${event.title}${event.output_path ? ` · ${event.output_path}` : ""}</span>
        </li>
      `,
    )
    .join("");
}

function renderGovernanceCandidate(row) {
  const committee = row.committee;
  const continuity = row.continuity;
  const resonance = row.resonance;
  const gate = row.promotion_gate;
  const title = row.candidate.title[i18n.getLocale()] || row.candidate.title.en;
  const members = committee.members || [];
  const continuityReviewer = continuity.reviewers?.[0]?.id || "continuity_editor";
  const promotionLabel = row.promotion.promoted
    ? t("statusPromoted")
    : gate.state === "blocked"
      ? t("promotionBlocked")
      : t(gate.can_promote ? "promotionReady" : "promotionLocked");
  return `
    <article class="candidate-card governance-card" data-governance-id="${row.candidate.id}" data-revision="${row.candidate.revision_sha256}" data-continuity-reviewer="${continuityReviewer}">
      <div class="candidate-head">
        <span>${t("publicCanon")}</span>
        <strong>${title}</strong>
      </div>
      <p>${t("resonanceSummary", { support: resonance.support, revise: resonance.revise })}</p>
      <div class="candidate-meta governance-meta">
        <span>${t("continuityState", { status: t(`governanceContinuity${continuity.status[0].toUpperCase()}${continuity.status.slice(1)}`, {}, continuity.status) })}</span>
        <span>${t("committeeState", { approvals: committee.approvals, size: committee.size, threshold: committee.threshold })}</span>
        <span>${promotionLabel}</span>
        <a href="${row.candidate.public_href}" target="_blank" rel="noreferrer">${t("open")}</a>
      </div>
      <label class="reviewer-select"><span>${t("reviewer")}</span><select data-reviewer-select>
        ${members.map((member) => `<option value="${member.id}">${member.id}${member.decision ? ` · ${member.decision}` : ""}</option>`).join("")}
      </select></label>
      <div class="candidate-actions governance-actions">
        <button data-governance-action="approve">${t("approveVote")}</button>
        <button data-governance-action="reject">${t("rejectVote")}</button>
        <button data-governance-action="continuity-pass">${t("continuityPass")}</button>
        <button data-governance-action="continuity-veto">${t("continuityVeto")}</button>
        <button data-governance-action="promote" ${gate.can_promote ? "" : "disabled"}>${t("promote")}</button>
      </div>
    </article>
  `;
}

function renderCandidates(candidates, governanceCandidates = []) {
  const grid = $("#candidate-grid");
  if (!candidates?.length && !governanceCandidates?.length) {
    grid.innerHTML = `<div class="empty-state">${t("noCandidates")}</div>`;
    return;
  }
  const governanceMarkup = governanceCandidates.map(renderGovernanceCandidate).join("");
  const legacyMarkup = candidates
    .slice()
    .reverse()
    .map((row) => {
      const event = row.event;
      const decision = row.latest_decision;
      const promotion = row.promotion;
      const reason = decision?.summary || event.summary || t("awaitingReview");
      return `
        <article class="candidate-card" data-event-id="${event.event_id}">
          <div class="candidate-head">
            <span>${i18n.translateMode(event.mode)}</span>
            <strong>${event.title}</strong>
          </div>
          <p>${truncate(reason, 190)}</p>
          <div class="candidate-meta">
            <span>${i18n.translateStatus(row.status)}</span>
            ${event.output_path ? `<a href="/${event.output_path}" target="_blank" rel="noreferrer">${t("open")}</a>` : ""}
            ${promotion?.output_path ? `<a href="/${promotion.output_path}" target="_blank" rel="noreferrer">${t("canon")}</a>` : ""}
          </div>
          <div class="candidate-actions">
            <button data-action="accept">${t("accept")}</button>
            <button data-action="reject">${t("reject")}</button>
            <button data-action="promote" ${row.can_promote ? "" : "disabled"}>${t("promote")}</button>
          </div>
        </article>
      `;
    })
    .join("");
  grid.innerHTML = governanceMarkup + legacyMarkup;
}

async function refresh() {
  try {
    setEngineState("syncing");
    const [health, characters, plan, octopus, assets, events, candidates, governanceCandidates] = await Promise.all([
      requestJson("/api/health"),
      requestJson("/api/canon/characters"),
      requestJson("/api/integrations/octopus/plan"),
      requestJson("/api/integrations/octopus/status"),
      requestJson("/api/assets/characters"),
      requestJson("/api/journal/events?limit=16"),
      requestJson("/api/journal/candidates?limit=24"),
      requestJson("/api/canon/governance/candidates"),
    ]);
    state.status = health.canon;
    state.characters = characters;
    state.assets = assets;
    state.candidates = candidates;
    state.governanceCandidates = governanceCandidates;
    state.events = events;
    renderMetrics(health.canon);
    renderCharacters(characters);
    renderAssets(assets);
    renderJournal(events);
    renderCandidates(candidates, governanceCandidates);
    state.octopusPlanKey = null;
    $("#octopus-plan").textContent = plan.content;
    state.octopusStatusKey = octopus.configured ? "linked" : "notLinked";
    $("#octopus-status").textContent = t(state.octopusStatusKey);
    setEngineState("online", true);
  } catch (error) {
    setEngineState("offline", false, { message: error.message });
  }
}

async function reviewCandidate(eventId, decision) {
  const reason =
    decision === "accepted"
      ? "Reviewed in ECHO OS console and accepted for canon promotion."
      : "Reviewed in ECHO OS console and rejected from canon promotion.";
  await requestJson("/api/journal/decisions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ event_id: eventId, decision, reason, reviewer: "console" }),
  });
}

async function promoteCandidate(eventId) {
  return requestJson("/api/canon/promotions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ event_id: eventId }),
  });
}

async function reviewGovernanceCandidate(candidateId, reviewer, decision, revision) {
  return requestJson(`/api/canon/governance/candidates/${candidateId}/committee-votes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reviewer, decision, expected_revision_sha256: revision, reason: "Recorded in the ECHO OS canon governance console." }),
  });
}

async function checkGovernanceContinuity(candidateId, reviewer, verdict, revision) {
  return requestJson(`/api/canon/governance/candidates/${candidateId}/continuity-checks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ reviewer, verdict, expected_revision_sha256: revision, reason: "Continuity decision recorded in the ECHO OS console.", issues: verdict === "veto" ? ["continuity_review_required"] : [] }),
  });
}

async function promoteGovernanceCandidate(candidateId, revision) {
  return requestJson(`/api/canon/governance/candidates/${candidateId}/promotions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expected_revision_sha256: revision }),
  });
}

async function syncOctopusRuntime() {
  return requestJson("/api/integrations/octopus/sync-agents", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
}

async function runCommand(url, label = t("running")) {
  openWindow("factory");
  setOutputModeRaw(label);
  setOutputContent("runningDots");
  try {
    const result = await requestJson(url, { method: "POST" });
    setOutputModeRaw(result.mode ? i18n.translateMode(result.mode) : t("done"));
    setOutputContentRaw(result.content || JSON.stringify(result, null, 2));
    renderMemory(result);
    await refresh();
  } catch (error) {
    setOutputMode("error");
    setOutputContentRaw(error.message);
  }
}

function installDock() {
  $all(".dock-item").forEach((item) => {
    item.addEventListener("click", () => openWindow(item.dataset.window));
  });
}

function installWindowControls() {
  $all(".window-close").forEach((button) => {
    button.addEventListener("click", () => closeWindow(button.closest(".window")));
  });
}

function installCommands() {
  $("#refresh-btn").addEventListener("click", refresh);
  $("#octopus-sync-btn").addEventListener("click", async () => {
    openWindow("octopus");
    setOutputMode("octopusSync");
    setOutputContent("syncingAgents");
    try {
      const result = await syncOctopusRuntime();
      setOutputContentRaw(JSON.stringify(result, null, 2));
      await refresh();
    } catch (error) {
      setOutputMode("error");
      setOutputContentRaw(error.message);
    }
  });
  $all(".forge-command").forEach((item) => {
    item.addEventListener("click", () => runCommand(item.dataset.command, item.textContent.trim()));
  });
  $("#candidate-grid").addEventListener("click", async (event) => {
    const button = event.target.closest("button[data-action]");
    const governanceButton = event.target.closest("button[data-governance-action]");
    if (governanceButton) {
      const governanceCard = governanceButton.closest("[data-governance-id]");
      const candidateId = governanceCard?.dataset.governanceId;
      const revision = governanceCard?.dataset.revision;
      const action = governanceButton.dataset.governanceAction;
      if (!candidateId || !revision || !action) return;
      if (action === "continuity-veto" && !window.confirm(t("confirmContinuityVeto"))) return;
      if (action === "promote" && !window.confirm(t("confirmCanonPromotion"))) return;
      setOutputModeRaw(t("canonGovernance"));
      setOutputContent("updatingJournal");
      try {
        if (action === "approve" || action === "reject") {
          const reviewer = governanceCard.querySelector("[data-reviewer-select]")?.value;
          await reviewGovernanceCandidate(candidateId, reviewer, action, revision);
        } else if (action === "continuity-pass" || action === "continuity-veto") {
          const reviewer = governanceCard.dataset.continuityReviewer;
          await checkGovernanceContinuity(candidateId, reviewer, action === "continuity-pass" ? "pass" : "veto", revision);
        } else if (action === "promote") {
          const result = await promoteGovernanceCandidate(candidateId, revision);
          setOutputContentRaw(JSON.stringify(result, null, 2));
        }
        await refresh();
      } catch (error) {
        setOutputMode("error");
        setOutputContentRaw(error.message);
      }
      return;
    }
    if (!button) return;
    const card = button.closest("[data-event-id]");
    const eventId = card?.dataset.eventId;
    if (!eventId) return;
    const action = button.dataset.action;
    setOutputMode(action);
    setOutputContent("updatingJournal");
    try {
      if (action === "accept") {
        await reviewCandidate(eventId, "accepted");
      } else if (action === "reject") {
        await reviewCandidate(eventId, "rejected");
      } else if (action === "promote") {
        const result = await promoteCandidate(eventId);
        setOutputContentRaw(JSON.stringify(result, null, 2));
      }
      await refresh();
    } catch (error) {
      setOutputMode("error");
      setOutputContentRaw(error.message);
    }
  });
}

function tickClock() {
  $("#system-clock").textContent = i18n.formatTime(new Date());
}

function renderCurrentLocale() {
  if (state.status) renderMetrics(state.status);
  if (state.characters.length) renderCharacters(state.characters);
  if (state.assets) renderAssets(state.assets);
  if (state.events.length) renderJournal(state.events);
  if (state.candidates || state.governanceCandidates) renderCandidates(state.candidates, state.governanceCandidates);
  setEngineState(state.engineState.key, state.engineState.ok, state.engineState.params);
  if (state.outputModeKey) $("#output-mode").textContent = t(state.outputModeKey);
  if (state.outputContentKey) $("#factory-output").textContent = t(state.outputContentKey);
  if (state.octopusStatusKey) $("#octopus-status").textContent = t(state.octopusStatusKey);
  if (state.octopusPlanKey) $("#octopus-plan").textContent = t(state.octopusPlanKey);
  tickClock();
}

installDock();
installWindowControls();
installCommands();
installRuntimeVisibility();
setEngineState("connecting");
setOutputMode("idle");
setOutputContent("awaitingSignal");
$("#octopus-status").textContent = t("adapter");
$("#octopus-plan").textContent = t("loadingRuntime");
i18n.subscribe(renderCurrentLocale);
tickClock();
setInterval(tickClock, 30_000);
refresh();
