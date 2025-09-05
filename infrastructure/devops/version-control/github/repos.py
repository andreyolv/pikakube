import requests
import os

# Obtém o token de autenticação da variável de ambiente
TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com/user/starred"
PAGE = 1
PER_PAGE = 100  # Número máximo de itens por página permitido pela API do GitHub

# Listas para armazenar os repositórios
repos_list = []

# Limpa as listas antes de começar
while True:
    # Faz a requisição para a API com paginação
    headers = {'Authorization': f'token {TOKEN}'} if TOKEN else {}
    response = requests.get(f"{BASE_URL}?page={PAGE}&per_page={PER_PAGE}", headers=headers)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        print("Erro ao acessar a API:", response.status_code)
        break

    repos = response.json()
    # Se não houver mais repositórios, sai do loop
    if not repos:
        break

    # Processa os dados (URL completa do repositório e número de estrelas)
    for repo in repos:
        full_name = repo['full_name']
        stars_count = repo['stargazers_count']
        repo_url = f"https://github.com/{full_name}"  # Monta a URL completa
        repos_list.append((repo_url, stars_count))  # Adiciona a tupla (URL, estrelas) à lista

    # Incrementa o número da página
    PAGE += 1

# Ordena os repositórios pela URL (alfabeticamente) e pela quantidade de estrelas
repos_list_sorted_alpha = sorted(repos_list, key=lambda x: x[0])
repos_list_sorted_stars = sorted(repos_list, key=lambda x: x[1], reverse=True)

# Escreve o arquivo ordenado alfabeticamente
with open("my-stars-repos-alpha.txt", 'w') as output_file_alpha:
    for repo_url, stars_count in repos_list_sorted_alpha:
        output_file_alpha.write(f"{repo_url}: {stars_count}\n")

# Escreve o arquivo ordenado por quantidade de estrelas
with open("my-stars-repos-stars.txt", 'w') as output_file_stars:
    for repo_url, stars_count in repos_list_sorted_stars:
        output_file_stars.write(f"{repo_url}: {stars_count}\n")

print("Os repositórios foram salvos nos arquivos:")
print("1. Ordenado alfabeticamente: my-stars-repos-alpha.txt")
print("2. Ordenado por quantidade de estrelas: my-stars-repos-stars.txt")
