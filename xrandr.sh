#!/bin/bash

xrandr_output=$(xrandr --listmonitors)

# Use grep to find the lines containing DP-0 and DP-4
dp0_line=$(echo "$xrandr_output" | grep -m 1 "DP-0")
dp2_line=$(echo "$xrandr_output" | grep -m 1 "DP-2")
dp4_line=$(echo "$xrandr_output" | grep -m 1 "DP-4")

# Use awk to extract the monitor resolutions from the lines
dp0=$(echo "$dp0_line" | awk '{print $2}' | sed 's/[+*]//g')
dp2=$(echo "$dp2_line" | awk '{print $2}' | sed 's/[+*]//g')
dp4=$(echo "$dp4_line" | awk '{print $2}' | sed 's/[+*]//g')


echo "$dp0"
echo "$dp2"
echo "$dp4"


