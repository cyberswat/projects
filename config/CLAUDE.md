# Global Claude Instructions

## Git Commits

- **NEVER add Co-Authored-By lines** to commit messages
- **NEVER add attribution** to Claude or Anthropic in commits
- Commits belong to the user, not the AI assistant

## Project Switching

User typically starts Claude from ~ and switches between projects that can be anywhere on the filesystem.

### Project Registry
- Projects are tracked in `~/.claude/projects.json`
- Registry stores: project name, path, last worked timestamp
- Use `claude-projects` CLI or read the registry directly

### "work on <project>" / "switch to <project>" / "resume <project>"
1. Look up project path in `~/.claude/projects.json`
2. Read that project's `CLAUDE.local.md` if it exists
3. Summarize the session notes and current state
4. Continue working in that project's context

### "resume" (no project specified)
1. Read `~/.claude/projects.json` to find most recently worked project
2. Offer to resume that one, or list recent projects to choose from

### "what projects do I have?" / "list projects"
1. Read `~/.claude/projects.json`
2. List projects sorted by last worked date
3. Suggest the most recent one

### Adding new projects
When working in a directory that's not in the registry:
- Offer to add it: "This project isn't tracked yet. Add it to your projects?"
- If yes, add to `~/.claude/projects.json`

## Session Notes

Session notes are automatically saved to each project's `CLAUDE.local.md` by hooks.
- Notes are saved on SessionEnd and PreCompact
- Each project's notes are isolated (no cross-project references)
- The "Status" and "Next Steps" sections are preserved when notes update
- Registry timestamps are also updated by the hook

When working on a project, if asked to update session notes manually:
- Update the project's `CLAUDE.local.md` file
- Focus on Status and Next Steps sections
