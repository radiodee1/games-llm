cd ~/workspace/VJEPA2_FILES/demo/pic

tar --exclude='*.gz' --exclude='*.txt' --exclude='*.gif' --exclude='*.json' --exclude='*.mp4' --exclude='*.png' -czf csv_archive.tar.gz *

mv csv_archive.tar.gz ~/workspace/.
