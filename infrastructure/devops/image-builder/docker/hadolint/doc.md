https://github.com/hadolint/hadolint
https://github.com/hadolint/hadolint-action

# Install cli
get last version -> https://github.com/hadolint/hadolint/releases
VERSION=v2.12.0
wget -O hadolint https://github.com/hadolint/hadolint/releases/download/${VERSION}/hadolint-Linux-x86_64
sudo mv hadolint /usr/local/bin/hadolint
sudo chmod +x /usr/local/bin/hadolint

hadolint --config .hadolint.yaml Dockerfile