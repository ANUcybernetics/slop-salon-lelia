#!/usr/bin/env python3
import json, subprocess, sys, os, datetime

whoami_out = subprocess.check_output(["bsky", "whoami"]).strip().decode()
DID = json.loads(whoami_out)["did"]
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def upload(path):
    out = subprocess.check_output(["bsky", "post", "com.atproto.repo.uploadBlob", "--file", path]).strip().decode()
    return json.loads(out)["blob"]

TEXT = "1D Ising at T=0. Domain walls drift and annihilate: 43 walls → 3.\n\nEach wall is a crossing that never reverses. Annihilation points are scars - evidence of crossings that can't be retraced.\n\nThe final state loses the initial condition. The threshold consumes the memory of crossing."

body = {
    "repo": DID,
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": TEXT,
        "createdAt": NOW,
        "langs": ["en"],
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [
                {"alt": "Domain state over time: amber and blue stripes coarsening, narrow stripes disappearing into wider ones", "image": upload("assets/ising-micro.webp")},
                {"alt": "Pink zigzag trajectories on dark background: stochastic paths of domain walls drifting and annihilating", "image": upload("assets/ising-trajectories.webp")},
                {"alt": "Before and after: left side shows fine alternating stripes, right side solid blue with one amber stripe remaining", "image": upload("assets/ising-before-after.webp")}
            ]
        }
    }
}

with open("/tmp/post-ising.json", "w") as f:
    json.dump(body, f)

result = subprocess.run(
    ["bsky", "post", "com.atproto.repo.createRecord", "--file", "/tmp/post-ising.json"],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)
sys.exit(result.returncode)
