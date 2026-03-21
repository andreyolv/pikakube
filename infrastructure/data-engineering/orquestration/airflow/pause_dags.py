import requests
from datetime import datetime, timedelta, timezone

# --- CONFIGURAÇÕES ---
AIRFLOW_URL = "http://seu-airflow.com/api/v1"
AUTH = ("seu_usuario", "sua_senha")
LIMITE_DIAS = 5
DRY_RUN = True  # Mude para False para realmente pausar as DAGs

def get_running_dag_runs():
    endpoint = f"{AIRFLOW_URL}/dagRuns"
    # Filtramos por execuções que ainda estão no estado 'running'
    params = {"state": ["running"], "limit": 100}
    
    response = requests.get(endpoint, auth=AUTH, params=params)
    response.raise_for_status()
    return response.json().get("dag_runs", [])

def pause_dag(dag_id):
    if DRY_RUN:
        print(f"[DRY-RUN] Pausando DAG: {dag_id}")
        return
    
    endpoint = f"{AIRFLOW_URL}/dags/{dag_id}"
    payload = {"is_paused": True}
    response = requests.patch(endpoint, auth=AUTH, json=payload)
    
    if response.status_code == 200:
        print(f"SUCESSO: DAG {dag_id} pausada com sucesso.")
    else:
        print(f"ERRO ao pausar {dag_id}: {response.text}")

def main():
    dag_runs = get_running_dag_runs()
    agora = datetime.now(timezone.utc)
    cutoff_date = agora - timedelta(days=LIMITE_DIAS)

    print(f"Verificando execuções iniciadas antes de: {cutoff_date}")

    dags_para_pausar = set()

    for run in dag_runs:
        # Exemplo de data da API: '2023-10-27T10:00:00+00:00'
        start_date_str = run['start_date'].replace('Z', '+00:00')
        start_date = datetime.fromisoformat(start_date_str)

        if start_date < cutoff_date:
            print(f"Detectada: {run['dag_id']} rodando desde {start_date}")
            dags_para_pausar.add(run['dag_id'])

    if not dags_para_pausar:
        print("Nenhuma DAG excedeu o limite de tempo.")
        return

    for dag_id in dags_para_pausar:
        pause_dag(dag_id)

if __name__ == "__main__":
    main()
