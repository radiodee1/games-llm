#!/bin/bash

python3 ./main.py --model vjepa --plugin pong --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --thinking --threshold 100 --stream --inverse_size 4 --video 5
