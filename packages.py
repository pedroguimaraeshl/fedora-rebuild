# Fedora Rebuild - packages.py
#
# Functions to install some packages in Fedora
#
# Author: Pedro Guimarães
# Date: 2019-06-01
# Version: 0.1


from sh import grep, sed, contrib, mv, command, cp


# Function to install ASUS ROG Gui and Asusctl packages
def asus():
    print(">> ASUS CONFIG <<")
    print("Installing ASUS ROG Gui and Asusctl packages...")

    try:
        print("Enter sudo password to install ASUS packages")

        with contrib.sudo:
            command('dnf', 'copr', 'enable', 'lukenukem/asus-linux', '-y')
            command('dnf', 'update', '-y')
            command('dnf', 'install', 'asusctl', 'supergfxctl', '-y')
            command('dnf', 'update', '--refresh', '-y')
            command('systemctl', 'enable', 'supergfxd.service')
            command('dnf', 'install', 'asusctl-rog-gui', '-y')
    except Exception as error:
        print(f"ERROR: Can not configure or install ASUS packages: {error}")
        return
    return


# Function to install better fonts
def better_fonts():
    print(">> FONTS CONFIG <<")
    print("Installing better fonts...")

    try:
        print("Enter sudo password to install better-fonts packages")

        with contrib.sudo:
            command('dnf', 'copr', 'enable', 'chriscowleyunix/better_fonts', '-y')
            command('dnf', 'install', 'fontconfig-font-replacements', '-y')
            #command('dnf', 'install', 'fontconfig-enhanced-defaults', '-y')
    except Exception as error:
        print(f"ERROR: Can not configure or install better-fonts packages: {error}")
        return
    return


# Function to install VSCode package
def vscode():
    # VSCODE CONSTANTS
    VSCODE_REPO = "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc"
    
    print(">> VSCODE CONFIG <<")
    print("Installing VSCode...")

    try:
        print("Enter sudo password to install VSCode")

        with contrib.sudo:
            command('rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc')
            #command('echo', '-e', VSCODE_REPO, '> ', '/etc/yum.repos.d/vscode.repo')
            grep(command('echo', '-e', VSCODE_REPO), 'tee', '/etc/yum.repos.d/vscode.repo', '>', '/dev/null')
            command('dnf', 'check-update', '-y')
            command('dnf', 'install', 'code', '-y')
    except Exception as error:
        print(f"ERROR: Can not configure or install VSCode package: {error}")
        return
    return


# Function to install oh-my-zsh
def oh_my_zsh():
    print(">> OH-MY-ZSH  CONFIG <<")
    print("Installing oh-my-zsh...")

    try:
        print("Enter sudo password to install oh-my-zsh")

        with contrib.sudo:
            print("Installing zsh...")
            command('dnf', 'install', 'zsh', '-y')
            print("Installing oh-my-zsh...")
            command('sh', '-c', '"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"')
            print("/root and /home/pedro .zshrc configuration...")
            cp('configs/root.zshrc', '/root/.zshrc')

        cp('configs/piotrek.zshrc', '/home/pedro/.zshrc')
    except Exception as error:
        print(f"ERROR: Can not configure or install oh-my-zsh: {error}")
        return
    return
