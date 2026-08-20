#!/bin/bash

shopt -s extglob

cp -r !(02_copy_scripts.sh|README.md|03_copy_games.sh) ../vjepa2/.

cp classes_pong.json ../VJEPA2_FILES/demo/json/.

echo "cp to vjepa2 folder"
