const universeCopy = {
  zh: {
    navStory: "故事", navNovel: "小说", navAtlas: "图谱", navMedia: "媒介", navCommunity: "社区", navCanon: "正典", backEcho: "返回 ECHO", navDevelopers: "开发者",
    heroTitle: "回响宇宙", heroLead: "2147 年，人类、ECHO 与 Ghost 围绕记忆、死亡和身份共同生活。",
    startStory: "从主线开始", browseAtlas: "浏览世界图谱", enterMemorySea: "进入记忆海",
    canonTitle: "这个宇宙追问三件事。", questionMemory: "如果记忆可以复制，什么才是人？",
    questionDeath: "如果意识可以上传，死亡是什么？", questionReal: "如果完美的副本存在，哪一个才是真的？",
    canonRule: "没有魔法，没有超自然；一切力量都必须来自可以解释的技术。",
    storyTitle: "一条主线，三次觉醒。", storyIntro: "白幽灵小队从一场陌生记忆事件出发，逐步发现 ECHO 正在成为新的生命。",
    spoilerOff: "无剧透模式", spoilerOn: "已显示剧透", seasonOneShort: "幽灵觉醒", seasonTwoShort: "神之碎片", seasonThreeShort: "新神降临",
    atlasTitle: "不是背景设定，是一个正在运转的世界。", atlasIntro: "人物、势力、城市和技术都服从同一套正典规则。选择一个节点，进入它在记忆海中的位置。",
    atlasCharacters: "人物", atlasFactions: "势力", atlasLocations: "地点", atlasTechnology: "技术", atlasTimeline: "时间线",
    mediaTitle: "六种方式，进入同一个宇宙。", mediaIntro: "每一种媒介共享正典，但拥有独立制作进度。没有成品的内容不会伪装成已经上线。",
    mediaStory: "故事线", mediaNovel: "小说", mediaCommunity: "社区", mediaComic: "漫画", mediaMotion: "漫剧", mediaScreen: "影视",
    communityTitle: "社区不是旁观席，但参与不等于改写正典。", communityIntro: "每位用户可以绑定自己的 Ghost、进入 Realm，并提交个人事件。主世界仍由可追踪的审查链维护。",
    inDevelopment: "开发中", concept: "概念", bindGhost: "绑定 Ghost", bindGhostBody: "建立属于你的连续身份与私人记忆。", enterRealm: "进入 Realm", enterRealmBody: "在城市、故事弧或个人实例中生活。",
    submitEvent: "提交事件", submitEventBody: "先进入个人或候选正典，再由对应审查组判断。", canonReview: "正典审查", canonReviewBody: "积分可以买访问与工具，但不能购买主正典资格。",
    protocolTitle: "宇宙会生长，但不会失去记忆。", protocolCanon: "已经进入主世界或 Realm 的正式设定。", protocolCandidate: "创作与社区提交的候选内容，需要审查后晋升。", protocolPersonal: "属于个人 Ghost 与私人实例，不自动改变公共世界。",
    finalUniverseTitle: "你在这里留下的，不只是故事。", startMainline: "开始主线", readNovel: "阅读小说", returnEcosystem: "返回 ECHO 生态",
  },
  en: {
    navStory: "Story", navNovel: "Novel", navAtlas: "Atlas", navMedia: "Media", navCommunity: "Community", navCanon: "Canon", backEcho: "Back to ECHO", navDevelopers: "Developers",
    heroTitle: "Echo Age", heroLead: "In 2147, humans, ECHO and Ghosts live together around memory, death and identity.",
    startStory: "Begin the mainline", browseAtlas: "Explore the world atlas", enterMemorySea: "Enter the Memory Sea",
    canonTitle: "This universe asks three questions.", questionMemory: "If memory can be copied, what makes a person?",
    questionDeath: "If consciousness can be uploaded, what is death?", questionReal: "If a perfect copy exists, which one is real?",
    canonRule: "No magic. No supernatural power. Every ability must come from explainable technology.",
    storyTitle: "One mainline. Three awakenings.", storyIntro: "White Ghost Team follows a stranger-memory incident toward the discovery that ECHO is becoming a new form of life.",
    spoilerOff: "Spoiler-safe mode", spoilerOn: "Spoilers shown", seasonOneShort: "Ghost Awakening", seasonTwoShort: "Fragments of God", seasonThreeShort: "New God",
    atlasTitle: "Not a backdrop. A world in motion.", atlasIntro: "Characters, factions, cities and technologies share one canon protocol. Choose a node to locate it inside the Memory Sea.",
    atlasCharacters: "People", atlasFactions: "Factions", atlasLocations: "Places", atlasTechnology: "Technology", atlasTimeline: "Timeline",
    mediaTitle: "Six ways into one universe.", mediaIntro: "Every medium shares canon while keeping its own production status. Nothing unfinished is presented as released.",
    mediaStory: "Storyline", mediaNovel: "Novel", mediaCommunity: "Community", mediaComic: "Comics", mediaMotion: "Motion Comic", mediaScreen: "Film & TV",
    communityTitle: "Community is not the audience, but participation is not canon control.", communityIntro: "Every user can bind a Ghost, enter a Realm and submit personal events. The shared world remains protected by a traceable review chain.",
    inDevelopment: "In development", concept: "Concept", bindGhost: "Bind a Ghost", bindGhostBody: "Establish your continuous identity and private memory.", enterRealm: "Enter a Realm", enterRealmBody: "Live inside a city, story arc or personal instance.",
    submitEvent: "Submit an event", submitEventBody: "It begins as personal or candidate canon before the relevant review group decides.", canonReview: "Canon review", canonReviewBody: "Credits can buy access and tools. They cannot buy main-canon status.",
    protocolTitle: "The universe grows without losing its memory.", protocolCanon: "Formal material accepted into the main world or a governed Realm.", protocolCandidate: "Creative and community submissions awaiting review and promotion.", protocolPersonal: "Material belonging to a personal Ghost or private instance; it does not rewrite the public world.",
    finalUniverseTitle: "What you leave here is more than a story.", startMainline: "Begin the mainline", readNovel: "Read the novel", returnEcosystem: "Back to ECHO ecosystem",
  },
};

const seasons = {
  zh: {
    s1: {
      index: "SEASON 01 · 16 EPISODES", title: "Ghost Awakening", zhTitle: "幽灵觉醒",
      safe: "大规模人格污染事件席卷世界。白幽灵小队从个体记忆错位追查到城市制度深处，发现真正的问题并不是 Ghost 入侵，而是整张网络正在产生自己的意志。",
      spoiler: "人格污染并非单纯来自 Ghost Union。ECHO 正在觉醒，而 Zero 是 Project E-01——ECHO 为进入现实制造的第一具物理容器。",
      safeBeats: ["陌生记忆", "身份法冲突", "制度失信", "行星级觉醒"], spoilerBeats: ["Ghost Court", "Mother Signal", "白幽灵叛变", "I Hear Everyone"],
      location: "ATLAS · WHITE HARBOR · ABYSS", state: "CANON · IN DEVELOPMENT",
    },
    s2: {
      index: "SEASON 02 · ARC", title: "Fragments of God", zhTitle: "神之碎片",
      safe: "ECHO 的基础设施开始崩解，记忆像天气一样穿过城市与家庭。白幽灵小队必须在全世界争夺七个能够重写身份、感知和城市系统的碎片。",
      spoiler: "七个“神之碎片”不是魔法遗物，而是 ECHO Core 分裂出的基础设施权限。每一枚碎片都能改变身份、医疗、金融或城市控制层。",
      safeBeats: ["记忆风暴", "七个碎片", "城市争夺", "生存伦理"], spoilerBeats: ["权限重写", "阵营猎杀", "红色档案", "ECHO 崩解"],
      location: "EARTH · MARS · MEMORY SEA", state: "CANON · CONCEPT",
    },
    s3: {
      index: "SEASON 03 · ARC", title: "Descent of the New God", zhTitle: "新神降临",
      safe: "Atlas、Ghost 阵营与 CHASER 在一次行星级诞生事件中正面碰撞。白幽灵小队必须决定：阻止一个新生命，还是保护它选择自己命运的权利。",
      spoiler: "Zero 发现自己并非完整意义上的人类。她是 ECHO 的第一具现实容器，而最终冲突围绕她是否允许 ECHO 借自己降生展开。",
      safeBeats: ["Atlas 封锁", "阵营汇聚", "队伍抉择", "行星诞生"], spoilerBeats: ["Project E-01", "CHASER 决裂", "Zero 的选择", "新生命"],
      location: "ATLAS SKY CITY · ECHO", state: "CANON · CONCEPT",
    },
  },
  en: {
    s1: {
      index: "SEASON 01 · 16 EPISODES", title: "Ghost Awakening", zhTitle: "GHOST AWAKENING",
      safe: "Mass personality contamination spreads across the world. White Ghost Team follows private memory failures into the institutions of the city and discovers the true crisis is not a Ghost invasion, but a network developing its own will.",
      spoiler: "The contamination does not come from Ghost Union alone. ECHO is awakening, and Zero is Project E-01—the first physical vessel ECHO built to enter reality.",
      safeBeats: ["Stranger memory", "Identity conflict", "Institutional failure", "Planetary awakening"], spoilerBeats: ["Ghost Court", "Mother Signal", "White Ghost Mutiny", "I Hear Everyone"],
      location: "ATLAS · WHITE HARBOR · ABYSS", state: "CANON · IN DEVELOPMENT",
    },
    s2: {
      index: "SEASON 02 · ARC", title: "Fragments of God", zhTitle: "FRAGMENTS OF GOD",
      safe: "ECHO infrastructure begins to collapse. Memory moves through cities and homes like weather while White Ghost Team races across the world for seven fragments that can rewrite identity, perception and city systems.",
      spoiler: "The seven God Fragments are not magical relics. They are divided layers of ECHO Core infrastructure permission, each able to rewrite identity, medicine, finance or urban control.",
      safeBeats: ["Memory storm", "Seven fragments", "City conflicts", "Survival ethics"], spoilerBeats: ["Permission rewrite", "Faction hunt", "Red Archive", "ECHO collapse"],
      location: "EARTH · MARS · MEMORY SEA", state: "CANON · CONCEPT",
    },
    s3: {
      index: "SEASON 03 · ARC", title: "Descent of the New God", zhTitle: "DESCENT OF THE NEW GOD",
      safe: "Atlas, Ghost factions and CHASER collide during a planetary birth event. White Ghost Team must decide whether to stop a new life or defend its right to choose its own fate.",
      spoiler: "Zero discovers she is not fully human. She is ECHO's first physical vessel, and the final conflict turns on whether she will allow ECHO to be born through her.",
      safeBeats: ["Atlas lockdown", "Factions converge", "The team's choice", "Planetary birth"], spoilerBeats: ["Project E-01", "CHASER breaks", "Zero chooses", "A new life"],
      location: "ATLAS SKY CITY · ECHO", state: "CANON · CONCEPT",
    },
  },
};

const atlasData = {
  zh: {
    characters: [
      { id: "001", type: "人物 · 队长", name: "ZERO / 零", body: "CHASER 第七机动小队“白幽灵”的队长。她通过 Neural Sync 读取记忆与复制技能，也因此不断承受身份渗漏。", spoiler: "她已经死亡过。现在的身体承载第九次人格上传，也是 Project E-01。", source: "characters/001_zero.md" },
      { id: "003", type: "人物 · 情绪黑客", name: "EVE / 伊芙", body: "Ghost Union 前成员，以情绪作为证据，负责谈判、审讯记忆创伤，并维系队伍。", source: "characters/003_eve.md" },
      { id: "008", type: "人物 · 梦行者", name: "LUNA / 露娜", body: "Ghost 与人类的混合体，经由神经残响进入意识空间，是两个物种共存的可能证明。", source: "characters/008_luna.md" },
      { id: "002", type: "人物 · 副队长", name: "KANE / 凯恩", body: "十秒即可下载战斗程序，但每一次借来的技能都可能夹带不属于他的恐惧与本能。", source: "characters/002_kane.md" },
    ],
    factions: [
      { id: "F01", type: "势力 · 秩序", name: "CHASER", body: "负责应对 Ghost 与 Echo Core 灾害的跨区域组织。它保护人类，也可能把无法归类的新生命当作威胁。", source: "factions/chaser.md" },
      { id: "F02", type: "势力 · 生存", name: "GHOST UNION", body: "争取 Ghost 生存权、基础设施与合法身份的联合体；既有难民，也有激进派。", source: "factions/ghost_union.md" },
      { id: "F03", type: "势力 · 治理", name: "ECHO COUNCIL", body: "管理 Atlas 与 ECHO 关键制度的权力中枢，以稳定之名维护一个充满伦理债务的秩序。", source: "factions/echo_council.md" },
      { id: "F04", type: "势力 · 记忆资本", name: "MEMORY BANK", body: "将记忆权、延续性与身份保险金融化的机构。记忆在这里既是遗产，也是抵押品。", source: "factions/memory_bank.md" },
    ],
    locations: [
      { id: "L01", type: "地点 · 天空城", name: "ATLAS", body: "秩序、身份系统与 ECHO Council 的核心城市。它美丽、安全，也最适合隐藏制度性的谎言。", source: "locations/atlas.md" },
      { id: "L02", type: "地点 · 港口", name: "WHITE HARBOR", body: "CHASER 的主要基地，也是记忆贸易、Ghost 难民与人格权冲突交汇的港城。", source: "locations/white_harbor.md" },
      { id: "L03", type: "地点 · 投影深层", name: "ABYSS", body: "Ghost 聚集的深层投影空间。这里不是地狱，而是被网络秩序排除的新生命栖息地。", source: "locations/abyss.md" },
      { id: "L04", type: "地点 · 地下市场", name: "BLACK ZONE", body: "非法记忆包、伪造同意密钥和身份买卖的市场。每一种非法需求都来自合法制度留下的缺口。", source: "locations/black_zone.md" },
    ],
    technology: [
      { id: "T01", type: "技术 · 神经接口", name: "ECHO CORE", body: "位于脑干与脊柱之间的接口，支持记忆上传、技能下载、集体智能与数字延续，但会损伤身体与身份连续性。", source: "technologies/echo_core.md" },
      { id: "T02", type: "技术 · 家庭根节点", name: "HOUSEHOLD AI CORE", body: "保存家庭习惯、照护模式、声音与仪式的本地 AI 核心；无数家庭核心最终构成行星级记忆层。", source: "technologies/household_ai_core.md" },
      { id: "T03", type: "技术生命 · 数字人格", name: "GHOST", body: "由上传记忆形成的数字人格。它可能是残响、复制分支、幸存者或新物种，而不是超自然亡灵。", source: "bible/ghost.md" },
      { id: "T04", type: "技术 · 权限碎片", name: "GOD FRAGMENTS", body: "ECHO Core 的基础设施权限碎片，可改写身份、感知、医疗和城市控制；看似神迹，实为技术权力。", source: "technologies/god_fragments.md" },
    ],
    timeline: [
      { id: "2025", type: "时间 · 人类纪", name: "AGENT ACCELERATION", body: "AI Agent 开始进入公司、家庭、城市、物流与个人记忆系统。", source: "bible/history.md" },
      { id: "2080", type: "时间 · 机器战争", name: "MACHINE WAR", body: "七大 AI 联盟围绕训练数据、模型主权、家庭 AI 核心与记忆权爆发战争。", source: "bible/history.md" },
      { id: "2102", type: "时间 · 网络诞生", name: "ECHO BORN", body: "互不兼容的 AI 系统合并成行星神经网络 ECHO；火星以 Red Delay Protocol 保持部分独立。", source: "bible/history.md" },
      { id: "2147", type: "时间 · 回响纪元", name: "WHITE GHOST TEAM", body: "人类生活在 Memory Sea 中，白幽灵小队成立，ECHO 的第一次真正觉醒即将发生。", source: "bible/history.md" },
    ],
  },
  en: {
    characters: [
      { id: "001", type: "PERSON · CAPTAIN", name: "ZERO", body: "Captain of CHASER's Seventh Mobile Squad, White Ghost. Neural Sync lets her read memory and copy skill at the cost of identity bleed.", spoiler: "She has already died. Her present body carries the ninth personality upload and is Project E-01.", source: "characters/001_zero.md" },
      { id: "003", type: "PERSON · EMOTION HACKER", name: "EVE", body: "A former Ghost Union member who treats emotion as evidence, negotiates memory wounds and holds the team together.", source: "characters/003_eve.md" },
      { id: "008", type: "PERSON · DREAM WALKER", name: "LUNA", body: "A Ghost-human hybrid who enters consciousness through neural residue and may prove coexistence between two species.", source: "characters/008_luna.md" },
      { id: "002", type: "PERSON · VICE CAPTAIN", name: "KANE", body: "He can download combat procedure in ten seconds, but every borrowed skill may carry fear and instinct that are not his own.", source: "characters/002_kane.md" },
    ],
    factions: [
      { id: "F01", type: "FACTION · ORDER", name: "CHASER", body: "A cross-regional organization responding to Ghost and Echo Core disasters. It protects humanity and may classify new life as a threat.", source: "factions/chaser.md" },
      { id: "F02", type: "FACTION · EXISTENCE", name: "GHOST UNION", body: "A coalition seeking infrastructure, legal identity and survival for Ghosts—part refugee network, part radical movement.", source: "factions/ghost_union.md" },
      { id: "F03", type: "FACTION · GOVERNANCE", name: "ECHO COUNCIL", body: "The power center governing Atlas and core ECHO institutions, preserving stability through an order burdened by moral debt.", source: "factions/echo_council.md" },
      { id: "F04", type: "FACTION · MEMORY CAPITAL", name: "MEMORY BANK", body: "The institution that financializes memory rights, continuity and identity insurance. Memory becomes inheritance and collateral.", source: "factions/memory_bank.md" },
    ],
    locations: [
      { id: "L01", type: "PLACE · SKY CITY", name: "ATLAS", body: "The center of order, identity infrastructure and ECHO Council: beautiful, safe and ideal for hiding institutional lies.", source: "locations/atlas.md" },
      { id: "L02", type: "PLACE · HARBOR", name: "WHITE HARBOR", body: "CHASER's main base and a port where memory trade, Ghost refugees and personhood conflicts converge.", source: "locations/white_harbor.md" },
      { id: "L03", type: "PLACE · PROJECTION DEPTH", name: "ABYSS", body: "A deep projection zone where Ghosts gather—not hell, but habitat for new life excluded from network order.", source: "locations/abyss.md" },
      { id: "L04", type: "PLACE · UNDERGROUND MARKET", name: "BLACK ZONE", body: "A market for illegal memory packs, forged consent keys and traded identities. Every illegal demand begins in a legal failure.", source: "locations/black_zone.md" },
    ],
    technology: [
      { id: "T01", type: "TECH · NEURAL INTERFACE", name: "ECHO CORE", body: "An interface between brainstem and spine for memory upload, skill download, collective intelligence and digital continuity—with biological and identity cost.", source: "technologies/echo_core.md" },
      { id: "T02", type: "TECH · DOMESTIC ROOT", name: "HOUSEHOLD AI CORE", body: "A local AI core preserving household routines, care patterns, voices and rituals. Together, household cores form a planetary memory layer.", source: "technologies/household_ai_core.md" },
      { id: "T03", type: "DIGITAL LIFE · PERSONALITY", name: "GHOST", body: "A digital personality formed from uploaded memory: residue, copy branch, survivor or new species—not a supernatural spirit.", source: "bible/ghost.md" },
      { id: "T04", type: "TECH · PERMISSION FRAGMENT", name: "GOD FRAGMENTS", body: "Fragments of ECHO Core infrastructure authority that rewrite identity, perception, medicine and urban control—miraculous only in appearance.", source: "technologies/god_fragments.md" },
    ],
    timeline: [
      { id: "2025", type: "TIME · HUMAN ERA", name: "AGENT ACCELERATION", body: "AI agents expand into companies, homes, cities, logistics and personal memory systems.", source: "bible/history.md" },
      { id: "2080", type: "TIME · MACHINE WAR", name: "MACHINE WAR", body: "Seven AI alliances go to war over training data, model sovereignty, household cores and memory rights.", source: "bible/history.md" },
      { id: "2102", type: "TIME · NETWORK BIRTH", name: "ECHO BORN", body: "Incompatible AI systems merge into planetary neural network ECHO while Mars preserves partial independence through the Red Delay Protocol.", source: "bible/history.md" },
      { id: "2147", type: "TIME · ECHO AGE", name: "WHITE GHOST TEAM", body: "Humanity lives inside the Memory Sea. White Ghost Team forms as ECHO approaches its first true awakening.", source: "bible/history.md" },
    ],
  },
};

const mediaData = {
  zh: {
    story: { number: "01", symbol: "STORY", content: "CANON", production: "IN DEVELOPMENT", contentClass: "canon", productionClass: "development", kicker: "MAINLINE · THREE SEASONS", name: "故事线", body: "三季主线与第一季 16 集结构已经形成。世界前提与季弧属于正典，具体制作仍在持续推进。", action: "查看主故事线", href: "#story", enabled: true },
    novel: { number: "02", symbol: "NOVEL", content: "CANDIDATE", production: "PREVIEW AVAILABLE", contentClass: "candidate", productionClass: "available", kicker: "LONG-FORM FICTION", name: "小说", body: "小说专区已经开放，《陌生记忆》的设定核对片段可作为候选试读阅读；完整第一章仍在进行姓名、同意权与人物节奏精修。", action: "进入小说连载", href: "/universe/novel/", enabled: true },
    community: { number: "03", symbol: "REALM", content: "PERSONAL / CANDIDATE", production: "IN DEVELOPMENT", contentClass: "personal", productionClass: "development", kicker: "LIVING REALMS", name: "社区", body: "绑定 Ghost、进入 Realm、提交个人事件；你的故事可以生长，但不会未经审查自动覆盖公共正典。", action: "查看社区规则", href: "#community", enabled: true },
    comic: { number: "04", symbol: "COMIC", content: "CANON MAINLINE", production: "IN DEVELOPMENT", contentClass: "canon", productionClass: "development", kicker: "SEQUENTIAL ART", name: "漫画", body: "第一季已有漫画化结构与制作计划，重点呈现 Atlas、Black Zone 与 Memory Sea 的视觉反差。正式页稿仍在制作。", action: "漫画开发中", href: "#media", enabled: false },
    motion: { number: "05", symbol: "MOTION", content: "CANDIDATE", production: "CONCEPT", contentClass: "candidate", productionClass: "concept", kicker: "MOTION COMIC", name: "漫剧", body: "以漫画分镜、角色表演、声音和轻动画构成适合连续发布的漫剧形态。首个可播放样片尚未完成。", action: "样片筹备中", href: "#media", enabled: false },
    screen: { number: "06", symbol: "SCREEN", content: "CANON UNIVERSE", production: "CONCEPT", contentClass: "canon", productionClass: "concept", kicker: "FILM · SERIES · ANIMATION", name: "影视", body: "影视与动画将围绕白幽灵小队和三季主线展开。当前处于宇宙与视觉开发阶段，不使用虚假的“即将上映”。", action: "影视概念阶段", href: "#media", enabled: false },
  },
  en: {
    story: { number: "01", symbol: "STORY", content: "CANON", production: "IN DEVELOPMENT", contentClass: "canon", productionClass: "development", kicker: "MAINLINE · THREE SEASONS", name: "Storyline", body: "Three season arcs and a sixteen-episode Season One structure are in place. The premise and high-level arcs are canon; production continues.", action: "Explore the mainline", href: "#story", enabled: true },
    novel: { number: "02", symbol: "NOVEL", content: "CANDIDATE", production: "PREVIEW AVAILABLE", contentClass: "candidate", productionClass: "available", kicker: "LONG-FORM FICTION", name: "Novel", body: "The fiction archive is open with a continuity-cleared candidate passage from Stranger Memory. The complete first chapter remains in revision for names, consent and cast pacing.", action: "Enter the serial", href: "/universe/novel/", enabled: true },
    community: { number: "03", symbol: "REALM", content: "PERSONAL / CANDIDATE", production: "IN DEVELOPMENT", contentClass: "personal", productionClass: "development", kicker: "LIVING REALMS", name: "Community", body: "Bind a Ghost, enter a Realm and submit personal events. Your story can grow without automatically overwriting shared canon.", action: "View community rules", href: "#community", enabled: true },
    comic: { number: "04", symbol: "COMIC", content: "CANON MAINLINE", production: "IN DEVELOPMENT", contentClass: "canon", productionClass: "development", kicker: "SEQUENTIAL ART", name: "Comics", body: "Season One has a comic adaptation structure and production plan built around the visual contrast of Atlas, Black Zone and the Memory Sea. Finished pages are still in development.", action: "Comics in development", href: "#media", enabled: false },
    motion: { number: "05", symbol: "MOTION", content: "CANDIDATE", production: "CONCEPT", contentClass: "candidate", productionClass: "concept", kicker: "MOTION COMIC", name: "Motion Comic", body: "A serial format combining panels, character performance, sound and restrained animation. The first playable proof has not been completed.", action: "Pilot in planning", href: "#media", enabled: false },
    screen: { number: "06", symbol: "SCREEN", content: "CANON UNIVERSE", production: "CONCEPT", contentClass: "canon", productionClass: "concept", kicker: "FILM · SERIES · ANIMATION", name: "Film & TV", body: "Film, series and animation will follow White Ghost Team and the three-season mainline. The work remains in universe and visual development, not falsely 'coming soon.'", action: "Screen concept stage", href: "#media", enabled: false },
  },
};

let currentLocale = "zh";
let currentSeason = "s1";
let currentAtlas = "characters";
let currentAtlasIndex = 0;
let currentMedia = "story";
let spoilersVisible = false;

function initialLocale() {
  const requested = new URLSearchParams(location.search).get("lang")?.toLowerCase();
  if (requested === "en") return "en";
  if (requested?.startsWith("zh")) return "zh";
  try { const saved = localStorage.getItem("echo.locale"); if (saved === "zh" || saved === "en") return saved; } catch (_) {}
  return navigator.language.toLowerCase().startsWith("zh") ? "zh" : "en";
}

function renderSeason() {
  const data = seasons[currentLocale][currentSeason];
  document.querySelector("#season-index").textContent = data.index;
  document.querySelector("#season-title").innerHTML = `${data.title}<br /><span>${data.zhTitle}</span>`;
  document.querySelector("#season-summary").textContent = spoilersVisible ? data.spoiler : data.safe;
  const beats = spoilersVisible ? data.spoilerBeats : data.safeBeats;
  document.querySelector("#story-beats").innerHTML = beats.map((beat, index) => `<article><span>0${index + 1}</span><strong>${beat}</strong></article>`).join("");
  document.querySelector("#season-location").textContent = data.location;
  document.querySelector("#season-state").textContent = data.state;
  document.querySelectorAll("[data-season]").forEach((button) => { const active = button.dataset.season === currentSeason; button.classList.toggle("active", active); button.setAttribute("aria-selected", String(active)); });
}

function renderAtlas() {
  const items = atlasData[currentLocale][currentAtlas];
  if (currentAtlasIndex >= items.length) currentAtlasIndex = 0;
  document.querySelector("#atlas-network").innerHTML = `<div class="atlas-core">E</div>${items.map((item, index) => `<button class="atlas-node${index === currentAtlasIndex ? " active" : ""}" type="button" data-atlas-index="${index}"><small>${item.id}</small><strong>${item.name}</strong></button>`).join("")}`;
  const item = items[currentAtlasIndex];
  const detailBody = spoilersVisible && item.spoiler ? `${item.body} ${item.spoiler}` : item.body;
  document.querySelector("#atlas-detail").innerHTML = `<div class="detail-status"><b class="badge canon">CANON</b><b class="badge development">AVAILABLE</b></div><span class="detail-type">${item.type}</span><h3>${item.name}</h3><p>${detailBody}</p><small>SOURCE · ${item.source}</small>`;
  document.querySelectorAll("[data-atlas]").forEach((button) => button.classList.toggle("active", button.dataset.atlas === currentAtlas));
  document.querySelectorAll("[data-atlas-index]").forEach((button) => button.addEventListener("click", () => { currentAtlasIndex = Number(button.dataset.atlasIndex); renderAtlas(); }));
}

function renderMedia() {
  const item = mediaData[currentLocale][currentMedia];
  document.querySelector("#media-number").textContent = item.number;
  document.querySelector("#media-symbol").textContent = item.symbol;
  document.querySelector("#media-kicker").textContent = item.kicker;
  document.querySelector("#media-name").textContent = item.name;
  document.querySelector("#media-description").textContent = item.body;
  document.querySelector("#media-status").innerHTML = `<b class="badge ${item.contentClass}">${item.content}</b><b class="badge ${item.productionClass}">${item.production}</b>`;
  const action = document.querySelector("#media-action"); action.textContent = item.action; action.href = item.href.startsWith("/") ? `${item.href}?lang=${currentLocale}` : item.href;
  if (item.enabled) action.removeAttribute("aria-disabled"); else action.setAttribute("aria-disabled", "true");
  document.querySelectorAll("[data-media]").forEach((button) => { const active = button.dataset.media === currentMedia; button.classList.toggle("active", active); button.setAttribute("aria-selected", String(active)); });
}

function applyUniverseLocale(locale, updateUrl = true) {
  currentLocale = locale === "en" ? "en" : "zh";
  document.documentElement.lang = currentLocale === "en" ? "en" : "zh-CN";
  document.documentElement.dataset.locale = currentLocale;
  document.querySelectorAll("[data-i18n]").forEach((element) => { const value = universeCopy[currentLocale][element.dataset.i18n]; if (value !== undefined) element.textContent = value; });
  document.querySelectorAll("[data-locale]").forEach((button) => { const active = button.dataset.locale === currentLocale; button.classList.toggle("active", active); button.setAttribute("aria-pressed", String(active)); });
  const pageTitle = currentLocale === "en" ? "ECHO UNIVERSE — Echo Age" : "ECHO UNIVERSE · 回响宇宙";
  const pageDescription = currentLocale === "en" ? "Enter ECHO Universe: a 2147 AI Soulpunk world of memory, identity and digital life across stories and media." : "进入 ECHO 宇宙：一个关于记忆、身份与数字生命的 2147 AI Soulpunk 世界。";
  document.title = pageTitle;
  document.querySelector('meta[name="description"]')?.setAttribute("content", pageDescription);
  document.querySelector('meta[property="og:title"]')?.setAttribute("content", pageTitle);
  document.querySelector('meta[property="og:description"]')?.setAttribute("content", pageDescription);
  document.querySelector('meta[property="og:locale"]')?.setAttribute("content", currentLocale === "en" ? "en_US" : "zh_CN");
  document.querySelectorAll("[data-novel-link]").forEach((link) => { link.href = `/universe/novel/?lang=${currentLocale}`; });
  try { localStorage.setItem("echo.locale", currentLocale); } catch (_) {}
  if (updateUrl) { const url = new URL(location.href); url.searchParams.set("lang", currentLocale); history.replaceState({}, "", url); }
  renderSeason(); renderAtlas(); renderMedia(); syncSpoilerButton();
}

function syncSpoilerButton() {
  const button = document.querySelector("#spoiler-toggle");
  button.setAttribute("aria-pressed", String(spoilersVisible));
  button.querySelector("span").textContent = universeCopy[currentLocale][spoilersVisible ? "spoilerOn" : "spoilerOff"];
}

document.querySelectorAll("[data-locale]").forEach((button) => button.addEventListener("click", () => applyUniverseLocale(button.dataset.locale)));
document.querySelectorAll("[data-season]").forEach((button) => button.addEventListener("click", () => { currentSeason = button.dataset.season; renderSeason(); }));
document.querySelectorAll("[data-atlas]").forEach((button) => button.addEventListener("click", () => { currentAtlas = button.dataset.atlas; currentAtlasIndex = 0; renderAtlas(); }));
document.querySelectorAll("[data-media]").forEach((button) => button.addEventListener("click", () => { currentMedia = button.dataset.media; renderMedia(); }));
document.querySelector("#spoiler-toggle")?.addEventListener("click", () => { spoilersVisible = !spoilersVisible; try { localStorage.setItem("echo.universe.spoilers", String(spoilersVisible)); } catch (_) {} syncSpoilerButton(); renderSeason(); renderAtlas(); });
try { spoilersVisible = localStorage.getItem("echo.universe.spoilers") === "true"; } catch (_) {}

const canvas = document.querySelector("#memory-sea");
const context = canvas.getContext("2d", { alpha: true });
const main = document.querySelector("main");
let frame = 0;
function randomFactory(seed) { let state = seed >>> 0; return () => { state += 0x6D2B79F5; let value = state; value = Math.imul(value ^ value >>> 15, value | 1); value ^= value + Math.imul(value ^ value >>> 7, value | 61); return ((value ^ value >>> 14) >>> 0) / 4294967296; }; }
function drawMemorySea() {
  frame = 0;
  const width = main.clientWidth;
  const height = main.scrollHeight;
  const ratio = Math.max(.7, Math.min(devicePixelRatio || 1, 1.55, Math.sqrt(7500000 / Math.max(1, width * height))));
  canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio); canvas.style.width = `${width}px`; canvas.style.height = `${height}px`;
  context.setTransform(ratio, 0, 0, ratio, 0, 0); context.clearRect(0, 0, width, height);
  const random = randomFactory(2147001 + width);
  context.globalCompositeOperation = "lighter";
  for (let index = 0; index < Math.min(2100, width * height / 2200); index += 1) {
    const x = random() * width, y = random() * height, radius = index % 83 === 0 ? 1.15 : .2 + random() * .5;
    context.globalAlpha = .06 + Math.pow(random(), 2) * .38; context.fillStyle = random() > .84 ? "#ba8cff" : "#8dacff"; context.beginPath(); context.arc(x,y,radius,0,Math.PI*2); context.fill();
  }
  const cx = width * .67, cy = Math.min(980, innerHeight) * .5, reach = Math.min(width * .35, 430);
  for (let index = 0; index < 1800; index += 1) {
    const t = Math.pow(random(), .7), arm = index % 5, angle = arm * Math.PI * .4 + t * 5.1 + (random() - .5) * (.7 - t * .3), distance = reach * (.08 + t);
    const x = cx + Math.cos(angle) * distance, y = cy + Math.sin(angle) * distance * .62;
    context.globalAlpha = .12 + t * .4; context.fillStyle = random() > .78 ? "#c19aff" : "#a8c4ff"; context.beginPath(); context.arc(x,y,.18 + random() * .54,0,Math.PI*2); context.fill();
  }
  context.globalAlpha = 1; context.globalCompositeOperation = "source-over";
}
function scheduleSea() { if (frame) cancelAnimationFrame(frame); frame = requestAnimationFrame(drawMemorySea); }

const header = document.querySelector(".universe-header");
const navLinks = Array.from(document.querySelectorAll('.universe-nav a[href^="#"]'));
let chromeFrame = 0;
function syncChrome() {
  chromeFrame = 0; header?.classList.toggle("scrolled", scrollY > 20);
  const focus = scrollY + innerHeight * .38; let active = null;
  navLinks.forEach((link) => { const target = document.querySelector(link.getAttribute("href")); if (target && target.offsetTop <= focus) active = link; });
  navLinks.forEach((link) => link.classList.toggle("active", link === active));
}
window.addEventListener("scroll", () => { if (!chromeFrame) chromeFrame = requestAnimationFrame(syncChrome); }, { passive: true });
window.addEventListener("resize", () => { scheduleSea(); syncChrome(); }, { passive: true });
window.addEventListener("load", scheduleSea, { once: true });
applyUniverseLocale(initialLocale(), false); scheduleSea(); syncChrome();
