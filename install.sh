#!/bin/bash

# Path to your script
SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/app/main.py"
TARGET_PATH="/usr/bin/task-cli"

# Ensure the script is executable
chmod +x "$SCRIPT_PATH"

# Ask for sudo permissions and install 
echo "Installing task-cli to /usr/bin..."
sudo ln -sf "$SCRIPT_PATH" "$TARGET_PATH"

# Confirm success
if [ $? -eq 0 ]; then
    echo "task-cli installed successfully!"
else
    echo "Installation failed"
fi