"""Vercel serverless function: mints a LiveKit room-join token.

Deployed as /api/livekit_token (not /api/token — that name would shadow
Python's stdlib `token` module, which `tokenize` imports internally). Reads
LIVEKIT_API_KEY / LIVEKIT_API_SECRET / LIVEKIT_URL from Vercel project
environment variables (set these in the Vercel dashboard, not from a .env
file — .env is not deployed).

Same logic as token_server.py (used for local dev); kept as a separate file
because Vercel's Python runtime maps one function per file under /api.
"""

import os
import uuid

from flask import Flask, jsonify
from livekit import api

app = Flask(__name__)

ROOM_NAME = "kings-hospital-demo"


@app.route("/api/livekit_token")
def get_token():
    identity = f"patient-{uuid.uuid4().hex[:8]}"

    access_token = (
        api.AccessToken(os.environ["LIVEKIT_API_KEY"], os.environ["LIVEKIT_API_SECRET"])
        .with_identity(identity)
        .with_name(identity)
        .with_grants(api.VideoGrants(room_join=True, room=ROOM_NAME))
    )

    return jsonify(
        {
            "token": access_token.to_jwt(),
            "url": os.environ["LIVEKIT_URL"],
            "room": ROOM_NAME,
            "identity": identity,
        }
    )
