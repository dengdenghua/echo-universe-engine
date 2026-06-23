const state = {
  room: "overview",
  status: null,
  characters: [],
};

const titles = {
  overview: "World Brain Overview",
  characters: "Character Agents",
  factory: "Universe Factory",
  octopus: "Octopus Runtime",
};

function $(selector) {
  return document.querySelector(selector);
}

function truncate(value, size = 220) {
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
  $("#engine-state").textContent = label;
  $(".pulse").classList.toggle("ok", ok);
}

function switchRoom(room) {
  state.room = room;
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.room === room);
  });
  document.querySelectorAll(".room").forEach((item) => {
    item.classList.toggle("active", item.id === `room-${room}`);
  });
  $("#room-title").textContent = titles[room];
}

function renderMetrics(status) {
  const metrics = [
    ["Bible", status.bible_files],
    ["Characters", status.characters],
    ["Factions", status.factions],
    ["Timeline", status.timeline_files],
    ["Locations", status.locations],
    ["Tech", status.technologies],
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
  $("#character-grid").innerHTML = cards
    .map(
      (card) => `
        <article class="character-card">
          <h3>${card.name}</h3>
          <div class="code">${card.codename || card.name} / ${card.faction || "Unknown"}</div>
          <div class="tags">
            <span class="tag">${card.role || "Unassigned"}</span>
            <span class="tag">${card.rank || "No rank"}</span>
            <span class="tag">${card.status}</span>
          </div>
          <p>${truncate(card.description)}</p>
          <div class="tags">
            ${(card.abilities || []).map((ability) => `<span class="tag">${ability}</span>`).join("")}
          </div>
        </article>
      `,
    )
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
  $("#output-mode").textContent = label;
  $("#factory-output").textContent = "Running...";
  try {
    const result = await requestJson(url, { method: "POST" });
    $("#output-mode").textContent = result.mode || "Done";
    $("#factory-output").textContent = result.content || JSON.stringify(result, null, 2);
    await refresh();
  } catch (error) {
    $("#output-mode").textContent = "Error";
    $("#factory-output").textContent = error.message;
  }
}

document.querySelectorAll(".nav-item").forEach((item) => {
  item.addEventListener("click", () => switchRoom(item.dataset.room));
});

document.querySelectorAll(".command").forEach((item) => {
  item.addEventListener("click", () => runCommand(item.dataset.command, item.textContent.trim()));
});

$("#refresh-btn").addEventListener("click", refresh);
$("#daily-life-btn").addEventListener("click", () => {
  switchRoom("factory");
  runCommand("/api/neural/daily-life/run", "Digital Life");
});

refresh();
