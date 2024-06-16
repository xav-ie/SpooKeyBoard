# SpooKeyBoard

"spooky action at a distance" + "keyboard" = "SpooKeyBoard"

Control your computers through SSH! Do you have access to ssh into your computer, but don't have a keyboard to control it? This program creates a virtual keyboard and forwards all keyboard events from your terminal it can capture to the remote device.

This just takes your local ANSI inputs and escape sequences and converts them to uinput key combos. I am honestly surprised something like this does not exist, yet. 

## Installation

0. `git clone` this repo
1. ssh into remote machine
2. `nix-shell`
3. `sudo python3 spookeyboard.py`

> [!IMPORTANT]
> Please make sure you do not ssh and use a multiplexer like tmux or zellij.
> These programs intercept a lot of the keypresses you would actually like to send to the native machine.
> Best results are with a boring terminal with no intercepting of key combos.

## TODO

- [ ] custom bindings
- [ ] refactoring
- [ ] rewrite in TS? <- I ran into several issues using python that would have been caught by TS.
- [ ] add mouse support? <- I am not sure a terminal can detect mouse move events... Maybe mouse drag events could be interpreted as mouse move events...
- [ ] quiet mode
- [ ] flakify for easier running

I am thinking that creating a gui program for all of this will be better because:

1. you don't have to worry about multiplexers and other programs like the terminal itself intercepting key presses
2. you can visualize your keypresses easily. 

The downside is that it is not nearly as simple as ssh + SpooKeyBoard = remote device keyboard :(.
