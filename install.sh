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

# Copy config files (don't overwrite if they exist and are different)
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

# Install configuration files
install_file "$SCRIPT_DIR/config/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
install_file "$SCRIPT_DIR/config/settings.json" "$CLAUDE_DIR/settings.json"
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
