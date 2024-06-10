# SpooKey

"spooky action at a distance" + "key" = "spookey"

Control your computers through SSH.

Do you have access to ssh into your computer, but don't have a keyboard to control it? This program creates a virtual keyboard and forwards all keyboard events it can capture to the remote device.

## Installation

1. ssh into remote machine
2. `sudo python3 spookey.py`

> [!IMPORTANT]
> Please make sure you do not ssh and use a multiplexer like tmux or zellij.
> These programs intercept a lot of the keypresses you would actually like to send to the native machine.

## TODO

- [ ] get ESC working
- [ ] get ctrl+KEY working
- [ ] visualize custom binding map

I am thinking that creating a gui program for all of this will be better because:

1. you don't have to worry about multiplexers and other programs like the terminal itself intercepting key presses
2. you can visualize your keypresses

The downside is that it is not nearly as simple as ssh + spookey = remote device keyboard :(.
