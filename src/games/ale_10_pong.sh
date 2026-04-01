#!/bin/bash


uv run ./main.py --plugin pong --model gpt-5.2 --sudden_death 2 --context_size 4 --image_strip -1 --q_len 1  --threshold 100  --stream  --inverse_size 1 --temperature 0.01 #  --top_p 0.01 # --small_test 3 # --no_llm 1 --thinking 
