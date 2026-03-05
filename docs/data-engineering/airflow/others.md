##	Lineage

##	Custom Python Package

https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/modules_management.html

The list of directories from which Python tries to load the module is given by the variable sys.path
então teoricamente se tu subir a customlib em /opt/airflow/dags/customlib como se fosse uma dag que o github actions faz

import sys
from pprint import pprint
print(sys.path)

## Custo Airflow Operator
https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html


## Memcached


