---
name: switch
description: Use this skill when the user says "work on <project>", "switch to <project>", "resume <project>", "resume" (no project), "list projects", or "what projects do I have". Also use when working in a directory not in the registry.
version: 1.0.0
---

# Switch Projects

Manage context when switching between projects tracked in `~/.claude/projects.json`.

## Registry Location

Projects are tracked in `~/.claude/projects.json`:

```json
{
  "projects": {
    "name": {
      "path": "/absolute/path",
      "last_worked": "YYYY-MM-DD"
    }
  }
}
```

## Commands

### "work on <project>" / "switch to <project>" / "resume <project>"

1. Read `~/.claude/projects.json`
2. Look up project path by name
3. Read the project's `CLAUDE.local.md` if it exists
4. Read the project's `decisions.md` if it exists
5. Check git status, current branch, recent commits
6. Summarize context and continue

### "resume" (no project specified)

1. Read `~/.claude/projects.json`
2. Find project with most recent `last_worked` date
3. Offer to resume that one, or list recent projects to choose from
4. Once selected, follow the "work on" steps above

### "list projects" / "what projects do I have?"

1. Read `~/.claude/projects.json`
2. List projects sorted by `last_worked` date (most recent first)
3. Show name, path, and last worked date

## Adding New Projects

When working in a directory that's not in the registry:

- Offer to add it: "This project isn't tracked yet. Add it to your projects?"
- If yes, add to `~/.claude/projects.json` with current date

## Project Context Files

When resuming a project, read these files if they exist:

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project-specific instructions |
| `CLAUDE.local.md` | Session notes, current state |
| `decisions.md` | Decision history |

## Plans

When creating a plan for a non-trivial task:
- Save it to the project's `CLAUDE.local.md`

When a plan is completed:
- Clear or update `CLAUDE.local.md`
