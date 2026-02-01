# Decisions

## 2026-02-01: Convert to Claude Code plugin
Context: Wanted easier installation and portability for other users beyond install scripts and PATH configuration
Decision: Convert from install.sh + CLI tool to Claude Code plugin with marketplace.json
Rationale: Plugins provide one-line install (`/plugin marketplace add`), discoverable commands (`/projects`), automatic hook registration, and follow the intended distribution model for Claude Code extensions
