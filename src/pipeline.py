"""Quality-gated snapshot approval entry point."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.quality_gates import require_quality, run_quality_gates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    snapshot = json.loads(Path(args.input).read_text(encoding="utf-8"))
    gates = run_quality_gates(snapshot)
    for gate in gates:
        print(f"{gate.name}: {'PASS' if gate.passed else 'FAIL'} | {gate.detail}")
    require_quality(snapshot)
    print("Snapshot approved for downstream analytics.")


if __name__ == "__main__":
    main()
