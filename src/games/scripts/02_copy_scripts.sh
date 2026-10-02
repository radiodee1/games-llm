#!/bin/bash

shopt -s extglob

mkdir -p ~/workspace/VJEPA2_FILES/demo/pic ~/workspace/VJEPA2_FILES/demo/json

cp -r !(02_copy_scripts.sh|03_copy_games.sh|README.md) ../../../../vjepa2/.

cp classes_pong.json ../../../../VJEPA2_FILES/demo/json/.

cp -v ../notebooks/vjepa2_classifier_cpu.py ../notebooks/vjepa2_demo_cpu.py ../../../../vjepa2/notebooks/.

cp -r ../http ../../../../vjepa2/.

mkdir -p ~/workspace/VJEPA2_FILES/demo/pic/train ~/workspace/VJEPA2_FILES/demo/pic/train2 ~/workspace/VJEPA2_FILES/demo/pic/train3 ~/workspace/VJEPA2_FILES/demo/pic/train4

cd ~/workspace/vjepa2/pic

mkdir -p train train2 train3 train4

echo "cp to vjepa2 folder"
