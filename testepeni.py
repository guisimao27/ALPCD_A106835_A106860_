import requests
import typer
import json
import csv
from datetime import datetime

app = typer.Typer()

BASE_URL = 'https://api.itjobs.pt'
API_KEY = 'bb25acacbc908a8d2c53a67fb4d1c3d2'  # Substitua pela sua chave de API
HEADERS = {'User-Agent': 'Mozilla'}

def get_data(query_type, method, parameters=[]):
    url_extension = f'/{query_type}/{method}.json?'
    for param in parameters:
        url_extension += f'&{param}'
    url = f'{BASE_URL}{url_extension}&api_key={API_KEY}'

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro {response.status_code} - {response.text}")
        return None

def search_by_skills(skills, data_inicial, data_final):
    # Formatar as datas para o formato da API (YYYY-MM-DD)
    data_inicial_str = datetime.strptime(data_inicial, "%Y-%m-%d").date()
    data_final_str = datetime.strptime(data_final, "%Y-%m-%d").date()
    
    # Construir a lista de parâmetros
    params = [
        f'skills={",".join(skills)}',
        f'date_start={data_inicial_str}',
        f'date_end={data_final_str}'
    ]
    
    data = get_data('job', 'search', params)
    if data and 'results' in data:
        return data['results']
    else:
        print("Não foram encontrados dados ou houve um erro.")
        return []

def export_to_csv(data, filename="jobs_export.csv"):
    # Definir as colunas a serem exportadas
    keys = ["id", "title", "company", "publishedAt", "allowRemote", "locations", "wage"]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        
        for item in data:
            writer.writerow({
                "id": item.get("id"),
                "title": item.get("title"),
                "company": item["company"].get("name") if "company" in item else "",
                "publishedAt": item.get("publishedAt"),
                "allowRemote": item.get("allowRemote"),
                "locations": ', '.join([location["name"] for location in item.get("locations", [])]),
                "wage": item.get("wage")
            })

    print(f"Dados exportados para {filename}")

@app.command()
def skills(skills: str, data_inicial: str, data_final: str, csv: bool = False):
    """
    Comando para buscar trabalhos que requerem uma lista de skills em um período de tempo.
    """
    skills_list = skills.split(",")
    results = search_by_skills(skills_list, data_inicial, data_final)
    
    if results:
        if csv:
            export_to_csv(results, filename="skills_export.csv")
        else:
            print(json.dumps(results, indent=2))
    else:
        print("Nenhum trabalho encontrado para os critérios fornecidos.")

if __name__ == "__main__":
    app()

