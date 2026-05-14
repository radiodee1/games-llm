#!/bin/bash

## do not set --temperature for gemini-3 models.

uv run ./main.py --plugin dots --model gemini-3.1-pro-preview --sudden_death 2 --context_size -1 --image_strip -1 --q_len 1 --stream --inverse_size 1 --skip 1 --no_pic --total 2 #  --top_p 0.01 # --small_test 3 # --no_llm 1 --thinking
