# Fedora Rebuild
#
# Python application to assist in fedora post installation
#
# Author: Pedro Guimarães
# Date: 2025-01-22
# Version: 0.1

# NVIDIA

# extensions
# extensions config

# fedora config text

# Importing os.system module
from os import system


system('sh ./run_first.sh')


# Import project python files
import configs as configs
import packages as packages


#configs.dnf5()
#configs.grub_before_nvidia("fullhd")
#configs.change_dns()
#packages.asus()
#packages.better_fonts()
#packages.vscode()

##packages.oh_my_zsh()

#packages.install_packages()
packages.install_flatpaks()