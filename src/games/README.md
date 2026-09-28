# LAUNCHER SCRIPTS

The launcher scripts all include numbers with the filename. This is so that they show up in a certain order when the user executes `ls`. In this repository that's not so important. The only item that needs to be executed in any order is the `do_10_ollama.sh` script, which sets up ollama on the computer. For testing with local LLMs, that script needs to be run first. In most all other cases there is no order constraint. The practice of numbering the shell scripts is maintained, though, as it might be used later on. The numbers in the filenames go up by ten with each file. This is so that if it were necessary, a script could be inserted between two others. As noted, that's not a likely scenario in this repository.

This list shows the first set of launcher scripts. More may be added later without documentation.

- `ale_10_pong_gpt52.sh` - Simple script for launching the ALE / Gymnasium Pong game.
- `ale_20_lunarlander.sh` - Simple script for launching Lunar Lander.
- `ale_30_pong_gpt54.sh` - Simple script for launching the ALE / Gymnasium Pong game.
- `ale_40_gemini3flash.sh` - Simple script for launching the ALE / Gymnasium Pong game.
- `ale_50_no_llm.sh` - Test out main without calls to LLM.
- `ale_60_breakout_gemini.sh` - Breakout.
- `ale_70_gemma4_pong.sh` - More pong.
- `ale_80_test_dots.sh` - Test dots.

These launcher scripts are for local LLMs and remote LLMs with the pygame Pong code.

- `do_10_ollama.sh` - Setup ollama on your computer.
- `do_20_pixtral_large.sh` - Try pixtral with pygame Pong code.
- `do_30_gemini_arrows_for_mp4.sh` - Use Gemini LLM with pygame Pong code and save the images for conversion into an mp4 video file.
- `do_40_curl.sh` - Use curl to send a request to a local LLM with ollama.
- `do_50_gemini_double_arrow.sh` - Use Gemini LLM with pygame Pong code. Enable double arrows in the images.
- `do_60_openai_large_double_arrow.sh` - Use OpenAI with a larger image size and double arrows in the images.
- `do_70_openai_corpus.sh` - Use OpenAI and save images and text for later training. This code was never tested in training.
- `do_80_hinting_openai.sh` - Implement a special '--hinting' function to improve output.
- `do_90_ffmpeg.sh` - Some code to convert saved images into mp4 video file. Works best with larger images.



