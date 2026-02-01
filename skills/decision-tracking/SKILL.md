---
name: decision-tracking
description: Use this skill when a significant decision has been made and confirmed, when you need to record why a choice was made, or when referencing past decisions. Do not use for routine implementation choices or decisions still being discussed.
version: 1.0.0
---

# Decision Tracking

Projects may have a `decisions.md` file for recording significant decisions.

## When to Record Decisions

Record a decision when:
- A significant choice was made after considering alternatives
- The decision affects future work (even if no code was written)
- You'd want to remember "why did we decide this?" later

Do NOT record:
- Exploration or experiments that didn't pan out
- Routine implementation choices
- Decisions still being discussed

## Recording Format

Append to the project's `decisions.md`:

```markdown
## YYYY-MM-DD: Brief Title
Context: [What prompted this decision]
Decision: [What we decided]
Rationale: [Why we chose this]
```

## Example

```markdown
# Decisions

## 2026-01-31: Use plugin architecture
Context: Wanted easier installation and portability for other users
Decision: Convert from install script to Claude Code plugin
Rationale: Plugins have one-line install, discoverable commands, and built-in distribution

## 2026-01-30: Marker-based merge for config
Context: Users may have custom content in their CLAUDE.md
Decision: Use HTML comment markers to delimit managed sections
Rationale: Preserves user customizations while allowing updates
```

## On Resume

When resuming a project:
- Read `decisions.md` if it exists
- Reference relevant past decisions when they affect current work

## Timing

Only record after the decision is confirmed and being acted on, not during exploration.
