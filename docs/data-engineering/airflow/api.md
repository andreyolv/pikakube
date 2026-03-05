airflow roles create api_test

airflow roles add-perms api_test -a can_edit -r DAG:dummy_fail 
airflow roles add-perms api_test -a can_read -r DAGs

airflow users create \
    --username api_test \
    --password api_test_password \
    --firstname API \
    --lastname Test \
    --role api_test \
    --email api_test@test.com


airflow users delete -u api_test

airflow roles delete api_test
