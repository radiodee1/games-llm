# Epic Runs - `pygame_dots.py` 

The idea here is to construct an image, once for each time step, that shows a group of dots. Then you ask the model to tell you how many are in the picture. Not all LLMs can do this. It seems, though, that the larger models can, and some of the smaller models cannot. It goes without saying that the models in question need to have visual input.

Here is an image showing a typical group of dots. The dots picture is passed to the LLM as a `png`.

![ Dots Image ](/pic/dots.png)

This is a ridiculously small sample of output.

| Date | Time | Total | Model | Average | Percent Right | Elapsed Time | Image Size | Description |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 05/13/26 | 8:37am | 3 | gemma4:e4b | 7 | 0 | 0:32 | Largest | Local |


```
model: gemma4:e4b
l_score: 0 r_score: 0
step-count: 3
Elapsed time: 0:32 minutes
---
percent right 0
average 7
```

### Comparison Goals

We want to try four models. Two of the models should be small local models. The third would be an OpenAI model, and the fourth would be something like Google's Gemini.

This is a ridiculously small sample of output.

| Date | Time | Total | Model | Average | Percent Right | Elapsed Time | Image Size | Description |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 05/13/26 | 12:12pm | 50 | gemma4:e4b | 4 | 62 | 9:29 | Largest | Small Local |
| 05/13/26 | 2:17pm | 50 | gpt-5.2 | 4 | 96 | 0:57 | Largest | Large Remote |
| 05/14/26 | 12:26pm | 50 | gemini-3.1-pro-preview | 5 | 100 | 4:48 | Largest | Large Remote |
| 05/14/26 | 1:55pm | 50 | qwen3-vl:4b | 5 | 76 | 38:17 | Largest | Small Local |

Below is some screen content for the first row of the table.

```
model: gemma4:e4b
l_score: 0 r_score: 0
step-count: 50
Elapsed time: 9:29 minutes
---
percent right 62
average 4
```

Note, there's content in this screen shot that applies only to the Pong environment. Below is some text from the second row of the table.

```
model: gpt-5.2
l_score: 0 r_score: 0
step-count: 50
Elapsed time: 0:57 minutes
---
percent right 96
average 4
```

Below is more text from the 'gemini-3.1-pro-preview' run.

```
model: gemini-3.1-pro-preview
l_score: 0 r_score: 0
step-count: 50
Elapsed time: 4:48 minutes
---
percent right 100
average 5
```

Final row of table.

```
model: qwen3-vl:4b
l_score: 0 r_score: 0
step-count: 50
Elapsed time: 38:17 minutes
---
percent right 76
average 5
```
