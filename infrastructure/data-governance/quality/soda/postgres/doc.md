https://github.com/sodadata/soda-core/blob/main/examples/postgres_example.md
https://github.com/sodadata/datatalks-workshop/tree/main/checks
https://www.youtube.com/watch?v=CSqHZ1eJ5is

pip install soda-core
pip install soda-core-postgres

soda test-connection -c configuration.yml -d my_postgres

soda scan -c configuration.yml -d my_postgres checks.yml -V
