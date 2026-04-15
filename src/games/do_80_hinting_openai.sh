#!/bin/bash

uv run ./main.py --plugin pygame --model gpt-5.2 --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --video --thinking --threshold 80 --hinting --no_llm 3 # --small_test 3 # --no_llm 1
