---
description: List all tracked projects
allowed-tools: [Read]
---

# List Projects

List all projects from the registry at `~/.claude/projects.json`.

## Instructions

1. Read `~/.claude/projects.json`
2. Display projects sorted by `last_worked` (most recent first)
3. Show: name, path, last worked date

## Output Format

```
name                path                                      last_worked
----                ----                                      -----------
myproject           /home/user/projects/myproject             2026-01-31
another             /home/user/another                        2026-01-30
```

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
