# amcp
Model Context Protocol and Random LLM Stuff

## Projects/Folders

* There are three mcp projects in this repo. One is called 'weather' and it is an example of a working mcp server culled from internet posts. The second is called 'audio' and it contains speech-to-text and text-to-speech code. The third is called 'remember'. I wrote the second and third -- 'audio' and 'remember' server -- and I use the first, the 'weather' server, as an example and a reference.

* There is also a 'local' folder which contains scripts for setting up your environment. Specifically the scripts help set up a local llm on your computer. The llm is a 7B model. This is the directory with the docker code.

* There is a 'visual' folder that has a project that runs a visual model. This project does not use MCP. In fact it is an attempt to make a model play a simple computerized version of PONG.

## Image from PONG

This image comes from the code found in the 'visual' folder. Here I've tried to get an LLM to play Ping Pong. The first image is included to show the size of the game field, and show the basic operation of the paddles. There is an arrow in the image that points in the direction of the movement of the ball.

Making this image, the LLM was not used. For this reason the right paddle does not move. During actual testing the LLM is controlling the right paddle.

![ Image of game ](./pic/basic.gif)
