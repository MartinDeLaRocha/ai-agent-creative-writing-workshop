# AIRemember contribution (Pollinations edition)

This folder contains a contribution intended for
[ronibandini/AIRemember](https://github.com/ronibandini/AIRemember).

**Why it is here:** the available GitHub credentials have only READ access to
`ronibandini/AIRemember` and cannot push a branch, create a fork, or open a PR
there. The files are kept here so the work is not lost and can be moved into
the target repo with a writable credential.

## Contents

- `aiRememberPollinations.py` — standalone no-key version using the Pollinations
  free text API, with CLI options, robust evaluation parsing, deduplication,
  rate-limit backoff and `--dry-run`.
- `README-Pollinations.md` — documentation and usage.
- `test_pollinations.py` — offline tests (4 passing).
- `README-original.md` — copy of the original AIRemember README for reference.

## Additional fix for the original repo

`aiRememberUpload.py` in `ronibandini/AIRemember` has a pre-existing syntax
error: `evaluarTexto()` opens a `try:` at line 91 that is never closed before
`def recuerdo()` at line 118. The missing handler is:

```python
    except Exception as e:
        print(f"Error en la evaluación: {e}")
        return None
```

Insert it after the inner `except Exception` block (around line 116) and the
original script compiles again. This fix was verified locally against a clone.

## Verification performed

- `python test_pollinations.py` — all 4 tests pass.
- `python aiRememberPollinations.py --count 2 --output /tmp/aire.txt` — two real
  "Me acuerdo" lines generated through Pollinations; rate-limit backoff fired
  and the run completed.
