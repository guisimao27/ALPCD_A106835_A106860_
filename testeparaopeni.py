import requests
import json
import re
import sys

# Configurações da API
API_URL = "https://api.itjobs.pt/job/get.json"
API_KEY = "bb25acebcb908a8d2c53a67fb4d1c3d2"  # Substitua pela sua chave da API

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
        # Fazendo a requisição à API
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Levanta exceção se o status não for 200
        job_data = response.json()

        # Verificar o campo 'wage' diretamente
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
