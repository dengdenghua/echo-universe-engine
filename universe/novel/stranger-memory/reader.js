const readerCopy = {
  zh: {
    backCatalog: "小说目录", chapterTitle: "陌生记忆", themeLabel: "纸色", themePaper: "纸色", themeNight: "深色", railStatus: "状态", candidateStatus: "候选精修中", railLocation: "地点", railViewpoint: "视角", railReading: "阅读", fiveMinutes: "约 5 分钟", candidateBanner: "候选试读 · 非最终正典。内容可能在连续性审核后调整。", chapterLogline: "她从未学过外科，却用一个死者留下的双手救活了孩子。", editionLabel: "候选试读版", revisionDate: "依据 2026.08.22 编辑核对", englishNotice: "当前候选试读以中文原文呈现；英文文学版本正在编辑翻译中。", savedAt: "上次读到", resumeReading: "继续上次进度", restartReading: "从头阅读", loadingChapter: "正在打开记忆档案……", loadError: "试读内容暂时无法载入，请稍后重试。", previewEndTitle: "第一道封锁线落下之后，白幽灵小队才会抵达。", previewEndBody: "后续精修将进入白幽灵调查、可撤回的同步同意程序，以及 ECHO 网络中尚未命名的信号。本次停在已经通过设定核对的公开边界。", backDirectory: "返回章节目录", saveSerial: "收藏连载", savedSerial: "已收藏", notCanon: "尚未晋升正典", savedToast: "已收藏在当前设备", removedToast: "已取消收藏", pageTitle: "第一章：陌生记忆 · ECHO NOVEL", pageDescription: "《回响纪元》第一章《陌生记忆》候选试读：她从未学过外科，却用一个死者留下的双手救活了孩子。"
  },
  en: {
    backCatalog: "Novel index", chapterTitle: "Stranger Memory", themeLabel: "Paper", themePaper: "Paper", themeNight: "Night", railStatus: "Status", candidateStatus: "Candidate revision", railLocation: "Location", railViewpoint: "Viewpoint", railReading: "Reading", fiveMinutes: "About 5 minutes", candidateBanner: "Candidate preview · Not final canon. Text may change after continuity review.", chapterLogline: "She never studied surgery, yet saves a child with the hands a dead doctor left behind.", editionLabel: "Candidate preview edition", revisionDate: "Based on the 2026.08.22 editorial review", englishNotice: "This candidate preview is currently presented in its Chinese original. The English literary edition is in editorial translation.", savedAt: "Last position", resumeReading: "Resume", restartReading: "Start over", loadingChapter: "Opening memory archive…", loadError: "The preview could not be loaded. Please try again shortly.", previewEndTitle: "White Ghost Team arrives after the first containment line falls.", previewEndBody: "The revision continues into the White Ghost investigation, a revocable memory-sync consent procedure and an unnamed signal inside ECHO. This preview stops at the boundary already cleared for public reading.", backDirectory: "Back to chapters", saveSerial: "Save serial", savedSerial: "Saved", notCanon: "Not promoted to canon", savedToast: "Saved on this device", removedToast: "Removed from saved", pageTitle: "Chapter 01: Stranger Memory · ECHO NOVEL", pageDescription: "Candidate preview of Stranger Memory, Chapter One of ECHO: Echo Age."
  }
};

const chapterIllustrations = [
  {
    id: "white-harbor",
    anchor: "回响纪元的人把家装进脊柱。",
    src: "/universe/novel/assets/illustration-white-harbor-agnes-v1.png",
    width: 1248,
    height: 832,
    copy: {
      zh: {
        title: "白港晨醒",
        caption: "家园核心逐层点亮，城市把昨日未能记住的事保存下来。",
        alt: "银白晨雾中的白港，高层住宅、垂直交通轨道与蓝紫色家园核心灯光在海岸线上苏醒。"
      },
      en: {
        title: "White Harbor Wakes",
        caption: "Home cores light floor by floor, preserving what the city could not remember yesterday.",
        alt: "White Harbor waking in silver morning fog, with coastal towers, vertical transit rails and blue-violet home-core lights."
      }
    }
  },
  {
    id: "l7-collapse",
    anchor: "亮到每个乘客都能清楚看见城市是如何精确地失败。",
    src: "/universe/novel/assets/illustration-l7-collapse-agnes-v1.png",
    width: 1248,
    height: 832,
    copy: {
      zh: {
        title: "精确地失败",
        caption: "安全系统没有黑屏；它让每个人清楚看见城市如何精确地失败。",
        alt: "L-7 交通车厢坍塌后的内部，应急灯照亮碎裂的白色复合玻璃、变形座椅和奔向受困孩子的林乔。"
      },
      en: {
        title: "A Precise Failure",
        caption: "The safety system never went dark; it made everyone watch the city fail precisely.",
        alt: "Inside the collapsed L-7 carriage, emergency lights reveal shattered white composite glass, twisted seats and Lin Qiao moving toward a trapped child."
      }
    }
  },
  {
    id: "stranger-hands",
    anchor: "三分钟后，男孩活了下来。",
    src: "/universe/novel/assets/illustration-stranger-hands-agnes-v1.png",
    width: 1248,
    height: 832,
    copy: {
      zh: {
        title: "陌生的手",
        caption: "林乔从未学过外科，但她的双手知道如何救下那个孩子。",
        alt: "冷蓝诊断光下，林乔以陌生却精准的动作操作医疗无人机急救组件，身旁的男孩恢复生命体征。"
      },
      en: {
        title: "Stranger Hands",
        caption: "Lin Qiao never studied surgery, yet her hands know how to save the child.",
        alt: "Under cold blue diagnostic light, Lin Qiao handles a medical-drone emergency cartridge with unfamiliar precision as the child stabilizes beside her."
      }
    }
  }
];

const chapterIllustrationById = new Map(chapterIllustrations.map((illustration) => [illustration.id, illustration]));

const progressKey = "echo.novel.stranger-memory.progress";
const followKey = "echo.novel.following";
const sizeKey = "echo.novel.reader.size";
const themeKey = "echo.novel.reader.theme";
let locale = "zh";
let savedProgress = 0;
let fontSize = 19;
let theme = "night";
let chapterLoaded = false;

function preferredLocale() {
  const query = new URLSearchParams(location.search).get("lang");
  if (query === "zh" || query === "en") return query;
  try { const stored = localStorage.getItem("echo.locale"); if (stored === "zh" || stored === "en") return stored; } catch (_) {}
  return navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
}

function getStoredNumber(key, fallback) { try { const value = Number(localStorage.getItem(key)); return Number.isFinite(value) ? value : fallback; } catch (_) { return fallback; } }
function followed() { try { return localStorage.getItem(followKey) === "true"; } catch (_) { return false; } }

function showToast(message) {
  const toast = document.querySelector("#novel-toast"); if (!toast) return;
  toast.textContent = message; toast.classList.add("show"); clearTimeout(showToast.timer); showToast.timer = setTimeout(() => toast.classList.remove("show"), 1800);
}

function syncFollow() {
  const active = followed(); const button = document.querySelector("#reader-follow"); if (!button) return;
  button.classList.toggle("active", active); button.setAttribute("aria-pressed", String(active)); button.querySelector("span").textContent = readerCopy[locale][active ? "savedSerial" : "saveSerial"]; button.querySelector("i").textContent = active ? "✓" : "＋";
}

function applyLocale(next, updateUrl = true) {
  locale = next === "en" ? "en" : "zh"; const copy = readerCopy[locale];
  document.documentElement.lang = locale === "en" ? "en" : "zh-CN";
  document.querySelectorAll("[data-i18n]").forEach((element) => { if (copy[element.dataset.i18n] !== undefined) element.textContent = copy[element.dataset.i18n]; });
  document.querySelectorAll("[data-locale]").forEach((button) => { const active = button.dataset.locale === locale; button.classList.toggle("active", active); button.setAttribute("aria-pressed", String(active)); });
  document.querySelectorAll("[data-catalog-link]").forEach((link) => { const url = new URL(link.href); url.searchParams.set("lang", locale); link.href = `${url.pathname}${url.search}`; });
  document.querySelector("#language-note").hidden = locale !== "en";
  document.title = copy.pageTitle; document.querySelector('meta[name="description"]')?.setAttribute("content", copy.pageDescription); document.querySelector('meta[property="og:title"]')?.setAttribute("content", copy.pageTitle); document.querySelector('meta[property="og:description"]')?.setAttribute("content", copy.pageDescription); document.querySelector('meta[property="og:locale"]')?.setAttribute("content", locale === "en" ? "en_US" : "zh_CN");
  try { localStorage.setItem("echo.locale", locale); } catch (_) {}
  if (updateUrl) { const url = new URL(location.href); url.searchParams.set("lang", locale); history.replaceState({}, "", url); }
  syncFollow(); syncThemeControl(); syncChapterIllustrations();
}

function syncThemeControl() {
  const button = document.querySelector("#theme-toggle"); if (!button) return;
  button.setAttribute("aria-pressed", String(theme === "paper")); button.querySelector("span").textContent = readerCopy[locale][theme === "paper" ? "themeNight" : "themePaper"];
}

function applyReaderPreferences() {
  fontSize = Math.max(17, Math.min(25, getStoredNumber(sizeKey, 19)));
  try { theme = localStorage.getItem(themeKey) === "paper" ? "paper" : "night"; } catch (_) { theme = "night"; }
  document.documentElement.style.setProperty("--reader-size", `${fontSize}px`); document.body.dataset.theme = theme;
  syncThemeControl();
}

function setFontSize(value) { fontSize = Math.max(17, Math.min(25, value)); document.documentElement.style.setProperty("--reader-size", `${fontSize}px`); try { localStorage.setItem(sizeKey, String(fontSize)); } catch (_) {} }

function createChapterIllustration(illustration, index) {
  const figure = document.createElement("figure");
  figure.className = "chapter-illustration";
  figure.dataset.illustration = illustration.id;

  const frame = document.createElement("div");
  frame.className = "chapter-illustration-frame";
  const image = document.createElement("img");
  image.src = illustration.src;
  image.width = illustration.width;
  image.height = illustration.height;
  image.loading = "lazy";
  image.decoding = "async";
  frame.append(image);

  const caption = document.createElement("figcaption");
  const marker = document.createElement("span");
  marker.className = "chapter-illustration-index";
  marker.textContent = `MEMORY PLATE ${String(index + 1).padStart(2, "0")}`;
  const copy = document.createElement("div");
  const title = document.createElement("strong");
  title.dataset.illustrationTitle = "";
  const description = document.createElement("p");
  description.dataset.illustrationCaption = "";
  copy.append(title, description);
  caption.append(marker, copy);
  figure.append(frame, caption);
  return figure;
}

function syncChapterIllustrations() {
  document.querySelectorAll("[data-illustration]").forEach((figure) => {
    const illustration = chapterIllustrationById.get(figure.dataset.illustration);
    if (!illustration) return;
    const copy = illustration.copy[locale];
    const image = figure.querySelector("img");
    if (image) image.alt = copy.alt;
    const title = figure.querySelector("[data-illustration-title]");
    if (title) title.textContent = copy.title;
    const caption = figure.querySelector("[data-illustration-caption]");
    if (caption) caption.textContent = copy.caption;
  });
}

function buildChapter(text) {
  const container = document.querySelector("#chapter-content"); container.replaceChildren();
  text.trim().split(/\n\s*\n/).forEach((block, index) => {
    if (block.trim() === "---") { const divider = document.createElement("div"); divider.className = "memory-divider"; divider.setAttribute("aria-hidden", "true"); divider.innerHTML = "<i></i><b>E</b><i></i>"; container.append(divider); return; }
    const paragraph = document.createElement("p"); paragraph.textContent = block.replace(/\n/g, " ").trim();
    if (index === 0) paragraph.className = "chapter-opening";
    container.append(paragraph);
    chapterIllustrations.forEach((illustration, illustrationIndex) => {
      if (paragraph.textContent.includes(illustration.anchor)) container.append(createChapterIllustration(illustration, illustrationIndex));
    });
  });
  syncChapterIllustrations();
}

async function loadChapter() {
  try { const response = await fetch("/universe/novel/content/stranger-memory.zh.md", { cache: "no-store" }); if (!response.ok) throw new Error(String(response.status)); buildChapter(await response.text()); chapterLoaded = true; requestAnimationFrame(syncProgress); }
  catch (_) { document.querySelector("#chapter-content").innerHTML = `<p class="loading-copy">${readerCopy[locale].loadError}</p>`; }
}

function articleProgress() {
  const article = document.querySelector("#reader-article"); if (!article) return 0;
  const start = article.offsetTop; const distance = Math.max(1, article.scrollHeight - innerHeight * .72); return Math.max(0, Math.min(1, (scrollY - start) / distance));
}

let progressFrame = 0;
function syncProgress() {
  progressFrame = 0; const progress = articleProgress(); document.querySelector("#reading-progress-bar").style.width = `${progress * 100}%`;
  if (chapterLoaded && progress > .01) { try { localStorage.setItem(progressKey, String(progress * 100)); } catch (_) {} }
}

function scrollToProgress(progress) { const article = document.querySelector("#reader-article"); const distance = Math.max(1, article.scrollHeight - innerHeight * .72); scrollTo({ top: article.offsetTop + distance * progress / 100, behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" }); }

savedProgress = Math.max(0, Math.min(100, getStoredNumber(progressKey, 0)));
if (savedProgress > 4 && savedProgress < 96) { const prompt = document.querySelector("#resume-prompt"); prompt.hidden = false; document.querySelector("#resume-percent").textContent = `${Math.round(savedProgress)}%`; }
document.querySelector("#resume-button")?.addEventListener("click", () => { document.querySelector("#resume-prompt").hidden = true; scrollToProgress(savedProgress); });
document.querySelector("#restart-button")?.addEventListener("click", () => { try { localStorage.setItem(progressKey, "0"); } catch (_) {} document.querySelector("#resume-prompt").hidden = true; scrollTo({ top: document.querySelector(".chapter-heading").offsetTop - 80, behavior: "smooth" }); });
document.querySelector("#font-down")?.addEventListener("click", () => setFontSize(fontSize - 1)); document.querySelector("#font-up")?.addEventListener("click", () => setFontSize(fontSize + 1));
document.querySelector("#theme-toggle")?.addEventListener("click", () => { theme = theme === "night" ? "paper" : "night"; document.body.dataset.theme = theme; syncThemeControl(); try { localStorage.setItem(themeKey, theme); } catch (_) {} });
document.querySelector("#reader-follow")?.addEventListener("click", () => { const value = !followed(); try { localStorage.setItem(followKey, String(value)); } catch (_) {} syncFollow(); showToast(readerCopy[locale][value ? "savedToast" : "removedToast"]); });
document.querySelectorAll("[data-locale]").forEach((button) => button.addEventListener("click", () => applyLocale(button.dataset.locale)));
window.addEventListener("scroll", () => { if (!progressFrame) progressFrame = requestAnimationFrame(syncProgress); }, { passive: true }); window.addEventListener("resize", syncProgress, { passive: true });

applyReaderPreferences(); applyLocale(preferredLocale(), false); loadChapter();
