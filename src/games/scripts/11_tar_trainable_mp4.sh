cd pic

tar --exclude='*.gz' --exclude='*.png' --exclude='*.txt' --exclude='*.gif' -czf train_archive.tar.gz *

mv train_archive.tar.gz ..
