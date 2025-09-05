https://github.com/Azure/Azurite

python3 -m venv venv
source venv/bin/activate
deactivate

pip install azure-storage-blob
pip install pandas

k port-forward svc/azurite 10000

https://github.com/Azure/Azurite/issues/2373