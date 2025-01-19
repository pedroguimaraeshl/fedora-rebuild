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
import configs as cfg
from sh import which

result = which('./run_first.sh')

#cfg.dnf5()
cfg.grub_before_nvidia("hd")