# To generate ssh secret

# identity
cd ~/.ssh
mkdir key1
ssh-keygen -f key1/id_rsa
## Add public key (cat /home/andreyolv/.ssh/id_rsa.pub) into your repository in https://github.com/andreyolv/big-data-platform-on-k8s/settings/keys
## Add private key (cat /home/andreyolv/.ssh/id_rsa | base64) in identity key 

# known_hosts
## Second key converted to base64 -> https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints
## Or cat /home/andreyolv/.ssh/known_hosts -> github.com ecdsa-sha2-nistp256 AAAA..