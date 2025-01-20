# Fedora Rebuild - packages.py
#
# Functions to install some packages in Fedora
#
# Author: Pedro Guimarães
# Date: 2019-06-01
# Version: 0.1


from sh import contrib, command, cp

# Function to install ASUS ROG Gui and Asusctl packages
def asus():
    print(">> ASUS CONFIG <<")
    print("Installing ASUS ROG Gui and Asusctl packages...")

    try:
        print("Enter sudo password to install ASUS packages")

        with contrib.sudo:
            print("Enabling ASUS repository...")
            command('dnf', 'copr', 'enable', 'lukenukem/asus-linux', '-y', _fg=True)

            print("Updating DNF packages...")
            command('dnf', 'update', '-y', _fg=True)

            print("Installing ASUS packages...")
            command('dnf', 'install', 'asusctl', 'supergfxctl', '-y', _fg=True)

            print("Refreshing DNF packages...")
            command('dnf', 'update', '--refresh', '-y', _fg=True)

            print("Enabling supergfxd service...")
            command('systemctl', 'enable', 'supergfxd.service', _fg=True)

            print("Installing ASUS ROG Gui...")
            command('dnf', 'install', 'asusctl-rog-gui', '-y', _fg=True)
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
            print("Enabling better-fonts repository...")
            command('dnf', 'copr', 'enable', 'chriscowleyunix/better_fonts', '-y', _fg=True)

            print("Installing better-fonts packages...")
            command('dnf', 'install', 'fontconfig-font-replacements', '-y', _fg=True)

            #print("Installing fontconfig-enhanced-defaults...")
            #command('dnf', 'install', 'fontconfig-enhanced-defaults', '-y', _fg=True)
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
            print("Importing Microsoft GPG key...")
            command('rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc')

            print("Adding VSCode repository...")
            cp('configs/vscode.repo', '/etc/yum.repos.d/vscode.repo')
            
            print("Updating DNF packages...")
            command('dnf', 'check-update', '-y')

            print("Installing VSCode...")
            command('dnf', 'install', 'code', '-y')
    except Exception as error:
        print(f"ERROR: Can not configure or install VSCode package: {error}")
        return
    return


'''
# Function to install oh-my-zsh
def oh_my_zsh():
    # OH-MY-ZSH CONSTANTS
    CURL_COMMAND = '"' + '$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'

    print(">> OH-MY-ZSH  CONFIG <<")
    print("Installing oh-my-zsh...")

    try:
        print("Enter sudo password to install oh-my-zsh")

        with contrib.sudo:
            print("Installing zsh...")
            command('dnf', 'install', 'zsh', '-y')

        print("Installing oh-my-zsh for current user...")
        command('sh', '-c', '"$(' + curl('https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh', '-fsSL') + ')"')

        print("Copying .zshrc to user folder...")
        cp('configs/piotrek.zshrc', '/home/pedro/.zshrc')

        with contrib.sudo:
            print("Copying .zshrc to root folder...")
            cp('configs/root.zshrc', '/root/.zshrc')
        
        
    except Exception as error:
        print(f"ERROR: Can not configure or install oh-my-zsh: {error}")
        return
    return
'''
