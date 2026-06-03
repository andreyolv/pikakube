https://github.com/microsoft/WSL

# How to install WSL
https://learn.microsoft.com/en-us/windows/wsl/install#install-wsl-command
# At PowerShell:
wsl --install

# To discovery which Ubuntu version is installed
lsb_release -a

# Na teoria isso seria lindo, mas na prática não funciona e dá erro, não usar essa merda
sudo vi /etc/wsl.conf
'''
[boot]
command = service docker start
'''

# WSL creates a Virtual Hard Disk (VHD) of size default 1TB at C:\Users\Andrey\AppData\Local\wsl

# If add memory and cpu limits to WSL edit .wslconfig file in your user profile directory C:\Users\<YourUserName>\.wslconfig
https://learn.microsoft.com/en-us/windows/wsl/wsl-config#example-wslconfig-file

# If enterprise VPN block network to wsl
https://github.com/sakai135/wsl-vpnkit

wsl.exe -d wsl-vpnkit --cd /app sed -i -- "s/enabled=false/enabled=true/" /etc/wsl.conf
wsl.exe -d wsl-vpnkit --cd /app wsl-vpnkit

# Disk Increasing
https://stephenreescarter.net/how-to-shrink-a-wsl2-virtual-disk/