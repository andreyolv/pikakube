https://github.com/nektos/act
https://github.com/cplee/github-actions-demo/tree/master

curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
sudo mv ./bin/act /usr/local/bin/

act
act -W '.github/workflows/main.yml'
