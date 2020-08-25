#!/bin/bash

nitrogen --restore &
redshift -l (your location) &
picom &
xset r rate 300 50 &
setxkbmap -option caps:swapescape
setxkbmap -layout it
