"""Entry point. Read-only: this never writes to or modifies MTG Arena."""
from __future__ import annotations

import argparse
import json
import queue
import sys
import threading
from pathlib import Path

from .arenadb import CardResolver, CardInfo
from .logwatch import LogTailer, PackEvent, PickEvent, PoolEvent, find_log_path, parse_text
from .model import Ratings, PoolState, score_pack
from .review import review_all
from .session import DraftSession, DRAFT_DIR


def _resolver(args, ratings: Ratings) -> CardResolver:
    if getattr(args, "card_map", None):
        raw = json.loads(Path(args.card_map).read_text(encoding="utf-8"))
        cards = {}
        for k, v in raw.items():
            if isinstance(v, dict):
                v.setdefault("grpid", int(k))
                cards[int(k)] = CardInfo(**v)
            else:
                cards[int(k)] = CardInfo(int(k), str(v))
        print(f"card names: {len(cards)} from {args.card_map}")
        return CardResolver(cards)
    return CardResolver.build(setcode=ratings.raw.get("set"), db_path=args.card_db,
                              allow_network=not args.offline,
                              refresh=getattr(args, "refresh_cards", False))


def _banner(r: Ratings) -> None:
    print(f"MTGA Coach - {r.raw.get('set_name', '')} ({r.raw.get('set', '')})")
    if r.confidence == "eval":
        print(f"  ratings: {r.source}")
        print("  These are a PRE-RELEASE PRIOR, not 17Lands data. Import real data with")
        print("  --import-17lands once you have it.")


def _feed(session: DraftSession, ev, q=None) -> bool:
    def apply() -> bool:
        if isinstance(ev, PackEvent):
            return session.on_pack(ev.pack_number, ev.pick_number, ev.card_ids, ev.draft_id)
        if isinstance(ev, PickEvent):
            return session.on_pick(ev.card_id)
        if isinstance(ev, PoolEvent):
            session.on_pool(ev.card_ids)
            return True
        return False
    if q is not None:
        q.put(apply)
        return True
    return apply()


def cmd_overlay(args, ratings: Ratings) -> int:
    log = find_log_path(args.log)
    if not log:
        print("Could not find Player.log. Pass --log <path>.\n"
              "  Windows: %APPDATA%\\..\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log\n"
              "  macOS:   ~/Library/Logs/Wizards Of The Coast/MTGA/Player.log")
        return 2
    print(f"watching {log}")
    resolver = _resolver(args, ratings)
    profile = None
    if not args.no_profile:
        from .playstyle import build_profile
        profile = build_profile(ratings)
        if profile:
            print(f"playstyle: {profile.label()} "
                  f"({profile.n_drafts} drafts, {profile.confidence})")
    session = DraftSession(resolver, ratings, mode=args.mode, profile=profile)
    q: "queue.Queue" = queue.Queue()

    unknown_fh = open(args.dump_unknown, "a", encoding="utf-8") if args.dump_unknown else None

    def on_unknown(obj):
        if unknown_fh:
            try:
                unknown_fh.write(json.dumps(obj)[:4000] + "\n")
                unknown_fh.flush()
            except (OSError, TypeError):
                pass

    def watch():
        tailer = LogTailer(log, from_start=args.from_start)
        for ev in tailer.events(on_unknown=on_unknown if unknown_fh else None):
            _feed(session, ev, q)

    threading.Thread(target=watch, daemon=True).start()

    from .overlay import Overlay
    ui = Overlay(session, q, alpha=args.alpha, frameless=args.frameless,
                 topmost=not args.no_topmost)
    try:
        ui.run()
    finally:
        p = session.save()
        if p:
            print(f"saved draft -> {p}")
        if unknown_fh:
            unknown_fh.close()
    return 0


def cmd_replay(args, ratings: Ratings) -> int:
    """Parse a saved log file end to end and print what the overlay would show."""
    text = Path(args.replay).read_text(encoding="utf-8", errors="replace")
    resolver = _resolver(args, ratings)
    session = DraftSession(resolver, ratings, mode=args.mode)
    n = 0
    for ev in parse_text(text):
        if _feed(session, ev):
            n += 1
            if isinstance(ev, PackEvent) and session.current_scored:
                top = session.current_scored[0]
                print(f"P{session.pack_number}p{session.pick_number}: "
                      f"take {top.card.name} ({top.score:.2f}) - {top.reasons[0]}")
    print(f"\n{n} events applied.")
    sm = session.summary()
    print(f"pool {sm['picks']} cards, colours {sm['colors']}, "
          f"lean {sm['top_name']} ({sm['top_pair']}), interaction {sm['interaction']}")
    print(sm["verdict"])
    p = session.save()
    if p:
        print(f"saved -> {p}")
    return 0


def cmd_import_cards(args, ratings: Ratings) -> int:
    """Replace the generated placeholders with the real card list."""
    from .cardimport import load_cards, build_ratings
    src = Path(args.import_cards)
    cards = load_cards(src)
    print(f"read {len(cards)} records from {src.name}")
    out, stats = build_ratings(cards, ratings.raw, ratings.raw.get("set", "FRA"),
                               prune=args.prune)
    dest = Path(args.out or (Path(__file__).resolve().parent.parent
                             / "data" / "fra_ratings.json"))
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    by_rarity: dict = {}
    for e in out["cards"].values():
        r = e.get("rarity") or "?"
        by_rarity[r] = by_rarity.get(r, 0) + 1
    print(f"imported {stats['added']} cards -> {dest}")
    print("  " + "  ".join(f"{k}:{v}" for k, v in sorted(by_rarity.items())))
    print(f"  kept {stats['kept_hand_grade']} hand-written grades, "
          f"skipped {stats['skipped']} tokens/basics")
    if stats["unmatched"]:
        print(f"\n  {len(stats['unmatched'])} hand-written card(s) are NOT in the real")
        print("  list - those names were guessed wrong during research:")
        for n in stats["unmatched"][:20]:
            print(f"    - {n}")
        if len(stats["unmatched"]) > 20:
            print(f"    ... and {len(stats['unmatched']) - 20} more")
        if stats["pruned"]:
            print(f"  removed all {stats['pruned']} (--prune).")
        else:
            print("  re-run with --prune to drop them.")
    print("\nPractice drafts will now use the real cards, and the overlay will")
    print("recognise them. Grades are still heuristic - run --import-17lands")
    print("once win-rate data exists.")
    return 0


def cmd_import_17lands(args, ratings: Ratings) -> int:
    """Convert a 17Lands card-ratings CSV into the ratings file.

    Accepts any CSV with a name column and a win-rate column (GIH WR preferred).
    Win rates may be 0-1 or 0-100.
    """
    import csv
    src = Path(args.import_17lands)
    rows = list(csv.DictReader(src.open(encoding="utf-8-sig")))
    if not rows:
        print("empty CSV")
        return 2
    cols = rows[0].keys()
    name_col = next((c for c in cols if c.strip().lower() in ("name", "card", "card name")), None)
    wr_col = next((c for c in cols if "gih" in c.lower() and "wr" in c.lower()), None) \
        or next((c for c in cols if "gih" in c.lower()), None) \
        or next((c for c in cols if "wr" in c.lower()), None)
    if not name_col or not wr_col:
        print(f"could not find name/winrate columns in: {list(cols)}")
        return 2
    print(f"using '{name_col}' and '{wr_col}'")

    def grade(wr: float) -> float:
        if wr > 1.5:
            wr /= 100.0
        # 50% GIH WR ~ 3.0, 60% ~ 4.5, clamped to the 0-5 limited scale.
        return max(0.0, min(5.0, round(3.0 + (wr - 0.50) * 15.0, 2)))

    cards = dict(ratings.cards)
    n = 0
    for r in rows:
        nm = (r.get(name_col) or "").strip()
        raw = (r.get(wr_col) or "").strip().rstrip("%")
        if not nm or not raw:
            continue
        try:
            g = grade(float(raw))
        except ValueError:
            continue
        entry = dict(cards.get(nm, {}))
        entry["grade"] = g
        entry["source"] = "17lands"
        cards[nm] = entry
        n += 1
    out = dict(ratings.raw)
    out["cards"] = cards
    out["confidence"] = "data"
    out["source"] = f"17Lands import from {src.name} ({n} cards) merged over the pre-release prior"
    dest = Path(args.out or (Path(__file__).resolve().parent.parent / "data" / "fra_ratings.json"))
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"imported {n} card ratings -> {dest}")
    print("The overlay will now say 'data' instead of 'eval'.")
    return 0


def cmd_selftest(ratings: Ratings) -> int:
    from .arenadb import CardInfo as CI
    ok = True
    premier = ('[UnityCrossThreadLogger]<== Draft.Notify '
               '{"draftId":"x","SelfPick":1,"SelfPack":1,"PackCards":"1,2,3"}')
    evs = list(parse_text(premier))
    ok &= len(evs) == 1 and isinstance(evs[0], PackEvent) and evs[0].card_ids == [1, 2, 3]
    print(f"  parse premier pack ......... {'ok' if ok else 'FAIL'}")

    pack = [CI(1, "Denzilore Fatehold", "WU", "mythic", "FRA", 4),
            CI(2, "Prudent Fateseer", "WU", "common", "FRA", 3),
            CI(3, "Hallway Heckler", "BR", "common", "FRA", 2)]
    pool = PoolState(mode="draft")
    sc = score_pack(pack, pool, ratings, 1, 1)
    bomb_first = sc[0].card.name == "Denzilore Fatehold"
    print(f"  bomb ranks first ........... {'ok' if bomb_first else 'FAIL'}")
    ok &= bomb_first

    for _ in range(6):
        pool.add(CI(9, "Prudent Fateseer", "WU", "common", "FRA", 3))
    sc2 = score_pack(pack, pool, ratings, 2, 8)
    off = next(s for s in sc2 if s.card.name == "Hallway Heckler")
    penalised = any("off-colour" in r for r in off.reasons)
    print(f"  off-colour penalty late .... {'ok' if penalised else 'FAIL'}")
    ok &= penalised

    from .analysis import archetype_affinity, splash_advice
    bomb = CI(1, "Denzilore Fatehold", "WU", "mythic", "FRA", 4, "Creature", "{2}{W}{U}")
    aff = archetype_affinity(bomb, ratings)
    ok_aff = bool(aff) and aff[0]["pair"] == "WU"
    print(f"  affinity picks WU ......... {'ok' if ok_aff else 'FAIL'}")
    ok &= ok_aff
    single = CI(2, "Test Wipe", "", "rare", "FRA", 5, "Sorcery", "{4}{W}")
    sp = splash_advice(single, ratings)
    ok_sp = sp["ease"] == "easy"
    print(f"  single pip is splashable .. {'ok' if ok_sp else 'FAIL (' + sp['ease'] + ')'}")
    ok &= ok_sp
    gold = CI(3, "Test Gold", "BR", "uncommon", "FRA", 3, "Creature", "{1}{B}{R}")
    ok_g = splash_advice(gold, ratings)["ease"] == "hard"
    print(f"  gold is not splashable .... {'ok' if ok_g else 'FAIL'}")
    ok &= ok_g

    lean = pool.archetype_lean(ratings)[0][0]
    print(f"  archetype lean detected .... {'ok (' + lean + ')' if lean == 'WU' else 'FAIL (' + lean + ')'}")
    ok &= lean == "WU"
    return 0 if ok else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="mtga-coach",
        description="Read-only MTG Arena draft/sealed overlay and trainer for Reality Fracture.")
    p.add_argument("--log", help="path to Player.log")
    p.add_argument("--card-db", help="path to Raw_CardDatabase_*.mtga")
    p.add_argument("--card-map", metavar="JSON",
                   help="fallback grpId->name map, if Arena's database cannot be read")
    p.add_argument("--ratings", help="path to a ratings json")
    p.add_argument("--mode", choices=["draft", "sealed"], default="draft")
    p.add_argument("--offline", action="store_true", help="never touch the network")
    p.add_argument("--refresh-cards", action="store_true", help="rebuild the card-name cache")
    p.add_argument("--from-start", action="store_true", help="read the log from the beginning")
    p.add_argument("--alpha", type=float, default=0.93)
    p.add_argument("--frameless", action="store_true")
    p.add_argument("--no-topmost", action="store_true")
    p.add_argument("--dump-unknown", metavar="FILE",
                   help="log payloads the parser did not recognise (send me this file)")
    p.add_argument("--replay", metavar="FILE", help="parse a saved log instead of watching")
    p.add_argument("--review", action="store_true", help="grade your saved drafts")
    p.add_argument("--playstyle", action="store_true",
                   help="profile how you draft, and what would stretch you")
    p.add_argument("--no-profile", action="store_true",
                   help="do not use your playstyle in the overlay")
    p.add_argument("--quiz", action="store_true", help="replay real packs and test your picks")
    p.add_argument("--drills", action="store_true", help="concept drills (no drafts needed)")
    p.add_argument("--practice", action="store_true",
                   help="draft a full pod against bots - no Arena needed")
    p.add_argument("--practice-sealed", action="store_true",
                   help="open six packs and build a sealed deck")
    p.add_argument("--coach", action="store_true",
                   help="practice with the model's picks shown BEFORE you choose")
    p.add_argument("--silent", action="store_true",
                   help="practice with no feedback until the end")
    p.add_argument("--auto", action="store_true", help="let the model draft (a demo)")
    p.add_argument("--seats", type=int, default=8)
    p.add_argument("--gui", action="store_true",
                   help="practice in a window with card images and hover detail")
    p.add_argument("--no-art", action="store_true",
                   help="--gui without downloading card images")
    p.add_argument("--card-scale", type=float, default=1.0,
                   help="card size in the window (e.g. 1.3)")
    p.add_argument("--real-only", action="store_true",
                   help="review/playstyle: ignore practice drafts")
    p.add_argument("--hard", action="store_true", help="quiz only on picks you got wrong")
    p.add_argument("-n", type=int, default=10, help="questions per session")
    p.add_argument("--seed", type=int)
    p.add_argument("--import-cards", metavar="FILE",
                   help="rebuild ratings from a real card list "
                        "(Scryfall JSON, MTGJSON, or CSV)")
    p.add_argument("--prune", action="store_true",
                   help="--import-cards: drop hand-written cards the real list lacks")
    p.add_argument("--import-17lands", metavar="CSV")
    p.add_argument("--out", metavar="JSON", help="where --import-17lands writes")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)

    ratings = Ratings.load(args.ratings)

    if args.selftest:
        print("selftest")
        return cmd_selftest(ratings)
    if args.import_cards:
        return cmd_import_cards(args, ratings)
    if args.import_17lands:
        return cmd_import_17lands(args, ratings)
    _banner(ratings)
    if args.drills:
        from .quiz import run_drills
        run_drills(args.n, args.seed)
        return 0
    if args.quiz:
        from .quiz import run_pack_quiz
        run_pack_quiz(ratings, DRAFT_DIR, args.n, args.seed, hard_only=args.hard)
        return 0
    if args.practice or args.practice_sealed:
        from .sim import run_draft, run_sealed
        profile = None
        if not args.no_profile:
            from .playstyle import build_profile
            profile = build_profile(ratings)
        if args.practice_sealed:
            run_sealed(ratings, args.seed, auto=args.auto, profile=profile)
        elif args.gui:
            try:
                from .gui import run_gui
                run_gui(ratings, args.seed, seats=args.seats, profile=profile,
                        art_enabled=not (args.no_art or args.offline),
                        scale=args.card_scale)
            except RuntimeError as e:
                print(f"\n{e}\n\nThe terminal draft needs none of that:"
                      "\n  python run_overlay.py --practice")
                return 2
        else:
            run_draft(ratings, args.seed, seats=args.seats, coach=args.coach,
                      auto=args.auto, feedback=not args.silent, profile=profile)
        return 0
    if args.playstyle:
        from .playstyle import build_profile, report
        print(report(build_profile(ratings, real_only=args.real_only), ratings))
        return 0
    if args.review:
        print(review_all(ratings, real_only=args.real_only))
        return 0
    if args.replay:
        return cmd_replay(args, ratings)
    return cmd_overlay(args, ratings)
