#!/bin/bash

uv run ./main_chat.py --plugin chat --model gpt-4o-mini --context_size 100 --image_strip -1 --q_len -1 --stream --temperature 0.01 --total 2 #  --top_p 0.01 # --small_test 3 # --no_llm 1 --thinking
