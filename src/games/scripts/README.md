# Further Pong Projects 

Originally this project and repository were focused on using Large Language Models to play Pong. After following this course for some time the project focus moved to playing Pong with `vjepa2`. All the scripts in this folder, along with the scripts in the `notebooks` folder are somehow related to `vjepa2.` 

There is a common design philosophy that says pick one function for your coding and when you implement it, implement it well. We have not used that philosophy here. We do not use LLMs in all our code, but even when we do not use LLMs and instead we use vjepa2, we continue to focus on playing Pong.

## Project File Setup

For this set of scripts it is assumed that the user will set up a directory on their system called `workspace`. On modern Linux distros there is a `Projects` directory but the author of this repo does not use that name. Instead, all code goes into the `workspace` folder.

The `workspace` folder is just a regular folder in the home directory of the user. It would be found at `~/workspace/`.

There are three important directories in the `workspace` folder. The first is this repo. It holds the Pong game files. The second is the `vjepa2` folder. This goes in the `workspace` file also. Finally there is the home of all the data for the `vjepa2` project. This goes in the `workspace` folder also. The data folder is `VJEPA2_FILES/demo/`.

The original `games-llm` project uses LLMs to play 'pong.' That code is called from this repo, in the `~/workspace/games-llm/src/games/` folder. This `games-llm` repo also houses code that tries to use `vjepa2` to play 'pong.' Some of the code for this experiment is found in this directory and the `notebooks` directory. The code from the `notebooks` directory needs to be copied to the `vjepa2` repo, and then executed there.

If you want to use a folder other than the `workspace` folder, you need to rewrite some of the code in the `notebooks` folder, and if you use the launcher scripts, you may need to edit some of them also. There is also code in the `games-llm` project that uses the `workspace` folder name for the default file storage location.

## Execute these commands in your 'workspace' directory. 

```
cd ~/workspace 
git clone https://github.com/radiodee1/games-llm.git ## <-- this may be private...
git clone https://github.com/facebookresearch/vjepa2.git
```

## Some system packages need to be present

```
sudo pacman -S swig hdf5 vtk
#sudo apt update && sudo apt install -y swig libhdf5-dev libvtk9-dev

```
## Preperation 

You must set up python 3.10. You must also have a set of images in the `pic` folder. The script number is `13_corpus_1000_mt.sh`. When you run this the `pic` folder is created.

## vjepa2 scripts

Here are some vjepa2 scripts. These scripts are to be copied to the `vjepa2` folder. Then they should function correctly. There is a script in this folder that will do the copying. It's called `./02_copy_scripts.sh` There is another script called `./03_copy_games.sh` that copies the relevant game code to the `vjepa2` folder. 

These scripts also copy some setup code for UV. After the code is copied, execute the 'uv init' command as shown below.

## Set up uv on vjepa2 folder 

Do this after copying all the `vjepa2` scripts to the `vjepa2` folder. The author of the `vjepa2` project uses 'conda' or 'miniconda' but we try to use 'uv.'

```
cd ~/workspace/vjepa2/ 
uv init
## or 
uv sync
```

## Project Status 

It is clear that the `vjepa2` project cannot play pong on its own right out of the box. Some amount of training must be done. At this stage of the project, we use LoRA to train some characteristics into the model. With 500 - 1,000 training samples we still don't have the model operating as we would like. It may be that the model doesn't respond to training until some larger number of samples is provided. This number might be 2,000 or even 20,000 or more. 

We are using a computer with no gpu, and our batch size is 2 images. The training would be categorized as 'Reinforcement Learning.' Essentially we show the model video of a computer playing pong, and then we give it the input of the computer to the game that would produce the movements on the screen. Finally we usually only show the model video where the ball is in play with the computer. In other words, we show the ball when it is being hit on the player's side. We do not show the ball when it is being fielded by the game.

Because our training takes so long, we don't expect exemplary results. We are using a laptop with nothing more than a CPU to do our initial testing. The training is very slow and the laptop heats up during the testing. We are fighting with time and temperature to complete this training. In the future we would like to train on a platform like `runpod` to see if our demo works.

## Training Data 

Below are some numbered steps for generating training data. Training data is important. Here I've tried to describe a good way to generate lots of mp4 video.

1. Review the contents of the file `./13_corpus_1000_mt.sh`. This file will run in the `vjepa2` folder, generating 1000 mp4 files. Each video will have 4 frames and a number in their file name that will identify them. Later we edit these files, so it might be better to run the command from the `./13_corpus_1000_mt.sh` file with something like 3000 for the corpus number.
2. After starting the command from the file, use the arrow keys to move the right paddle and play the game. During this time the up key moves the paddle up, the down key moves the paddle down, and every other key passes the 'wait' or 'no-op' signal to the program. The escape key will exit the program prematurely. This process takes some time, especially if you set the corpus number to something like 3000.
3. When the program ends you will have a folder at `~/workspace/vjepa2/pic/train/` that will contain what amounts to a recording of you playing pong with the computer. Also in that folder is a json file that contains all the labels for your movements during the game. Do not delete the label file.
4. Now we use Nautilus, the Linux/Gnome File Manager, to edit the files in one further step. First open the File Manager and navigate to the directory `~/workspace/vjepa2/pic/train/`. You will see all your mp4 files and importantly the thumbnails for each of those files. Here we use the keyboard to delete some files. Place the cursor on the first file and click it to highlight it. Now use the Right arrow and the delete key to edit the files. You want to delete files showing the ball traveling to the left paddle. The left paddle is the computer's paddle. You want to leave all files showing the ball traveling to the right paddle. The right paddle is the player's paddle.
5. You can get through the list of files quickly if you put one finger on the 'right' key and one finger on the 'delete' key. Start with the first thumbnail and make your way through all the files in order. Delete all files where the ball is in the left side of the field. This process can take some time. You will end up with approximately half of the files you started with.

At this point you want to `tar` your files. There is a script for `tar` that saves all the training data. You may also want to generate more training data. If so, move the files you just edited from the `train` folder to one of the folders `train2`, `train3`, or `train4`. Then go through the process above again to re-populate the `train` folder. Remember, always keep the json file with the mp4 files. The goal is to use all the training folders sequentially when the training is being done. Because the train script puts the training data in the `train` folder every time it is run, special care has to be taken to save the mp4 files after each run of `./13_corpus_1000_mt.sh`. Bye the way, in `./13_corpus_1000_mt.sh` the 'mt' in the title stands for 'Mechanical Turk'. There is a script that does something similar using 'AI' to control the right paddle. That script is  called `./12_corpus_1000_ai.sh`.

## Follow this link to the original 'vjepa2' project.

https://github.com/facebookresearch/vjepa2
