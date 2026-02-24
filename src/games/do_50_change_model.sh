#!/bin/bash


uv run ./main.py --model qwen3-vl:4b --sudden_death 2 --context_size 3 --image_strip 3 --stream # --no_llm 30  --generate 
