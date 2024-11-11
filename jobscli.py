#a)
import requests
import json
import csv
import sys

# Configurações da API
API_URL = "https://api.itjobs.pt/job/list.json"  # URL da API
API_KEY = "bb25acebcb908a8d2c53a67fb4d1c3d2"  # Chave da API fornecida

def top(n: int, csv_output: bool = False):
    """
    Lista os N trabalhos mais recentes em formato JSON ou exporta para CSV.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }
    params = {
        "api_key": API_KEY,
        "limit": n
    }
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Levanta uma exceção se o status não for 200
        data = response.json()  # Tenta decodificar o JSON da resposta
        
        # Formata os trabalhos em JSON
        if "results" in data:
            jobs = []
            for job in data["results"]:
                job_info = {
                    "Título": job['title'],
                    "Empresa": job['company']['name'],
                    "Descrição": job.get('body', ''),  # Descrição pode estar no campo 'body'
                    "Data de Publicação": job['publishedAt'],
                    "Salário": job.get('wage', 'Não especificado'),
                    "Localização": ", ".join([location['name'] for location in job['locations']])
                }
                jobs.append(job_info)
            
            # Exibe o JSON formatado ou exporta para CSV
            if csv_output:
                export_to_csv(jobs, 'top_jobs.csv')
            else:
                print(json.dumps(jobs, indent=4, ensure_ascii=False))
        else:
            print("Nenhum trabalho encontrado.")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON.")
        print(response.text)  # Exibe o conteúdo bruto para depuração

def export_to_csv(jobs, filename):
    """
    Exporta a lista de trabalhos para um arquivo CSV com os campos desejados.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Título", "Empresa", "Descrição", "Data de Publicação", "Salário", "Localização"])
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    print(f"Dados exportados para {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            # Obtém o valor de N passado como argumento na linha de comando
            n = int(sys.argv[1])
            # Verifica se o argumento "--csv-output" foi passado
            csv_output = "--csv-output" in sys.argv
            top(n, csv_output=csv_output)
        except ValueError:
            print("Por favor, insira um número válido.")
    else:
        print("Uso: python jobscli.py <número> [--csv-output]")






#b)


import requests
import json
import csv
import sys

# Configurações da API
API_URL = "https://api.itjobs.pt/job/list.json"
API_KEY = "bb25acebcb908a8d2c53a67fb4d1c3d2"  # Insira sua chave da API

def search_jobs(localidade: str, empresa: str, numero_de_trabalhos: int, csv_output: bool = False):
    """
    Lista os trabalhos full-time de uma determinada empresa em uma localidade específica.
    
    Parâmetros:
    - localidade (str): Nome da localidade (ex: "Lisboa", "Porto").
    - empresa (str): Nome da empresa (ex: "Integer Consulting", "Growin - Know to grow").
    - numero_de_trabalhos (int): Número de trabalhos a exibir.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }
    params = {
        "api_key": API_KEY,
        "limit": numero_de_trabalhos
    }

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Verifica se o status é 200
        data = response.json()  # Decodifica o JSON da resposta
        
        # Filtra os resultados para a localidade e empresa especificadas
        trabalhos_filtrados = []
        for trabalho in data.get("results", []):
            if any(loc["name"] == localidade for loc in trabalho["locations"]) and trabalho["company"]["name"].lower() == empresa.lower():
                trabalho_info = {
                    "Título": trabalho['title'],
                    "Empresa": trabalho['company']['name'],
                    "Descrição": trabalho.get('body', ''),
                    "Data de Publicação": trabalho['publishedAt'],
                    "Salário": trabalho.get('wage', 'Não especificado'),
                    "Localização": ", ".join([loc['name'] for loc in trabalho['locations']])
                }
                trabalhos_filtrados.append(trabalho_info)
        
        # Exibe os resultados em formato JSON ou exporta para CSV
        if trabalhos_filtrados:
            if csv_output:
                export_to_csv(trabalhos_filtrados, 'search_jobs.csv')
            else:
                print(json.dumps(trabalhos_filtrados, indent=4, ensure_ascii=False))
        else:
            print("Nenhum trabalho encontrado para os critérios especificados.")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON.")
        print(response.text)  # Exibe o conteúdo bruto para depuração

def export_to_csv(jobs, filename):
    """
    Exporta a lista de trabalhos para um arquivo CSV com os campos desejados.
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Título", "Empresa", "Descrição", "Data de Publicação", "Salário", "Localização"])
        writer.writeheader()
        for job in jobs:
            writer.writerow(job)
    print(f"Dados exportados para {filename}")

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        localidade = sys.argv[1]
        empresa = sys.argv[2]
        try:
            numero_de_trabalhos = int(sys.argv[3])
            # Verifica se o argumento "--csv-output" foi passado
            csv_output = "--csv-output" in sys.argv
            search_jobs(localidade, empresa, numero_de_trabalhos, csv_output=csv_output)
        except ValueError:
            print("Por favor, insira um número válido para o número de trabalhos.")
    else:
        print("Uso: python jobscli.py <localidade> <empresa> <numero_de_trabalhos> [--csv-output]")







#d)

import requests
import typer
import json
import csv
from datetime import datetime

# Inicializa o aplicativo Typer
app = typer.Typer()

# Chave da API e URL base
API_KEY = "1b37922841c011a91e1b71c117f2b949"
BASE_URL = "https://api.itjobs.pt/job/list.json"  # Usando o endpoint List

# Função para buscar trabalhos com base nas skills e intervalo de datas
def buscar_trabalhos_por_skills(lista_skills, data_inicio, data_fim):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }
    params = {
        "api_key": API_KEY,
        "q": ",".join(lista_skills),
        "date_posted_min": data_inicio,
        "date_posted_max": data_fim,
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        typer.echo(f"Erro ao buscar dados: {response.status_code}")
        return []

# Função para exportar dados para CSV
def exportar_para_csv(trabalhos, nome_arquivo):
    with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(["Título", "Empresa", "Descrição", "Data de Publicação", "Salário", "Localização"])
        
        for trabalho in trabalhos:
            writer.writerow([
                trabalho.get("title", ""),
                trabalho.get("company", {}).get("name", ""),
                trabalho.get("body", ""),
                trabalho.get("publishedAt", ""),
                trabalho.get("wage", "Não especificado"),
                ", ".join([loc.get("name", "") for loc in trabalho.get("locations", [])])
            ])

# Comando da CLI para buscar trabalhos com as skills e datas especificadas
@app.command()
def skills(
    lista_skills: str = typer.Argument(..., help="Lista de skills separadas por vírgula (ex: Python,SQL,Java)"),
    data_inicio: str = typer.Argument(..., help="Data de início no formato YYYY-MM-DD"),
    data_fim: str = typer.Argument(..., help="Data de fim no formato YYYY-MM-DD"),
    exportar_csv: bool = typer.Option(False, "--export-csv", help="Exportar resultados para CSV"),
):
    # Divide as skills em uma lista
    skills = lista_skills.split(",")
    resultados = buscar_trabalhos_por_skills(skills, data_inicio, data_fim)

    # Exibe os resultados em JSON
    typer.echo(json.dumps(resultados, indent=4, ensure_ascii=False))

    # Exporta para CSV, se solicitado
    if exportar_csv:
        nome_arquivo = "trabalhos_skills.csv"
        exportar_para_csv(resultados, nome_arquivo)
        typer.echo(f"Resultados exportados para {nome_arquivo}")

if __name__ == "__main__":
    app()
