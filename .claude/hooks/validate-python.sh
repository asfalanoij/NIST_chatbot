#!/usr/bin/env bash
# PostToolUse hook: py_compile on every .py file edit
# Configured in .claude/settings.json

FILE=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.file_path // empty')

if [[ "$FILE" == *.py ]]; then
    BACKEND_DIR="/Users/asfalanoi/app_oct2025/NIST_chatbot_v02/backend"
    PYTHON="$BACKEND_DIR/venv/bin/python"

    if [[ -f "$PYTHON" ]]; then
        result=$("$PYTHON" -m py_compile "$FILE" 2>&1)
        if [[ -n "$result" ]]; then
            echo "SYNTAX ERROR in $FILE:"
            echo "$result"
            exit 1
        fi
    fi
fi

exit 0
