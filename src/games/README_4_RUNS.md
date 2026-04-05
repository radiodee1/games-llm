# Epic Runs - `ale_10_pong_gpt52.sh` 

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time   |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 04/01/26 | 1:03pm | Computer | gpt-5.2 | ? | 2 | 565 | 39:13 |


```
model: gpt-5.2
serves_num: 0
l_score: 2 r_score: 0
step-count: 565
Elapsed time: 39:13 minutes
```

### Re-Arrange Context

The original launcher specified that the model look at 4 images in succsession, with no previous context. The '--context' was set to 0 and '--q_len' was set to 4. This was so that the model could tell where the ball was moving to. If there were only one image, the direction of the ball would be impossible to determine. With 4 images it was like there was a tiny little video being transmitted to the model with each step. Unfortunately the model had no history, so every turn it looked at the four images and determined which or what action to take.

I wanted to give the model some history. I could do this by setting the context to some number. With the '--context' set to 3 or 4, the model would get information about its previous moves. The problem was that the program would also include all three (or four) images with each context step. I was considering making a special option in the model code that stripped the images from the previous context, but I decided against that.

What I settled on was to change the number of images to 1, and set the context to three. If the model only looked at the most recent image, there would not be enough information to see where the ball was going. That was assuming the model only looked at that most recent context. If the model could look at all the images from the previous context, then it could determine the ball direction. Not knowing weather or not the model could critically examine the previous images was the issue. Trying it out, it seems that the model does know the direction of the ball and the only way it could would be if the model looked at the previous context information.

The difference here is small. On one hand you have 4 images and zero past context. On the other you have four context frames with one image in each one. The benefit is not apparent, but if you note that the context also comes with a record of what the model was doing at each step, there is reason to believe that the change is positive. That extra recorded material might help the model plan the moves it makes in advance. The information would be organized in pairs. There would be one image and the move the model made then. Then there would be another image, and then the move that the model made then. Together the model might have a better idea of - possibly - how fast the paddle moves, and maybe some insight into how the ball moves.

This only works if the model can critically compare the images from one context iteration with the image in another context iteration. Luckily it seems that the model can do this. (I am using the OpenAI model for tests here.)

### More Runs

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time   |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 04/03/26 | 1:25pm | Computer | gpt-5.2 | ? | 2 | 476 | 17:18 |

```
model: gpt-5.2
serves_num: 0
l_score: 2 r_score: 0
step-count: 476
Elapsed time: 17:18 minutes
```

I counted the 'Right Bounces' at 5.



### Frameskip - Longer Runs

The ALE/Gymnasium agent name is 'PongNoFrameskip-v4'.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time   |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 04/03/26 | 2:01pm | AI | gpt-5.2 | ? | 2 | 1678 | 80:30 |

```
model: gpt-5.2
serves_num: 0
l_score: 0 r_score: 2
step-count: 1678
Elapsed time: 80:30 minutes
```

I counted the 'Right Bounces' at 6 here also. This run uses a frameskip of 1. The step-count is therefore something like 4 times higher. The frameskip is usually set to 4 so that the training process is less deterministic. Of course I am not doing training. I'm doing testing only and I don't want to add anything that would decrease deterministic outcomes. Since the frameskip is lower and the step-count is higher, this run may not be comparable to previous runs. Still, in this run the AI won the game.

There is also something called 'repeat_action_probability'. In the model used for this run the 'repeat_action_probability' is set to 0. This is another option, usually set to 0.25, that is meant to make training less deterministic. Again, I want more deterministic, not less.

### Google - More Runs `ale_40_gemini3flash.sh`

The ALE/Gymnasium agent name is 'PongNoFrameskip-v4'.

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time   |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 04/04/26 | 12:33pm | Computer | gemini-3-flash-preview | ? | 2 | 1080 | 49:00 |

```
model: gemini-3-flash-preview
serves_num: 0
l_score: 2 r_score: 0
step-count: 1080 
Elapsed time: 49:00 minutes
```

Another run that went well. Here the Right Bounces are only 3. The history mechanism was improved here and the 'context_size' was set to 3. 

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time   |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 04/05/26 | 8:00am | AI | gemini-3-flash-preview | ? | 2 | 958 | 33:12 |

```
model: gemini-3-flash-preview
serves_num: 0
l_score: 0 r_score: 2
step-count: 958
Elapsed time: 33:12 minutes
```


