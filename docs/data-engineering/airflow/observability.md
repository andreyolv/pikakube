# Airflow Observability

## Kubernetes Infrastructure

MONITORING
https://grafana.com/grafana/dashboards/14448-airflow-monitoring/

GRAFANA Variables:
Tags: SELECT name FROM dag_tag
Dags: SELECT pd.dag_id FROM public.dag pd INNER JOIN dag_tag dt ON dt.dag_id=pd.dag_id WHERE dt.name = ('$Tags')

SELECT dag_id, is_paused, has_import_errors
FROM dag
ORDER BY dag_id
LIMIT 10;

SELECT 
  filename, 
  stacktrace,
  substring(stacktrace from '^\S+') as first_word,
  (regexp_matches(stacktrace, 'DAG ([^ ]+) has'))[1] as extracted_text,
  substring(stacktrace from position('has' in stacktrace) + 4) as text_after_has
FROM import_error
WHERE stacktrace LIKE 'AirflowClusterPolicyError%'
  OR stacktrace LIKE 'AirflowClusterPolicyViolation%';

SELECT 
    ab_user.id AS user_id,
    ab_user.username,
    ab_role.id AS role_id,
    ab_role.name AS role_name
FROM 
    ab_user_role
JOIN 
    ab_role ON ab_user_role.role_id = ab_role.id
JOIN 
    ab_user ON ab_user_role.user_id = ab_user.id;

SELECT 
    tablename AS table_name,
    pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS pretty_size,
    pg_total_relation_size(schemaname || '.' || tablename)
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size DESC;


## DAG's
SMTP teste
https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237?hl=pt-br
https://medium.com/@chibuokejuliet/email-alerting-with-airflow-c0a5a1f413b4

SLA
https://blog.clairvoyantsoft.com/introducing-a-new-way-to-analyze-airflow-sla-misses-2b8ac7958738
https://blog.clairvoyantsoft.com/airflow-service-level-agreement-sla-2f3c91cd84cc
https://github.com/teamclairvoyant/airflow-maintenance-dags/tree/master/sla-miss-report


## Tasks
Notificações


