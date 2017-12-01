# Kalinesweeper
Minesweeper using pygame

## Before playing
To be able to play the game you need to have both python (preferably python 3) and pygame install on your machine.
To install pygame you just have to follow the stages described on the link below depending on the OS your are using:
https://www.pygame.org/wiki/GettingStarted

## Launch the game
Once everything is installed all you have to do is clone the repository Kalinesweeper and run the script play.py.

## The game itself
There are three screens in the game:

### The first screen
In this view you can choose the size of the minesweeper board in which you want to play and the number of mine in it. To do that you just have to select one of the three fields (by clicking on it or using the keyboard), tap a number in it, do the same for the other fields and then press Enter. If you just press Enter without completing the form or with some fields containing other characters than integers, the game will be launched with the default parameters.

### The second screen
This is the minesweeper screen in which you can play freely with the mouse. The controls are
* Left click to reveal a case
* Right click to put a flag
* Q (Keyboard button) to quit the game
When the game is finished (win, lose or quit), you have to press Enter to pass to the final screen (a reminder will show up)

### The third screen
This is where you can choose wether or not you want to play again. You just have to choose between the two buttons (yes and no) that you select using the Keyboard + Enter or using the mouse
