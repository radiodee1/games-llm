# Visual Models - Initial Coding With Local Models
* This is the url for the original PONG code. The code is found in the file `pong_original.py`.

```
https://gist.github.com/vinothpandian/4337527
```

* Ollama supports some models that take images as input. I'm interested in seeing if these models can play video games. 

* I'm not doing any training at all. The test is weather or not the model in question can play a game at inference time, after training is over. 

* In this folder at least for starters I am trying to get `qwen3-vl:2b` to play `pong` against the computer. I pass the visual model a series of `png` files and some text, and ask the model to move one of the paddles with a special command. So far the model will use the command, but does not win the game. The model loses. It should be noted that the game plays out very slowly. The model takes several minutes to respond to each set of images because I am using just CPU processing.

* The early pong code relies on `python3-pygame`. It does not have many other requirements, so I do not use `uv` to manage dependencies in this folder for the early versions. Also, this code does not make use of the `tools` in the other parts of this repository. (There are three tools in this repository right now. They are `audio`, `remember`, and `weather`. I wrote `audio` and `remember`. The `weather` tool comes from the internet and is something I keep around as a refference.)

* In the final analysis, local models with visual abilities from Ollama don't perform the way I want. I don't know what they do well. Maybe they do optical character recognition very well. One thing they don't seem to do well is predicting where the ball is in this simple version of pong. The best of them, `qwen3-vl`, only picks up from the images clues about whether or not the ball is going to the right or left. None of the models tested detect the angle of the ball's movement, and many of the models don't get the ball's movement at all.


### Finding Better Models 

- The 'qwen3-vl:2b' model was used for initial development. The 4b and 8b varieties were tried also. It was found that they needed an arrow on the screen in order to estimate and understand the ball position. Even then, the model understood left and right pointing arrows but seemed unable to understand the angle that the arrow was pointing in. It is not clear why this happens, so it is time to maybe consider other models, and see if they all exhibit the same behavior.

- The models we are considering need to have vision capabilities and also be reasonably small. The thinking models should also be considered first, but the qwen3-vl models may be the only models with thinking. We want to start with 2b to 4b, and only go as high as 8b if it is really necessary.

- The models have to come from the Ollama.cpp site.

- We can do two tests. We can run the llm in the pong game, and we can call the Ollama program and pass it the picture of the game, and ask it to discuss what it sees.

![pygame pong image](/pic/figure_02.png)

>  the ./pic/figure_0.png picture is from the pong game play...
>
> ollama run qwen3-vl:4b "describe the arrow in this picture? is it pointing angled up or angled down? ./pic/figure_0.png"


### List

Below is a list of models offered for local use by Ollama.cpp. These are the ones I noted to myself as having vision properties. In parentheses after the model listing is a description of the model capabilities as I understand them. Some of the larger models were not tested.

- qwen3-vl:2b qwen3-vl:4b (does not see arrow angle. does see arrow left/right) 
- qwen3-vl:8b (does not see arrow angle. does see arrow left/right)
- gemma3:4b (gets right and left confused and sees arrow angle inconsistently.) 
- gemma3:1b (has no vision)
- moondream:1.8b (sees arrow pointing to center of field)
- granite3.2-vision:2b (does not answer in proper format. may not understand game.)
- ministral-3:3b (right and left may be confused as well as up and down. answers in nice format.) 
- ministral-3:8b 
- llava-phi3:3.8b (gets right and left backwards. answers the 'describe the arrow' question badly.) 
- llava:7b (answers the 'describe the arrow' question incorrectly and inaccurately.)
- bakllava:7b 
- minicpm-v:8b 
- llama3.2-vision:11b (answers the 'describe the arrow' question incorrectly and not consistently.)

So most of the models don't see the images correctly. Maybe I'll try OpenAI. The OpenAI model GPT5 gets the essance of what the arrows are doing from an uploaded picture and the 'describe the arrow' question text. It's funny that qwen3-vl models are the best of the group when testing out local models using Ollama. Those are the very first ones I tried.

That means that I'd be switching from locally hosted models to models hosted on-line. The on-line models are fast, but they cost money for access. The good thing is that they are very large compared to models hosted locally.

Locally, I was using a laptop for testing. I would edit code on my desktop, and commit to github. Then I would pull the github repository on the laptop and run for long periods of time there. I did this several times. This was good, as the models were slow. The laptop in question had a small gpu. The desktop I'm using has no gpu. I could use the laptop to get a little more efficiency, but now I don't need it, as the OpenAI models are fast. I suppose the downside is that they cost money. In any case, I don't need the laptop now.


