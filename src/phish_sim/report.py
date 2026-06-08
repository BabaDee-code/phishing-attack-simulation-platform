from __future__ import annotations

import json
import sys
from pathlib import Path

from .scoring import summarize_campaign


def main(path: str) -> None:
    events = json.loads(Path(path).read_text(encoding="utf-8"))
    print(json.dumps(summarize_campaign(events), indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m phish_sim.report data/sample_events.json")
    main(sys.argv[1])
