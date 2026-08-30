const copy = {
  zh: {
    reviewDesk: "正典审核台", logout: "退出", title: "让每一次正典晋升，都能被追溯。",
    subtitle: "每位委员只能操作自己的席位。社区共鸣提供参考，不代替连续性审校与委员会决定。",
    signIn: "委员身份验证", signInBody: "粘贴 ECHO 账号系统签发的委员令牌。令牌只保存在当前浏览器会话中。",
    tokenLabel: "委员令牌", enter: "进入审核台", queue: "我的正典审核队列", refresh: "刷新",
    publicPage: "返回小说连载页", loading: "正在同步当前版本与审核状态…", empty: "当前没有需要审核的候选。",
    invalid: "令牌无效或不具备正典委员权限。", saved: "审核决定已记录。", failed: "操作失败：{message}",
    continuity: "连续性", committee: "委员会", resonance: "社区共鸣", pass: "通过连续性", veto: "连续性否决",
    approve: "同意晋升", reject: "退回修改", reason: "审核说明（建议填写）", pending: "待处理",
    noSeat: "你不是此候选的审核席位。", boundary: "所有决定绑定当前正文与治理规则版本；版本变化后需要重新审核。",
    confirmVeto: "连续性否决必须通过新版本才能解除，确认提交？",
  },
  en: {
    reviewDesk: "Canon Review", logout: "Sign out", title: "Make every canon promotion traceable.",
    subtitle: "Each reviewer controls one seat only. Community resonance informs priority; it never replaces continuity or committee review.",
    signIn: "Reviewer verification", signInBody: "Paste a reviewer token issued by the ECHO account service. It is kept for this browser session only.",
    tokenLabel: "Reviewer token", enter: "Enter review desk", queue: "My canon review queue", refresh: "Refresh",
    publicPage: "Back to serial fiction", loading: "Syncing the current revision and review state…", empty: "No candidates currently require your review.",
    invalid: "This token is invalid or lacks canon reviewer permission.", saved: "Review decision recorded.", failed: "Action failed: {message}",
    continuity: "Continuity", committee: "Committee", resonance: "Resonance", pass: "Pass continuity", veto: "Continuity veto",
    approve: "Approve promotion", reject: "Return for revision", reason: "Review note (recommended)", pending: "Pending",
    noSeat: "You do not hold a review seat for this candidate.", boundary: "Every decision is bound to the current prose and policy revision; any change requires a fresh review.",
    confirmVeto: "A continuity veto can only be cleared by a new revision. Submit it?",
  },
};

let locale = new URLSearchParams(location.search).get("lang") === "en" ? "en" : "zh";
let candidates = [];

const $ = (selector) => document.querySelector(selector);
const text = (key, params = {}) => Object.entries(params).reduce(
  (value, [name, replacement]) => value.replace(`{${name}}`, replacement),
  copy[locale][key] || key,
);

function token() {
  try { return sessionStorage.getItem("echo.reviewer.token") || localStorage.getItem("echo.auth.token") || ""; }
  catch (_) { return ""; }
}

function claims() {
  try {
    const payload = token().split(".")[1];
    const normalized = payload.replace(/-/g, "+").replace(/_/g, "/");
    const binary = atob(normalized.padEnd(Math.ceil(normalized.length / 4) * 4, "="));
    const bytes = Uint8Array.from(binary, (character) => character.charCodeAt(0));
    return JSON.parse(new TextDecoder().decode(bytes));
  } catch (_) { return {}; }
}

function reviewerId() { return String(claims().reviewer_id || ""); }

async function request(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Authorization", `Bearer ${token()}`);
  const response = await fetch(url, { ...options, headers });
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try { message = (await response.json()).detail || message; } catch (_) { /* use status */ }
    throw new Error(message);
  }
  return response.json();
}

function element(tag, className, value) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (value !== undefined) node.textContent = value;
  return node;
}

function metric(value, label) {
  const node = element("div", "metric");
  node.append(element("b", "", value), element("span", "", label));
  return node;
}

function action(label, className, handler, enabled = true) {
  const button = element("button", `action ${className}`, label);
  button.type = "button";
  button.disabled = !enabled;
  button.addEventListener("click", handler);
  return button;
}

async function submitDecision(row, kind, decision, reason) {
  if (kind === "continuity" && decision === "veto" && !confirm(text("confirmVeto"))) return;
  const suffix = kind === "committee" ? "committee-votes" : "continuity-checks";
  const body = kind === "committee"
    ? { decision, expected_revision_sha256: row.candidate.revision_sha256, reason }
    : { verdict: decision, expected_revision_sha256: row.candidate.revision_sha256, reason, issues: decision === "veto" ? ["continuity_review_required"] : [] };
  try {
    await request(`/api/canon/governance/candidates/${row.candidate.id}/${suffix}`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    });
    setNotice(text("saved"));
    await load();
  } catch (error) { setNotice(text("failed", { message: error.message }), true); }
}

function renderCard(row) {
  const card = element("article", "candidate-card");
  const head = element("div", "candidate-head");
  const titleWrap = element("div", "candidate-title");
  const title = row.candidate.title[locale] || row.candidate.title.en;
  titleWrap.append(element("h3", "", title), element("small", "", `${row.candidate.version} · ${row.candidate.revision_sha256.slice(0, 12)}`));
  head.append(titleWrap, element("span", "badge", row.promotion_gate.state));
  card.append(head);

  const metrics = element("div", "metrics");
  metrics.append(
    metric(row.continuity.status, text("continuity")),
    metric(`${row.committee.approvals}/${row.committee.size} · ≥${row.committee.threshold}`, text("committee")),
    metric(`${row.resonance.support} / ${row.resonance.revise}`, text("resonance")),
  );
  card.append(metrics);

  const reason = element("textarea", "review-reason");
  reason.placeholder = text("reason");
  card.append(reason);

  const reviewer = reviewerId();
  const committeeSeat = (row.committee.members || []).some((member) => member.id === reviewer);
  const continuitySeat = (row.continuity.reviewers || []).some((member) => member.id === reviewer);
  const actions = element("div", "actions");
  actions.append(
    action(text("approve"), "approve", () => submitDecision(row, "committee", "approve", reason.value), committeeSeat),
    action(text("reject"), "reject", () => submitDecision(row, "committee", "reject", reason.value), committeeSeat),
    action(text("pass"), "approve", () => submitDecision(row, "continuity", "pass", reason.value), continuitySeat),
    action(text("veto"), "veto", () => submitDecision(row, "continuity", "veto", reason.value), continuitySeat),
  );
  card.append(actions);
  if (!committeeSeat && !continuitySeat) card.append(element("p", "", text("noSeat")));
  card.append(element("div", "boundary", text("boundary")));
  return card;
}

function render() {
  document.documentElement.lang = locale === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-copy]").forEach((node) => { node.textContent = text(node.dataset.copy); });
  $("#lang-toggle").textContent = locale === "zh" ? "EN" : "中文";
  const list = $("#candidate-list");
  list.replaceChildren();
  if (!candidates.length) list.append(element("div", "notice", text("empty")));
  else candidates.forEach((row) => list.append(renderCard(row)));
}

function setNotice(message, isError = false) {
  const notice = $("#notice");
  notice.textContent = message;
  notice.classList.toggle("error", isError);
}

async function load() {
  if (!token()) return showLogin();
  setNotice(text("loading"));
  try {
    candidates = await request("/api/canon/governance/candidates");
    $("#login-card").hidden = true;
    $("#workspace").hidden = false;
    $("#logout").hidden = false;
    $("#reviewer-identity").hidden = false;
    $("#reviewer-identity").textContent = reviewerId();
    $("#login-error").textContent = "";
    setNotice("");
    render();
  } catch (_) { showLogin(text("invalid")); }
}

function showLogin(message = "") {
  $("#login-card").hidden = false;
  $("#workspace").hidden = true;
  $("#logout").hidden = true;
  $("#reviewer-identity").hidden = true;
  $("#login-error").textContent = message;
}

$("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  sessionStorage.setItem("echo.reviewer.token", $("#reviewer-token").value.trim());
  $("#reviewer-token").value = "";
  await load();
});
$("#logout").addEventListener("click", () => { sessionStorage.removeItem("echo.reviewer.token"); candidates = []; showLogin(); });
$("#refresh").addEventListener("click", load);
$("#lang-toggle").addEventListener("click", () => { locale = locale === "zh" ? "en" : "zh"; render(); });

render();
load();
setInterval(() => { if (!document.hidden && token()) load(); }, 30000);
