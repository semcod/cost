#!/usr/bin/env bash

# Function to install pre-commit hook
install_hook() {
    HOOK_SOURCE="./hooks/pre-commit"
    HOOK_TARGET=".git/hooks/pre-commit"

    if [ -f "$HOOK_SOURCE" ]; then
        echo "🔗 Installing pre-commit hook..."
        cp "$HOOK_SOURCE" "$HOOK_TARGET"
        chmod +x "$HOOK_TARGET"
        echo "✅ Pre-commit hook installed"
        echo "   The hook will automatically update AI cost badge on each commit"
    else
        echo "⚠️  Hook source not found: $HOOK_SOURCE"
    fi
}

clear
pip install -e .
install_hook  # Install pre-commit hook
pip install prefact --upgrade
pip install vallm --upgrade
pip install redup --upgrade
pip install glon --upgrade
pip install goal --upgrade
pip install code2logic --upgrade
pip install code2llm --upgrade
#code2llm ./ -f toon,evolution,code2logic,project-yaml -o ./project --no-chunk
code2llm ./ -f all -o ./project --no-chunk
#code2llm report --format all       # → all views
rm project/analysis.json
rm project/analysis.yaml

pip install code2docs --upgrade
code2docs ./ --readme-only
redup scan . --format toon --output ./project
#redup scan . --functions-only -f toon --output ./project
#vallm batch ./src --recursive --semantic --model qwen2.5-coder:7b
#vallm batch --parallel .
vallm batch . --recursive --format toon --output ./project
prefact -a