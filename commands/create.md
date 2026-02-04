---
description: Create a new project with git repo and GitHub remote
argument-hint: <name>
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
---

# Create Project

Create a new project directory, initialize git, create a private GitHub repo, and register it.

## Arguments

The user invoked this command with: $ARGUMENTS

Expected format: `<name>`

## Instructions

1. Read `~/.claude/projects.json`
2. Check for `config.base_path` and `config.default_visibility`
   - If missing, ask user for base path (e.g., `~/github.com/username`)
   - Save config to `projects.json` for future use
3. Expand `~` to actual home directory
4. Create directory at `<base_path>/<name>/`
5. Initialize git with `main` branch
6. Create `CLAUDE.md` with basic project template:
   ```markdown
   # <name>

   ## Purpose
   [Describe the project purpose]

   ## Key Files
   [List important files as they're created]
   ```
7. Create initial commit
8. Create GitHub repo using `gh repo create <username>/<name> --<visibility> --source=. --push`
   - Parse username from base_path (last component of path)
   - Use `default_visibility` from config (default: private)
9. Add project to `~/.claude/projects.json` with today's date
10. Confirm: "Created <name> at <path>"
    - Show GitHub URL

## Registry Format

```json
{
  "config": {
    "base_path": "~/github.com/username",
    "default_visibility": "private"
  },
  "projects": {
    "name": {
      "path": "/absolute/path",
      "last_worked": "YYYY-MM-DD"
    }
  }
}
```

## Error Handling

- If project name already exists in registry, abort with message
- If directory already exists, ask if user wants to use it anyway
- If `gh` command fails, still complete local setup and register project
- If config is missing, prompt user and save for future use
