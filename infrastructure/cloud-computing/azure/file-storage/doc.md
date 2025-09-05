az storage file download-batch \
--account-key <VARIABLE> \
--account-name <VARIABLE> \
--source airflow/dags \
--destination .

az storage file upload-batch \
--account-key <VARIABLE> \
--account-name <VARIABLE> \
--source prog-export-data \
--destination airflow/dags \
--destination-path prog-export-data