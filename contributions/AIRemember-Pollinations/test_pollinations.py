"""Offline tests for aiRememberPollinations."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiRememberPollinations import is_valid, normalize, parse_score, main


def test_parse_score():
    assert parse_score("8") == 8
    assert parse_score("8/10") == 8
    assert parse_score("Puntuación: 9/10") == 9
    assert parse_score("no number") is None
    assert parse_score("11") is None
    assert parse_score("score 10") == 10


def test_validation():
    assert is_valid("Me acuerdo de la lluvia.")
    assert not is_valid("Recuerdo la lluvia.")
    assert not is_valid("Me acuerdo... Nota: algo")


def test_normalize():
    a = normalize("Me acuerdo del café, ayer.")
    b = normalize("Me acuerdo del café ayer")
    assert a == b


def test_dry_run(tmp_path=None):
    d = tmp_path or tempfile.mkdtemp()
    out = os.path.join(d, "book.txt")
    assert main(["--dry-run", "--count", "3", "--output", out]) == 0
    lines = [x.strip() for x in open(out, encoding="utf-8") if x.strip()]
    assert len(lines) == 3
    assert all(is_valid(x) for x in lines)


if __name__ == "__main__":
    for fn in [test_parse_score, test_validation, test_normalize, test_dry_run]:
        try:
            fn()
            print("PASS", fn.__name__)
        except AssertionError as e:
            print("FAIL", fn.__name__, e)
            raise
