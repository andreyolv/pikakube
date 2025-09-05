https://github.com/pypiserver/pypiserver

tutorials
https://testdriven.io/blog/private-pypi/
https://python.plainenglish.io/private-pypi-server-on-kubernetes-7df169864972


k port-forward svc/pypi-server 8080:80 

-dentro da pasta pypi-server/package:
python3 setup.py sdist
pip install twine
twine upload --repository-url http://127.0.0.1:8080 dist/*

pip install muddy_wave --index-url http://127.0.0.1:8080
pip uninstall muddy_wave

top!

modo mais antigo esse acima
testar build e publish de pacote com poetry e uv

github packages not support python packages
https://github.com/orgs/community/discussions/8542
