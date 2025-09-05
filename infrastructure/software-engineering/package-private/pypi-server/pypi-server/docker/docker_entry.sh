#!/bin/bash
htpasswd -b -c /pypi-server/auth/.htpasswd $PYPI_USER $PYPI_PASS
pypi-server -p 80 -v --log-file /var/log/pypi-server.log -P /pypi-server/auth/.htpasswd -a update,download,list ./packages