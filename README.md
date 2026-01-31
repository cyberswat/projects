# Claude Session Management

Portable session management for Claude Code. Works on any machine (Linux, macOS, work, personal).

## Quick Start

```bash
# Clone anywhere you like
git clone git@github.com:cyberswat/claude-workspace.git
cd claude-workspace

# Install
./install.sh

# Add to PATH (follow the instructions printed by install.sh)
# Then reload your shell
source ~/.zshrc  # or ~/.bashrc
```

## What It Does

- **Automatic session notes**: When you end a Claude session, notes are saved to `CLAUDE.local.md` in each project you worked on
- **Project registry**: Track projects across your filesystem in `~/.claude/projects.json`
- **Easy resumption**: Say "work on dotfiles" or "resume" to pick up where you left off

## Daily Workflow

```bash
cd ~
claude

> resume                    # offers most recent project
> work on dotfiles          # switch to specific project
> list projects             # see all tracked projects

# ... work ...
# close terminal - notes save automatically
```

## CLI Commands

```bash
claude-projects list              # List all projects (sorted by recent)
claude-projects add <name> <path> # Add a project to registry
claude-projects remove <name>     # Remove a project
```

## Claude Commands

| Say this | What happens |
|----------|--------------|
| "work on dotfiles" | Switches to project, reads session notes |
| "resume dotfiles" | Same as above |
| "resume" | Offers most recent project |
| "list projects" | Shows all tracked projects |

## How It Works

### Hooks

Claude Code hooks fire on `SessionEnd` and `PreCompact`, running `save-session.py` which:

1. Parses the conversation transcript
2. Identifies which project directories were accessed
3. Generates/updates `CLAUDE.local.md` in each project
4. Updates the registry timestamp

### Session Notes Format

Each project's `CLAUDE.local.md`:

```markdown
# Session Notes
Last updated: 2026-01-31 02:30

## Files Modified
- src/main.py
- tests/test_main.py

## Commands Run
- Run test suite

## Status
Working on the API refactor

## Next Steps
- Add error handling
```

"Files Modified" and "Commands Run" are auto-generated.
"Status" and "Next Steps" are preserved when you edit them.

## Files Installed

| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` | Global Claude instructions |
| `~/.claude/settings.json` | Hook configuration |
| `~/.claude/hooks/save-session.py` | Auto-save script |
| `~/.claude/projects.json` | Project registry (machine-specific) |

## Repository Structure

```
claude-workspace/
├── install.sh              # Installation script
├── claude-projects         # CLI tool
├── config/
│   ├── CLAUDE.md           # Global instructions template
│   ├── settings.json       # Hook configuration
│   └── save-session.py     # Hook script
├── lib/
│   └── registry.py         # Registry operations
└── README.md
```

## Updating

To update to latest version:

```bash
cd claude-workspace
git pull
./install.sh  # Re-run to update config files
```

Existing files are backed up before overwriting.

## Uninstalling

```bash
rm -rf ~/.claude/hooks/save-session.py
rm ~/.claude/settings.json
# Optionally: rm ~/.claude/CLAUDE.md
# Keep ~/.claude/projects.json if you want to preserve your project list
```

Remove the PATH entry from your shell config.
