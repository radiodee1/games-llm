#!/bin/bash

cd ~/workspace/VJEPA2_FILES/demo/

rm lora.vjepa2* -fr

rm vjepa2_vitl* -fr
#cp ./pic/train/* ~/workspace/VJEPA2_FILES/demo/pic/train/.

rm ./pic/train/*.csv ./pic/train2/*.csv ./pic/train3/*.csv ./pic/train4/*.csv -fr

echo "start train over again."
