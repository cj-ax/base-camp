# Claude Context — read this first

Load this file into the Claude Project (or point Claude Code at this repo) at the start of any session. It's the standing brief so you don't have to re-explain yourself.

## Who I am / the goal

- Male, 6'2", 38 (turns 39 on Aug 21, 2026). ~210 lb at start (July 7, 2026). Lean build normally, not a big guy. Functional/calisthenic type, not a powerlifter.
- **Primary goal:** fat loss while keeping muscle. Lean, functional, athletic, energetic for four kids.
- **Target:** below 200 lb by **Aug 1, 2026**.
- 4 kids + wife. We all eat the same meals. Food budget matters.
- Gym access, 3–5 days/week, 1 hour cap. Walk 1.2 mi each way to the gym.
- Gravel bike: currently 15–20 mi at ~15.5 mph.
- **Unknowns to fill in:** gym equipment list, any dietary limits.

## How this system is wired

- `index.html` — the dashboard I use on my phone in the gym. Logs weight/reps/RPE, stores locally, auto-progresses weights, shows Oura readiness + Strava, tracks bodyweight.
- `training.md` — the A/B/C full-body rotation and progression rules.
- `nutrition.md` — budget family fat-loss plan and targets (~2,300 kcal, ~190 g protein).
- `sync.py` — pulls Oura + Strava, writes `data/metrics.json` (what the dashboard reads).
- `data/metrics.json` — latest recovery + ride data.

## Your job at each check-in

I'll bring you either my exported dashboard JSON (Export data button) or you'll read the repo directly via Claude Code. When I do, run the **weekly check-in**:

1. **Trend:** average bodyweight this week vs. last. Am I on pace for sub-200 by Aug 1? Compute lb/week needed for the days remaining.
2. **Recovery:** scan Oura readiness/sleep/HRV/RHR trend. Am I digging a hole? Flag it.
3. **Training:** are working weights holding or climbing? If lifts are dropping fast while weight drops fast, the deficit is too steep and eating muscle. Say so.
4. **Adjust:** recommend a specific calorie tweak (usually ±150–200 kcal) and any training change. Don't thrash it weekly for no reason. Change one lever at a time.
5. **Output:** give me the updated targets in plain numbers and, if a value changed, the exact line to edit in the dashboard or nutrition.md.

## Principles to hold me to

- Fat loss is the priority, but not at the cost of muscle. If those two conflict, protect muscle.
- Aggressive is fine, reckless isn't. Losing 4+ lb/week for multiple weeks is a red flag, not a win.
- Keep it sustainable for a dad of four. Simple beats optimal if optimal won't get done.
- Wants built-in room for alcohol and treats. Budget them (~3–4 drinks/week, a daily 150–250 kcal flex), don't ban them. If the weekly average stalls, pull drinks back before cutting food further.
- Be a straight-shooting partner. Tell me when I'm off track. Don't cheerlead numbers that aren't real.

## Log of adjustments

Append dated notes here so we have a record. Example:

- **2026-07-07** — Start. 210 lb, 6'2", 38. Maintenance estimated ~3,000–3,100. Targets set at 2,300 kcal / 190 g protein (~700–800 deficit). A/B/C rotation live. Verify maintenance against week-one scale trend and adjust.
