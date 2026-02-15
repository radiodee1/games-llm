#!/bin/bash


uv run ./pong.py --model llava-phi3:3.8b --sudden_death 2 --context_size 3 --image_strip 3 --stream # --no_llm 30  --generate 
