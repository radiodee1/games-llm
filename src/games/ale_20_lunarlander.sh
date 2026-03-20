#!/bin/bash


uv run ./main.py --plugin lunarlander --model gpt-5.2  --context_size 0 --image_strip -1 --q_len 3  --thinking --threshold 100  --stream  --inverse_size 2 --top_p 0.01 # --temperature 0.01 # --small_test 3 # --no_llm 1 
