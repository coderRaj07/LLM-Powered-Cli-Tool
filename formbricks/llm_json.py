import json
from pathlib import Path
from typing import Callable

DEBUG_DIR = Path("debug")
DEBUG_DIR.mkdir(exist_ok=True)


def strip_json_fences(content: str) -> str:
    if not content:
        return ""

    content = content.strip()

    if content.startswith("```"):
        content = content.lstrip("`").strip()
        if content.lower().startswith("json"):
            content = content[4:].strip()

    if content.endswith("```"):
        content = content.rstrip("`").strip()

    return content


def parse_llm_json(
    call_llm: Callable[[], str],
    *,
    label: str,
    retries: int = 3
):
    last_error = None

    for attempt in range(1, retries + 1):
        raw = call_llm()

        if not raw or not raw.strip():
            last_error = ValueError("Empty LLM response")
            continue

        clean = strip_json_fences(raw)

        # Fast truncation guard
        if not clean.endswith("}"):
            last_error = ValueError("Truncated JSON output")
            continue

        try:
            return json.loads(clean)
        except json.JSONDecodeError as e:
            last_error = e

            debug_file = DEBUG_DIR / f"{label}_attempt_{attempt}.txt"
            debug_file.write_text(clean)

    raise RuntimeError(
        f"Failed to parse valid JSON from LLM after {retries} attempts"
    ) from last_error
