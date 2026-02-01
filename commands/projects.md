---
description: List, add, or remove projects from the registry
argument-hint: [list|add <name> <path>|remove <name>]
allowed-tools: [Read, Write, Bash]
---

# Projects Command

Manage the project registry at `~/.claude/projects.json`.

## Arguments

The user invoked this command with: $ARGUMENTS

## Usage

- `/projects` or `/projects list` - List all projects sorted by last worked date
- `/projects add <name> <path>` - Add a project to the registry
- `/projects remove <name>` - Remove a project from the registry

## Instructions

### List (default)

1. Read `~/.claude/projects.json`
2. Display projects sorted by `last_worked` (most recent first)
3. Show: name, path, last worked date

Format:
```
name                path                                      last_worked
----                ----                                      -----------
myproject           /home/user/projects/myproject             2026-01-31
another             /home/user/another                        2026-01-30
```

### Add

1. Validate the path exists
2. Read `~/.claude/projects.json`
3. Add the project with current date as `last_worked`
4. Write updated registry
5. Confirm: "Added <name>"

### Remove

1. Read `~/.claude/projects.json`
2. Remove the project entry
3. Write updated registry
4. Confirm: "Removed <name>"

## Registry Format

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
