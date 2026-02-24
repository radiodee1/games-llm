#!/bin/bash


uv run ./main.py --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --stream_openai --video_openai --thinking --threshold 50  --no_llm 3 # --small_test 2 
