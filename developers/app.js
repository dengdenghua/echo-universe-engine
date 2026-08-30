/* 开发者中心。零依赖，与首页同一套 data-i18n 约定。
   与 homepage/app.js 的一点差异：中文文案不再在这里重复一遍，而是页面加载时
   从 DOM 里取初始文本作为 zh 基线，只显式维护 en。这样接口文案改 HTML 一处即可，
   不会出现 HTML 与 translations 对不上的情况。 */

const localeMetadata = {
  zh: {
    lang: "zh-CN",
    title: "ECHO DEVELOPERS · 开发者中心",
    description: "ECHO 宇宙内容接口文档：公开只读端点、三层身份、真实限制与在线试调。",
  },
  en: {
    lang: "en",
    title: "ECHO DEVELOPERS · Content API",
    description: "ECHO universe content API: public read endpoints, three identity tiers, real limits, live playground.",
  },
};

const enCopy = {
  skipToContent: "Skip to content",
  brandHome: "Back to ECHO home",
  devNavigation: "Developer navigation",
  footerNavigation: "Footer navigation",
  languageSelector: "Language",
  backUniverse: "Universe",
  footerHome: "Home",
  navStart: "Quick start",
  navAuth: "Identity",
  navEndpoints: "Endpoints",
  navPlayground: "Playground",
  navLimits: "Limits",
  heroTitle: "Read the universe over HTTP",
  heroLead:
    "Characters, factions, canon status and the economy catalogue are served as plain JSON. No key needed for the public layer, no SDK to install.",
  factEndpoints: "public read endpoints",
  factCharacters: "character files",
  factAuth: "public layer auth",
  factAuthValue: "none",
  startTitle: "One request",
  startBody:
    "Every public response is JSON with no envelope. Start with canon status — it tells you how much of the world has passed continuity review.",
  startNote:
    "Base URL is https://universe.echo-age.com. Running locally, swap in http://127.0.0.1:8010.",
  copy: "Copy",
  authTitle: "Three tiers",
  authBody:
    "Endpoints are split by visibility. Anything past the public layer needs credentials in production; with no credentials configured the service returns 503 rather than quietly falling open.",
  tierPublicName: "Public read",
  tierPublicBody: "World content, canon status, economy products and identity tiers. No credentials.",
  tierUserName: "User",
  tierUserBody: "Bindings, balance and the universe feed. Needs a user JWT, and only reaches your own data.",
  tierAdminName: "Admin",
  tierAdminBody: "Content writes, agent runs, asset generation and governance promotion. Operations only.",
  authWarn:
    "Cross-user access is refused: a valid JWT asking for someone else's user_id still returns 403.",
  endpointsTitle: "Public endpoints",
  endpointsBody:
    "The full list of what the public layer exposes, derived from the server allowlist rather than from what happens to answer today.",
  filterLabel: "Filter",
  tableCaption: "Public read endpoints of the ECHO content API",
  thMethod: "Method",
  thPath: "Path",
  thDesc: "Returns",
  noMatch: "No matching endpoint.",
  playTitle: "Try it",
  playBody:
    "Requests go to this same origin from your browser, so what you see here is exactly what the server returns.",
  playSelectLabel: "Endpoint",
  send: "Send request",
  idle: "Idle",
  playHint: "Pick an endpoint and send — the response shows up here.",
  limitsTitle: "What it actually can't do",
  limitsBody: "This is the current state, not a roadmap. Read it before you build on it.",
  limitCorsName: "No CORS headers",
  limitCorsBody:
    "Cross-origin browser requests are blocked. Third-party frontends need their own server-side proxy, or to wait for a formal opening.",
  limitRateName: "No rate limiting",
  limitRateBody:
    "The public layer is unthrottled, and correspondingly makes no availability promise. Cache and back off on your side; do not treat it as a high-availability source.",
  limitStableName: "Fields are not frozen",
  limitStableBody:
    "The API is unversioned and fields may shift as the content layer evolves. Tolerate unknown fields.",
  limitSdkName: "No SDK",
  limitSdkBody: "There is no official client library. Plain HTTP is enough; responses are ordinary JSON.",
  limitCandidateName: "Candidate content moves",
  limitCandidateBody:
    "Entries with status candidate have not cleared continuity review. Keep the candidate marker when you display them.",
};

/* 端点清单来自 echo_engine/api.py 的 _PUBLIC_EXACT_PATHS 与 _PUBLIC_READ_PATTERNS。
   注意 /api/characters 不在此列：它在本机能返回数据只是因为没配置管理密钥，
   生产环境属于管理层，写进文档会误导调用方。 */
const endpoints = [
  { method: "GET", path: "/api/canon/status", zh: "正典审核进度：已确认、候选与待审条目的数量。", en: "Canon review progress: confirmed, candidate and pending counts." },
  { method: "GET", path: "/api/canon/characters", zh: "已通过连续性审核的角色档案。", en: "Character files that cleared continuity review." },
  { method: "GET", path: "/api/assets/characters", zh: "角色视觉资产索引：立绘、转身图与头像路径。", en: "Character visual asset index: refs, turnarounds, avatars." },
  { method: "GET", path: "/api/realms", zh: "世界层级：记忆海各层的名称与设定。", en: "World layers: the names and premise of each memory-sea layer." },
  { method: "GET", path: "/api/npcs", zh: "可交互角色列表及其所属阵营。", en: "Interactive characters and the factions they belong to." },
  { method: "GET", path: "/api/journal/events", zh: "世界日志事件流：内容层的公开变更记录。", en: "World journal event stream: public content-layer changes." },
  { method: "GET", path: "/api/economy/products", zh: "经济商品目录：定价与可售状态。", en: "Economy catalogue: pricing and availability." },
  { method: "GET", path: "/api/identity/tiers", zh: "身份档位定义与各档权限。", en: "Identity tier definitions and their entitlements." },
  { method: "GET", path: "/api/skins/policies", zh: "外观策略：可用皮肤与适用规则。", en: "Skin policies: available skins and the rules that apply." },
  { method: "GET", path: "/api/health", zh: "健康检查。用于探活，不含业务数据。", en: "Health check. Liveness only, no business data." },
  { method: "GET", path: "/api/canon/candidates/{id}/governance", zh: "单个候选条目的治理状态与审核意见。", en: "Governance state and review notes for one candidate entry." },
  { method: "GET", path: "/openapi.json", zh: "OpenAPI 规范。字段权威来源，以此为准。", en: "OpenAPI schema. The authoritative field reference." },
];

/* HTML 里的初始文本即中文基线，必须在任何一次 applyLocale 之前抓取，
   否则切到英文后就再也取不回中文。 */
const zhCopy = {};
document.querySelectorAll("[data-i18n]").forEach((element) => {
  zhCopy[element.dataset.i18n] = element.textContent;
});
document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
  zhCopy[element.dataset.i18nAria] = element.getAttribute("aria-label") ?? "";
});

const translations = { zh: zhCopy, en: enCopy };
let locale = "zh";

function resolveInitialLocale() {
  const requested = new URLSearchParams(location.search).get("lang")?.toLowerCase();
  if (requested?.startsWith("zh")) return "zh";
  if (requested === "en") return "en";
  try {
    const saved = localStorage.getItem("echo.locale");
    if (saved === "zh" || saved === "en") return saved;
  } catch (_) {
    // 存储不可用时退回浏览器语言，本页仍然可以正常切换。
  }
  return navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
}

function applyLocale(next, updateUrl = true) {
  locale = next === "en" ? "en" : "zh";
  const copy = translations[locale];
  const metadata = localeMetadata[locale];

  document.documentElement.lang = metadata.lang;
  document.documentElement.dataset.locale = locale;
  document.title = metadata.title;
  document.querySelector('meta[name="description"]')?.setAttribute("content", metadata.description);
  document.querySelector('meta[property="og:title"]')?.setAttribute("content", metadata.title);
  document.querySelector('meta[property="og:description"]')?.setAttribute("content", metadata.description);

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const value = copy[element.dataset.i18n];
    if (value !== undefined) element.textContent = value;
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    const value = copy[element.dataset.i18nAria];
    if (value) element.setAttribute("aria-label", value);
  });
  document.querySelectorAll("[data-locale]").forEach((button) => {
    const active = button.dataset.locale === locale;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });

  try {
    localStorage.setItem("echo.locale", locale);
  } catch (_) {
    // 本页仍生效，只是不跨页记忆。
  }
  if (updateUrl) {
    const url = new URL(location.href);
    url.searchParams.set("lang", locale);
    history.replaceState({ locale }, "", url);
  }
  renderEndpoints();
}

document.querySelectorAll("[data-locale]").forEach((button) => {
  button.addEventListener("click", () => applyLocale(button.dataset.locale));
});

const endpointRows = document.getElementById("endpoint-rows");
const endpointEmpty = document.getElementById("endpoint-empty");
const endpointFilter = document.getElementById("endpoint-filter");

function renderEndpoints() {
  if (!endpointRows) return;
  const needle = (endpointFilter?.value ?? "").trim().toLowerCase();
  const matched = endpoints.filter((item) => {
    if (!needle) return true;
    return `${item.path} ${item.zh} ${item.en}`.toLowerCase().includes(needle);
  });

  endpointRows.replaceChildren();
  matched.forEach((item) => {
    const row = document.createElement("tr");

    const method = document.createElement("td");
    const badge = document.createElement("span");
    badge.className = `method method-${item.method.toLowerCase()}`;
    badge.textContent = item.method;
    method.append(badge);

    const path = document.createElement("td");
    path.className = "path";
    path.textContent = item.path;

    const desc = document.createElement("td");
    desc.className = "desc";
    desc.textContent = item[locale];

    row.append(method, path, desc);
    endpointRows.append(row);
  });

  if (endpointEmpty) endpointEmpty.hidden = matched.length > 0;
}

endpointFilter?.addEventListener("input", renderEndpoints);

/* 试调只列可直接 GET 的端点，带路径参数的候选治理接口需要具体 id，放进去只会 404。 */
const playSelect = document.getElementById("play-endpoint");
if (playSelect) {
  endpoints
    .filter((item) => item.method === "GET" && !item.path.includes("{"))
    .forEach((item) => {
      const option = document.createElement("option");
      option.value = item.path;
      option.textContent = item.path;
      playSelect.append(option);
    });
}

const playSend = document.getElementById("play-send");
const playStatus = document.getElementById("play-status");
const playTime = document.getElementById("play-time");
const playOutput = document.getElementById("play-output");

function setOutput(text) {
  if (!playOutput) return;
  const code = playOutput.querySelector("code") ?? playOutput;
  code.textContent = text;
}

playSend?.addEventListener("click", async () => {
  if (!playSelect || !playSelect.value) return;
  playSend.disabled = true;
  if (playStatus) {
    playStatus.className = "result-status";
    playStatus.textContent = locale === "en" ? "Sending…" : "请求中…";
  }
  if (playTime) playTime.textContent = "";

  const started = performance.now();
  try {
    const response = await fetch(playSelect.value, { headers: { Accept: "application/json" } });
    const elapsed = Math.round(performance.now() - started);
    const body = await response.text();
    if (playStatus) {
      playStatus.className = `result-status ${response.ok ? "ok" : "err"}`;
      playStatus.textContent = `${response.status} ${response.statusText}`.trim();
    }
    if (playTime) playTime.textContent = `${elapsed} ms`;
    // 响应不一定是 JSON（503、HTML 错误页都可能），解析失败就原样显示。
    try {
      setOutput(JSON.stringify(JSON.parse(body), null, 2));
    } catch (_) {
      setOutput(body || (locale === "en" ? "(empty body)" : "（空响应）"));
    }
  } catch (error) {
    if (playStatus) {
      playStatus.className = "result-status err";
      playStatus.textContent = locale === "en" ? "Request failed" : "请求失败";
    }
    setOutput(String(error));
  } finally {
    playSend.disabled = false;
  }
});

document.querySelectorAll(".copy-btn").forEach((button) => {
  button.addEventListener("click", async () => {
    const source = document.getElementById(button.dataset.copy);
    if (!source) return;
    const done = () => {
      button.classList.add("copied");
      button.textContent = locale === "en" ? "Copied" : "已复制";
      setTimeout(() => {
        button.classList.remove("copied");
        button.textContent = translations[locale].copy ?? "复制";
      }, 1600);
    };
    try {
      await navigator.clipboard.writeText(source.textContent.trim());
      done();
    } catch (_) {
      // 非安全上下文或用户拒权时剪贴板不可用，退回选中让用户自己复制。
      const range = document.createRange();
      range.selectNodeContents(source);
      const selection = getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);
    }
  });
});

/* 首屏两个计数直接问接口，问不到就留破折号，不编数字。 */
async function loadFacts() {
  const endpointCount = document.getElementById("fact-endpoints");
  if (endpointCount) endpointCount.textContent = String(endpoints.length);
  const characterCount = document.getElementById("fact-characters");
  if (!characterCount) return;
  try {
    const response = await fetch("/api/canon/characters", { headers: { Accept: "application/json" } });
    if (!response.ok) return;
    const data = await response.json();
    const list = Array.isArray(data) ? data : data.characters ?? data.items ?? [];
    if (Array.isArray(list) && list.length) characterCount.textContent = String(list.length);
  } catch (_) {
    // 保留破折号。
  }
}

const devHeader = document.querySelector(".dev-header");
const navLinks = Array.from(document.querySelectorAll('.dev-nav a[href^="#"]'));
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

let scrollQueued = false;
function onScroll() {
  if (scrollQueued) return;
  scrollQueued = true;
  requestAnimationFrame(() => {
    scrollQueued = false;
    devHeader?.classList.toggle("is-scrolled", scrollY > 24);
    const probe = scrollY + innerHeight * 0.34;
    let activeIndex = -1;
    sections.forEach((section, index) => {
      if (section.offsetTop <= probe) activeIndex = index;
    });
    navLinks.forEach((link, index) => link.classList.toggle("active", index === activeIndex));
  });
}

addEventListener("scroll", onScroll, { passive: true });
applyLocale(resolveInitialLocale(), false);
loadFacts();
onScroll();

