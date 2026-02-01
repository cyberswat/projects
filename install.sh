#!/bin/bash
#
# Install Claude session management system
# Works on Linux and macOS
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "Installing Claude session management..."

# Create directories
mkdir -p "$CLAUDE_DIR/hooks"

# Copy config files (backup if different)
install_file() {
    local src="$1"
    local dest="$2"

    if [ -f "$dest" ]; then
        if ! diff -q "$src" "$dest" > /dev/null 2>&1; then
            echo "  $dest exists and differs - backing up to ${dest}.backup"
            cp "$dest" "${dest}.backup"
        fi
    fi
    cp "$src" "$dest"
    echo "  Installed: $dest"
}

# Merge managed section into CLAUDE.md (preserves user content)
merge_claude_md() {
    local src="$1"
    local dest="$2"

    if [ ! -f "$dest" ]; then
        # No existing file, just copy
        cp "$src" "$dest"
        echo "  Created: $dest"
        return
    fi

    # Check if markers exist in destination
    if grep -qF '<!-- BEGIN CLAUDE-WORKSPACE -->' "$dest"; then
        # Replace existing managed section using awk
        awk '
            /<!-- BEGIN CLAUDE-WORKSPACE -->/ { skip=1; next }
            /<!-- END CLAUDE-WORKSPACE -->/ { skip=0; next }
            !skip { print }
        ' "$dest" > "$dest.tmp"

        # Insert new managed content
        {
            cat "$dest.tmp"
            cat "$src"
        } > "$dest"
        rm "$dest.tmp"
        echo "  Updated managed section in: $dest"
    else
        # No markers, append managed section
        echo "" >> "$dest"
        cat "$src" >> "$dest"
        echo "  Appended managed section to: $dest"
    fi
}

# Merge hooks into existing settings.json (preserves all other settings)
merge_settings() {
    local hooks_file="$1"
    local dest="$2"

    if [ -f "$dest" ]; then
        # Merge hooks into existing settings
        local merged
        merged=$("$SCRIPT_DIR/config/merge-settings.py" "$dest" "$hooks_file")
        if [ $? -eq 0 ]; then
            echo "$merged" > "$dest"
            echo "  Merged hooks into: $dest"
        else
            echo "  ERROR: Failed to merge settings" >&2
            exit 1
        fi
    else
        # No existing settings, just copy
        cp "$hooks_file" "$dest"
        echo "  Created: $dest"
    fi
}

# Install configuration files
merge_claude_md "$SCRIPT_DIR/config/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
merge_settings "$SCRIPT_DIR/config/settings.json" "$CLAUDE_DIR/settings.json"
install_file "$SCRIPT_DIR/config/save-session.py" "$CLAUDE_DIR/hooks/save-session.py"

# Make hook script executable
chmod +x "$CLAUDE_DIR/hooks/save-session.py"

# Initialize empty projects registry if it doesn't exist
if [ ! -f "$CLAUDE_DIR/projects.json" ]; then
    echo '{"projects": {}}' > "$CLAUDE_DIR/projects.json"
    echo "  Created: $CLAUDE_DIR/projects.json"
fi

echo ""
echo "Installation complete!"
echo ""

# Check if claude-workspace is in PATH
if ! echo "$PATH" | grep -q "$SCRIPT_DIR"; then
    echo "Add claude-workspace to your PATH by adding this to your shell config:"
    echo ""
    echo "  # For bash (~/.bashrc):"
    echo "  export PATH=\"$SCRIPT_DIR:\$PATH\""
    echo ""
    echo "  # For zsh (~/.zshrc):"
    echo "  export PATH=\"$SCRIPT_DIR:\$PATH\""
    echo ""
    echo "Then reload your shell: source ~/.bashrc  (or ~/.zshrc)"
else
    echo "claude-workspace is already in your PATH"
fi

echo ""
echo "Usage:"
echo "  claude-projects list          # List all projects"
echo "  claude-projects add <n> <p>   # Add a project"
echo ""
echo "In Claude, say:"
echo "  'work on <project>'           # Switch to a project"
echo "  'resume'                      # Resume most recent project"
echo "  'list projects'               # Show all projects"
