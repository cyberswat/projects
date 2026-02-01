<!-- BEGIN CLAUDE-WORKSPACE -->
# Claude Workspace

## Git Commits

- **NEVER add Co-Authored-By lines** to commit messages
- **NEVER add attribution** to Claude or Anthropic in commits
- Commits belong to the user, not the AI assistant

## Project Switching

User typically starts Claude from ~ and switches between projects that can be anywhere on the filesystem.

### Project Registry
- Projects are tracked in `~/.claude/projects.json`
- Registry stores: project name, path, last worked timestamp
- Registry is updated automatically by hooks on SessionEnd/PreCompact

### "work on <project>" / "switch to <project>" / "resume <project>"
1. Look up project path in `~/.claude/projects.json`
2. Read the project's `CLAUDE.local.md` if it exists
3. Check git status, current branch, recent commits
4. Summarize context and continue

### "resume" (no project specified)
1. Read `~/.claude/projects.json` to find most recently worked project
2. Offer to resume that one, or list recent projects to choose from

### "what projects do I have?" / "list projects"
1. Read `~/.claude/projects.json`
2. List projects sorted by last worked date

### Adding new projects
When working in a directory that's not in the registry:
- Offer to add it: "This project isn't tracked yet. Add it to your projects?"
- If yes, add to `~/.claude/projects.json`

## Plans

When creating a plan for a non-trivial task:
- Save it to the project's `CLAUDE.local.md`

When a plan is completed:
- Clear or update `CLAUDE.local.md`

On resume:
- Read `CLAUDE.local.md` if it exists
- Read `decisions.md` if it exists for context on past decisions
- Check git state (status, branch, recent commits)
- Summarize and continue

## Decision Tracking

Projects may have a `decisions.md` file for recording significant decisions.

### When to Record Decisions
Record a decision when:
- A significant choice was made after considering alternatives
- The decision affects future work (even if no code was written)
- You'd want to remember "why did we decide this?" later

Do NOT record:
- Exploration or experiments that didn't pan out
- Routine implementation choices
- Decisions still being discussed

### Recording Format
Append to `decisions.md`:
```
## YYYY-MM-DD: Brief Title
Context: [What prompted this]
Decision: [What we decided]
Rationale: [Why]
```

Only record after the decision is confirmed and being acted on.
<!-- END CLAUDE-WORKSPACE -->
