#cd pic
# ffmpeg -framerate 16 -i figure_%010d.png -c:v libx264  -vf "scale=648:448:flags=neighbor" -crf 0  -pix_fmt yuv444p output.mp4

## magick figure_000000000*.png -delay 100 -loop 0  fig_0.gif
## ls figure_{0000000001..0000000012}.png

uv run ./main.py --model gpt-5.2 --plugin pong --sudden_death 2 --context_size 0 --image_strip -1 --q_len 3 --thinking --threshold 100 --stream --double_arrow --inverse_size 4 --no_llm 48 --video 4
