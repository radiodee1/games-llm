#!/bin/bash


uv run ./main.py --model gpt-5.2 --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --stream_openai --video_openai --thinking --threshold 80 --hinting # --small_test 3 # --no_llm 1 
