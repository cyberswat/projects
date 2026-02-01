---
description: Add a project to the registry
argument-hint: <name> <path>
allowed-tools: [Read, Write, Bash]
---

# Add Project

Add a project to the registry at `~/.claude/projects.json`.

## Arguments

The user invoked this command with: $ARGUMENTS

Expected format: `<name> <path>`

## Instructions

1. Parse the name and path from arguments
2. Validate the path exists (use Bash to check)
3. Read `~/.claude/projects.json`
4. Add the project with current date as `last_worked`
5. Write updated registry
6. Confirm: "Added <name>"

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

- If path doesn't exist, ask user to confirm or provide correct path
- If project name already exists, ask if they want to update the path
