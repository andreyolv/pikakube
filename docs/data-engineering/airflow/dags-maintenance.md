
https://github.com/teamclairvoyant/airflow-maintenance-dags


find dag_id=airflow_stress_test -type f -mtime +3 -print -delete; find {folder} -type d -empty -print -delete

cd /opt/airflow/logs/dag_processor
find . -maxdepth 1 -type d -mtime +2 -not -path '.' -exec rm -rf {} +

du -h --max-depth=1 | sort -rh

find . -type f | awk -F/ '{print $2}' | sort | uniq -c | sort -nr