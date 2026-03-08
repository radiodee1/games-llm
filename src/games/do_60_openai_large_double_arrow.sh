#!/bin/bash


uv run ./main.py --model gpt-5.2 --sudden_death 2 --context_size 0 --image_strip -1 --q_len 1  --thinking --threshold 100  --stream --double_arrow --inverse_size 1 --temperature 0.0  # --small_test 3 # --no_llm 1 
