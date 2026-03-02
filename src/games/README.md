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

```
# the ./pic/figure_0.png picture is from the pong game play...

ollama run qwen3-vl:4b "describe the arrow in this picture? is it pointing angled up or angled down? ./pic/figure_0.png"
```

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


### OpenAI

OpenAI and Google Gemini models need to be paid for. You need to set up an account, and after doing that you can download an API KEY. The key is secret, and goes in the `.env` file.

The `.env` file should look like this. Commented lines are not important:

```
OPENAI_API_KEY="openai-api-key-here"
#OPENAI_MODEL="gpt-4o-mini"

GEMINI_API_KEY="gemini-api-key-here"
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials/file.json

#GOOGLE_GEMINI_MODEL="gemini-3-flash-preview"
```

To use OpenAI models you need to set up an account with them and pay some money. Then you can get an OPENAI_API_KEY. This key must be placed in your `.env` file. You can use any OPENAI_MODEL you like.

Similarly, Google's Gemini models require an api key. The key should be placed in the `.env` file. In its present configuration the program looks for the keys in the `.env` file. It does not pay attention to the MODEL specification in the file. The model name, for example, and the URL, are not found hard coded in the `.env` file.

### Some Results

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Strip Size | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/01/26 | 11:06am | Computer | gpt-4o-mini | ? | 2 | 213 | 3:42 | 3 | 3 | 80 |
| 02/01/26 | 11:19am | Computer | gpt-4o-mini | ? | 2 | 290 | 3:56 | 3 | 1 | 80 |
| 02/01/26 | 11:26am | Computer | gpt-5.2 | ? | 2 | 328 | 4:23 | 3 | 1 | 80 |
| 02/01/26 | 11:34am | Computer | gpt-5.2 | ? | 2 | 231 | 3:00 | ? | 1 | ? |
| 02/01/26 | 11:40am | Computer | gpt-5.2 | ? | 2 | 134 | 1:38 | 2 | 0 | 50 |
| 02/01/26 | 12:01pm | Computer | gpt-5.2 | 3 | 2 | 255 | 3:12 | 2 | 0 | 50 | 


- `Winner` - The computer always won. The algorithm used for controlling the computer's paddle is simple, but unbeatable for most settings of 'Threshold'. See 'Threshold' below.
- `Model` - The first couple of models I tested were 'gpt-4o-mini'. Then I switched to 'gpt-5.2', which generally did better, providing higher 'Steps' and also 'Elapsed Time'.
- `Serves` - When recorded this number is usually 2. It corresponds to the 'Sudden Death' setting.
- `Sudden Death` - The first player to get to two scores wins.
- `Steps` - Number of steps that transpired from the start of the program.
- `Elapsed Time` - Time spent playing the game.
- `Strip Size` - This is the number of frames from the game that are included in a single png image. The images together look something like a comic book strip. It is typically between 1 and 3.
- `Context Size` - This is how many previous AI answers are included in the prompt. A number of 3 is common for me, and a number of 0 means the model has no previous answers to work with.
- `Threshold` - This is the percentage of the time that the computer tries to move its paddle. The algorithm dictates that, for example, 80 percent of the time the paddle will move to the horizontal position of the ball. 20 percent of the time it does not even see the position of the ball. The computer always wins when the percentage is higher. I try 50 percent in some of the tests. That may even be too high.

The AI seems to be able to return the ball once if the serve is to its side. When the ball goes to the computer's side the AI does not know what to do. Surely this is not the biggest problem, for if it was the solution would be to limit the strip size and the context size and let the AI think the ball is new on the field every time.

The overall time of gameplay seemed to go up when the model was switched from gpt-4o-mini to gpt-5.2. This is encouraging. It says to me that improvements can still be made.

### `--video_openai` setting 

The '--video_openai' setting takes it's number of images from the '--q_len' parameter. The idea is to give the visual images to the model in a way close to how it expects to receive video. Maybe it will work better with these provisions. Note also that in the code the 'detail' parameter is set to 'high' for each image.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Strip Size | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/02/26 | 1:11pm | Computer | gpt-5.2 | 3 | 2 | 270 | 3:47 | 0* | 0 | 50 |

'*'-The 'strip_size' here is 0, but three images are used by the model to simulate video using the '--video_openai' setting. The 3 images are shown to the model as if they were recorded as video. It's hoped that by putting them in this format the results will be better. Only one run is shown here.

### Striping The Paddles 

I have tried to make the paddles more visible. I make them two-colored now. The computer paddle is one combination, and the AI paddle is a different combination. They do not look exactly the same.
| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/03/26 | 9:09am | Computer | gpt-5.2 | 4 | 2 | 395 | 5:47 | 3 | 0 | 50 |

This 'Elapsed Time' value is higher than many recorded values from the previous day. It may be that the Threshold is lower and by luck the AI scored once before the game was over. That does not mean that the striping of the paddles didn't have any effect. It may be the first score by the AI recorded.

### Comparing Runs 

With a threshold over 50 percent the computer almost never misses the ball. It is not likely under those circumstances that the computer would ever loose a game. You would just have to wait long enough and the AI would make some mistake, and the computer would win. If the threshold is set at something very high, like the 80 percent setting of the early runs, then success for the AI would be whenever the playing time was longest. The strategy would be to set the Threshold at 80, set the Sudden Death to 2, and record the statistics for the run. Then, the longer runs would be signs that the AI is doing better and that the programmer was doing their job.

The algorithm for the computer is very simple. It looks at the y value of the ball. If the ball is higher than the paddle, and a random test succeeds, then move that paddle up. If the ball is lower than the paddle, and a random test succeeds, then move the paddle down. The random test mentioned compares a call to the python 'random' library to the Threshold set on the 'pong.py' command line. This is the same Threshold as in our tables. The computer has many chances to move the paddle to the ball. A setting of 80 ensures the ball is almost always returned. A setting of 50 is not a big difference from 80, and surely does not signify that 50 percent of the time the ball is returned. The ball is still returned a high percent of the time.

During the period where I was using the local visual models, the AI would sometimes reply with hallucinations or weird text, depending on the model I was using. Then with other models the AI would reply with the text that was required to play the game. At these times the AI would reply with 'control.move.up' and 'control.move.down'. The AI was at least playing the game. Often the AI could not score a point, not even hit the ball when it came to the paddle. If it could never hit the ball then it could not win the game. Then I could say that the AI was playing, but not winning. Now the AI, with a model that's much larger from OpenAI, does hit the ball sometimes. It is playing the game at a different level.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/03/26 | 2:13pm | Computer | gpt-5.2 | 3 | 2 | 324 | 4:43 | 3 | 0 | 80 |
| 02/03/26 | 2:54pm | Computer | gpt-5.2 | 4* | 2 | 328 | 5:03 | 3 | 0 | 80 |

'*'-The AI scored once in this run, randomly. This drove the game on and sent the elapsed time higher.

### Failing and `--hinting`

At the time of this writing the model plays the game, but does not win. Frequently the model will hit the ball back to the left side. Unfortunately the model does not always hit the ball to the left side. Quite frequently the model moves the paddle to the position that the ball is set to travel to, and then for no known reason, the model moves the paddle away. I don't know why this happens, but it does. I thought that possibly the direction arrow was obscured when the ball got very close to the paddle, so I added a second direction arrow. Unfortunately this must not have been the reason because the second arrow did not get rid of the problem or the behavior.

I want the model to return the ball every time. The computer can reliably return the ball, so I think the AI should be able to do so as well.

I am considering a '--hinting' option that confirms for the AI when it is in the area where the ball will end up. This would be close to cheating, but might work. I feel I could use the function for a line and figure out where the ball is going to strike, and then if the model puts the paddle there, to tell the model in the prompt that it was doing the right thing. By making it an option I can stop using it if later on I figure out what the actual problem really is.

### `--hinting` Implemented 

Hinting, as described above, makes a big difference. I ran the program and stopped it manually at around the 7 minute mark. There were no signs of it stopping. Other statistics for this run are: Left bounces 5, Right bounces 4, and a single arrow was used. It could be that if I left it running the OpenAI model could charge me a lot of money. It was obvious right away that the `--hinting` was going to work.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/04/26 | 2:38pm | INTERRUPTED | gpt-5.2 | 2 | 2 | 461 | 7:13 | 3 | 0 | 80 |

The AI is not invincible here. If it doesn't go to the hinting y location, then the program doesn't tell it to wait for the ball. This could happen for instance, when the ball bounces off of the wall just before it gets to the area where the paddle should be waiting for it. The AI has to have the paddle go to the right location before the hinting will start.

Below I will put examples of the prompt used.

### Prompt 

The standard prompt is below:

```
Turn-based Pong or Tennis game. AI vs computer. - Their score 1 / Your score 0 - Enter "control.move.up" or "control.move.down" to move the Paddle in anticipation of the ball. The paddle only moves up and down. Enter "control.move.wait" to skip one turn. The ball is red. The ball is moving in the direction of the arrow. The arrow is blue. You, the AI, are the right paddle. Your paddle is blue and green. Hit the ball if it comes to you. AI must use the picture and reply to play the game! Answer in one line under 20 characters.
```

If `--hinting` is on, and the AI has visited the spot that the ball is going to go to, the phrase below is added to the prompt:

```
Hint: wait right there!
```

### The Problem With `--hinting`

It might be seen as cheating somehow. It's like making the paddle very very large. It certainly makes the job of the AI alot easier. What would be best is if the prompt could be changed somehow to allow the AI to play the game better without `--hinting`. This would still be an OpenAI sort of project. The local models have shown that they don't see the things that I would like them to see in order to play this simple video game. OpenAI is more than capable enough to do this job. Maybe I can give it something in the prompt that will change things. Maybe my current prompt is somehow ambiguous and does not tell the AI how to play this game. 

First modified prompt:

```
Turn-based Pong or Tennis game. AI vs computer. - Their score 1 / Your score 0 - Left Bounces 4 / Right Bounces 2 - Enter "control.move.up" or "control.move.down" to move the Paddle in anticipation of the ball. The paddle only moves up and down. Enter "control.move.wait" to skip one turn. The ball is red. The ball is moving in the direction of the arrow. The arrow is blue. You, the AI, are the right paddle. Your paddle is blue and green. Estimate the angle of the ball from the arrow and move your paddle to the position where you can hit the ball back to the other side. Hit the ball when it comes to you. This is the only way to win. AI must use the picture and reply to play the game! Answer in one line under 20 characters.
```

Note that there is extra language in the prompt telling the AI to go to the location where the ball will be.

Second modified prompt:

```
Turn-based Pong or Tennis game. AI vs computer. - Their score 1 / Your score 1 - Left Bounces 4 / Right Bounces 4 - Enter "control.move.up" or "control.move.down" to move the Paddle in anticipation of the ball. The paddle only moves up and down. Enter "control.move.wait" to skip one turn. The ball is red. The ball is moving in the direction of the arrow. The arrow is blue. You, the AI, are the right paddle. Your paddle is blue and green. It is very small. Estimate the angle of the ball from the arrow and move your paddle to the position where you can hit the ball back to the other side. Hit the ball on the MIDDLE of the paddle. Hit the ball when it comes to you. This is the only way to win. AI must use the picture and reply to play the game! Answer in one line under 20 characters.
```

Note that ther is extra language in the prompt telling the AI to hit the ball with the MIDDLE of the paddle.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/08/26 | 9:48am | Computer | gpt-5.2 | 4 | 2 | 329 | 4:02 | 3 | 0 | 80 |

Here is some screen output from this run. Unfortunately this run may not be typical of future runs.

```
model: gpt-5.2
serves_num: 4
Left-bounces: 4 Right-bounces: 4
l_score: 2 r_score: 1
step-count: 312
Elapsed time: 4:02 minutes
```

There were 4 right bounces. That is a marked improvement. Also the AI scored and the elapsed time is larger than most other runs. Another good run is below.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/08/26 | 11:15am | Computer | gpt-5.2 | 3 | 2 | 360 | 4:29 | 3 | 0 | 80 |

This run went well.

This prompt uses strategy II. Third modified prompt:

```
Turn-based Pong or Tennis game. AI vs computer. - Their score 1 / Your score 0 - Left Bounces 3 / Right Bounces 2 - 
 You, the AI, are the right paddle. Solve this problem in steps: 
1. Notice the position of the ball. What is its HEIGHT or Y value? 
2. Notice the position of the right paddle. What is the HEIGHT? 
3. Calculate the horizontal line that comes from the ball across the screen.
4. Keep the paddle always at the height of the ball. 
5. Enter "control.move.up" or "control.move.down" to move the Paddle to the ball. 
You move your paddle a small amount from where it already is. 
Hit the ball in the MIDDLE of the paddle. 
If the ball passes the paddle you will lose a point.
NOTE:
 Your paddle is blue and green. It is very small.
 The paddle only moves up and down.
 Enter "control.move.wait" to skip one turn.
 The ball is red. The ball is moving in the direction of the arrow. The arrow is blue.
 The shadow of the ball, drawn in grey, also shows the direction the ball is taking. It always follows the ball.
 Hit the ball when it comes to you.
 This is the only way to win.
 AI must use the picture and reply to play the game! Show your thinking and then reply in one line.
```
| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/09/26 | 1:13pm | Computer | gpt-5.2 | 2 | 2 | 324 | 8:37 | 3 | 0 | 80 |

Some screen output from this run.

```
model: gpt-5.2
serves_num: 2
Left-bounces: 3 Right-bounces: 2
l_score: 1 r_score: 0
step-count: 324
Elapsed time: 8:37 minutes
computer paddle up -8
hint_y 85.5
sudden_death_score 2 0
```

Going back to older prompt, strategy I:

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/10/26 | 7:58am | Computer | gpt-5.2 | 4 | 2 | 507 | 8:25 | 3 | 0 | 80 |


The `--hinting` option was not used. Some screen output for this run.
```
model: gpt-5.2
serves_num: 4
Left-bounces: 5 Right-bounces: 5
l_score: 2 r_score: 1
step-count: 508
Elapsed time: 8:25 minutes
```
### Strategy I and II 

* There are two strategies that I've suggested that the AI should use in the prompt. One involves looking at the angle that the ball is traveling in, and then projecting a line from the ball to the right side of the screen. Then the model would move the paddle to the spot where the line crosses this right side. The `--hinting` option works very well with this strategy. It also works fairly well without the 'hinting' option.

* The second strategy involves estimating the height of the ball on the screen and moving the paddle to that height. When this is done repeatedly the paddle ends up in a position to return the ball. The `--hinting` option does not do anything special for this strategy. This strategy does, in fact, mirror the strategy that is employed by the left paddle. It's very simple to code this kind of behavior, so this is the method that the computer uses with the left paddle and has used throughout the project.

The prompt for the tests using the second strategy included a line to have the model show it's thinking. The model did this. The reply included some description of the vertical position of the ball and the paddle and some kind of decision on which way to move the paddle given that description. The funny thing was, when consulting the image of the game at that time, the ball and paddle where not always in the positions described by the AI.

With the first strategy the model had a habit of going in the right direction with the paddle and then just before the ball moved to that spot, the AI would move the paddle away. This is why the 'hinting' would work. Again, without the hinting the model did well, but the strange behavior would return sometimes. There was no way to determine what the thinking process for this strategy was. 

### Different Model 

The error that the second prompt shows might be what they call hallucinations. If this is so, it might be happenning in both strategies, with the second strategy being the one where the error can actually be pointed out. In other words, it may be happenning in both cases, but is visible only when the 'thinking' is shown to us in the second strategy. What does this mean? Maybe the thing to do is to try another model. At the time of this writing the latest model is 'gpt-5.2'. Maybe use an older model or wait for another one to be released? 

I should note here that I've tried 'gpt-4o-mini' and 'gpt-4o' and they do not give better answers than 'gpt-5.2'. The answers are worse. Also, it could be a long time before OpenAI releases another model in the 'gpt' series. I may just be stuck with the results I have. 

At this time we create a repo for the project. Before this the pong code lived as a subdirectory of another project that was oriented around MCP servers. Also at this point we start to code all 'requests' code in a separate sub module. That is to say all 'post' requests and the code around them are moved to a separate sub module inside the 'games' folder. There are separate classes for OpenAI, Ollama, and Gemini. The code is much neater.

### Gemini Google Model

It became clear that the Google Gemini model took input in the same format as OpenAI. For this reason coding a python class for Gemini was fast. The model itself takes more time, but performs at the task better.

```
model: gemini-3-flash-preview
serves_num: 3
Left-bounces: 1 Right-bounces: 2
l_score: 0 r_score: 2
step-count: 57
Elapsed time: 12:09 minutes
```

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/19/26 | 2:50pm | AI | gemini-3-flash-preview | 3 | 2 | 57 | 12:09 | 3 | 0 | 80 |

With this test the AI wins for the first time. This could be a fluke of the random number generator. In the future we will set the threshold to 100. Then we will measure success by the number of steps that the model can continue to take before losing sudden death style.

Keeping track of the elapsed time would be good, but the Gemini model is slower than the OpenAI models. The Ollama models are local, and they are very slow. The best measure of success would be the 'Steps'.

### `--threshold` 100 

We are most interested in testing the Gemini model but we may try out the OpenAI model for one or more of our runs, just for comparison. 

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/20/26 | 10:40am | Computer | gemini-3-flash-preview | 3 | 2 | 78 | 17:31 | 3 | 0 | 100 |


```
model: gemini-3-flash-preview
serves_num: 3
Left-bounces: 3 Right-bounces: 1
l_score: 2 r_score: 0
step-count: 78
Elapsed time: 17:31 minutes
```

---
| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/20/26 | 11:10am | Computer | gemini-3-flash-preview | 4 | 2 | 95 | 18:38 | 3 | 0 | 100 |


```
model: gemini-3-flash-preview
serves_num: 4
Left-bounces: 3 Right-bounces: 3
l_score: 2 r_score: 1
step-count: 97
Elapsed time: 18:36 minutes
```
---
### `--double_arrow` Setting 

With the original arrow position, the arrow itself dissapears when the ball is closest to the goal. Since the image size is only three, this is when the arrow is most necessary. To remidy this, we have a second arrow. This one does the same as the first one, but it follows the ball instead of leading the ball. When the ball gets close to the goal, the second arrow is behind the ball, so it does not dissapear. In the OpenAI models, using the double arrow does not help much. In the Gemini model that we are testing here, it may be helpful.

In the first of the following runs the AI wins again.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time | Num of Images | Context Size | Threshold |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/21/26 | 7:32am | AI | gemini-3-flash-preview | 3 | 2 | 85 | 18:27 | 3 | 0 | 100 |
| 02/21/26 | 3:38pm | INTERRUPTED | gemini-3-flash-preview | 2 | 2 | 133 | 30:21 | 3 | 0 | 100 |

```
model: gemini-3-flash-preview
serves_num: 2
Left-bounces: 5 Right-bounces: 5
l_score: 1 r_score: 0
step-count: 133
Elapsed time: 30:21 minutes
```

The Gemini model seems to understand the game. Looking at the model output, one gets the feeling that maybe the Gemini model has played simple video games before. Some model output here: 

```
Based on the latest image (Image 3), the red ball is currently in the bottom-left area of the court and is moving further down and to the left, as indicated by the blue arrow. 

Since the ball is heading toward the bottom corner, it is highly likely to bounce off the bottom wall or the left paddle and then travel diagonally upward toward the right side of the screen. My paddle (the blue and green one on the right) is currently positioned quite low. To anticipate the ball's upward trajectory after its next bounce, I should begin moving my paddle toward a more central or higher position.

**control.move.up**
```

### Epic runs

We started out this project with the models not understanding how to play the game. It didn't last for long, but at the start they couldn't figure out how to respond. Now that's the distant past. The models have in a couple of cases, actually won the game. Now I'm going to wrap this stage of testing up and try to get one or two more epic runs. I want to follow the output for a long time. 

I'm also going to start tracking the value of what's called the 'Right-bounces' above. From the beginning I've been changing the code as I do the testing. Then I change the model. For this reason 'Time Elapsed' and 'step-count' cannot be compared with different models and similarly with different snapshots over time. I've found that the Elapsed Time for gemini-3-flash-preview is much greater than that for OpenAI gpt-5.2. Also the step-count for gemini is about a third the size of gpt-5.2. What has obviously improved is the 'Winner' status. For gemini I've had to interrupt the model. Who knows where those runs would have ended.

I'm going to try a couple of runs just aimed at keeping the model going as long as possible. I'm switching from the 'gemini-3-flash-preview' model to the 'gemini-3-pro-preview' model. I will record 'Right-bounces' in my chart. I'll take out 'Context Size' and 'Num of Images'.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time  | Threshold | Right Bounces |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 02/24/26 | 12:24pm | AI | gemini-3-pro-preview | 2 | 2 | 76 | 66:28 | 100 | 4 |

```
model: gemini-3-pro-preview
serves_num: 3
Left-bounces: 2 Right-bounces: 4
l_score: 0 r_score: 2
step-count: 76
Elapsed time: 66:28 minutes
```
Back to OpenAI:

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time  | Threshold | Right Bounces |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 03/02/26 | 12:34pm | Computer | gpt-5.2 | 3 | 2 | 407 | 10:56 | 100 | 4 |


From the screen:
```
model: gpt-5.2
serves_num: 3
Left-bounces: 5 Right-bounces: 4
l_score: 2 r_score: 0
step-count: 408
Elapsed time: 10:56 minutes
```
