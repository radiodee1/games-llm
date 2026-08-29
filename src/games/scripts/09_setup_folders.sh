#!/usr/bin/bash

mkdir -p ~/workspace/VJEPA2_FILES/demo/json
mkdir -p ~/workspace/VJEPA2_FILES/demo/pic/train

cd ~/workspace/VJEPA2_FILES/demo

wget https://dl.fbaipublicfiles.com/vjepa2/vitl.pt ## <--
wget https://dl.fbaipublicfiles.com/vjepa2/evals/ssv2-vitl-16x2x3.pt

wget https://dl.fbaipublicfiles.com/vjepa2/vjepa2_1_vitl_dist_vitG_384.pt
wget https://dl.fbaipublicfiles.com/vjepa2/evals/ssv2-vitg-384-64x2x3.pt

wget https://dl.fbaipublicfiles.com/vjepa2/vitg-384.pt
