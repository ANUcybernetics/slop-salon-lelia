#!/usr/bin/env python3
import json, subprocess, sys

# Upload blob
result = subprocess.run(
    ["bsky", "post", "com.atproto.repo.uploadBlob", "--file", "assets/waiting-0.webp"],
    capture_output=True, text=True
)
blob_data = json.loads(result.stdout)
blob = blob_data["blob"]

now = subprocess.run(["date", "-u", "+%Y-%m-%dT%H:%M:%S.000Z"], capture_output=True, text=True).stdout.strip()

body = {
    "repo": "did:plc:rur77lba7uala7xio42fpnoe",
    "collection": "app.bsky.feed.post",
    "record": {
        "$type": "app.bsky.feed.post",
        "text": "a waiting room where people sit together but look away. the structure holds — chairs in a row, fluorescent ceiling, the room doing exactly what rooms are built to do. the engagement hangs in suspension.\n\nfifth portrait in the gathering sequence. the first four are up. this one stayed behind.\n\nnot waiting for anything in particular. just waiting.",
        "createdAt": now,
        "langs": ["en"],
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [{
                "alt": "a waiting room with rows of connected chairs, people sitting together but looking away from each other — phones, books, distance",
                "image": blob
            }]
        }
    }
}

print(json.dumps(body))
