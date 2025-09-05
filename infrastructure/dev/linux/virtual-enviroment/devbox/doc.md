https://github.com/jetify-com/devbox

# Devbox uses nix package manager
https://github.com/NixOS/nix

# Where nix packages are located | Nix Package Registry
https://www.nixhub.io/
https://github.com/NixOS/nixpkgs

# Run only fist time to create files structure
devbox init 

# Init shell envirorment
devbox shell

# Exit shell envirorment
exit

# Update packages in your devbox.json
devbox update

# Update devbox version
devbox version update

# Automatically init devbox shell in terminal
echo 'devbox shell --config /home/andrey/projects/pikakube' >> ~/.bashrc
source ~/.bashrc

# Devbox packages are installed at /nix/store
sudo du -sh /nix/store

# How to clear unused packages storage at /nix/store
devbox run -- nix store gc --extra-experimental-features nix-command

# How to migrate manualy installed packages
# How to know which packages was installed manualy
apt-mark showmanual | sort

# How to know specific version
apt list --installed | grep <nome>

# Sucks to comment json list, for this reason I use devbox-comments.yaml to save all packages I could use
https://github.com/jetify-com/devbox/issues/2602

# Is needed to install docker outside devbox to run docker daemon
https://github.com/jetify-com/devbox/issues/2485
https://github.com/NixOS/nixpkgs/issues/47201

# You need to install docker and kubectl outside devbox to run this vscode extensions??? When add extensions is required install dependencies

# After install docker add my user do docker group, So I can run docker without sudo
sudo usermod -aG docker $USER