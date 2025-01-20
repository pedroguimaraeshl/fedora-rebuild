# Fedora Rebuild - config.py
#
# Functions to custom configs in Fedora
#
# Author: Pedro Guimarães
# Date: 2019-06-01
# Version: 0.1


from sh import grep, sed, contrib, mv, command


# Function to configure DNF5 max_parallel_downloads
def dnf5():
    # DNF5 CONSTANTS
    MAX_PARALLEL_DOWNLOADS_FILE = '/etc/dnf/dnf.conf'
    MAX_PARALLEL_DOWNLOADS_MIN = 3
    MAX_PARALLEL_DOWNLOADS_MAX = 21

    print(">> DNF5 CONFIG <<")
    print("Configuring max_parallel_downloads...")
    
    try:
        grep('max_parallel_downloads', MAX_PARALLEL_DOWNLOADS_FILE)
        print("WARNING: max_parallel_downloads is already configured.")
    except:
        while True:
            value = input(f"max_parallel_downloads value: ")

            if MAX_PARALLEL_DOWNLOADS_MIN < int(value) < MAX_PARALLEL_DOWNLOADS_MAX:
                break

        try:
            print("Enter sudo password to configure max_parallel_downloads")

            with contrib.sudo:
                sed('-i', '/main/ a\max_parallel_downloads = ' + value + '    # added by fedora-rebuild at pedroguimaraeshl on github', MAX_PARALLEL_DOWNLOADS_FILE)
                print("SUCCESS: max_parallel_downloads configuration completed")
        except:
            print("ERROR: max_parallel_downloads configuration failed")
            return
        return


# Function to configure GRUB before NVIDIA installation
def grub_before_nvidia(screen_res):
    # GRUB CONSTANTS
    GRUB_FILE = '/etc/default/grub'
    GRUB_CFG = ('GRUB_TIMEOUT=30', \
                'GRUB_DISTRIBUTOR="$(sed ' + "'s, release .*$,,g' /etc/system-release)" + '"', \
                'GRUB_DEFAULT=saved', \
                'GRUB_DISABLE_SUBMENU=true', \
                'GRUB_TERMINAL_OUTPUT="gfxterm"', \
                None, \
                'GRUB_DISABLE_RECOVERY="true"', \
                'GRUB_ENABLE_BLSCFG=true', \
                'GRUB_GFXPAYLOAD="keep"', \
                'GRUBGFXMODE=1920x1080x32,auto')

    print(">> GRUB CONFIG <<\n")
    print("Configuring GRUB before NVIDIA installation...")

    try:
        with open('grub', 'w') as file:
            file.write('# GRUB2 configuration file - generated by fedora-rebuild at pedroguimaraeshl on github\n')

            for idx in range(len(GRUB_CFG)):
                if GRUB_CFG[idx] is not None:
                    file.write(GRUB_CFG[idx] + '\n')
                elif idx == 5:
                    line = grep('GRUB_CMDLINE_LINUX', GRUB_FILE)

                    if line is not None or line != '':
                        file.write(line)
                elif idx == 9:
                    if screen_res == 'fullhd':
                        file.write(GRUB_CFG[idx])
                    elif screen_res == 'hd':
                        file.write('GRUB_GFXMODE=1366x768x32,auto')
                    elif screen_res == 'wxga':
                        file.write('GRUB_GFXMODE=1600x900X32,auto')
                    elif screen_res == '4k':
                        file.write('GRUB_GFXMODE=3840x2160x32,auto')
    except:
        print("ERROR: GRUB configuration failed")
        return

    try:
        print("Enter sudo password to configure grub configuration")

        with contrib.sudo:
            mv('grub', '/etc/default/grub')

            try:
                command('grub2-mkconfig', '-o', '/etc/grub2-efi.cfg', _fg=True)
                print("SUCCESS: GRUB configuration completed")
            except EnvironmentError as error:
                print(f"ERROR: GRUB configuration failed: {error}")
    except EnvironmentError as error:
        print(f"ERROR: GRUB configuration failed: {error}")
        return


# Function to change DNS servers
def change_dns():
    # DNS CONSTANTS
    GOOGLE_IPV4_SERVERS = '8.8.8.8,8.8.4.4'
    GOOGLE_IPV6_SERVERS = '2001:4860:4860::8888,2001:4860:4860::8844'

    print(">> DNS CONFIG <<\n")

    try:
        print("Avaliable connections:")
        command('nmcli', 'device', 'status', _fg=True)

        custom_ipv4_dns = input("\nDo you want to configure custom IPV4 DNS servers? (Enter for Google DNS): ")
        custom_ipv6_dns = input("Do you want to configure custom IPV6 DNS servers? (Enter for Google DNS): ")
        conn_name = input("\nConnection name: ")

        if conn_name == '':
            print("ERROR: Connection name is required")
            return

        print("Configuring DNS servers...")
        print("Enter sudo password to configure DNS servers")

        with contrib.sudo:
            if custom_ipv4_dns == '':
                command('nmcli', 'connection', 'modify', conn_name, 'ipv4.dns', GOOGLE_IPV4_SERVERS)
            else:
                command('nmcli', 'connection', 'modify', conn_name, 'ipv4.dns', custom_ipv4_dns)

            if custom_ipv6_dns == '':
                command('nmcli', 'connection', 'modify', conn_name, 'ipv6.dns', GOOGLE_IPV6_SERVERS)
            else:
                command('nmcli', 'connection', 'modify', conn_name, 'ipv6.dns', custom_ipv6_dns)
                
        print("SUCCESS: DNS configuration completed")
    except EnvironmentError as error:
        print(f"ERROR: DNS configuration failed: {error}")
        return
