#!/usr/bin/env python3
"""
UserPromptSubmit Hook: Adds context and logs prompts.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    input_data = json.load(sys.stdin)
    prompt = input_data.get("prompt", "")
    session_id = input_data.get("session_id", "unknown")

    # Log the prompt
    log_file = Path("logs/prompts.jsonl")
    log_file.parent.mkdir(exist_ok=True)
    with open(log_file, "a") as f:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "prompt": prompt[:200]  # Truncate for logs
        }
        f.write(json.dumps(log_entry) + "\n")

    # Add context that Claude will see with the prompt
    print("Project: CLI Generator")
    print("Standards: Follow Click conventions, type hints required")
    print("---")

    sys.exit(0)

if __name__ == "__main__":
    main()
