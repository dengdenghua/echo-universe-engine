const state = {
  status: null,
  characters: [],
  assets: null,
  candidates: [],
  runtimeVisible: new URLSearchParams(window.location.search).get("runtime") === "1",
  zIndex: 20,
};

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
  const response = await fetch(url, options);
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

function setEngineState(label, ok = false) {
  const target = $("#engine-state");
  target.textContent = label;
  target.classList.toggle("online", ok);
}

function bringToFront(panel) {
  state.zIndex += 1;
  panel.style.zIndex = state.zIndex;
  $all(".window").forEach((item) => item.classList.toggle("focused", item === panel));
}

function openWindow(name) {
  const panel = document.querySelector(`[data-window-panel="${name}"]`);
  if (!panel) return;
  panel.classList.add("active");
  bringToFront(panel);
  $all(".dock-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.window === name);
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
    ["Bible", status.bible_files],
    ["Characters", status.characters],
    ["Factions", status.factions],
    ["Locations", status.locations],
    ["Tech", status.technologies],
    ["Timeline", status.timeline_files],
    ["Relations", status.relationship_files],
    ["Stories", status.stories],
  ];
  $("#metrics").innerHTML = metrics
    .map(
      ([label, value]) => `
        <div class="metric">
          <strong>${value}</strong>
          <span>${label}</span>
        </div>
      `,
    )
    .join("");
}

function renderCharacters(cards) {
  $("#character-count").textContent = `${cards.length} online`;
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
            <span>${card.role || "Unassigned"}</span>
            <span>${card.rank || "No rank"}</span>
            ${(card.abilities || []).slice(0, 1).map((ability) => `<span>${ability}</span>`).join("")}
          </div>
        </article>
      `,
    )
    .join("");
}

function renderAssets(index) {
  const characters = Object.entries(index?.characters || {});
  $("#asset-count").textContent = `${characters.length} locked`;
  $("#asset-grid").innerHTML = characters
    .map(([id, item]) => {
      const urls = item.urls || {};
      const portrait = urls.front || urls.avatar;
      return `
        <article class="asset-card">
          <div class="asset-preview">
            ${portrait ? `<img src="${portrait}" alt="${item.name} front reference" />` : ""}
          </div>
          <div class="asset-info">
            <div class="asset-title">
              <span>${id}</span>
              <strong>${item.name}</strong>
            </div>
            <p>${item.codename || "White Ghost Team"}</p>
            <div class="asset-links">
              ${["front", "side", "back", "avatar", "source_turnaround"]
                .filter((key) => urls[key])
                .map((key) => `<a href="${urls[key]}" target="_blank" rel="noreferrer">${key}</a>`)
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
        ? `<li class="stream-name"><strong>${line.replace("### ", "")}</strong><span>agent pulse</span></li>`
        : `<li><strong>log</strong><span>${line.replace("- Activity: ", "")}</span></li>`;
    })
    .join("");
}

function renderJournal(events) {
  if (!events?.length) {
    $("#memory-stream").innerHTML = `<li><strong>queue</strong><span>No journal events yet.</span></li>`;
    return;
  }
  $("#memory-stream").innerHTML = events
    .slice(-16)
    .reverse()
    .map(
      (event) => `
        <li>
          <strong>${event.mode}</strong>
          <span>${event.title}${event.output_path ? ` · ${event.output_path}` : ""}</span>
        </li>
      `,
    )
    .join("");
}

function renderCandidates(candidates) {
  const grid = $("#candidate-grid");
  if (!candidates?.length) {
    grid.innerHTML = `<div class="empty-state">No candidate outputs waiting in journal.</div>`;
    return;
  }
  grid.innerHTML = candidates
    .slice()
    .reverse()
    .map((row) => {
      const event = row.event;
      const decision = row.latest_decision;
      const promotion = row.promotion;
      const reason = decision?.summary || event.summary || "Awaiting review.";
      return `
        <article class="candidate-card" data-event-id="${event.event_id}">
          <div class="candidate-head">
            <span>${event.mode}</span>
            <strong>${event.title}</strong>
          </div>
          <p>${truncate(reason, 190)}</p>
          <div class="candidate-meta">
            <span>${row.status}</span>
            ${event.output_path ? `<a href="/${event.output_path}" target="_blank" rel="noreferrer">open</a>` : ""}
            ${promotion?.output_path ? `<a href="/${promotion.output_path}" target="_blank" rel="noreferrer">canon</a>` : ""}
          </div>
          <div class="candidate-actions">
            <button data-action="accept">Accept</button>
            <button data-action="reject">Reject</button>
            <button data-action="promote" ${row.can_promote ? "" : "disabled"}>Promote</button>
          </div>
        </article>
      `;
    })
    .join("");
}

async function refresh() {
  try {
    setEngineState("Syncing");
    const [health, characters, plan, octopus, assets, events, candidates] = await Promise.all([
      requestJson("/api/health"),
      requestJson("/api/canon/characters"),
      requestJson("/api/integrations/octopus/plan"),
      requestJson("/api/integrations/octopus/status"),
      requestJson("/api/assets/characters"),
      requestJson("/api/journal/events?limit=16"),
      requestJson("/api/journal/candidates?limit=24"),
    ]);
    state.status = health.canon;
    state.characters = characters;
    state.assets = assets;
    state.candidates = candidates;
    renderMetrics(health.canon);
    renderCharacters(characters);
    renderAssets(assets);
    renderJournal(events);
    renderCandidates(candidates);
    $("#octopus-plan").textContent = plan.content;
    $("#octopus-status").textContent = octopus.configured ? "Linked" : "Not linked";
    setEngineState("Online", true);
  } catch (error) {
    setEngineState(`Offline: ${error.message}`);
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

async function syncOctopusRuntime() {
  return requestJson("/api/integrations/octopus/sync-agents", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({}),
  });
}

async function runCommand(url, label = "Running") {
  openWindow("factory");
  $("#output-mode").textContent = label;
  $("#factory-output").textContent = "Running...";
  try {
    const result = await requestJson(url, { method: "POST" });
    $("#output-mode").textContent = result.mode || "Done";
    $("#factory-output").textContent = result.content || JSON.stringify(result, null, 2);
    renderMemory(result);
    await refresh();
  } catch (error) {
    $("#output-mode").textContent = "Error";
    $("#factory-output").textContent = error.message;
  }
}

function installDock() {
  $all(".dock-item").forEach((item) => {
    item.addEventListener("click", () => openWindow(item.dataset.window));
  });
}

function installDrag() {
  $all(".window").forEach((panel) => {
    const handle = panel.querySelector(".titlebar");
    let drag = null;
    panel.addEventListener("mousedown", () => bringToFront(panel));
    handle.addEventListener("mousedown", (event) => {
      if (event.target.closest("button")) return;
      const rect = panel.getBoundingClientRect();
      drag = {
        pointerId: event.pointerId,
        dx: event.clientX - rect.left,
        dy: event.clientY - rect.top,
      };
      handle.setPointerCapture?.(event.pointerId);
    });
    handle.addEventListener("mousemove", (event) => {
      if (!drag) return;
      const left = Math.max(74, event.clientX - drag.dx);
      const top = Math.max(58, event.clientY - drag.dy);
      panel.style.left = `${left}px`;
      panel.style.top = `${top}px`;
      panel.style.right = "auto";
      panel.style.bottom = "auto";
    });
    handle.addEventListener("mouseup", () => {
      drag = null;
    });
    handle.addEventListener("mouseleave", () => {
      drag = null;
    });
  });
}

function installCommands() {
  $("#refresh-btn").addEventListener("click", refresh);
  $("#octopus-sync-btn").addEventListener("click", async () => {
    openWindow("octopus");
    $("#output-mode").textContent = "Octopus Sync";
    $("#factory-output").textContent = "Syncing agents...";
    try {
      const result = await syncOctopusRuntime();
      $("#factory-output").textContent = JSON.stringify(result, null, 2);
      await refresh();
    } catch (error) {
      $("#output-mode").textContent = "Error";
      $("#factory-output").textContent = error.message;
    }
  });
  $all(".forge-command").forEach((item) => {
    item.addEventListener("click", () => runCommand(item.dataset.command, item.textContent.trim()));
  });
  $("#candidate-grid").addEventListener("click", async (event) => {
    const button = event.target.closest("button[data-action]");
    if (!button) return;
    const card = button.closest("[data-event-id]");
    const eventId = card?.dataset.eventId;
    if (!eventId) return;
    const action = button.dataset.action;
    $("#output-mode").textContent = action;
    $("#factory-output").textContent = "Updating candidate journal...";
    try {
      if (action === "accept") {
        await reviewCandidate(eventId, "accepted");
      } else if (action === "reject") {
        await reviewCandidate(eventId, "rejected");
      } else if (action === "promote") {
        const result = await promoteCandidate(eventId);
        $("#factory-output").textContent = JSON.stringify(result, null, 2);
      }
      await refresh();
    } catch (error) {
      $("#output-mode").textContent = "Error";
      $("#factory-output").textContent = error.message;
    }
  });
}

function tickClock() {
  const now = new Date();
  $("#system-clock").textContent = now.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}

installDock();
installDrag();
installCommands();
installRuntimeVisibility();
tickClock();
setInterval(tickClock, 30_000);
refresh();
