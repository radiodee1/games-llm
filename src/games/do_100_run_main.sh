#!/bin/bash


uv run ./main.py --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3  --thinking --threshold 80  # --small_test 3 # --no_llm 1 
