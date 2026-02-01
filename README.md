# Claude Workspace

Portable session management for Claude Code. Works on any machine (Linux, macOS).

## Quick Start

```bash
# Clone anywhere you like
git clone git@github.com:cyberswat/claude-workspace.git
cd claude-workspace

# Install
./install.sh
```

Add to your PATH in `~/.zshrc` or `~/.bashrc`:

```bash
export PATH="/path/to/claude-workspace:$PATH"
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

## What It Does

- **Project registry**: Track projects across your filesystem in `~/.claude/projects.json`
- **Session notes**: Auto-generated `CLAUDE.local.md` in each project with files modified and commands run
- **Decision tracking**: Optional `decisions.md` for recording significant decisions
- **Easy resumption**: Say "work on myproject" or "resume" to pick up where you left off

## Daily Workflow

```bash
cd ~
claude

> resume                    # offers most recent project
> work on myproject         # switch to specific project
> list projects             # see all tracked projects

# ... work ...
# session notes save automatically on exit
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
| "work on myproject" | Switches to project, reads context files |
| "resume myproject" | Same as above |
| "resume" | Offers most recent project |
| "list projects" | Shows all tracked projects |

## Project Files

Projects can have these optional files:

| File | Purpose | Commit? |
|------|---------|---------|
| `CLAUDE.md` | Project-specific instructions for Claude | Yes |
| `CLAUDE.local.md` | Session notes, current state | Your choice |
| `decisions.md` | Decision history | Your choice |

### decisions.md

Record significant decisions with context:

```markdown
# Decisions

## 2026-01-31: Use markers for CLAUDE.md merge
Context: Users may have custom content in ~/.claude/CLAUDE.md
Decision: Use HTML comment markers to delimit managed section
Rationale: Preserves user customizations while allowing updates
```

Claude reads this on resume and references relevant decisions.

## How It Works

### Hooks

Claude Code hooks fire on `SessionEnd` and `PreCompact`, running `save-session.py` which:

1. Parses the conversation transcript
2. Identifies which project directories were accessed
3. Generates/updates `CLAUDE.local.md` in each project
4. Updates the registry timestamp

### Global Instructions

The installer merges content into `~/.claude/CLAUDE.md` using markers:

```markdown
<!-- BEGIN CLAUDE-WORKSPACE -->
...managed content...
<!-- END CLAUDE-WORKSPACE -->
```

Your custom instructions outside these markers are preserved on update.

## Files Installed

| File | Purpose |
|------|---------|
| `~/.claude/CLAUDE.md` | Global Claude instructions (merged) |
| `~/.claude/settings.json` | Hook configuration (merged) |
| `~/.claude/hooks/save-session.py` | Auto-save script |
| `~/.claude/projects.json` | Project registry |

## Updating

```bash
cd claude-workspace
git pull
./install.sh  # Merges updates, preserves your customizations
```

## Uninstalling

```bash
rm ~/.claude/hooks/save-session.py
# Edit ~/.claude/settings.json to remove hooks
# Edit ~/.claude/CLAUDE.md to remove managed section (or delete)
# Keep ~/.claude/projects.json if you want to preserve your project list
```

Remove the PATH entry from your shell config.
