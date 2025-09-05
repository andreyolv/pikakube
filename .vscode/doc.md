https://code.visualstudio.com/docs/configure/extensions/extension-marketplace#_workspace-recommended-extensions

# Is not possible to run 'code --install-extension .vscode/extensions.json' and install all extensions at once.
# To install all extensions, run the following command:
jq -r '.recommendations[]' .vscode/extensions.json | xargs -L 1 code --install-extension

# This install extensions in /home/$USER/.vscode-server/extensions