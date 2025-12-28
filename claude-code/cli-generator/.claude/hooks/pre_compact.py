#!/usr/bin/env python3
"""
PreCompact Hook: Runs before context summarization.
Inject reminders that survive compaction.
"""
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)

        # Remind Claude of critical context before compaction
        print("Remember: Generated CLIs use Click, type hints required.")

        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
