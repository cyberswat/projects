---
name: switch
description: Use this skill when the user says "work on <project>", "switch to <project>", "resume <project>", "resume" (no project), "list projects", or "what projects do I have". Also use when working in a directory not in the registry.
version: 1.2.0
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

1. **Save context for current project** (if switching from another tracked project):
   - Write a summary to the current project's `CLAUDE.local.md` with:
     - What was done this session
     - Any pending items or next steps
     - Relevant context for resuming later
   - Update `last_worked` to today's date in `~/.claude/projects.json`
2. Read `~/.claude/projects.json`
3. Look up target project path by name
4. Update target project's `last_worked` to today's date
5. Read the project's `CLAUDE.local.md` if it exists
6. Read the project's `decisions.md` if it exists
7. Check git status, current branch, recent commits
8. Summarize context and continue

### "resume" (no project specified)

1. Read `~/.claude/projects.json`
2. Find project with most recent `last_worked` date
3. Offer to resume that one, or list recent projects to choose from
4. Once selected, follow the "work on" steps above (skip step 1 if no current project)

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
| `CLAUDE.local.md` | Current state - where you left off |
| `decisions.md` | Decision history |

## CLAUDE.local.md

This file captures **current state**, not history. It gets overwritten (not appended) when:
- Switching away from a project (summary of where you left off)
- Creating a plan for a non-trivial task
- Completing a plan (clear or update)

Example content:
```markdown
# project-name

## Current State
Implemented the new authentication flow. Tests passing.

## Pending
- Add rate limiting to login endpoint
- Update API docs

## Context
Using JWT tokens, decided against sessions (see decisions.md)
```

## Relationship with SessionEnd Hook

The SessionEnd hook updates `last_worked` timestamps based on file operations. This skill also updates timestamps on explicit switches. Both are safe:
- They write the same date (idempotent)
- Hook catches implicit work (editing files without switching)
- Skill captures explicit switches with context summaries
