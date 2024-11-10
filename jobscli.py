

import requests
import json
import sys

# Configurações da API
API_URL = "https://api.itjobs.pt/job/list.json"  # URL da API
API_KEY = "bb25acebcb908a8d2c53a67fb4d1c3d2"  # Chave da API fornecida

def top(n: int):
    """
    Lista os N trabalhos mais recentes em formato JSON.
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
                    "Localização": [location['name'] for location in job['locations']],
                    "Publicado em": job['publishedAt']
                }
                jobs.append(job_info)
            
            # Exibe o JSON formatado
            print(json.dumps(jobs, indent=4, ensure_ascii=False))
        else:
            print("Nenhum trabalho encontrado.")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON.")
        print(response.text)  # Exibe o conteúdo bruto para depuração

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            # Obtém o valor de N passado como argumento na linha de comando
            n = int(sys.argv[1])
            top(n)
        except ValueError:
            print("Por favor, insira um número válido.")
    else:
        print("Uso: python jobscli.py <número>")


#python jobscli.py 5  -- usar isto no terminal 

#b)

import requests
import json
import sys

# Configurações da API
API_URL = "https://api.itjobs.pt/job/list.json"
API_KEY = "bb25acebcb908a8d2c53a67fb4d1c3d2"  # Insira sua chave da API

def search_jobs(localidade: str, empresa: str, numero_de_trabalhos: int):
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
                trabalhos_filtrados.append({
                    "Título": trabalho['title'],
                    "Empresa": trabalho['company']['name'],
                    "Localidade": [loc['name'] for loc in trabalho['locations']],
                    "Publicado em": trabalho['publishedAt'],
                    "Link": f"https://www.itjobs.pt/oferta/{trabalho['slug']}"
                })
        
        # Exibe os resultados em formato JSON
        if trabalhos_filtrados:
            print(json.dumps(trabalhos_filtrados, indent=4, ensure_ascii=False))
        else:
            print("Nenhum trabalho encontrado para os critérios especificados.")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON.")
        print(response.text)  # Exibe o conteúdo bruto para depuração

if __name__ == "__main__":
    if len(sys.argv) == 4:
        localidade = sys.argv[1]
        empresa = sys.argv[2]
        try:
            numero_de_trabalhos = int(sys.argv[3])
            search_jobs(localidade, empresa, numero_de_trabalhos)
        except ValueError:
            print("Por favor, insira um número válido para o número de trabalhos.")
    else:
        print("Uso: python jobscli.py <localidade> <empresa> <numero_de_trabalhos>")


#USAR NO TERMINAL ( python jobscli.py "Lisboa" "Integer Consulting" 3)



#C)



import requests
import json
import re
import sys

# Configurações da API
API_URL = "https://api.itjobs.pt/job/get.json"
API_KEY = "bb25acebcb908a8d2c53a67fb4d1c3d2"

def extract_salary(job_id: int):
    """
    Extrai a informação de salário para um determinado job ID em formato JSON.
    Se o campo 'wage' for nulo, procura no campo 'body' com expressões regulares.
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }
    params = {
        "api_key": API_KEY,
        "id": job_id
    }
    
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Levanta exceção se o status não for 200
        job_data = response.json()
        
        # Verificar o campo wage diretamente
        wage = job_data.get("wage")
        if wage:
            salary_info = {"Salário": wage}
            print(json.dumps(salary_info, ensure_ascii=False, indent=4))
            return

        # Se o campo wage for nulo, buscar no campo 'body'
        body_text = job_data.get("body", "")
        
        # Procurar padrões de salário usando expressões regulares
        salary_patterns = [
            r"(\d{1,3}(?:[.,]?\d{3})+)\s*(EUR|€)",  # Ex: 40.000 EUR, 40.000€
            r"\b(?:sal[aá]rio|remunera[cç][aã]o)\s*[:\-]?\s*(\d{1,3}(?:[.,]?\d{3})*)",  # Salário: 40000
            r"\b(?:oferecemos)\s*(\d{1,3}(?:[.,]?\d{3})*)",  # Oferecemos 40000
        ]
        
        for pattern in salary_patterns:
            match = re.search(pattern, body_text, re.IGNORECASE)
            if match:
                salary = match.group(1).replace('.', '').replace(',', '.')
                salary_info = {"Salário (extraído do corpo da descrição)": salary}
                print(json.dumps(salary_info, ensure_ascii=False, indent=4))
                return

        print(json.dumps({"Salário": "Informação não encontrada"}, ensure_ascii=False, indent=4))

    except requests.exceptions.RequestException as e:
        print(json.dumps({"Erro": f"Erro ao acessar a API: {e}"}, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "salary":
        try:
            job_id = int(sys.argv[2])
            extract_salary(job_id)
        except ValueError:
            print(json.dumps({"Erro": "Por favor, insira um job id válido."}, ensure_ascii=False, indent=4))
    else:
        print("Uso: python jobscli.py salary <JOBID>")


#usar no terminal python jobscli.py salary 492169



