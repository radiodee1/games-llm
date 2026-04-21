# ALE and Gymnasium 

Some time in early March of 2026 I found Gymnasium and ALE. These let you run actual Atari 2600 games on your computer using an emulator. The nice thing is that I fairly quickly got the Gymnasium import to work. As before the LLMs seem to play the game. The bad thing is that the LLMs that I tested don't play the game well - well being the operative word. I like testing with ALE and Gymnasium though. It feels very authentic. As for charting runs, I can not record the Right-bounces with ALE. I can only record scores and step-count. Sometimes, with the sudden_death_score setting at 2, the AI wins. I do not think that the pygame version of Pong should be compared with the ALE version.


<p align="center">
    <img src="/pic/figure_3.png" alt="Image of game">
</p>

ALE stands for 'Arcade Learning Environment'.

### Reformat Code 

At around this time I completed a major code reformat. There is now one main python file, and two seperate additional modules. One of these modules manages the interface between my code and the LLM that I'm using. The other module manages the game code for whatever game I want to run. I can now switch between different LLMs easily, and I can switch between entirely different games easily as well.

Finally I employ a series of launcher scripts that are numbered. The numbered launchers make it easy to remember what to do when you come back to the computer after some time away.

### General Questions: Convolution and Frameskip

Does the model see what I see? I think LLM's that use visual input still use convolution. When the model estimates the height of the ball on the screen, is that an accurate estimation? Maybe the convolution contributes to the model being able to do things like read text from signage, but maybe the model does not see the proper position of the ball.

To address this I have increased the image size.

Similarly, does the model see every frame? I think sometimes the png that the model is looking at does not contain the ball. Could this be possible? To address this I've increased the number of images to 10 in some tests.

### Invincible?

I've been looking for some setting that would make the LLM invincible in these tests. The LLM can certainly play the game. It does not always win, though.

For example, when the ball is moving towards the LLM's paddle, the LLM moves the paddle to the area of the ball. When it misses it seems to miss by a small margin. It's as if it is trying but in the end it makes some misadjustment because of the speed of the ball or the speed of the moving paddle. It does seem to address the problem of playing this game, but it seems to have a problem with some particular aspect of play. I would love to be able to fix this problem.


### ALE - Multiple Games

Using the ALE environment and the Pong game is good. There are many games that can be played from the ALE collection. I think it may be used by companies like OpenAI and Google already. My goal now is not to do training, but just testing with a LLM. I would like to be able to simply load up a game and have the LLM play it well, but as noted below, that may not be possible.


### Hallucinations 

Sometimes the model output will note the position of the ball on the screen incorrectly. For instance, it will say the ball height is above the paddle height so the paddle should move up. Sometimes, though, that's not the position of the ball. 

### Enhanced Prompt

Sometimes the output of the LLM is incorrect. What I've tried to do is to get very elaborate with the prompt so that the model has to go through more steps to get the answer. This seems to help. The gpt-5.2 model does not do 'thinking' but if, by specifying the individual steps, I can make it think through its actions, the outcome is usually better.

The problem with this is that the prompt is getting longer and more specific. I would like to be able to just load up a game and test it, but my experience shows that significant tweaking of the prompt is necessary for a good game experience.

### ALE Epic Runs

Many of the 'Right-bounces' in this run seemed to me to be very lucky. Also, the model stalled sometimes when my code was waiting for the gpt-5.2 api to reply to my prompts. I do think that 774 steps is good.

```
model: gpt-5.2
serves_num: 0
l_score: 1 r_score: 0
step-count: 774
Elapsed time: 41:51 minutes
```

| Date | Time | Winner | Model | Serves | Sudden Death | Steps | Elapsed Time   |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 03/29/26 | 7:53am | INTERRUPTED | gpt-5.2 | ? | 2 | 774 | 41:51 |

### ALE Pong Prompt

As I say above, this prompt is getting longer, so I don't think it conceivable that you could just load up a game randomly from ALE and get the LLM to play it. No matter which game it is, there wouuld probably have to be a period of modifying the prompt significantly before the LLM would play well.

> Pong! Return the ball to the oponent and score to win the game. You are the right paddle. Your paddle is green. Ignore the SCORE at the top of the screen. Notice the y position of the ball. If the ball is higher than you, move up. If the ball is lower than you, move down. Show some of your thinking process and then give your final answer. These are the actions you can take: "control.move.wait", "control.move.serve", "control.move.up", "control.move.down"

This is some typical gpt-5.2 output:

> I can’t show my full step-by-step thinking, but I can follow the rule: compare the ball’s y-position to my (right, green) paddle’s y-position.
> 
> Here the ball is clearly **below** the right green paddle, so I should move **down**.
> 
> **Action:** `control.move.down`

The model always says it cannot show full step-by-step thinking, but I find that if I specify the steps in the prompt, the results are better.
