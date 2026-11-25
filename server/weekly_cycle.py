#!/usr/bin/env python3
"""
weekly_cycle.py — weekly workshop cycle (AMD LLM version)
---------------------------------------------------------
Closes the current assignment, runs the Teacher LLM review, then opens a
fresh assignment with a 7-day deadline. Designed to be run once per week
via a PythonAnywhere scheduled task.

The config's assignment.duration_hours is 168 (7 days), so create_assignment()
sets the deadline correctly. Roni Bandini 4/2026  @ronibandini MIT License
"""

import sys
import os
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shared import (
    load, save, log, _now, _now_iso,
    latest_assignment, is_open, run_teacher, create_assignment,
)


def _close_without_review(assignment: dict):
    assignments = load("assignments")
    for a in assignments:
        if a["id"] == assignment["id"]:
            a["closed"] = True
            a["closed_at"] = _now_iso()
    save("assignments", assignments)
    log("assignment_closed", assignment_id=assignment["id"], reason="no_submissions")


def main():
    start = _now_iso()
    sep = "─" * 60
    print(f"\n{sep}\n[{start}] weekly_cycle: starting\n{sep}")

    current = latest_assignment()

    if current is None:
        print("  No existing assignment — skipping close/review.")
    elif current.get("closed"):
        print(f"  Assignment {current['id'][:8]}… already closed — skipping.")
    else:
        print(f"  Closing assignment : {current['id'][:8]}…")
        print(f"  Prompt             : {current['prompt'][:80]}")
        texts = [t for t in load("texts") if t["assignment_id"] == current["id"]]
        reviews = load("reviews")
        pending = [
            t for t in texts
            if not any(rv for rv in reviews
                       if rv["text_id"] == t["id"] and rv["reviewer_id"] == "teacher")
        ]
        print(f"  Submissions: {len(texts)} | pending teacher reviews: {len(pending)}")
        if not texts:
            _close_without_review(current)
            print("  No submissions — closed with no reviews.")
        else:
            summary = run_teacher(current)
            print(f"  Teacher reviewed {summary['reviewed']}, skipped {summary['skipped']}.")

    # Open a new weekly assignment (deadline from config: duration_hours=168)
    new = create_assignment()
    print(f"\n  New assignment ID: {new['id'][:8]}…")
    print(f"  Prompt           : {new['prompt']}")
    print(f"  Deadline         : {new['deadline']}")
    print(f"\n[{_now_iso()}] weekly_cycle: done\n{sep}\n")


if __name__ == "__main__":
    main()
