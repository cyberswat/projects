# Claude Projects

Multi-project management for Claude Code. Track projects, switch between them, and resume with context.

## Install

```
/plugin install cyberswat/claude-workspace
```

Or clone and install locally:

```bash
git clone git@github.com:cyberswat/claude-workspace.git
# Then in Claude: /plugin install /path/to/claude-workspace
```

## Commands

| Command | Description |
|---------|-------------|
| `/projects:list` | List all projects |
| `/projects:add <name> <path>` | Add a project |
| `/projects:remove <name>` | Remove a project |

## Natural Language

You can also just say:

- "work on myproject" - switch to a project
- "resume" - resume most recent project
- "resume myproject" - resume specific project
- "list projects" - show all projects

## Project Files

Projects can have these optional files:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project-specific instructions |
| `CLAUDE.local.md` | Session notes, current state |
| `decisions.md` | Decision history |

### decisions.md

Record significant decisions:

```markdown
# Decisions

## 2026-01-31: Use plugin architecture
Context: Wanted easier installation for other users
Decision: Convert from install script to Claude Code plugin
Rationale: One-line install, discoverable commands
```

## How It Works

### Project Registry

Projects are tracked in `~/.claude/projects.json`:

```json
{
  "projects": {
    "myproject": {
      "path": "/home/user/projects/myproject",
      "last_worked": "2026-01-31"
    }
  }
}
```

### Auto-Save Hook

The plugin includes a hook that fires on `SessionEnd` and `PreCompact`:

- Detects which project directories were accessed
- Updates registry timestamps automatically
- Projects are auto-discovered when you work on them

## Plugin Structure

```
projects/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── list.md
│   ├── add.md
│   └── remove.md
├── skills/
│   ├── switch/
│   │   └── SKILL.md
│   └── decisions/
│       └── SKILL.md
├── hooks/
│   ├── hooks.json
│   └── save-session.py
└── lib/
    └── registry.py
```

## Uninstall

```
/plugin uninstall projects
```
