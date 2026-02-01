# Projects

Multi-project management for Claude Code. Track projects, switch between them, and resume with context.

## Install

Add the marketplace and install:

```
/plugin marketplace add cyberswat/plugins
/plugin install projects@cyberswat
```

## Usage

### Commands

| Command | Description |
|---------|-------------|
| `/projects:list` | List all tracked projects |
| `/projects:add <name> <path>` | Add a project to the registry |
| `/projects:remove <name>` | Remove a project from the registry |

### Natural Language

Just say what you want:

- "work on myproject" or "switch to myproject"
- "resume" (resumes most recent project)
- "resume myproject"
- "list projects"

## Features

### Context Saving

When you switch projects, Claude automatically:
- Saves a summary of what you did to `CLAUDE.local.md`
- Updates the `last_worked` timestamp
- Loads context from the target project

This means you can pick up exactly where you left off.

### Auto-Discovery

A hook runs on session end that detects which projects you worked on (based on file operations) and updates their timestamps. Projects are auto-discovered when you work on them.

## Project Files

Add these files to your project for richer context:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project-specific instructions (committed) |
| `CLAUDE.local.md` | Current state, auto-saved on switch (gitignored) |
| `decisions.md` | Decision history with rationale |

### decisions.md

Record significant decisions for future reference:

```markdown
# Decisions

## 2026-01-31: Use plugin architecture
Context: Wanted easier installation for other users
Decision: Convert from install script to Claude Code plugin
Rationale: One-line install, discoverable commands
```

## How It Works

Projects are tracked in `~/.claude/projects.json`:

```json
{
  "projects": {
    "myproject": {
      "path": "/home/user/myproject",
      "last_worked": "2026-01-31"
    }
  }
}
```

## Updating

**Option 1: Enable auto-update**

1. Run `/plugin` → **Marketplaces** → select `cyberswat` → enable auto-update

**Option 2: Manual update**

```bash
claude plugin update projects@cyberswat
```

## Uninstall

```
/plugin uninstall projects
```
