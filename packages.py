# Fedora Rebuild - packages.py
#
# Functions to install some packages in Fedora
#
# Author: Pedro Guimarães
# Date: 2025-01-22
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

            print("SUCCESS: ASUS packages successfully installed...")
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

            print("SUCCESS: Better fonts successfully installed...")
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
            command('rpm', '--import', 'https://packages.microsoft.com/keys/microsoft.asc', _fg=True)

            print("Adding VSCode repository...")
            cp('files/vscode.repo', '/etc/yum.repos.d/vscode.repo')
            
            print("Updating DNF packages...")
            command('dnf', 'check-update', '-y', _fg=True)

            print("Installing VSCode...")
            command('dnf', 'install', 'code', '-y', _fg=True)

            print("SUCCESS: VSCode successfully installed...")
    except Exception as error:
        print(f"ERROR: Can not configure or install VSCode package: {error}")
        return
    return


# Function to install oh-my-zsh
def oh_my_zsh():
    # OH-MY-ZSH CONSTANTS
    CURL_COMMAND = '"' + '$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"' + ' "" ' + '--unattended'
    #CURL_COMMAND = '"' + '$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"'

    print(">> OH-MY-ZSH  CONFIG <<")
    print("Installing oh-my-zsh...")

    print(CURL_COMMAND)

    try:
        print("Enter sudo password to install oh-my-zsh")

        with contrib.sudo:
            print("Installing zsh...")
            command('dnf', 'install', 'zsh', '-y', _fg=True) 
        
        print("Installing oh-my-zsh for current user...")
        command('sh', '-c', CURL_COMMAND, _fg=True)

        print("Copying .zshrc to user folder...")
        cp('configs/piotrek.zshrc', '/home/pedro/.zshrc')
   
        with contrib.sudo:
            print("Copying .zshrc to root folder...")
            cp('configs/root.zshrc', '/root/.zshrc')
        
    except Exception as error:
        print(f"ERROR: Can not configure or install oh-my-zsh: {error}")
        return
    return


# Functino to remove items. Used by packages e flatpak function
def remove_items(list, items):
    # Changing indexes to package name
    for idx, pkg in enumerate(items):
        value = int(pkg)
        limit = len(list)

        if value <= 0 or value > limit:
            print(f"ERROR: Package index {pkg} is invalid. Ignoring packages removal...")
            return False
        else:
            items[idx] = list[int(pkg) - 1]
    
    return items


# Function to install packages in system
def install_packages():
    custom_pkgs = []
    items_list = ['extremetuxracer','fastfetch','flatseal','google-chrome-stable','gnome-tweaks','pycharm-community','python3-pip','p7zip','p7zip-plugins', \
                'supertux','supertuxkart','unrar','unzip','vlc','vlc-bittorrent','vlc-extras','wormux',]
    
    print(">> PACKAGES CONFIG <<")
    print("List of default packages to install...")
    for idx in range(len(items_list)):
        print(f"{idx + 1}: {items_list[idx]}")
    
    remove_pkg = input("Do you want to remove any default package? (y/N): ")

    if remove_pkg.lower() == 'y':
        pkgs_to_remove = input("Enter the numbers of the packages to remove separated by comma (or leave empty to exit:): ")

        if pkgs_to_remove != '':
            pkgs_to_remove = pkgs_to_remove.split(',')            
            pkgs_to_remove = remove_items(items_list, pkgs_to_remove)

            if pkgs_to_remove is not False:
                print("List of packages to remove...")
                for pkg in pkgs_to_remove:
                    print(f" - {pkg}")
                
                confirm = input("Are you sure you want to remove these packages? (y/N): ")
                if confirm.lower() == 'y':
                    for pkg in pkgs_to_remove:
                        items_list.remove(pkg)

                    print("Packages removed...")

                    print("List of default packages to install...")
                    for idx in range(len(items_list)):
                        print(f"{idx + 1}: {items_list[idx]}")

    add_pkg = input("Do you want to add any custom package? (y/N): ")

    if add_pkg.lower() == 'y':
        while True:
            pkg_name = input("\nEnter the name of the package or leave empty to exit: ")

            if pkg_name.lower() == '':
                break
            else:
                print("Checking if package exists in repository:")
                search_result = command('dnf', 'search', pkg_name)

                if search_result == "No matches found.\n":
                    print("ERROR: Package not found in repository...")
                else:
                    print("Checking if package is already in the list...")
                    try:
                        if items_list.count(pkg_name):
                            print("Package already in list...")
                        else:
                            custom_pkgs.append(pkg_name)
                            print("Package added to list...")
                    except Exception as error:
                        print(f"ERROR: Can not find package {custom_pkgs} in repository: {error}")
                        continue
        
        if len(custom_pkgs) > 0:
            print("List of custom packages to install...")
        
            for idx in range(len(custom_pkgs)):
                print(f"{idx + 1}: {custom_pkgs[idx]}")

            add_pkgs = input("\nDo you want to add these packages to install? (Y/n): ")

            if add_pkgs.lower() == 'n':
                print("WARNING: Custom packages will not be installed...")
            else:
                items_list.extend(custom_pkgs)
                items_list.sort()
        
    print("Installing packages...")
    with contrib.sudo:
        try:
            command('dnf', 'install', items_list, '-y', _fg=True)
            print("SUCCESS: Packages installed successfully...")
        except Exception as error:
            print(f"ERROR: Can not install packages: {error}")
    
    return


# Function to install flatpaks
def install_flatpaks():
    custom_flatpaks = []
    flatpak_list = ['com.adobe.Reader','com.bitwarden.desktop','com.discordapp.Discord','com.jetbrains.IntelliJ-IDEA-Community', \
                  'com.mattjakeman.ExtensionManager','com.opera.Opera','com.protonvpn.www','com.spotify.Client','de.haeckerfelix.Fragments', \
                  'io.dbeaver.DBeaverCommunity','org.ferdium.Ferdium','org.nickvision.tubeconverter','us.zoom.Zoom']
    
    print(">> FLATPAK CONFIG <<")
    print("List of default packages to install by Application ID:")
    for idx in range(len(flatpak_list)):
        print(f"{idx + 1}: {flatpak_list[idx]}")

    remove_flatpak = input("Do you want to remove any default flatpak package? (y/N): ")

    if remove_flatpak.lower() == 'y':
        flatpaks_to_remove = input("Enter the numbers of the flatpak packages to remove separated by comma (or leave empty to exit:): ")

        if flatpaks_to_remove != '':
            flatpaks_to_remove = flatpaks_to_remove.split(',')            
            flatpaks_to_remove = remove_items(flatpak_list, flatpaks_to_remove)

            if flatpaks_to_remove is not False:
                print("List of packages to remove...")
                for pkg in flatpaks_to_remove:
                    print(f" - {pkg}")
                
                confirm = input("Are you sure you want to remove these flatpak packages? (y/N): ")
                if confirm.lower() == 'y':
                    for pkg in flatpaks_to_remove:
                        flatpak_list.remove(pkg)

                    print("Flatpak packages removed...")

                    print("List of default flatpak packages to install...")
                    for idx in range(len(flatpak_list)):
                        print(f"{idx + 1}: {flatpak_list[idx]}")
    
    add_flatpak = input("Do you want to add any custom flatpak package? (y/N): ")

    if add_flatpak.lower() == 'y':
        while True:
            flatpak_name = input("\nEnter the application ID of the flatpak package or leave empty to exit: ")

            if flatpak_name.lower() == '':
                break
            else:
                print("Checking if package exists in flatpak repository:")
                search_result = command('flatpak', 'search', flatpak_name)

                if search_result == "No matches found.\n" or search_result == "Nenhuma correspondência localizada\n":
                    print("ERROR: Package not found in repository...")
                else:
                    print("Checking if package is already in the list...")
                    try:
                        if flatpak_list.count(flatpak_name):
                            print("Package already in list...")
                        else:
                            custom_flatpaks.append(flatpak_name)
                            print("Package added to list...")
                    except Exception as error:
                        print(f"ERROR: Can not find package {flatpak_name} in repository: {error}")
                        continue
        
        if len(custom_flatpaks) > 0:
            print("List of custom packages to install...")
        
            for idx in range(len(custom_flatpaks)):
                print(f"{idx + 1}: {custom_flatpaks[idx]}")

            add_pkgs = input("\nDo you want to add these flatpak packages to install? (Y/n): ")

            if add_pkgs.lower() == 'n':
                print("WARNING: Custom flatpak packages will not be installed...")
            else:
                flatpak_list.extend(custom_flatpaks)
                flatpak_list.sort()
        
    print("Installing packages...")
    try:
        command('flatpak', 'install', flatpak_list, '-y', _fg=True)
        print("SUCCESS: Flatpak packages installed successfully...")
    except Exception as error:
        print(f"ERROR: Can not install flatpak packages: {error}")
    
    return
