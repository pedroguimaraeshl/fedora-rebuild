# Fedora Rebuild
#
# Python application to assist in fedora post installation
#
# Author: Pedro Guimarães
# Date: 2019-06-01
# Version: 0.1

# change DNS

# ASUS
# Better fonts
# NVIDIA
# VSCode
# oh-my-zsh
# packages
# flatpak

# extensions
# extensions config

# fedora config text

# Importing modules
from sh import run
import configs as cfg

run("run_first.sh")

#cfg.dnf5()
cfg.grub_before_nvidia("fullhd")