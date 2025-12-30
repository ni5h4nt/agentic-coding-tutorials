#!/usr/bin/env python3
"""Quality gate for agent output."""
import json
import sys
from pathlib import Path

def main() -> None:
    input_data = json.load(sys.stdin)
    transcript_path = input_data.get("transcript_path", "")

    if transcript_path:
        transcript = Path(transcript_path).expanduser()
        if transcript.exists():
            content = transcript.read_text()
            # Check if agent actually did something
            if "Write" not in content and "Edit" not in content:
                print(json.dumps({
                    "decision": "block",
                    "reason": "Agent completed without creating files. Please try again."
                }))
                sys.exit(2)

    print("✓ Agent output validated", file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
