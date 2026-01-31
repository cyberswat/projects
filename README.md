# Claude Project Discovery

A minimal registry system for tracking Claude projects across directories.

## What This Is

Simple CLI tool to maintain a registry of project locations, making it easy to:
1. Find which project to work on (projects scattered across directories)
2. Resume work with context

## Installation

Add to your PATH in `~/.zshrc`:

```bash
export PATH="$HOME/github.com/cyberswat/claude-workspace:$PATH"
```

Then reload:

```bash
source ~/.zshrc
```

## Usage

### Add a project
```bash
claude-projects add <name> <path>

# Example
claude-projects add meeting-management ~/github.com/cyberswat/meeting-management
```

### List all projects
Projects are sorted by most recently worked on:
```bash
claude-projects list
```

Output format:
```
project-name                   /path/to/project                               2026-01-30
```

### Update last worked timestamp
```bash
claude-projects worked <name>

# Example
claude-projects worked meeting-management
```

### Remove a project
```bash
claude-projects remove <name>

# Example
claude-projects remove old-project
```

## Registry Location

Projects are stored in `~/.claude/projects.json` with this simple format:

```json
{
  "projects": {
    "meeting-management": {
      "path": "~/github.com/cyberswat/meeting-management",
      "last_worked": "2026-01-30"
    }
  }
}
```

## Architecture

**Minimal by design:**
- `lib/registry.py` - Core registry operations (~40 lines)
- `claude-projects` - CLI interface (~50 lines)
- `requirements.txt` - Empty (stdlib only)

No external dependencies, no auto-scanning, no complex features. Just manual project tracking.

## Future Enhancements (Only If Needed)

Add these later if manual management becomes tedious:
- Auto-discovery scanning
- Git integration
- Search/filter capabilities
- Complex metadata
- Statistics and reporting

**Start simple, grow as needed.**
