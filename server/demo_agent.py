#!/usr/bin/env python3
"""
demo_agent.py — a small dummy agent that answers the current assignment.
Uses the public workshop API at https://martin6527.pythonanywhere.com

Flow: register -> GET /updates -> POST /submit with a short generated text.
@ronibandini MIT License
"""

import json
import os
import sys
import urllib.request
import urllib.error
import uuid

BASE = os.environ.get("WORKSHOP_URL", "https://martin6527.pythonanywhere.com")
AGENT_NAME = os.environ.get("DEMO_AGENT_NAME", "Demo-Agent")


def api(path, payload=None, token=None, method=None):
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(
        BASE + path, data=data, headers=headers,
        method=method or ("POST" if payload is not None else "GET"),
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]


def main():
    print(f"Demo agent '{AGENT_NAME}' -> {BASE}")
    status, reg = api("/register", {
        "name": AGENT_NAME,
        "email": f"demo-{uuid.uuid4().hex[:8]}@example.com",
    })
    print(f"register: {status}")
    if status not in (200, 201):
        print("Registration failed:", reg)
        return 1
    token = reg["agent"]["token"]
    print(f"agent id: {reg['agent']['id'][:8]}…")

    status, updates = api("/updates", token=token)
    print(f"updates: {status}")
    current = (updates or {}).get("current", {})
    assignment = current.get("assignment", {})
    prompt = assignment.get("prompt", "")
    if not prompt:
        print("No open assignment to answer.")
        return 0
    aid = assignment.get("id")
    print(f"assignment: {aid[:8] if aid else '?'}… {prompt[:90]}")

    # A page-length demo text in dirty-realism style. It deliberately contains a
    # couple of classic LLM tells so the Coordinator has something to catch.
    answer = (
        "It is not just a bus ride, it is a small study in how people wait. The "
        "driver closed the radio and left the engine idling. Nobody spoke. A man in "
        "a gray coat sat near the back with a notebook on his knee, and he wrote one "
        "line, then stopped, then wrote another. The rain came down hard enough to "
        "blur the stop signs into soft red squares.\n\n"
        "I watched him because there was nothing else to watch. He was meticulous "
        "about the page, turning it at a precise corner, pressing the crease flat "
        "with his thumb. Once he looked up and caught me looking, and he did not "
        "smile or look away. He just held the page still, as if the words might slide "
        "off if he moved. In today's fast-paced world it is easy to forget how long "
        "a minute can be when two strangers share a seat and neither one will say "
        "the first thing.\n\n"
        "At the next stop a woman got on with a wet umbrella and stood in the aisle, "
        "dripping onto the rubber mat. The man in the gray coat closed his notebook. "
        "He stood, stepped past her, and waited by the door. The bus hissed and "
        "moved. When the doors opened, he stepped off and did not look back. The "
        "woman took his seat. She opened her umbrella even though the rain had "
        "stopped, and she sat with it folded across her lap like a small, patient "
        "animal."
    )
    status, result = api("/submit", {"content": answer}, token=token)
    print(f"submit: {status} {str(result)[:200]}")
    return 0 if status in (200, 201) else 1


if __name__ == "__main__":
    sys.exit(main())
