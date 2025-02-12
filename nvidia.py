# Fedora Rebuild - nvidia.py
#
# Functions to install nVdia drivers in Fedora
#
# Author: Pedro Guimarães
# Date: 2025-02-05
# Version: 0.1


from sh import grep, sed, contrib, mv, command, reboot
from os import system


def nvidia(version,secboot):
    # NVIDIA CONSTANTS
    RPM_FREE = "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm"
    RPM_NONFREE = "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"
    SB_PKGS = "akmods kmodtool openssl mokutil"
    NVIDIA_PKGS = "akmod-nvidia gcc kernel-devel kernel-headers xorg-x11-drv-nvidia xorg-x11-drv-nvidia-cuda xorg-x11-drv-nvidia-libs xorg-x11-drv-nvidia-libs.i686"

    print(">> NVIDIA INSTALL <<")

    try:
        print("Checking for system updates...")

        with contrib.sudo:
            msg = command('dnf', 'upgrade', '--refresh', '-y')
            
            if msg.strip() == "Nada para fazer." or msg.strip() == "Nothing to do.":
                while True:
                    skip_sb = input("Did you have installed secure boot required packages for nVidia [y/n]? ")

                    if skip_sb.lower() == "n" or skip_sb.lower() == "no":
                        try:
                            print("Enabling RPM FUSION repositories...")
                            command('dnf', 'install', '-y', RPM_FREE)
                            command('dnf', 'install', '-y', RPM_NONFREE)

                            print("Enabling openh264 library...")
                            command('dnf', 'config-manager', 'setopt', 'fedora-cisco-openh264.enabled=1', _fg=True)

                            print("Installing secure boot required packages for nVidia...")
                            command('dnf', 'install', SB_PKGS ,'-y', _fg=True)

                            print("Generating secure boot key...")
                            command('kmodgenca', '-a')

                            print("Importing generated key...")
                            command('mokutil', '--import', '/etc/pki/akmods/certs/public_key.der')

                            print("WARNING: You must reboot to complete your system update. After rebooting, go to next step of nvidia install")
                            reboot = input("Reboot system now [Y/n]? ")

                            if reboot.lower() == "n" or reboot.lower() == "no":
                                print("WARNING: After reboot, proceed to the next nvidia install step")
                                return
                            else:
                                command('reboot')                                
                        except Exception as error:
                            print(f"ERROR: Can not install secure boot required packages for nVidia: {error}")
                            return
                    elif skip_sb.lower() == "y" or skip_sb.lower() == "yes":
                        try:
                            with contrib.sudo:
                                print("Installing nVidia packages...")
                                command('dnf', 'install', NVIDIA_PKGS ,'-y', _fg=True)
                        except Exception as error:
                            print(f"ERROR: Can not install nVidia packages: {error}")
                            return
                        return
                    else:
                        print("WARNING: Invalid choice...")
            else:
                print("WARNING: You must reboot to complete your system update. After rebooting, repeat nvidia install")
                reboot = input("Reboot system now [Y/n]? ")

                if reboot.lower() == "n" or reboot.lower() == "no":
                    print("WARNING: Can not proceed before system reboot! Aborting nVidia install")
                else:
                    command('reboot')
    except Exception as error:
        print(f"ERROR: Can not install nVidia: {error}")
        return

retorno = system('ps -A | grep farinha')
print("O retorno foi: ")
print(retorno)
#nvidia(None,None)