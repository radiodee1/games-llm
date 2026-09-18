#!/bin/bash

shopt -s extglob

cp -r !(02_copy_scripts.sh|03_copy_games.sh|README.md) ../../../../vjepa2/.

cp classes_pong.json ../../../../VJEPA2_FILES/demo/json/.

cp -v ../notebooks/vjepa2_classifier_cpu.py ../notebooks/vjepa2_demo_cpu.py ../../../../vjepa2/notebooks/.

cp -r ../http ../../../../vjepa2/.

echo "cp to vjepa2 folder"
