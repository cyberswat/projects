# Decisions

## 2026-02-01: Convert to Claude Code plugin
Context: Wanted easier installation and portability for other users beyond install scripts and PATH configuration
Decision: Convert from install.sh + CLI tool to Claude Code plugin with marketplace.json
Rationale: Plugins provide one-line install (`/plugin marketplace add`), discoverable commands (`/projects`), automatic hook registration, and follow the intended distribution model for Claude Code extensions

## 2026-02-01: Restructure plugin for clean namespacing
Context: Plugin commands were namespaced as `/claude-projects:projects` which was redundant and awkward
Decision: Rename plugin to "projects", split single command into `/projects:list`, `/projects:add`, `/projects:remove`, create separate marketplace repo (`cyberswat/plugins`)
Rationale: Cleaner command names (`/projects:list` vs `/claude-projects:projects list`), separate marketplace allows adding future plugins under the `cyberswat` namespace with simple install (`/plugin install X@cyberswat`)
