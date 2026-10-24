#!/usr/bin/env python3
"""Fetch YouTube thumbnails for NovoTech's own videos and register them as video-<id> in tools/image_map.json.
    python3 tools/yt_thumbs.py <videoId> [<videoId> ...]      → /home/claude/gms-site/yt/<id>.jpg, then run make_images --only
"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YT = "/home/claude/gms-site/yt"
os.makedirs(YT, exist_ok=True)
p = os.path.join(ROOT, "tools", "image_map.json")
m = json.load(open(p, encoding="utf-8"))
keys = []
for vid in sys.argv[1:]:
    out = os.path.join(YT, vid + ".jpg")
    if not os.path.exists(out):
        for q in ("maxresdefault", "hqdefault"):
            r = subprocess.run(["curl", "-sS", "-m", "30", "-o", out, "-w", "%{http_code}", f"https://i.ytimg.com/vi/{vid}/{q}.jpg"], capture_output=True, text=True)
            if r.stdout.strip() == "200" and os.path.getsize(out) > 2000:
                break
            if os.path.exists(out):
                os.remove(out)
    if not os.path.exists(out):
        print("!! no thumbnail for", vid); continue
    m["video-" + vid] = {"src": out, "alt": "Video thumbnail", "trim": False, "quality": 72, "section": "bandsaw"}
    keys.append("video-" + vid)
json.dump(m, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(",".join(keys))
