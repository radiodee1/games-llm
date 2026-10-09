#!/bin/bash


uv run ./main.py  --model gemini-3-pro-preview --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3  --thinking --threshold 100  --stream --double_arrow --inverse_size 1 #--no_llm 20 # --small_test 3 # --no_llm 1 
