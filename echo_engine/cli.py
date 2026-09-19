from __future__ import annotations

import argparse
import json
from pathlib import Path

from echo_engine.bindings import (
    BindingError,
    bind_user_to_character,
    get_user_binding,
    list_user_bindings,
    release_user_binding,
)
from echo_engine.economy import (
    EconomyError,
    activate_ghost_subscription,
    economy_account_summary,
    list_products,
    purchase_product,
    record_wallet_entry,
)
from echo_engine.identities import (
    IdentityError,
    assign_identity,
    check_npc_access,
    check_realm_event_access,
    get_universe_identity,
    list_identity_tiers,
)
from echo_engine.neural.simulator import UniverseEvent, simulate_event
from echo_engine.neural.octopus_ecosystem import render_octopus_ecosystem_plan
from echo_engine.neural.octopus_export import export_octopus_agents, sync_octopus_runtime_agents
from echo_engine.neural.utility_foundry import mint_utility_agents, publish_registry_json
from echo_engine.neural.octopus_runtime import reload_octopus_runtime_agents
from echo_engine.npcs import NPCError, get_npc, list_npcs, route_npc_interaction
from echo_engine.neural.digital_life import run_daily_life_tick
from echo_engine.journal import record_canon_decision, journal
from echo_engine.promotion import PromotionError, promote_candidate
from echo_engine.realm_events import RealmEventError, realm_event_queue, submit_realm_event
from echo_engine.realms import RealmError, get_realm, list_realms, route_realm_review
from echo_engine.reviewers import (
    ReviewerError,
    authorize_reviewer_for_event,
    get_reviewer_group,
    list_reviewer_groups,
)
from echo_engine.skins import SkinError, check_skin_access, list_skin_policies
from echo_engine.universe_feed import UniverseFeedError, get_universe_feed_for_user
from echo_engine.generators import (
    run_art_director_agent,
    run_character_agent,
    run_consistency_agent,
    run_faction_agent,
    run_lore_agent,
    run_relationship_agent,
    run_story_agent,
    run_technology_agent,
)
from echo_engine.store import CanonStore


def main() -> None:
    parser = argparse.ArgumentParser(prog="echo-engine")
    parser.add_argument(
        "command",
        choices=[
            "status",
            "character",
            "lore",
            "story",
            "relationship",
            "faction",
            "technology",
            "art",
            "consistency",
            "event",
            "daily-life",
            "journal",
            "review-candidate",
            "promote-candidate",
            "bind-character",
            "binding",
            "bindings",
            "release-binding",
            "universe-feed",
            "npcs",
            "npc",
            "route-npc",
            "realms",
            "realm",
            "route-review",
            "submit-realm-event",
            "realm-events",
            "reviewer-groups",
            "reviewer-group",
            "authorize-reviewer",
            "economy-products",
            "wallet-grant",
            "wallet",
            "purchase",
            "ghost-subscription",
            "identity-tiers",
            "identity",
            "assign-identity",
            "check-realm-access",
            "check-npc-access",
            "skin-policies",
            "check-skin-access",
            "export-octopus-agents",
            "mint-utility-agents",
            "rebuild-registry",
            "octopus-ecosystem-plan",
        ],
    )
    parser.add_argument("--input-dir", default=None, help="mint-utility-agents: 工具角色 .md spec 源目录")
    parser.add_argument("--publish-dir", default=None, help="mint-utility-agents: 发布扁平 registry JSON 的目标目录")
    parser.add_argument("--skill-dir", default=None, help="mint-utility-agents: 插件包技能(能力包)发布目标目录")
    parser.add_argument("--watch", action="store_true", help="rebuild-registry: 监听角色规格变化,自动重铸(常驻)")
    parser.add_argument("--watch-interval", type=float, default=3.0, help="rebuild-registry --watch: 轮询间隔秒")
    parser.add_argument("--title", default="Ghost Attack on Atlas")
    parser.add_argument("--location", default="Atlas")
    parser.add_argument(
        "--description",
        default=(
            "A Ghost contamination wave hits Atlas civic identity gates, causing citizens "
            "to remember lives from dead household AI cores."
        ),
    )
    parser.add_argument("--pressure", default="identity / Ghost personhood")
    parser.add_argument("--stakes", default="Atlas stability and White Ghost Team trust")
    parser.add_argument("--event-id", default="")
    parser.add_argument("--decision", choices=["accepted", "rejected", "superseded"], default="rejected")
    parser.add_argument("--reason", default="")
    parser.add_argument("--filename", default=None)
    parser.add_argument("--user-id", default="")
    parser.add_argument("--character-id", default="")
    parser.add_argument("--source", default="mobile")
    parser.add_argument("--realm-id", default="")
    parser.add_argument("--npc-id", default="")
    parser.add_argument("--npc-type", default="")
    parser.add_argument("--action", default="chat")
    parser.add_argument("--bindable", choices=["true", "false", "any"], default="any")
    parser.add_argument("--scope", default="personal")
    parser.add_argument("--submitter", default="anonymous")
    parser.add_argument("--summary", default="")
    parser.add_argument("--content", default="")
    parser.add_argument("--reviewer-group", default="")
    parser.add_argument("--reviewer", default="human")
    parser.add_argument("--amount", type=int, default=0)
    parser.add_argument("--product-id", default="")
    parser.add_argument("--duration-days", type=int, default=30)
    parser.add_argument("--tier", default="")
    parser.add_argument("--realms", default="")
    parser.add_argument("--skin-type", default="local_skin")
    parser.add_argument("--requested-scope", default="personal")
    parser.add_argument("--claims", default="")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for export commands, for example ../octopus-agent/agents",
    )
    parser.add_argument(
        "--sync-octopus-runtime",
        action="store_true",
        help="Write exported ECHO agents into ECHO_OCTOPUS_AGENTS_ROOT or --output-dir.",
    )
    parser.add_argument(
        "--reload-octopus-runtime",
        action="store_true",
        help="After syncing agent files, call ECHO_OCTOPUS_RUNTIME_URL/api/agents/reload.",
    )
    parser.add_argument(
        "--target-dir",
        default=None,
        help="Canon target directory for promote-candidate, for example stories",
    )
    parser.add_argument(
        "--no-refresh-octopus-agents",
        action="store_true",
        help="Do not refresh outputs/octopus_agents after promoting a character.",
    )
    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps(CanonStore().status().model_dump(), ensure_ascii=False, indent=2))
        return

    if args.command == "event":
        result = simulate_event(
            UniverseEvent(
                title=args.title,
                location=args.location,
                description=args.description,
                pressure=args.pressure,
                stakes=args.stakes,
            )
        )
        print(result.content)
        if result.output_path:
            print(f"\nSaved: {result.output_path}")
        return

    if args.command == "daily-life":
        result = run_daily_life_tick()
        print(result.content)
        if result.output_path:
            print(f"\nSaved: {result.output_path}")
        return

    if args.command == "journal":
        events = journal().read_all(limit=25)
        print(json.dumps([event.model_dump(mode="json") for event in events], ensure_ascii=False, indent=2))
        return

    if args.command == "review-candidate":
        if not args.event_id:
            parser.error("--event-id is required for review-candidate")
        if not args.reason:
            parser.error("--reason is required for review-candidate")
        try:
            event = record_canon_decision(
                event_id=args.event_id,
                decision=args.decision,
                reason=args.reason,
                reviewer=args.reviewer,
            )
        except ReviewerError as exc:
            parser.error(str(exc))
        print(json.dumps(event.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return

    if args.command == "promote-candidate":
        if not args.event_id:
            parser.error("--event-id is required for promote-candidate")
        try:
            result = promote_candidate(
                args.event_id,
                target_dir=args.target_dir,
                filename=args.filename,
                refresh_octopus_agents=not args.no_refresh_octopus_agents,
            )
        except PromotionError as exc:
            parser.error(str(exc))
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
        return

    if args.command == "bind-character":
        if not args.user_id:
            parser.error("--user-id is required for bind-character")
        if not args.character_id:
            parser.error("--character-id is required for bind-character")
        try:
            binding = bind_user_to_character(
                user_id=args.user_id,
                character_id=args.character_id,
                source=args.source,
            )
        except BindingError as exc:
            parser.error(str(exc))
        print(binding.model_dump_json(indent=2))
        return

    if args.command == "binding":
        if not args.user_id:
            parser.error("--user-id is required for binding")
        binding = get_user_binding(args.user_id)
        print(binding.model_dump_json(indent=2) if binding else "{}")
        return

    if args.command == "bindings":
        print(
            json.dumps(
                [binding.model_dump(mode="json") for binding in list_user_bindings()],
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.command == "release-binding":
        if not args.user_id:
            parser.error("--user-id is required for release-binding")
        try:
            binding = release_user_binding(args.user_id)
        except BindingError as exc:
            parser.error(str(exc))
        print(binding.model_dump_json(indent=2))
        return

    if args.command == "universe-feed":
        if not args.user_id:
            parser.error("--user-id is required for universe-feed")
        try:
            feed = get_universe_feed_for_user(args.user_id)
        except UniverseFeedError as exc:
            parser.error(str(exc))
        print(feed.model_dump_json(indent=2))
        return

    if args.command == "npcs":
        try:
            rows = list_npcs(
                realm_id=args.realm_id or None,
                npc_type=args.npc_type or None,
                bindable={"true": True, "false": False}.get(args.bindable),
            )
        except NPCError as exc:
            parser.error(str(exc))
        print(json.dumps([npc.model_dump(mode="json") for npc in rows], ensure_ascii=False, indent=2))
        return

    if args.command == "npc":
        if not args.npc_id:
            parser.error("--npc-id is required for npc")
        try:
            npc = get_npc(args.npc_id)
        except NPCError as exc:
            parser.error(str(exc))
        print(npc.model_dump_json(indent=2))
        return

    if args.command == "route-npc":
        if not args.npc_id:
            parser.error("--npc-id is required for route-npc")
        try:
            route = route_npc_interaction(npc_id=args.npc_id, action=args.action)
        except NPCError as exc:
            parser.error(str(exc))
        print(route.model_dump_json(indent=2))
        return

    if args.command == "realms":
        try:
            print(
                json.dumps(
                    [realm.model_dump(mode="json") for realm in list_realms()],
                    ensure_ascii=False,
                    indent=2,
                )
            )
        except RealmError as exc:
            parser.error(str(exc))
        return

    if args.command == "realm":
        if not args.realm_id:
            parser.error("--realm-id is required for realm")
        try:
            realm = get_realm(args.realm_id)
        except RealmError as exc:
            parser.error(str(exc))
        print(realm.model_dump_json(indent=2))
        return

    if args.command == "route-review":
        try:
            route = route_realm_review(scope=args.scope, realm_id=args.realm_id or None)
        except RealmError as exc:
            parser.error(str(exc))
        print(route.model_dump_json(indent=2))
        return

    if args.command == "submit-realm-event":
        if not args.summary:
            parser.error("--summary is required for submit-realm-event")
        try:
            event = submit_realm_event(
                title=args.title,
                summary=args.summary,
                scope=args.scope,
                realm_id=args.realm_id or None,
                submitter=args.submitter,
                content=args.content,
            )
        except RealmEventError as exc:
            parser.error(str(exc))
        print(event.model_dump_json(indent=2))
        return

    if args.command == "realm-events":
        events = realm_event_queue(
            reviewer_group=args.reviewer_group or None,
            realm_id=args.realm_id or None,
            limit=25,
        )
        print(json.dumps([event.model_dump(mode="json") for event in events], ensure_ascii=False, indent=2))
        return

    if args.command == "reviewer-groups":
        try:
            groups = list_reviewer_groups()
        except ReviewerError as exc:
            parser.error(str(exc))
        print(json.dumps([group.model_dump(mode="json") for group in groups], ensure_ascii=False, indent=2))
        return

    if args.command == "reviewer-group":
        if not args.reviewer_group:
            parser.error("--reviewer-group is required for reviewer-group")
        try:
            group = get_reviewer_group(args.reviewer_group)
        except ReviewerError as exc:
            parser.error(str(exc))
        print(group.model_dump_json(indent=2))
        return

    if args.command == "authorize-reviewer":
        if not args.event_id:
            parser.error("--event-id is required for authorize-reviewer")
        events = [event for event in journal().read_all() if str(event.event_id) == args.event_id]
        if not events:
            parser.error(f"event not found: {args.event_id}")
        try:
            auth = authorize_reviewer_for_event(reviewer=args.reviewer, event=events[-1])
        except ReviewerError as exc:
            parser.error(str(exc))
        print(auth.model_dump_json(indent=2))
        return

    if args.command == "economy-products":
        try:
            products = list_products()
        except EconomyError as exc:
            parser.error(str(exc))
        print(json.dumps([product.model_dump(mode="json") for product in products], ensure_ascii=False, indent=2))
        return

    if args.command == "wallet-grant":
        if not args.user_id:
            parser.error("--user-id is required for wallet-grant")
        if args.amount == 0:
            parser.error("--amount must not be zero for wallet-grant")
        try:
            entry = record_wallet_entry(
                user_id=args.user_id,
                amount=args.amount,
                reason=args.reason or "manual_grant",
            )
        except EconomyError as exc:
            parser.error(str(exc))
        print(entry.model_dump_json(indent=2))
        return

    if args.command == "wallet":
        if not args.user_id:
            parser.error("--user-id is required for wallet")
        try:
            summary = economy_account_summary(args.user_id)
        except EconomyError as exc:
            parser.error(str(exc))
        print(summary.model_dump_json(indent=2))
        return

    if args.command == "purchase":
        if not args.user_id:
            parser.error("--user-id is required for purchase")
        if not args.product_id:
            parser.error("--product-id is required for purchase")
        try:
            result = purchase_product(
                user_id=args.user_id,
                product_id=args.product_id,
                character_id=args.character_id or None,
            )
        except EconomyError as exc:
            parser.error(str(exc))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.command == "ghost-subscription":
        if not args.user_id:
            parser.error("--user-id is required for ghost-subscription")
        try:
            subscription = activate_ghost_subscription(
                user_id=args.user_id,
                character_id=args.character_id or None,
                duration_days=args.duration_days,
                source=args.source,
            )
        except EconomyError as exc:
            parser.error(str(exc))
        print(subscription.model_dump_json(indent=2))
        return

    if args.command == "identity-tiers":
        try:
            tiers = list_identity_tiers()
        except IdentityError as exc:
            parser.error(str(exc))
        print(json.dumps([tier.model_dump(mode="json") for tier in tiers], ensure_ascii=False, indent=2))
        return

    if args.command == "identity":
        if not args.user_id:
            parser.error("--user-id is required for identity")
        try:
            identity = get_universe_identity(args.user_id)
        except IdentityError as exc:
            parser.error(str(exc))
        print(identity.model_dump_json(indent=2))
        return

    if args.command == "assign-identity":
        if not args.user_id:
            parser.error("--user-id is required for assign-identity")
        if not args.tier:
            parser.error("--tier is required for assign-identity")
        try:
            assignment = assign_identity(
                user_id=args.user_id,
                tier=args.tier,
                realms=[item.strip() for item in args.realms.split(",") if item.strip()],
                source=args.source,
            )
        except IdentityError as exc:
            parser.error(str(exc))
        print(assignment.model_dump_json(indent=2))
        return

    if args.command == "check-realm-access":
        if not args.user_id:
            parser.error("--user-id is required for check-realm-access")
        try:
            decision = check_realm_event_access(
                user_id=args.user_id,
                scope=args.scope,
                realm_id=args.realm_id or None,
            )
        except IdentityError as exc:
            parser.error(str(exc))
        print(decision.model_dump_json(indent=2))
        return

    if args.command == "check-npc-access":
        if not args.user_id:
            parser.error("--user-id is required for check-npc-access")
        if not args.npc_id:
            parser.error("--npc-id is required for check-npc-access")
        try:
            decision = check_npc_access(user_id=args.user_id, npc_id=args.npc_id, action=args.action)
        except IdentityError as exc:
            parser.error(str(exc))
        print(decision.model_dump_json(indent=2))
        return

    if args.command == "skin-policies":
        try:
            policies = list_skin_policies()
        except SkinError as exc:
            parser.error(str(exc))
        print(json.dumps([policy.model_dump(mode="json") for policy in policies], ensure_ascii=False, indent=2))
        return

    if args.command == "check-skin-access":
        if not args.user_id:
            parser.error("--user-id is required for check-skin-access")
        try:
            decision = check_skin_access(
                user_id=args.user_id,
                skin_type=args.skin_type,
                requested_scope=args.requested_scope,
                realm_id=args.realm_id or None,
                claims=[item.strip() for item in args.claims.split(",") if item.strip()],
            )
        except SkinError as exc:
            parser.error(str(exc))
        print(decision.model_dump_json(indent=2))
        return

    if args.command == "export-octopus-agents":
        output_dir = Path(args.output_dir) if args.output_dir else None
        if args.sync_octopus_runtime:
            try:
                written = sync_octopus_runtime_agents(output_dir=output_dir)
            except ValueError as exc:
                parser.error(str(exc))
        else:
            written = export_octopus_agents(output_dir=output_dir)
        payload: dict[str, object] = {"written": [str(path) for path in written]}
        if args.reload_octopus_runtime:
            payload["reload"] = reload_octopus_runtime_agents().__dict__
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    if args.command == "mint-utility-agents":
        input_dir = Path(args.input_dir) if args.input_dir else Path("utility_roles")
        if not input_dir.is_dir():
            parser.error(f"utility role spec dir not found: {input_dir} (传 --input-dir 或建 utility_roles/)")
        out = Path(args.output_dir) if args.output_dir else Path("outputs/utility_agents")
        skill_dest = Path(args.skill_dir) if args.skill_dir else None
        minted = mint_utility_agents(input_dir, out, skill_dest=skill_dest)
        published = publish_registry_json(out, Path(args.publish_dir)) if args.publish_dir else []
        skills_pub = len(list(skill_dest.glob("*.md"))) if skill_dest and skill_dest.is_dir() else 0
        print(json.dumps(
            {"minted": len(minted), "output_dir": str(out),
             "published": len(published), "publish_dir": args.publish_dir,
             "capability_pack_skills": skills_pub, "skill_dir": args.skill_dir},
            ensure_ascii=False, indent=2,
        ))
        return

    if args.command == "rebuild-registry":
        # 活管线生产端:echo 的角色资产一键重铸 + 发布到 registry 源(--publish-dir=enterprise sources 根)
        if not args.publish_dir:
            parser.error("--publish-dir is required (enterprise .../agent_assets/sources 根目录)")
        sources = Path(args.publish_dir)
        _watch_dirs = [Path("utility_roles"), Path("characters"), Path("assets/characters")]

        def _rebuild() -> dict[str, object]:
            roles_out = Path("outputs/utility_agents")
            minted = mint_utility_agents(Path("utility_roles"), roles_out, skill_dest=sources / "plugin-skills")
            pub_roles = publish_registry_json(roles_out, sources / "echo-utility")
            chars_out = Path("outputs/octopus_agents")
            export_octopus_agents(output_dir=chars_out)
            char_dst = sources / "echo-characters"
            char_dst.mkdir(parents=True, exist_ok=True)
            pub_chars = 0
            for prof in sorted(chars_out.glob("echo_*/profile.jsonc")):
                (char_dst / f"{prof.parent.name}.json").write_text(prof.read_text(encoding="utf-8"), encoding="utf-8")
                pub_chars += 1
            return {"utility_roles_minted": len(minted), "utility_published": len(pub_roles),
                    "characters_published": pub_chars}

        def _spec_fp() -> str:
            mt, cnt = 0.0, 0
            for wd in _watch_dirs:
                if wd.is_dir():
                    for p in wd.rglob("*"):
                        if p.is_file():
                            cnt += 1
                            try:
                                mt = max(mt, p.stat().st_mtime)
                            except OSError:
                                pass
            return f"{mt:.3f}:{cnt}"

        if not args.watch:
            out = _rebuild()
            out.update(sources=str(sources), note="registry 消费端按 mtime 自动反映,无需重启")
            print(json.dumps(out, ensure_ascii=False, indent=2))
            return

        # --watch:监听角色规格目录,变了就自动重铸(常驻)。registry 端再按 mtime 自动反映 → 全程无人工。
        import time as _t
        print(f"[watch] 监听 {[str(d) for d in _watch_dirs]},间隔 {args.watch_interval}s,自动重铸…")
        out = _rebuild()
        last = _spec_fp()
        print(json.dumps({"event": "initial", **out, "fp": last}, ensure_ascii=False), flush=True)
        while True:
            _t.sleep(args.watch_interval)
            fp = _spec_fp()
            if fp != last:
                last = fp
                out = _rebuild()
                print(json.dumps({"event": "rebuilt", **out, "fp": fp}, ensure_ascii=False), flush=True)
        return

    if args.command == "octopus-ecosystem-plan":
        print(render_octopus_ecosystem_plan())
        return

    runners = {
        "character": run_character_agent,
        "lore": run_lore_agent,
        "story": run_story_agent,
        "relationship": run_relationship_agent,
        "faction": run_faction_agent,
        "technology": run_technology_agent,
        "art": run_art_director_agent,
        "consistency": run_consistency_agent,
    }
    result = runners[args.command]()
    print(result.content)
    if result.output_path:
        print(f"\nSaved: {result.output_path}")


if __name__ == "__main__":
    main()
