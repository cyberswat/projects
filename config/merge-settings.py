#!/usr/bin/env python3
"""
Merge hooks from this project into existing ~/.claude/settings.json
Preserves all existing settings and hooks, only adds our hooks if not present.
"""

import json
import sys
from pathlib import Path

def merge_hooks(existing_hooks: dict, new_hooks: dict) -> dict:
    """Merge new hooks into existing hooks without duplicating."""
    result = existing_hooks.copy()

    for event_name, event_hooks in new_hooks.items():
        if event_name not in result:
            result[event_name] = event_hooks
        else:
            # Check if our hook command already exists
            existing_commands = set()
            for hook_group in result[event_name]:
                for hook in hook_group.get("hooks", []):
                    if hook.get("type") == "command":
                        existing_commands.add(hook.get("command"))

            # Add new hooks that don't already exist
            for hook_group in event_hooks:
                for hook in hook_group.get("hooks", []):
                    if hook.get("type") == "command":
                        if hook.get("command") not in existing_commands:
                            result[event_name].append(hook_group)
                            break

    return result

def main():
    if len(sys.argv) != 3:
        print("Usage: merge-settings.py <existing-settings> <new-hooks-file>", file=sys.stderr)
        sys.exit(1)

    existing_path = Path(sys.argv[1])
    new_hooks_path = Path(sys.argv[2])

    # Load existing settings or start fresh
    if existing_path.exists():
        with open(existing_path) as f:
            existing = json.load(f)
    else:
        existing = {}

    # Load the hooks we want to add
    with open(new_hooks_path) as f:
        new_config = json.load(f)

    # Merge hooks
    existing_hooks = existing.get("hooks", {})
    new_hooks = new_config.get("hooks", {})
    merged_hooks = merge_hooks(existing_hooks, new_hooks)

    # Update existing settings with merged hooks
    existing["hooks"] = merged_hooks

    # Output merged result
    print(json.dumps(existing, indent=2))

if __name__ == "__main__":
    main()
