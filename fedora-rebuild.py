# Fedora Rebuild
#
# Python application to assist in fedora post installation
#
# Author: Pedro Guimarães
# Date: 2019-06-01
# Version: 0.1

# NVIDIA

# flatpak

# extensions
# extensions config

# fedora config text

# Importing modules

#from sh import command
import subprocess

#result = command('./run_first.sh')
subprocess.run('sh','./run_first.sh')


import configs as configs
import packages as packages


configs.dnf5()
configs.grub_before_nvidia("fullhd")
configs.change_dns()
packages.asus()
packages.better_fonts()
packages.vscode()

##packages.oh_my_zsh()

#packages.install_packages()
#packages.install_flatpaks()