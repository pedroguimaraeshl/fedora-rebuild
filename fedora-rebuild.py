# Fedora Rebuild
#
# Python application to assist in fedora post installation
#
# Author: Pedro Guimarães
# Date: 2019-06-01
# Version: 0.1

# NVIDIA

# packages
# flatpak

# extensions
# extensions config

# fedora config text

# Importing modules
import configs as cfg
from sh import command

result = command('./run_first.sh')

#cfg.dnf5()
#cfg.grub_before_nvidia("fullhd")
cfg.change_dns()