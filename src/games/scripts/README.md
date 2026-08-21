# vjepa2_scripts
some vjepa2 scripts. These scripts are to be copied to the `vjepa2` folder. Then they should function correctly. There is a script in this folder that will do the copying. It's called `./02_copy_scripts.sh` There is another script called `./03_copy_games.sh` that copies the relevant game code to the `vjepa2` folder.

## some system packages need to be present

```
sudo pacman -S swig hdf5 vtk
```

## also, set up uv on vjepa2 folder.

```
cd ../vjepa2/ 
uv init 
```

Use this code as example and also execute this command in your 'workspace' directory. 

```
git clone https://github.com/facebookresearch/vjepa2.git
```

https://github.com/facebookresearch/vjepa2
