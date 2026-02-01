#!/usr/bin/env python3
"""
Update project registry on SessionEnd and PreCompact.

Keeps it simple:
- Detect which projects were touched (any file operation)
- Update the project registry with timestamps
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def find_project_root(file_path):
    """Find the git root or directory containing CLAUDE.md for a file path."""
    try:
        path = Path(file_path).resolve()
    except (OSError, ValueError):
        return None

    for parent in [path] + list(path.parents):
        if (parent / '.git').exists():
            return str(parent)
        if (parent / 'CLAUDE.md').exists():
            return str(parent)
        if (parent / '.claude' / 'CLAUDE.md').exists():
            return str(parent)

    return None


def extract_project_roots(transcript_lines):
    """Extract project roots from any file paths in transcript."""
    project_roots = set()
    home = os.path.expanduser('~')

    for line in transcript_lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Tool uses are nested inside message.content
        message = entry.get('message', {})
        content = message.get('content', [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'tool_use':
                    tool_input = item.get('input', {})
                    for key in ['file_path', 'path', 'directory']:
                        path = tool_input.get(key)
                        if path and path.startswith('/'):
                            root = find_project_root(path)
                            # Exclude home dir and .claude config dir
                            if root and root != home and not root.endswith('/.claude'):
                                project_roots.add(root)

    return project_roots


def update_registry(project_roots):
    """Update the project registry with worked timestamps."""
    registry_path = os.path.expanduser('~/.claude/projects.json')

    registry = {"projects": {}}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    today = datetime.now().strftime('%Y-%m-%d')

    for project_root in project_roots:
        project_name = os.path.basename(project_root)
        registry["projects"][project_name] = {
            "path": project_root,
            "last_worked": today
        }

    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)

    return list(project_roots)


def main():
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    transcript_path = hook_input.get('transcript_path')
    if not transcript_path:
        sys.exit(0)

    transcript_path = os.path.expanduser(transcript_path)
    if not os.path.exists(transcript_path):
        sys.exit(0)

    with open(transcript_path, 'r') as f:
        transcript_lines = f.readlines()

    project_roots = extract_project_roots(transcript_lines)

    if project_roots:
        updated = update_registry(project_roots)
        print(f"Registry updated: {', '.join(os.path.basename(p) for p in updated)}", file=sys.stderr)

    sys.exit(0)


if __name__ == '__main__':
    main()
