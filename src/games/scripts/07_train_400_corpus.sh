#!/bin/bash

#source ~/workspace/miniconda3/etc/profile.d/conda.sh

#conda activate vjepa2-310

uv run python -m notebooks.vjepa2_demo_cpu --image_span 400 --save_checkpoint --foldername train
