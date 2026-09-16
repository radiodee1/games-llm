cd ~/workspace/VJEPA2_FILES/demo

tar --exclude='*.gz' --exclude='*.txt' --exclude='*.gif' --exclude='*.png' --exclude='*.mp4' --exclude='vitl.pt' --exclude='ssv2-vitl*.pt' --exclude='json' --exclude='pic' -czf checkpoint_archive.tar.gz *

mv checkpoint_archive.tar.gz ~/workspace/.
