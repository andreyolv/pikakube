#!/bin/bash

set -e



ln -sf $(pwd)/../.vscode/p-doc.md docs/devops/vscode-extensions.md
ln -sf $(pwd)/../infrastructure/dev/linux/virtual-enviroment/devbox/p-doc.md docs/devops/devbox.md

ln -sf $(pwd)/../infrastructure/network/troubleshooting/netshoot/p-doc.md docs/network/netshoot.md

ln -sf $(pwd)/../infrastructure/security/kubernetes-core/audit-logs/p-doc.md docs/security/kubernetes-audit-logs.md

