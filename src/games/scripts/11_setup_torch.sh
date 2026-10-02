#!/bin/bash

echo "Install pyproject.toml for entire system. Use system torch."
echo "Do not use 'uv sync' or 'uv lock'."

uv pip install --system -r pyproject.toml

#uv pip install torch --index https://download.pytorch.org/whl/cpu
#uv add torch --index https://download.pytorch.org/whl/cpu

#uv pip install torch --index https://download.pytorch.org/whl/cu126
#uv add torch --index https://download.pytorch.org/whl/cu126
