# Fedora Rebuild
#
# Python application to assist in fedora post installation
#
# Author: Pedro Guimarães
# Date: 2025-01-22
# Version: 0.1

# >> Missing <<
# NVIDIA
# extensions config
# fedora config text
# menu

# Importing os.system module
from os import system, path

try:
    folder = "venv"

    if path.isdir(folder):
        print("Enabling virtual environment...")
        system('sh ./run_first.sh')
    else:
        print("Creating virtual environment...")
        system('python -m venv venv')

        print("Enabling virtual environment...")
        system('source venv/bin/activate')
        system('pip install -r requirements.txt')
        #system('sh ./run_first.sh --install') 
except OSError as error:
    print(f"ERROR: Can not install or enable virtual environment: {error}")

#system('sh ./run_first.sh')


# Import project python files
import configs as configs
import packages as packages


#configs.dnf5()
#configs.grub("fullhd")
#configs.change_dns()
#packages.asus()
#packages.better_fonts()
#packages.vscode()
#packages.oh_my_zsh()
#packages.install_packages()
#packages.install_flatpaks()
packages.multimedia_group()
