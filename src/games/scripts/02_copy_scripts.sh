#!/bin/bash

shopt -s extglob

cp -r !(02_copy_scripts.sh|03_copy_games.sh) ../../../../vjepa2/.

cp classes_pong.json ../../../../VJEPA2_FILES/demo/json/.

cp ../notebooks/* ../../../../vjepa2/notebooks/.

echo "cp to vjepa2 folder"
