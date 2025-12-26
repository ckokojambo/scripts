#!/bin/bash

sudo apt update && sudo apt install -y locales && sudo locale-gen de_DE.UTF-8

sudo update-locale \
  LC_TIME=de_DE.UTF-8 \
  LC_NUMERIC=de_DE.UTF-8 \
  LC_MONETARY=de_DE.UTF-8 \
  LC_MEASUREMENT=de_DE.UTF-8 \
  LC_PAPER=de_DE.UTF-8 \
  LC_NAME=de_DE.UTF-8 \
  LC_ADDRESS=de_DE.UTF-8 \
  LC_TELEPHONE=de_DE.UTF-8

  sudo timedatectl set-timezone Europe/Berlin

  
