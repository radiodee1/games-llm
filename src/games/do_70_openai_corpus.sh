#!/bin/bash

uv run ./main.py --model gpt-5.2 --plugin pong --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --thinking --threshold 100 --stream --double_arrow --inverse_size 4 --make_corpus 5 # --small_test 3 # --no_llm 1
