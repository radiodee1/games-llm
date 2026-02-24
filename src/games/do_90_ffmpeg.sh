
cd pic 

ffmpeg -framerate 16 -i figure_%010d.png -c:v libx264  -vf "scale=648:448:flags=neighbor" -crf 0  -pix_fmt yuv444p output.mp4


## magick figure_000000000*.png -delay 100 -loop 0  fig_0.gif
## ls figure_{0000000001..0000000012}.png

