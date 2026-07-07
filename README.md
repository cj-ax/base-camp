# Base Camp — a fitness system

A phone dashboard, a training plan, a nutrition plan, and an automatic data pipeline that pulls your Oura recovery and Strava rides. Goal: lean out to sub-200 by Aug 1 without losing muscle, and stay lean and functional for the long run.

## What's in here

| File | What it does |
|------|--------------|
| `index.html` | The dashboard. Open it on your phone, add to home screen, use it in the gym. |
| `training.md` | The A/B/C full-body rotation and how weights progress. |
| `nutrition.md` | Budget family fat-loss plan and daily targets. |
| `claude-context.md` | Load this into Claude so any session picks up your full context. |
| `sync.py` | Pulls Oura + Strava, writes `data/metrics.json`. |
| `data/metrics.json` | Latest recovery + ride data the dashboard reads. |
| `.github/workflows/sync.yml` | Runs the sync every morning in the cloud, for free. |

## How "automatic" actually works

Two data streams, handled two ways:

1. **Recovery + rides (Oura, Strava)** flow in automatically. `sync.py` pulls them and writes `metrics.json`, GitHub Actions runs it every morning and commits the result, and the dashboard reads it. Nothing to keep running on your end.
2. **Your workout log** (weights, reps, bodyweight) lives on your phone in the dashboard. It auto-progresses your weights on its own, so day to day you don't need me in the loop. Once a week you hit **Export data** and bring that file to me for a check-in, where I look at the trend and adjust calories and training. Weekly is the right cadence anyway. Daily tweaks just create noise.

I don't run on a timer, so the honest version is: the pipeline keeps your *data* current and your dashboard live every day, and we recalibrate together every week.

## Setup

### 1. Use the dashboard (do this first, works immediately)
- Open `index.html` on your phone.
- iPhone: Share → Add to Home Screen. Android: menu → Add to Home Screen. Now it opens like an app.
- It works fully offline. Log lifts and bodyweight from day one. The Oura/Strava panels stay blank until you do step 3.

Easiest way to get it on your phone and keep it updated: host the repo on **GitHub Pages** (free). In the repo settings, Pages → deploy from `main`. Your dashboard lives at `https://<you>.github.io/<repo>/`. Add *that* to your home screen.

### 2. Feed me the context
- Start a Claude Project, upload `claude-context.md`, `training.md`, and `nutrition.md`.
- Or point Claude Code at this repo and it reads everything directly.

### 3. Wire up Oura + Strava (optional but worth it)
- **Oura token:** make a Personal Access Token at https://cloud.ouraring.com/personal-access-tokens
- **Strava app:** create one at https://www.strava.com/settings/api, then do the one-time OAuth to get a `refresh_token` with `activity:read` scope. (Ask Claude Code to walk you through the token exchange; it's a two-request flow.)
- Test locally:
  ```bash
  OURA_TOKEN=xxx STRAVA_CLIENT_ID=xxx STRAVA_CLIENT_SECRET=xxx STRAVA_REFRESH_TOKEN=xxx python sync.py
  ```
  You should see `metrics.json` fill in.

### 4. Automate it
- Push the repo to GitHub.
- Repo → Settings → Secrets and variables → Actions. Add `OURA_TOKEN`, `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, `STRAVA_REFRESH_TOKEN`.
- The workflow runs every morning. Trigger it once manually from the Actions tab to confirm.

## The weekly check-in

Every week: open the dashboard, hit **Export data**, bring me the file (or just tell Claude Code to read the repo). I'll check pace to goal, recovery trend, and whether your lifts are holding, then adjust your targets and tell you exactly what to change.

## Adjusting numbers

Your calorie and protein targets live in one place in `index.html` (the `defaults.profile` block) and in `nutrition.md`. When we change them at a check-in, I'll give you the exact line. Start weight, goal, and date live there too.
