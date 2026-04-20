#!/bin/bash

uv run ./main.py --plugin pong --model gemma4:e4b --sudden_death 2 --context_size 3 --image_strip -1 --q_len 1 --threshold 100 --stream --inverse_size 2 --temperature 0.01 --skip 4 --no_pic #  --top_p 0.01 # --small_test 3 # --no_llm 1 --thinking
