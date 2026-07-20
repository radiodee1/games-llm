#!/bin/bash

uv run ./main.py --model vjepa --plugin ssv --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --thinking --threshold 100 --stream --inverse_size 4 --video 10
