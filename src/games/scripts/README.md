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

Because our training takes so long, we don't expect exemplary results. We are fighting with time and temperature.

## Follow this link to the original 'vjepa2' project.

https://github.com/facebookresearch/vjepa2
