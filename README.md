# Claude Project Management

A registry system for tracking Claude projects across directories, with automatic session note persistence.

## What This Is

- **Project registry** (`~/.claude/projects.json`) - tracks where projects are
- **Session notes** (`CLAUDE.local.md` in each project) - tracks what you were doing
- **Automatic updates** via Claude Code hooks - no manual maintenance

## How It Works

1. Start Claude from anywhere (typically `~`)
2. Say "work on dotfiles" or "resume dotfiles"
3. Claude reads the project's session notes and continues where you left off
4. When you end the session, hooks automatically:
   - Save session notes to the project's `CLAUDE.local.md`
   - Update the registry's "last worked" timestamp

## Installation

### 1. Add to PATH

In `~/.zshrc`:

```bash
export PATH="$HOME/github.com/cyberswat/claude-workspace:$PATH"
```

### 2. Configure hooks

Copy hook configuration to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "hooks": [{
          "type": "command",
          "command": "$HOME/.claude/hooks/save-session.py"
        }]
      }
    ],
    "PreCompact": [
      {
        "hooks": [{
          "type": "command",
          "command": "$HOME/.claude/hooks/save-session.py"
        }]
      }
    ]
  }
}
```

### 3. Install hook script

The `save-session.py` script should be at `~/.claude/hooks/save-session.py`.

## CLI Usage

### List all projects
```bash
claude-projects list
```

Output (sorted by most recently worked):
```
dotfiles                       /home/user/github.com/user/dotfiles           2026-01-31
claude-workspace               /home/user/github.com/user/claude-workspace   2026-01-30
```

### Add a project manually
```bash
claude-projects add <name> <path>

# Example
claude-projects add my-api ~/projects/my-api
```

### Remove a project
```bash
claude-projects remove <name>
```

### Update timestamp manually (usually automatic)
```bash
claude-projects worked <name>
```

## Claude Commands

Inside Claude, say:

| Command | What happens |
|---------|--------------|
| "work on dotfiles" | Switches to project, reads session notes |
| "resume dotfiles" | Same as above |
| "resume" | Offers most recent project |
| "list projects" | Shows all tracked projects |
| "what projects do I have?" | Same as above |

## File Locations

| File | Purpose |
|------|---------|
| `~/.claude/projects.json` | Project registry |
| `~/.claude/settings.json` | Hook configuration |
| `~/.claude/hooks/save-session.py` | Auto-save script |
| `~/.claude/CLAUDE.md` | Global Claude instructions |
| `<project>/CLAUDE.local.md` | Per-project session notes |

## Session Notes Format

Each project's `CLAUDE.local.md`:

```markdown
# Session Notes
Last updated: 2026-01-31 02:30

## Files Modified
- src/main.py
- tests/test_main.py

## Commands Run
- Run test suite
- Git commit

## Status
Working on the API refactor

## Next Steps
- Add error handling
- Write integration tests
```

The "Files Modified" and "Commands Run" sections are auto-generated.
The "Status" and "Next Steps" sections are preserved when you edit them manually.

## Architecture

```
~/.claude/
├── projects.json          # Registry (auto-updated)
├── settings.json          # Hook config
├── hooks/
│   └── save-session.py    # Auto-save script
└── CLAUDE.md              # Global instructions

~/project/
└── CLAUDE.local.md        # Session notes (auto-generated)
```

No external dependencies. Pure Python stdlib.
