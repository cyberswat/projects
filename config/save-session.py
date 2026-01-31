#!/usr/bin/env python3
"""
Save session notes to CLAUDE.local.md for each project worked on.
Called by Claude Code hooks on SessionEnd and PreCompact.
"""

import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def find_project_root(file_path):
    """Find the git root or directory containing CLAUDE.md for a file path."""
    path = Path(file_path).resolve()

    # Walk up looking for .git or CLAUDE.md
    for parent in [path] + list(path.parents):
        if (parent / '.git').exists():
            return str(parent)
        if (parent / 'CLAUDE.md').exists():
            return str(parent)
        if (parent / '.claude' / 'CLAUDE.md').exists():
            return str(parent)

    return None

def extract_file_paths(transcript_lines):
    """Extract file paths from transcript tool calls."""
    paths = set()

    for line in transcript_lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Look for tool inputs with file paths
        if entry.get('type') == 'tool_use':
            tool_input = entry.get('input', {})
            for key in ['file_path', 'path', 'directory']:
                if key in tool_input and tool_input[key]:
                    paths.add(tool_input[key])

        # Also check tool results for file paths
        if entry.get('type') == 'tool_result':
            content = entry.get('content', '')
            if isinstance(content, str):
                # Look for absolute paths
                found = re.findall(r'(/[a-zA-Z0-9_\-./]+)', content)
                paths.update(found)

    return paths

def extract_project_info(transcript_lines, project_root):
    """Extract relevant information for a specific project from transcript."""
    info = {
        'files_modified': set(),
        'files_read': set(),
        'commands_run': [],
        'assistant_messages': [],
        'user_messages': []
    }

    for line in transcript_lines:
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Track file operations
        if entry.get('type') == 'tool_use':
            tool_name = entry.get('name', '')
            tool_input = entry.get('input', {})

            file_path = tool_input.get('file_path', tool_input.get('path', ''))
            if file_path and file_path.startswith(project_root):
                rel_path = os.path.relpath(file_path, project_root)

                if tool_name in ['Write', 'Edit']:
                    info['files_modified'].add(rel_path)
                elif tool_name == 'Read':
                    info['files_read'].add(rel_path)

            if tool_name == 'Bash':
                cmd = tool_input.get('command', '')
                desc = tool_input.get('description', '')
                if cmd and len(cmd) < 200:  # Skip very long commands
                    info['commands_run'].append(desc or cmd[:100])

        # Track messages
        if entry.get('type') == 'assistant' and entry.get('message'):
            msg = entry.get('message', {})
            if isinstance(msg, dict):
                content = msg.get('content', '')
                if isinstance(content, str) and len(content) > 50:
                    info['assistant_messages'].append(content[:500])

        if entry.get('type') == 'human' and entry.get('message'):
            msg = entry.get('message', '')
            if isinstance(msg, str) and len(msg) > 10:
                info['user_messages'].append(msg[:300])

    return info

def generate_notes(project_info):
    """Generate markdown session notes from extracted info."""
    lines = [
        "# Session Notes",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        ""
    ]

    if project_info['files_modified']:
        lines.append("## Files Modified")
        for f in sorted(project_info['files_modified'])[:10]:
            lines.append(f"- {f}")
        lines.append("")

    if project_info['commands_run']:
        lines.append("## Commands Run")
        for cmd in project_info['commands_run'][-5:]:  # Last 5
            lines.append(f"- {cmd}")
        lines.append("")

    # Add a section for manual notes that won't be overwritten
    lines.extend([
        "## Status",
        "_Update this section with current status_",
        "",
        "## Next Steps",
        "_Update this section with next steps_",
        ""
    ])

    return '\n'.join(lines)

def merge_notes(existing_content, new_notes):
    """Merge new auto-generated notes with existing manual notes."""
    # Preserve manual Status and Next Steps sections if they exist
    preserved_sections = {}

    if existing_content:
        # Extract manually edited sections
        for section in ['## Status', '## Next Steps', '## Key Decisions', '## Context']:
            pattern = rf'({section}\n)(.*?)(?=\n## |\Z)'
            match = re.search(pattern, existing_content, re.DOTALL)
            if match:
                content = match.group(2).strip()
                # Only preserve if it's been edited (not the placeholder)
                if content and not content.startswith('_Update this'):
                    preserved_sections[section] = content

    # Replace placeholders in new notes with preserved content
    result = new_notes
    for section, content in preserved_sections.items():
        placeholder_pattern = rf'({section}\n)_Update this.*?(?=\n\n|\n## |\Z)'
        result = re.sub(placeholder_pattern, f'{section}\n{content}\n', result, flags=re.DOTALL)

    return result

def update_registry(project_roots):
    """Update the project registry with worked timestamps."""
    registry_path = os.path.expanduser('~/.claude/projects.json')

    # Load existing registry
    registry = {"projects": {}}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    today = datetime.now().strftime('%Y-%m-%d')

    for project_root in project_roots:
        # Use directory name as project name
        project_name = os.path.basename(project_root)

        # Update or add project
        registry["projects"][project_name] = {
            "path": project_root,
            "last_worked": today
        }

    # Save registry
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)

    return list(project_roots)

def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Failed to parse hook input", file=sys.stderr)
        sys.exit(0)  # Don't block on errors

    transcript_path = hook_input.get('transcript_path')
    if not transcript_path:
        sys.exit(0)

    # Read transcript
    transcript_path = os.path.expanduser(transcript_path)
    if not os.path.exists(transcript_path):
        sys.exit(0)

    with open(transcript_path, 'r') as f:
        transcript_lines = f.readlines()

    # Find all file paths and their project roots
    file_paths = extract_file_paths(transcript_lines)
    project_roots = set()

    for fp in file_paths:
        root = find_project_root(fp)
        if root and root != os.path.expanduser('~'):
            project_roots.add(root)

    # Track which projects had significant activity
    active_projects = set()

    # Generate and save notes for each project
    for project_root in project_roots:
        project_info = extract_project_info(transcript_lines, project_root)

        # Skip if no significant activity
        if not project_info['files_modified'] and not project_info['commands_run']:
            continue

        active_projects.add(project_root)
        notes_path = os.path.join(project_root, 'CLAUDE.local.md')

        # Read existing notes
        existing_content = ''
        if os.path.exists(notes_path):
            with open(notes_path, 'r') as f:
                existing_content = f.read()

        # Generate and merge notes
        new_notes = generate_notes(project_info)
        final_notes = merge_notes(existing_content, new_notes)

        # Write notes
        with open(notes_path, 'w') as f:
            f.write(final_notes)

        print(f"Updated session notes: {notes_path}", file=sys.stderr)

    # Update the project registry
    if active_projects:
        updated = update_registry(active_projects)
        print(f"Updated registry for: {', '.join(os.path.basename(p) for p in updated)}", file=sys.stderr)

    sys.exit(0)

if __name__ == '__main__':
    main()
