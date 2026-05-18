#!/bin/bash

## do not set --temperature for gemini-3 models.

uv run ./main.py --plugin dots --model claude-3-5-sonnet-20240620 --sudden_death 2 --context_size -1 --image_strip -1 --q_len 1 --stream --inverse_size 1 --skip 1 --no_pic --no_llm 2 --temperature 0.95
