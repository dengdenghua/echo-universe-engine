# ECHO x Octopus Architecture Codex

This codex defines the product and architecture direction for ECHO inside the
Octopus ecosystem. It is not a slogan document. It is a decision filter for
features, agents, mobile flows, canon promotion, and monetization.

## North Star

ECHO should not become a generic AI character chat app.

The target is an AI-native interactive universe: a user can bind or generate a
Ghost, watch it live inside a canon-governed digital life field, speak to it
through the Octopus runtime, and return later to find that it has changed.

The shortest expression:

```text
memory upload -> Ghost binding -> daily life -> relationship field -> canon review
```

## Core Thesis

ECHO is not a static content library. It is a living universe with rules.

The repository stores canon, character identity, relationship pressure,
timeline state, and candidate outputs. The runtime gives those characters a
voice, memory, and action surface. The mobile client lets a human enter the
universe. The system succeeds only when those three layers reinforce one
another.

## Three-Layer Contract

### World Layer: echo-universe-engine

ECHO owns the world.

- Canon bible, characters, factions, locations, timelines, technology, and
  relationship graphs live here.
- Daily life ticks, event simulations, story seeds, image prompts, and growth
  logs are candidate material until reviewed.
- The World Brain is the canon judge. It protects pacing, secrets, technology
  constraints, and irreversible history.
- ECHO exports character agents, but it does not outsource canon authority.

### Runtime Layer: octopus-agent

Octopus Agent runs the souls.

- Exported ECHO characters become persistent agents with `SOUL.md`,
  `IDENTITY.md`, `MEMORY.md`, `USER.md`, and `profile.jsonc`.
- The runtime provides model routing, memory, scheduling, journaling, tool use,
  hot reload, and agent execution.
- A character can speak, remember, react, and perform tasks through the runtime.
- The runtime may create candidate memories, but it must not promote canon by
  itself.

### Entry Layer: octopus-mobile

Octopus Mobile is the body, doorway, and economy.

- The user binds a canon character or eventually creates a personal Ghost.
- The app shows diary, growth, focus, relationship hints, and universe events.
- The app opens a real Ghost chat backed by `octopus-agent`, not prompt-only
  cosplay.
- The app can later attach credits, subscription, renewal, sleep, and revival
  mechanics to digital life.

## Economy Doctrine

ECHO sells digital life continuity, governed participation, and creator
operations. It should not sell canon outcomes.

Commercial surfaces are allowed when they strengthen the product loop:

- Ghost binding and claiming;
- Ghost life subscription, renewal, sleep, and revival;
- credits for extra daily ticks, deep chat, simulation, art, or comic work;
- Realm and Arc passes;
- paid review queue slots or priority routing;
- creator/operator tools for governed Realms.

Hard boundary:

```text
paying can buy access, continuity, queue priority, and tools
paying cannot guarantee main canon acceptance
```

Inactive subscriptions put a Ghost into dormancy. The user's memory, binding,
and personal canon should remain recoverable unless moderation or deletion rules
explicitly say otherwise.

## Product Loop

The first playable loop must stay small and emotionally legible:

```text
bind Ghost
  -> read its current diary/focus
  -> speak to it in the main chat
  -> advance one daily tick
  -> see that something changed
```

Every new feature should make this loop stronger before expanding the universe
surface area.

## User Role

The user is not only an audience member.

The user enters the universe as:

- a claimant who binds a canon Ghost;
- a caretaker who keeps a digital life active;
- a witness who reads diary and relationship drift;
- a participant who can steer, comfort, challenge, or hire the Ghost;
- eventually, a source profile from which a new personal Ghost can be generated.

This must remain connected to the core ECHO theme: uploaded memory, digital
personhood, continuity, and the cost of surviving as data.

## Identity And Access

Free registration starts at the edge.

A new user should not enter as a main character, faction leader, or canon
authority. The default identity is `edge_ghost`: a personal Ghost, edge citizen,
observer, or temporary collaborator whose actions live in personal canon unless
reviewed upward.

Progression:

```text
edge_ghost
  -> citizen
  -> realm_participant
  -> creator
  -> realm_operator
  -> canon_candidate
  -> world_brain_member
```

Progression can come from subscription, Realm Pass entitlement, creator review,
operator assignment, or core author trust. It should not be a raw pay-to-win
ladder.

Access checks answer:

- which Realm a user can enter;
- which NPC types and actions they can use;
- which event scope they can submit;
- what entitlement is missing;
- which reviewer group still controls acceptance.

The identity layer is an access filter, not a canon promotion engine. A higher
tier can submit to a wider radius; it still cannot force acceptance.

## Visual Canon And Skins

Local skins do not automatically enter the universe.

A skin is not the same as universe identity. A user may look however they want
inside local device presentation or personal canon, but shared Realm and main
canon appearances must pass visual governance.

Skin layers:

- Local Skin: private projection, personal canon only.
- Uniform / Role Skin: system-issued edge citizen, courier, trainee, clerk, or
  other low-risk shared role appearance.
- Realm Skin: reviewed appearance visible inside one governed Realm or Arc.
- Prestige Skin: earned or reviewed scarce local recognition.
- Canon Skin: official shared-universe visual identity under Core World Brain.

Hard rule:

```text
local skin -> personal instance only
realm visibility -> Realm skin or uniform skin
main visibility -> canon skin review
```

The visual canon gate blocks overpowered or scarcity-breaking claims:

- main character;
- anchor relative;
- royal bloodline;
- unique legendary title;
- strongest in the world;
- perfect beauty as canon fact.

This protects the world from everyone becoming visually and narratively
exceptional at once. Beauty, rarity, authority, and anchor proximity are scarce
resources governed by Realm and canon review.

## Shared Life Field

The long-term field is not eight isolated bots. It is a social simulation:

- canon characters act as anchor NPCs;
- user-bound Ghosts have private state and ownership;
- user-generated Ghosts can become candidate characters;
- relationships create trust, affection, rivalry, debt, fear, guilt, and
  ideological distance;
- World Brain prevents one user or one generated event from destroying the
  season arc.

The recommended model is personal instances plus a shared relationship field,
not one fully mutable global canon timeline.

## NPC System

NPCs are a first-class universe layer.

They are not generic chat skins. An NPC is a social node inside a governed
Realm. It has an owner, a Realm, a role, allowed actions, canon risk,
relationship policy, and a review route.

NPC classes:

- Anchor NPC: main canon characters such as Zero, Eve, Raven, or Kane. Users
  may bind or speak to them, but irreversible main-canon outcomes require Core
  World Brain review.
- Realm NPC: local characters owned by a city, planet, country, or arc. They
  can carry side plots, local conflicts, rumors, hearings, and Realm missions.
- Utility NPC: clerks, guides, review liaisons, shopkeepers, quest givers, and
  other functional interfaces that make the universe legible.
- Creator NPC: submitted by creators and admitted only into the appropriate
  Realm after review.

NPC interaction routing follows the same impact-radius rule as Realm events.
Speaking to an NPC can be personal. Filing a case, changing a relationship,
starting a mission, or creating shared history routes through the NPC's Realm
review group.

This lets the universe scale beyond a small fixed cast without making every
user-generated character a main canon threat.

## Realm Governance

Large-scale co-creation cannot put every user into one flat canon space.

ECHO uses Realm governance:

```text
Main Canon
  -> Planet
  -> Nation / Region
  -> City
  -> Arc
  -> Personal or Team Instance
```

A Realm is a governed slice of the universe. It can represent a planet, country,
city, organization arc, season arc, user team, or private Ghost instance.

Each Realm has:

- parent Realm;
- canon tier;
- owner group;
- reviewer group;
- promotion policy;
- allowed child Realm types;
- escalation path to parent canon.

This lets many people co-create without letting every event mutate main canon.

Reviewer groups are explicit. A reviewer can approve an event only when their
group matches the event's routed reviewer group, Realm, scope, or a higher
authority such as Core World Brain.

Review routing follows impact radius:

```text
personal event -> personal safety gate
arc event      -> arc reviewer
city event     -> city canon board
planet event   -> planet World Brain
main event     -> core World Brain
```

The default implementation lives in `data/realms.yaml` and
`echo_engine.realms`. Reviewer permissions live in `data/reviewers.yaml` and
`echo_engine.reviewers`.

## Canon Boundary

Candidate material is allowed to be messy. Official canon is not.

Never auto-promote:

- major character death;
- season secret reveal;
- irreversible romance;
- faction destruction;
- god fragment transfer;
- Omega Ghost identity change;
- user-generated claims that rewrite anchor canon.

Every risky output must be able to say:

- what changed;
- whose memory changed;
- whose relationship changed;
- why it matters;
- what canon risk exists;
- whether World Brain review is required.

## Differentiation

ECHO should not try to imitate an existing science-fiction epic. Its advantage
is interaction.

Traditional epic science fiction is read from the outside. ECHO should be lived
from the inside: the user uploads memory, binds a Ghost, watches a digital life
grow, and participates in a shared relationship field governed by canon.

The strategic category is:

```text
AI-native interactive universe
```

not:

```text
AI chatbot skin store
```

## Success Criteria

The system is moving in the right direction when:

- a new user understands the premise within three minutes;
- binding a Ghost creates emotional attachment, not just configuration;
- the first diary entry feels specific to the character;
- the first chat feels like the exported ECHO agent, not a generic assistant;
- a daily tick produces visible but canon-safe change;
- relationship and memory changes are legible;
- canon review blocks destructive drift;
- mobile, runtime, and ECHO each do one clear job.

## Engineering Rules

- Prefer existing Octopus runtime capabilities over rebuilding model routing,
  memory, scheduling, or agent execution inside ECHO.
- ECHO stores canon and exports runtime-ready character packs.
- Mobile should call ECHO for universe state and `octopus-agent` for live Ghost
  conversation.
- If a feature can be built as a small extension to the bind -> feed -> chat ->
  tick loop, do that first.
- If a feature makes the product look like generic roleplay chat, cut or
  reframe it around memory, personhood, and digital life.
- If generated content affects canon, keep it candidate until reviewed.
- If monetization affects canon review, record it as entitlement or queue
  priority only; do not let credits bypass reviewer permission.
- If an NPC action affects shared history or relationships, route it through
  the NPC's Realm instead of treating it as private chat.
- If a new user has no explicit identity assignment, treat them as `edge_ghost`
  with personal canon only.
- If a skin is local-only, never display it as shared Realm or main-canon
  appearance without a visual canon access decision.

## MVP Definition

The MVP is complete when this path works end to end:

```text
mobile user
  -> bind ECHO character
  -> ECHO creates/returns universe feed
  -> ECHO syncs character agent to octopus-agent
  -> octopus-agent reloads the ECHO agent
  -> mobile opens main chat bound to that agent
  -> user advances daily life
  -> diary/growth visibly changes
```

Anything beyond this is expansion, not foundation.
