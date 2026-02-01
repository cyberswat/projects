---
description: Remove a project from the registry
argument-hint: <name>
allowed-tools: [Read, Write]
---

# Remove Project

Remove a project from the registry at `~/.claude/projects.json`.

## Arguments

The user invoked this command with: $ARGUMENTS

Expected format: `<name>`

## Instructions

1. Parse the project name from arguments
2. Read `~/.claude/projects.json`
3. Check if the project exists
4. Remove the project entry
5. Write updated registry
6. Confirm: "Removed <name>"

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

## Error Handling

- If project doesn't exist, inform user: "Project '<name>' not found in registry"
