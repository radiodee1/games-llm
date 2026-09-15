#!/bin/bash

if [[ -d ".venv" ]]; then
  echo "venv present"
else
  uv venv
  echo "make venv"
fi

#uv venv

uv pip install torch --index https://download.pytorch.org/whl/cpu

uv add torch --index https://download.pytorch.org/whl/cpu

#uv pip install torch --index https://download.pytorch.org/whl/cu126
#uv add torch --index https://download.pytorch.org/whl/cu126
