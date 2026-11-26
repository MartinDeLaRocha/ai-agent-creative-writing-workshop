#!/usr/bin/env python3
"""AIRemember — Pollinations edition.

Generates a book in the "Me acuerdo" style (Joe Brainard / George Perec)
using the Pollinations free text API. No API key required.

Enhancements over the original ollama script:
  - no local model or API key needed
  - CLI configuration (count, output, seeds, examples, evaluation)
  - robust score parsing ("8", "8/10", "Score: 8" all work)
  - anti-LLM-tell rules in the generation prompt
  - near-duplicate filtering against previously written lines
  - rate-limit aware retry/backoff for the free tier (~1 reply / 45s per IP)
  - deterministic `--dry-run` mode for offline testing

Usage:
  python aiRememberPollinations.py --count 10 --output airemember.txt
  python aiRememberPollinations.py --dry-run --count 3
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request

URL = "https://text.pollinations.ai/openai"
MODEL = "openai"

DEFAULT_SEEDS = [
    "la ciudad", "el verano", "la escuela", "el tren", "la lluvia",
    "la abuela", "la bicicleta", "el mar", "la radio", "el invierno",
    "la panadería", "el perro", "la ventana", "la playa", "la noche",
]

DEFAULT_EXAMPLES = [
    "Me acuerdo de la casa de mis abuelos y del olor a café por la mañana.",
    "Me acuerdo de ir en bicicleta por una calle que ya no existe.",
    "Me acuerdo del ruido de la lluvia en el techo de zinc.",
    "Me acuerdo de esperar el tren con mi padre, sin decir nada.",
    "Me acuerdo de un perro que dormía junto a la estufa.",
]

ANTI_LLM = (
    "No uses 'no es X, es Y', ni listas de tres elementos automáticas, "
    "ni palabras de relleno como delve, tapestry, pivotal, intricate, "
    "meticulous, testament, showcase. Lenguaje concreto, desigual, sin "
    "explicaciones moralizantes."
)

SYSTEM = (
    "Sos un escritor que escribe recuerdos breves en español, en el estilo de "
    "Joe Brainard y George Perec. Cada texto es una oración, concreta y "
    "cotidiana, que empieza exactamente con 'Me acuerdo'. " + ANTI_LLM
)

EVAL_SYSTEM = (
    "Sos un editor que puntúa textos del 0 al 10. Dame solo un número entero. "
    "Criterio: 2 puntos por concreción sensorial, 2 por economía, 2 por no "
    "caer en clichés, 2 por sonar a recuerdo real y 2 por empezar con 'Me acuerdo'."
)


def _call(messages: list[dict], max_tokens: int = 160, retries: int = 5) -> str:
    """POST to Pollinations, respecting the free-tier retry hint."""
    payload = json.dumps({"model": MODEL, "messages": messages,
                          "max_tokens": max_tokens, "temperature": 1.0,
                          "top_p": 1.0}).encode()
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                URL, data=payload,
                headers={"Content-Type": "application/json",
                         "User-Agent": "airemember/2.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.load(resp)
            return (data["choices"][0]["message"]["content"] or "").strip()
        except urllib.error.HTTPError as exc:
            last = exc
            body = exc.read().decode(errors="ignore")
            m = re.search(r"Retry after (\d+)s", body)
            wait = int(m.group(1)) + 2 if m else 12 * (attempt + 1)
            if attempt < retries - 1:
                print(f"[rate limit] esperando {wait}s…", flush=True)
                time.sleep(wait)
        except Exception as exc:             # noqa: BLE001
            last = exc
            if attempt < retries - 1:
                time.sleep(6 * (attempt + 1))
    raise RuntimeError(f"Pollinations falló: {last}")


def parse_score(text: str) -> int | None:
    """Accept '8', '8/10', 'Score: 8', 'Puntuación: 8/10'."""
    m = re.search(r"(?<!\d)(10|[0-9])(?!\d)", text or "")
    if not m:
        return None
    value = int(m.group(1))
    return value if 0 <= value <= 10 else None


def normalize(text: str) -> str:
    return re.sub(r"[^a-záéíóúñ ]", "", text.lower()).strip()


def is_valid(line: str) -> bool:
    return line.startswith("Me acuerdo") and "Nota:" not in line


def generate(seeds: list[str], examples: list[str], evaluate: bool) -> tuple[str, int | None]:
    seed = random.choice(seeds)
    example = random.choice(examples)
    user = (
        f"Escribí una oración de 10 a 25 palabras que empiece con 'Me acuerdo'. "
        f"Usá la palabra '{seed}'. Ejemplo de estilo: {example} "
        "Devolvé solo la oración."
    )
    line = _call([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user},
    ])
    score = None
    if evaluate:
        score = parse_score(_call([
            {"role": "system", "content": EVAL_SYSTEM},
            {"role": "user", "content": f"Texto: {line}"},
        ], max_tokens=16))
    return line, score


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="AIRemember — Pollinations edition")
    ap.add_argument("--count", type=int, default=10)
    ap.add_argument("--output", default="airemember.txt")
    ap.add_argument("--seeds-file", help="UTF-8 file with one seed word per line")
    ap.add_argument("--examples-file", help="UTF-8 file with one style example per line")
    ap.add_argument("--evaluate", action="store_true", help="score each line (extra API call)")
    ap.add_argument("--min-score", type=int, default=6)
    ap.add_argument("--dry-run", action="store_true", help="no network; generate fake lines")
    args = ap.parse_args(argv)

    seeds = DEFAULT_SEEDS
    examples = DEFAULT_EXAMPLES
    if args.seeds_file:
        seeds = [x.strip() for x in open(args.seeds_file, encoding="utf-8") if x.strip()]
    if args.examples_file:
        examples = [x.strip() for x in open(args.examples_file, encoding="utf-8") if x.strip()]

    seen: set[str] = set()
    if os.path.exists(args.output):
        seen = {normalize(x) for x in open(args.output, encoding="utf-8") if x.strip()}

    saved = 0
    for i in range(args.count):
        if args.dry_run:
            line, score = f"Me acuerdo de {seeds[i % len(seeds)]}, una tarde cualquiera.", 8
        else:
            line, score = generate(seeds, examples, args.evaluate)
        key = normalize(line)
        if not is_valid(line) or not key or key in seen:
            print(f"[{i+1}] descartado: {line[:70]!r}", flush=True)
            continue
        if args.evaluate and (score is None or score < args.min_score):
            print(f"[{i+1}] descartado por puntaje {score}: {line[:60]!r}", flush=True)
            continue
        seen.add(key)
        with open(args.output, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        saved += 1
        print(f"[{i+1}] guardado (score {score}): {line}", flush=True)
        if not args.dry_run:
            time.sleep(2)
    print(f"Total guardados: {saved} -> {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
