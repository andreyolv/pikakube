kubectl cp . airflow-dag-processor-7677669787-52ch6:/opt/airflow/dags/bp -c dag-processor

du -h --max-depth=1 | sort -rh

ls -la 

find . -type f | awk -F/ '{print $2}' | sort | uniq -c | sort -nr

