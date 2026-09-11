#!/bin/bash

uv run python -m notebooks.vjepa2_demo_cpu --image_span 5000 --save_checkpoint --foldername train --key vitl --batch 2
