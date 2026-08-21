# Project File Setup

For this set of scripts it is assumed that the user will set up a directory on their system called `workspace`. On modern Linux distros there is a `Projects` directory but the author of this repo does not use that name. Instead, all code goes into the `workspace` folder.

There are three important directories in the `workspace` folder. The first is this repo. It holds the Pong game files. The second is the `vjepa2` folder. This goes in the `workspace` file also. Finally there is the home of all the data for the `vjepa2` project. This goes in the `workspace` folder also. The data folder is `VJEPA2_FILES/demo/`.

If you want to use a folder other than the `workspace` folder, you need to rewrite some of the code in the `notebooks` folder, and if you use the launcher scripts, you may need to edit some of them also.

## vjepa2 scripts

Here are some vjepa2 scripts. These scripts are to be copied to the `vjepa2` folder. Then they should function correctly. There is a script in this folder that will do the copying. It's called `./02_copy_scripts.sh` There is another script called `./03_copy_games.sh` that copies the relevant game code to the `vjepa2` folder.

## some system packages need to be present

```
sudo pacman -S swig hdf5 vtk
```

## also, set up uv on vjepa2 folder.
Do this after copying all the `vjepa2` scripts to the `vjepa2` folder. The author of the `vjepa2` project uses 'conda' or 'miniconda' but we try to use 'uv.'

```
cd ~/workspace/vjepa2/ 
uv init 
```

## Execute this command in your 'workspace' directory. 

```
git clone https://github.com/facebookresearch/vjepa2.git
```

## Follow this link to the original 'vjepa2' project.

https://github.com/facebookresearch/vjepa2
