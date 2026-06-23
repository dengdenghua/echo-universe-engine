const state = {
  status: null,
  characters: [],
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
    throw new Error(`${response.status} ${response.statusText}`);
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

async function refresh() {
  try {
    setEngineState("Syncing");
    const [health, characters, plan] = await Promise.all([
      requestJson("/api/health"),
      requestJson("/api/canon/characters"),
      requestJson("/api/integrations/octopus/plan"),
    ]);
    state.status = health.canon;
    state.characters = characters;
    renderMetrics(health.canon);
    renderCharacters(characters);
    $("#octopus-plan").textContent = plan.content;
    setEngineState("Online", true);
  } catch (error) {
    setEngineState(`Offline: ${error.message}`);
  }
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
  $all(".forge-command").forEach((item) => {
    item.addEventListener("click", () => runCommand(item.dataset.command, item.textContent.trim()));
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
tickClock();
setInterval(tickClock, 30_000);
refresh();
