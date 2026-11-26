# AIRemember — Pollinations edition

A no-key version of [AIRemember](README.md) that writes a book in the
*"Me acuerdo"* style (Joe Brainard / George Perec) using the **Pollinations free
text API** instead of a local Ollama model.

The original script (`aiRememberUpload.py`) is kept unchanged for reference.

## Enhancements

- **No credentials and no local model** — calls `https://text.pollinations.ai/openai`.
- **CLI configuration** — `--count`, `--output`, `--seeds-file`, `--examples-file`,
  `--evaluate`, `--min-score`, `--dry-run`.
- **Robust evaluation** — accepts `8`, `8/10`, `Puntuación: 8/10`; rejects invalid scores.
- **Anti-LLM prompts** — generation rules forbid negative parallelism
  ("no es X, es Y"), automatic rule-of-three lists and stock AI vocabulary.
- **Deduplication** — normalizes and skips near-duplicate lines, including lines
  already in the output file.
- **Rate-limit aware** — parses the API's "Retry after Ns" hint and waits, so the
  free tier (~1 reply per 45 s per IP) does not abort a run.
- **Offline tests** — `python tests/test_pollinations.py`.

## Usage

```bash
pip install requests

python aiRememberPollinations.py --count 10 --output airemember.txt
python aiRememberPollinations.py --count 5 --evaluate --min-score 7
python aiRememberPollinations.py --seeds-file mis-palabras.txt --examples-file ejemplos.txt
python aiRememberPollinations.py --dry-run --count 3     # no network
```

With `--evaluate`, each line costs a second API call; the free tier then
allows roughly one finished, scored memory per 90 seconds. Without evaluation,
about one memory per 45 seconds.

## Output

Plain UTF-8 text, one "Me acuerdo" sentence per line, appended to `--output`.
Invalid lines (wrong opening, `Nota:`, low score or duplicate) are discarded.
