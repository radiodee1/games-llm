#!/bin/bash

uv run ./main.py --plugin dots --model gemma4:e4b --sudden_death 2 --context_size -1 --image_strip -1 --q_len 1 --stream --inverse_size 4 --temperature 0.95 --skip 1 --no_pic #  --top_p 0.01 # --small_test 3 # --no_llm 1 --thinking
