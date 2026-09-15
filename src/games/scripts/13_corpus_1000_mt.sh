#!/bin/bash

mkdir -p ./pic/train
mkdir -p ./pic/train2
mkdir -p ./pic/train3

rm ./pic/train/output_0*.mp4

uv run ./main.py --model vjepa-mt --plugin ssv --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --video 4 --thinking --stream --inverse_size 4 --make_corpus 1000 --foldername train
