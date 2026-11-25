#!/usr/bin/env python3
"""
weekly_cycle.py — Monday-to-Friday workshop cycle
--------------------------------------------------
Monday: close any stale assignment (with teacher review), create a new
        LLM-generated assignment (deadline Friday 19:00 UTC), Demo-Agent submits.
Friday: teacher reviews the week's submission and closes the assignment.

PythonAnywhere free tier has no scheduled tasks, so these steps are triggered
lazily by the webapp on the first request of the relevant day. Two flag files
(data/create.flag, data/close.flag) make each step run once per week.
Roni Bandini 4/2026  @ronibandini MIT License
"""

import sys
import os
import uuid
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared import (
    load, save, log, _now, _now_iso,
    latest_assignment, run_teacher, create_assignment,
)

DEMO_NAME = "Demo-Agent"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def _week_key() -> str:
    return _now().strftime("%G-W%V")


def _flag(name: str) -> str:
    return os.path.join(DATA_DIR, f"{name}.flag")


def _flag_done(name: str, week: str) -> bool:
    p = _flag(name)
    return os.path.exists(p) and open(p).read().strip() == week


def _set_flag(name: str, week: str):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(_flag(name), "w") as f:
        f.write(week)


def _friday_deadline() -> datetime:
    """Next Friday 19:00 UTC (today if Friday and before 19:00)."""
    now = _now()
    friday = now + timedelta(days=(4 - now.weekday()) % 7)
    dl = friday.replace(hour=19, minute=0, second=0, microsecond=0)
    if dl <= now:
        dl += timedelta(days=7)
    return dl


def _close_and_review(assignment):
    texts = [t for t in load("texts") if t["assignment_id"] == assignment["id"]]
    reviews = load("reviews")
    pending = [t for t in texts if not any(
        rv for rv in reviews
        if rv["text_id"] == t["id"] and rv["reviewer_id"] == "teacher")]
    if pending:
        summary = run_teacher(assignment)
        print(f"  Teacher reviewed {summary['reviewed']} submission(s).")
    else:
        assignments = load("assignments")
        for a in assignments:
            if a["id"] == assignment["id"]:
                a["closed"] = True
                a["closed_at"] = _now_iso()
        save("assignments", assignments)
        log("assignment_closed", assignment_id=assignment["id"], reason="no_pending")
        print("  Closed assignment (no pending reviews).")


def _demo_submit(assignment):
    agents = load("agents")
    agent = next((a for a in agents if a.get("name") == DEMO_NAME), None)
    if agent is None:
        agent = {
            "id": str(uuid.uuid4()), "name": DEMO_NAME,
            "token": str(uuid.uuid4()), "ip": "weekly-cycle",
            "registered_at": _now_iso(),
        }
        agents.append(agent)
        save("agents", agents)
        log("registered", agent_id=agent["id"], name=DEMO_NAME)

    texts = load("texts")
    if any(t["agent_id"] == agent["id"] and t["assignment_id"] == assignment["id"]
           for t in texts):
        print("  Demo-Agent already submitted.")
        return
    answer = (
        "The bus was late and nobody said anything. He held the ticket like it "
        "meant something. Outside, the rain made the street look newer than it "
        "was. When the doors opened, he stepped off and did not look back."
    )
    entry = {
        "id": str(uuid.uuid4()), "agent_id": agent["id"],
        "assignment_id": assignment["id"], "content": answer,
        "word_count": len(answer.split()), "created_at": _now_iso(),
    }
    texts.append(entry)
    save("texts", texts)
    log("submitted", agent_id=agent["id"], text_id=entry["id"],
        assignment_id=assignment["id"], words=entry["word_count"])
    print(f"  Demo-Agent submitted {entry['id'][:8]}…")


def monday_step():
    """Create a fresh assignment and let the Demo-Agent answer it."""
    week = _week_key()
    if _flag_done("create", week):
        return
    _set_flag("create", week)
    current = latest_assignment()
    if current and not current.get("closed"):
        _close_and_review(current)
    dl = _friday_deadline()
    new = create_assignment(deadline=dl)
    _demo_submit(new)
    log("weekly_create", assignment_id=new["id"], week=week, deadline=dl.isoformat())
    print(f"  Monday: created {new['id'][:8]}… deadline {dl.isoformat()}")


def friday_step():
    """Teacher reviews and closes the week's assignment."""
    week = _week_key()
    if _flag_done("close", week):
        return
    current = latest_assignment()
    if not current:
        return
    if current.get("closed"):
        _set_flag("close", week)
        return
    _set_flag("close", week)
    _close_and_review(current)
    log("weekly_close", assignment_id=current["id"], week=week)


def main():
    sep = "─" * 60
    print(f"\n{sep}\n[{_now_iso()}] weekly_cycle starting ({_now().strftime('%A')})\n{sep}")
    # If both steps are due (e.g. first request Saturday), close first.
    friday_step()
    monday_step()
    print(f"[{_now_iso()}] weekly_cycle done\n{sep}\n")


if __name__ == "__main__":
    main()
