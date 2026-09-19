(function installEchoConsoleI18n() {
  const messages = {
    zh: {
      pageTitle: "ECHO OS · 宇宙控制台",
      pageDescription: "ECHO OS 宇宙引擎控制台",
      languageSelector: "语言",
      connecting: "连接中",
      whiteGhostNetwork: "白幽灵网络",
      echoRooms: "ECHO 空间",
      worldBrain: "世界大脑",
      characterAgents: "角色智能体",
      universeFactory: "宇宙工厂",
      assetLocks: "资产锁定",
      memoryStream: "记忆流",
      octopusRuntime: "Octopus 运行时",
      layerOne: "第 1 层",
      layerThree: "第 3 层",
      layerFour: "第 4 层",
      refreshCanon: "刷新正典状态",
      refresh: "刷新",
      closeWindow: "关闭窗口",
      neuralCore: "ECHO 神经核心",
      lawNoMagic: "不存在魔法",
      lawDigitalGhosts: "Ghost 是数字人格",
      lawTechnology: "一切能力源于技术",
      lawCanonReview: "正典必须经过审核",
      factory: "工厂",
      universeForge: "宇宙熔炉",
      idle: "空闲",
      dailyLife: "日常生活",
      character: "角色",
      lore: "世界设定",
      story: "故事",
      audit: "审核",
      awaitingSignal: "等待信号。",
      visualCanon: "视觉正典",
      candidate: "候选",
      scheduleCharacter: "角色智能体准备新的灵魂草稿。",
      scheduleLife: "数字生活节拍记录私人记忆。",
      scheduleLore: "设定智能体扩展历史与制度。",
      scheduleStory: "故事智能体将压力转化为章节种子。",
      scheduleAudit: "一致性智能体审核正典风险。",
      runtime: "运行时",
      adapter: "适配器",
      syncAgents: "将智能体同步到 Octopus 运行时",
      sync: "同步",
      loadingRuntime: "正在加载运行时契约。",
      syncing: "正在同步",
      online: "在线",
      offline: "离线：{message}",
      linked: "已连接",
      notLinked: "未连接",
      onlineCount: "{count} 在线",
      lockedCount: "{count} 已锁定",
      unassigned: "未分配",
      noRank: "无等级",
      whiteGhostTeam: "白幽灵小队",
      frontReference: "{name} 正面参考图",
      agentPulse: "智能体脉冲",
      log: "日志",
      queue: "队列",
      noJournalEvents: "暂无日志事件。",
      noCandidates: "日志中暂无待审核的候选内容。",
      awaitingReview: "等待审核。",
      open: "打开",
      canon: "正典",
      accept: "接受",
      reject: "拒绝",
      promote: "晋升为正典",
      publicCanon: "公开候选",
      canonGovernance: "正典治理",
      resonanceSummary: "社区信号：{support} 份共鸣，{revise} 份建议精修。",
      continuityState: "连续性：{status}",
      committeeState: "委员会：{approvals}/{size}（门槛 {threshold}）",
      governanceContinuityPending: "待审校",
      governanceContinuityPassed: "已通过",
      governanceContinuityVetoed: "已阻塞",
      promotionReady: "可晋升",
      promotionLocked: "未解锁",
      promotionBlocked: "已阻塞",
      reviewer: "审核委员",
      approveVote: "投同意票",
      rejectVote: "投反对票",
      continuityPass: "连续性通过",
      continuityVeto: "连续性阻塞",
      confirmContinuityVeto: "这会锁定当前正文版本，只有修改正文后才能重新审校。确认阻塞吗？",
      confirmCanonPromotion: "这会把当前版本写入正式正典档案。确认晋升吗？",
      updatingJournal: "正在更新候选日志……",
      running: "正在运行",
      runningDots: "正在运行……",
      done: "已完成",
      error: "错误",
      octopusSync: "Octopus 同步",
      syncingAgents: "正在同步智能体……",
      metricBible: "设定集",
      metricCharacters: "角色",
      metricFactions: "派系",
      metricLocations: "地点",
      metricTech: "技术",
      metricTimeline: "时间线",
      metricRelations: "关系",
      metricStories: "故事",
      statusPending: "待审核",
      statusAccepted: "已接受",
      statusRejected: "已拒绝",
      statusPromoted: "已晋升",
      modeDailyLife: "日常生活",
      modeCharacter: "角色",
      modeLore: "世界设定",
      modeStory: "故事",
      modeConsistency: "一致性审核",
      linkFront: "正面",
      linkSide: "侧面",
      linkBack: "背面",
      linkAvatar: "头像",
      linkSourceTurnaround: "三视图源图",
    },
    en: {
      pageTitle: "ECHO OS · Universe Console",
      pageDescription: "ECHO OS Universe Engine console",
      languageSelector: "Language",
      connecting: "Connecting",
      whiteGhostNetwork: "White Ghost Network",
      echoRooms: "ECHO rooms",
      worldBrain: "World Brain",
      characterAgents: "Character Agents",
      universeFactory: "Universe Factory",
      assetLocks: "Asset Locks",
      memoryStream: "Memory Stream",
      octopusRuntime: "Octopus Runtime",
      layerOne: "Layer 1",
      layerThree: "Layer 3",
      layerFour: "Layer 4",
      refreshCanon: "Refresh canon state",
      refresh: "Refresh",
      closeWindow: "Close window",
      neuralCore: "ECHO neural core",
      lawNoMagic: "No magic",
      lawDigitalGhosts: "Ghosts are digital personalities",
      lawTechnology: "Every power is technological",
      lawCanonReview: "Canon requires review",
      factory: "Factory",
      universeForge: "Universe Forge",
      idle: "Idle",
      dailyLife: "Daily Life",
      character: "Character",
      lore: "Lore",
      story: "Story",
      audit: "Audit",
      awaitingSignal: "Awaiting signal.",
      visualCanon: "Visual Canon",
      candidate: "Candidate",
      scheduleCharacter: "Character Agent prepares a new soul draft.",
      scheduleLife: "Digital Life tick records private memories.",
      scheduleLore: "Lore Agent expands history and institutions.",
      scheduleStory: "Story Agent turns pressure into chapter seed.",
      scheduleAudit: "Consistency Agent reviews canon risk.",
      runtime: "Runtime",
      adapter: "Adapter",
      syncAgents: "Sync agents into Octopus runtime",
      sync: "Sync",
      loadingRuntime: "Loading runtime contract.",
      syncing: "Syncing",
      online: "Online",
      offline: "Offline: {message}",
      linked: "Linked",
      notLinked: "Not linked",
      onlineCount: "{count} online",
      lockedCount: "{count} locked",
      unassigned: "Unassigned",
      noRank: "No rank",
      whiteGhostTeam: "White Ghost Team",
      frontReference: "{name} front reference",
      agentPulse: "agent pulse",
      log: "log",
      queue: "queue",
      noJournalEvents: "No journal events yet.",
      noCandidates: "No candidate outputs waiting in journal.",
      awaitingReview: "Awaiting review.",
      open: "open",
      canon: "canon",
      accept: "Accept",
      reject: "Reject",
      promote: "Promote",
      publicCanon: "Public candidate",
      canonGovernance: "Canon governance",
      resonanceSummary: "Community signals: {support} resonate, {revise} recommend revision.",
      continuityState: "Continuity: {status}",
      committeeState: "Committee: {approvals}/{size} (threshold {threshold})",
      governanceContinuityPending: "pending",
      governanceContinuityPassed: "passed",
      governanceContinuityVetoed: "blocked",
      promotionReady: "Ready to promote",
      promotionLocked: "Locked",
      promotionBlocked: "Blocked",
      reviewer: "Reviewer",
      approveVote: "Approve",
      rejectVote: "Reject",
      continuityPass: "Pass continuity",
      continuityVeto: "Block continuity",
      confirmContinuityVeto: "This locks the current revision until the prose changes. Block continuity?",
      confirmCanonPromotion: "This writes the current revision into the formal canon archive. Promote it?",
      updatingJournal: "Updating candidate journal...",
      running: "Running",
      runningDots: "Running...",
      done: "Done",
      error: "Error",
      octopusSync: "Octopus Sync",
      syncingAgents: "Syncing agents...",
      metricBible: "Bible",
      metricCharacters: "Characters",
      metricFactions: "Factions",
      metricLocations: "Locations",
      metricTech: "Tech",
      metricTimeline: "Timeline",
      metricRelations: "Relations",
      metricStories: "Stories",
      statusPending: "Pending",
      statusAccepted: "Accepted",
      statusRejected: "Rejected",
      statusPromoted: "Promoted",
      modeDailyLife: "Daily Life",
      modeCharacter: "Character",
      modeLore: "Lore",
      modeStory: "Story",
      modeConsistency: "Consistency Audit",
      linkFront: "front",
      linkSide: "side",
      linkBack: "back",
      linkAvatar: "avatar",
      linkSourceTurnaround: "source turnaround",
    },
  };

  const listeners = new Set();
  let locale = "zh";

  function resolveInitialLocale() {
    const requested = new URLSearchParams(location.search).get("lang")?.toLowerCase();
    if (requested?.startsWith("zh")) return "zh";
    if (requested === "en") return "en";
    try {
      const saved = localStorage.getItem("echo.locale");
      if (saved === "zh" || saved === "en") return saved;
    } catch (_) {
      // Browser language remains a safe fallback when storage is unavailable.
    }
    return navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
  }

  function interpolate(value, params) {
    return Object.entries(params || {}).reduce(
      (result, [key, replacement]) => result.replaceAll(`{${key}}`, String(replacement)),
      value,
    );
  }

  function t(key, params, fallback = key) {
    return interpolate(messages[locale]?.[key] || fallback, params);
  }

  function translateDocument() {
    document.documentElement.lang = locale === "zh" ? "zh-CN" : "en";
    document.documentElement.dataset.locale = locale;
    document.title = t("pageTitle");
    document.querySelector('meta[name="description"]')?.setAttribute("content", t("pageDescription"));
    document.querySelectorAll("[data-i18n]").forEach((element) => {
      const value = messages[locale]?.[element.dataset.i18n];
      if (value !== undefined) element.textContent = value;
    });
    document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
      const value = messages[locale]?.[element.dataset.i18nAria];
      if (value !== undefined) element.setAttribute("aria-label", value);
    });
    document.querySelectorAll("[data-i18n-title]").forEach((element) => {
      const value = messages[locale]?.[element.dataset.i18nTitle];
      if (value !== undefined) element.setAttribute("title", value);
    });
    document.querySelectorAll("[data-locale]").forEach((button) => {
      const active = button.dataset.locale === locale;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", String(active));
    });
  }

  function setLocale(nextLocale, updateUrl = true) {
    locale = nextLocale === "en" ? "en" : "zh";
    translateDocument();
    try {
      localStorage.setItem("echo.locale", locale);
    } catch (_) {
      // The active page still uses the selected locale without persistence.
    }
    if (updateUrl) {
      const url = new URL(location.href);
      url.searchParams.set("lang", locale);
      history.replaceState({ locale }, "", url);
    }
    listeners.forEach((listener) => listener(locale));
  }

  function formatTime(date) {
    return new Intl.DateTimeFormat(locale === "zh" ? "zh-CN" : "en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: locale !== "zh",
    }).format(date);
  }

  function translateStatus(value) {
    const normalized = String(value || "").toLowerCase().replaceAll("-", "_");
    const keys = {
      pending: "statusPending",
      candidate: "statusPending",
      accepted: "statusAccepted",
      rejected: "statusRejected",
      promoted: "statusPromoted",
    };
    return keys[normalized] ? t(keys[normalized]) : value;
  }

  function translateMode(value) {
    const normalized = String(value || "").toLowerCase().replaceAll("-", "_");
    const keys = {
      daily_life: "modeDailyLife",
      character: "modeCharacter",
      lore: "modeLore",
      story: "modeStory",
      consistency: "modeConsistency",
      consistency_audit: "modeConsistency",
    };
    return keys[normalized] ? t(keys[normalized]) : value;
  }

  window.EchoI18n = {
    t,
    setLocale,
    getLocale: () => locale,
    getLocaleTag: () => (locale === "zh" ? "zh-CN" : "en-US"),
    formatTime,
    translateStatus,
    translateMode,
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
  };

  document.querySelectorAll("[data-locale]").forEach((button) => {
    button.addEventListener("click", () => setLocale(button.dataset.locale));
  });
  setLocale(resolveInitialLocale());
})();
