#!/usr/bin/env python3
"""
sync.py — pull Oura (recovery) + Strava (rides) and write data/metrics.json,
which index.html reads. Run it on a schedule (cron or GitHub Actions) or by hand.

Setup:
  Oura   -> https://cloud.ouraring.com/personal-access-tokens  (make a token)
  Strava -> https://www.strava.com/settings/api  (make an app: client id + secret,
            then do the one-time OAuth to get a refresh_token with activity:read scope)

Provide credentials as environment variables (never hard-code them):
  OURA_TOKEN
  STRAVA_CLIENT_ID
  STRAVA_CLIENT_SECRET
  STRAVA_REFRESH_TOKEN

Any missing credential is skipped gracefully. Field names below are current as of
this writing; if a value comes back empty, print the raw response and adjust.
"""

import os, json, datetime, sys
import urllib.request, urllib.parse, urllib.error

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "metrics.json")


def _get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def _post(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def fetch_oura():
    token = os.environ.get("OURA_TOKEN")
    out = {"readiness": None, "sleep": None, "hrv": None, "rhr": None}
    if not token:
        return out
    hdr = {"Authorization": f"Bearer {token}"}
    end = datetime.date.today()
    start = end - datetime.timedelta(days=3)
    q = urllib.parse.urlencode({"start_date": start.isoformat(), "end_date": end.isoformat()})
    base = "https://api.ouraring.com/v2/usercollection"
    try:
        r = _get(f"{base}/daily_readiness?{q}", hdr).get("data", [])
        if r:
            out["readiness"] = r[-1].get("score")
        s = _get(f"{base}/daily_sleep?{q}", hdr).get("data", [])
        if s:
            out["sleep"] = s[-1].get("score")
        # detailed sleep for HRV + lowest heart rate (resting HR proxy)
        d = _get(f"{base}/sleep?{q}", hdr).get("data", [])
        if d:
            last = d[-1]
            out["hrv"] = last.get("average_hrv")
            out["rhr"] = last.get("lowest_heart_rate")
    except urllib.error.HTTPError as e:
        print(f"[oura] HTTP {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"[oura] {e}", file=sys.stderr)
    return out


def fetch_strava():
    cid = os.environ.get("STRAVA_CLIENT_ID")
    secret = os.environ.get("STRAVA_CLIENT_SECRET")
    refresh = os.environ.get("STRAVA_REFRESH_TOKEN")
    if not (cid and secret and refresh):
        return {"lastRide": None}
    try:
        tok = _post("https://www.strava.com/oauth/token", {
            "client_id": cid, "client_secret": secret,
            "grant_type": "refresh_token", "refresh_token": refresh,
        })
        access = tok["access_token"]
        acts = _get(
            "https://www.strava.com/api/v3/athlete/activities?per_page=10",
            {"Authorization": f"Bearer {access}"},
        )
        for a in acts:
            if a.get("type") in ("Ride", "GravelRide", "VirtualRide"):
                miles = a.get("distance", 0) / 1609.34
                mph = a.get("average_speed", 0) * 2.23694
                return {"lastRide": f"{miles:.1f} mi · {mph:.1f} mph"}
        return {"lastRide": None}
    except urllib.error.HTTPError as e:
        print(f"[strava] HTTP {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"[strava] {e}", file=sys.stderr)
    return {"lastRide": None}


def main():
    metrics = {"updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
    metrics.update(fetch_oura())
    metrics.update(fetch_strava())
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print("wrote", DATA_PATH)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
