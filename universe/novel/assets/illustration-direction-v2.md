# 《陌生记忆》配图重绘方案 V2

状态：完成。经用户要求，使用已登录的 ChatGPT 网页按参考图和以下提示生成三张插画；已保存为 V2 PNG 并接入封面、目录、扉页及正文。

## 剧情和资产依据

- 正文：`universe/novel/content/stranger-memory.zh.md`，只以当前公开试读为画面边界。
- 世界视觉规范：`bible/visual_system_v1.md`：白色工业、外科灰、石墨黑、克制的神经玻璃青与医疗浅蓝。
- 已核对 `assets/characters/octopus_visual_asset_index.yaml` 与 `white_ghost_team_visual_locks.yaml`。现有正式立绘主要为白幽灵小队；当前试读结束时小队尚未抵达，不把其面孔、制服移植给林乔，也不新增队员出场。
- 林乔没有在上述角色图像索引中找到正式立绘。重绘沿用现有小说插图中的脸型与黑色低束发，作为候选插图连续性参考，不新增正式人物设定。
- 三张旧图保留，生成合格的新图后以版本化文件替换页面引用。

## 人物连续性

林乔：32 岁普通保险审计员；以旧事故图的脸型与黑色低束发为主参考，灰色通勤西装外套、浅灰衬衫、深灰长裤、深色平底鞋。事故后才出现撕破袖口与粉尘。不得变成战术人员、白发少女或超自然附身者。

男孩：约九岁，沿用旧急救图中的青绿色条纹上衣；事故和急救时躺在座椅下，受维护板困住，下半身由板材与阴影遮挡。

母亲：沿用旧急救图中的黑发与灰绿色衬衫，始终为同一人物。

## 分镜与验收

1. **07:13 / 白港晨醒**：住宅遮光板逐层开启、垂直轨道安全灯亮起、银灰海雾；城市宏大但结构可信。主塔居中，兼容目录封面纵向裁切和阅读页横幅。
2. **07:44 / 精确地失败**：车厢结构挤压、折叠座椅与断裂扶手；白色应急灯持续照明。不是爆炸，没有火球。林乔从断裂扶手下醒来，男孩受困、母亲伏在旁边，医疗无人机无法进入。
3. **事故后三分钟 / 陌生的手**：双手与真实急救动作为视觉中心，一手用撕下的袖口压迫带按住男孩肋骨下方衣物，另一手操作医疗无人机底部安全槽与卡匣。孩子躺着，母亲在旁；不出现外露伤口、额外手指、眼部激光、幽灵幻影。

生成后逐张检查人物脸型、服装连续性、手部解剖、男孩体位、列车变形、无人机动作、设备光源以及移动端裁切。随后更新目录封面、章节缩略图、阅读页扉页、正文插图与中英文图注，并验证图片加载。

## 最终生成提示词

生成方式：ChatGPT 网页图像生成，沿用现有配图作为人物和场景参考。原始 V1 保留。

### 1. harbor

参考文件：
- `universe/novel/assets/illustration-white-harbor-agnes-v1.png`

```text
Use case: illustration-story. Create a replacement premium illustrated novel plate, landscape 3:2 1536x1024, for ECHO AGE, chapter Stranger Memory. Reference 1 is the old White Harbor city plate: preserve its coastal white industrial identity and vertical transit concept, but redesign composition and increase cinematic scale, depth, material detail and sophisticated manga concept-art finish. Scene faithfully at 07:13 in 2147: immense coastal residential towers gradually waking, layered sleep shutters lifting, silver-grey sea mist between white civic architecture, vertical rail safety lights sequentially lighting, fine condensation on architectural membranes, distant quarantine port and surgical civic bridges. Safe and suffocating, quietly monitored. Real engineered rail connections, restrained pale blue home-core lights, NOT neon dystopia. Foreground a credible elevated transit structure leads the eye toward the immense main tower in central 50% so a portrait book-cover crop works; layers of inhabited towers recede to coastal haze. Pearl white, surgical grey, graphite, neural-glass cyan, restrained warm dawn glints. Drawn cinematic science-fiction graphic-novel painting with precise fine ink details and rich atmospheric perspective, not photoreal photo, not watercolor paper texture, no childish anime, no floating magical energy, no UI, no text, no logos or watermarks. No identifiable cast needed.
```

### 2. collapse

参考文件：
- `universe/novel/assets/illustration-l7-collapse-agnes-v1.png`
- `universe/novel/assets/illustration-stranger-hands-agnes-v1.png`

```text
Use case: illustration-story. Redraw the ECHO AGE L-7 transit crash scene as a premium cinematic manga novel illustration, landscape 3:2 1536x1024. Image 1 is prior scene and primary Lin Qiao face/hair/office silhouette reference, image 2 is supporting reference for the boy (teal striped shirt) and his mother (muted green blouse). Keep recognizable natural faces. Lin Qiao is an ordinary 32-year-old woman with black hair in a low tied bun/ponytail, grey office blazer over pale grey collared blouse, charcoal trousers, practical dark flat shoes. Never a white-haired tactical character. Correct the old art to the ACTUAL STORY: L-7 safety pressure misread makes carriages structurally accordion inward, NOT an explosion. Show dramatically buckled white ceiling beams, crushed white handrails, folded pale-grey seats, fine shattered white composite glass dust, a diagonal bent floor. Bright cold WHITE emergency strips remain ON, clearly exposing mechanical failure. Camera low at one end, strong cinematic perspective toward a twisted interior choke point, not an intact clean train with just cracked windows. Lin Qiao near lower left has only just regained consciousness beneath a snapped handrail, her face tense and dusty. Deeper to right a nine-year-old boy lies trapped BELOW a seat behind a displaced maintenance panel; his legs and lower body occluded, his mother in green crouches beside him gripping the panel. A small white/graphite medical drone with physical stabilization ring hovers close with restrained pale blue diagnostic lamp, unable to reach. NO seated healthy boy, NO neat undamaged rows, NO graphic wounds or blood, NO flames or explosions, NO laser eyes, NO supernatural ghost silhouettes, NO soldiers/White Ghost Team yet, NO readable text. World visual authority: clean surgical white industrial soulpunk, graphite supports, pale medical blue, silver sea mist through damaged window. Fine ink linework + polished cinematic painted lighting, emotionally grounded, dramatic spatial scale, realistic human anatomy.
```

### 3. hands

参考文件：
- `universe/novel/assets/illustration-l7-collapse-agnes-v1.png`
- `universe/novel/assets/illustration-stranger-hands-agnes-v1.png`

```text
Use case: illustration-story. Create the replacement pivotal Stranger Hands rescue plate for ECHO AGE novel. Landscape 3:2 1536x1024. Reference 1 fixes Lin Qiao's FACE and black low tied hair, grey office blazer/pale collared blouse/charcoal trousers. Reference 2 fixes the boy's teal striped shirt and mother's green blouse, but its action is WRONG and must be replaced. Show the ACTUAL prose: inside a badly compressed L-7 carriage under bright cold white emergency lighting, an ordinary 32-year-old insurance auditor Lin Qiao kneels beside a nine-year-old boy lying low on the floor trapped beneath a bent seat and opaque maintenance panel. His lower body and any injury are hidden. She has torn her blouse cuff into a pressure cloth. Her TWO anatomically correct hands are the focal point: one hand steadily holds the folded cloth against his lower ribcage over fabric, the other reaches upward to operate the physical underside release slot of a small hovering medical drone with a stabilization ring and tiny vascular-sealant cartridge. Her actions look uncannily practiced but she is frightened and concentrating, no magic. The mother crouches further behind, anxious, hand near the boy's shoulder. Do not show them casually seated or using a tablet. No extra arms/fingers, no surgical gore, no visible wounds, no exposed anatomy. Use a close/medium 3/4 camera framing Lin Qiao's face upper left, BOTH hands and drone mechanism near center, the boy safely reclined center-right, mother's face secondary at right. Keep all key subjects in middle 75% for responsive crops. Background white composite debris and distorted seat geometry; silver city glimpsed outside. Pearl whites, surgical greys, graphite, very restrained pale blue light from the physical drone, no lasers from eyes, no supernatural aura or floating ghost. Premium fine-ink cinematic manga painted illustration matching the other two plates, sophisticated faces, tactile torn cloth and engineered medical device, emotionally intense humane rescue. No white-haired squad members: they have not arrived. No text, logos, watermark.
```
