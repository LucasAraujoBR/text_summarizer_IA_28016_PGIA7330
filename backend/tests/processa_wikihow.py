import csv
import requests
import time
import os

# Configurações
CSV_ENTRADA = 'data/wikihowAll.csv'
CSV_SAIDA = 'data/wikihow_results.csv'
URL_API = 'http://localhost:8000/api/v1/analise'

# Parâmetros padrão para o resumo
OPCOES = {
    "max_length": 500,
    "language": "pt-BR",
    "nivel_ensino": "medio"
}

# Limite de textos a processar (ajuste para None para processar todos)
LIMITE = None  # Exemplo: processar só 100 para teste

def carregar_processados():
    """Carrega os títulos já processados do CSV de saída"""
    processados = set()
    if os.path.exists(CSV_SAIDA):
        with open(CSV_SAIDA, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                status = row.get('status', '').strip()
                # Só considera processado se status for "ok"
                if status == 'ok':
                    processados.add(row.get('title', '').strip())
    return processados

def main():
    # Carrega títulos já processados
    processados = carregar_processados()
    print(f"Encontrados {len(processados)} textos já processados")
    
    with open(CSV_ENTRADA, newline='', encoding='utf-8') as csvfile_in, \
         open(CSV_SAIDA, 'a', newline='', encoding='utf-8') as csvfile_out:
        reader = csv.DictReader(csvfile_in)
        
        # Verifica se o arquivo de saída está vazio para escrever o cabeçalho
        if os.path.getsize(CSV_SAIDA) == 0:
            fieldnames = [
                'headline', 'title', 'text',
                'resumo', 'classificacao', 'metadata',
                'max_length', 'language', 'nivel_ensino', 'status', 'erro'
            ]
            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
            writer.writeheader()
        else:
            fieldnames = [
                'headline', 'title', 'text',
                'resumo', 'classificacao', 'metadata',
                'max_length', 'language', 'nivel_ensino', 'status', 'erro'
            ]
            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)

        contador = 0
        for i, row in enumerate(reader):
            if LIMITE and contador >= LIMITE:
                break
                
            title = row.get('title', '').strip()
            headline = row.get('headline', '').strip()
            text = row.get('text', '').strip()
            
            # Pula se não tem texto ou se já foi processado
            if not text or title in processados:
                continue
                
            payload = {
                "texto": text,
                "opcoes": OPCOES
            }
            try:
                inicio = time.time()
                resp = requests.post(URL_API, json=payload, timeout=300)
                tempo = time.time() - inicio
                if resp.status_code == 201:
                    data = resp.json()
                    writer.writerow({
                        'headline': headline,
                        'title': title,
                        'text': text,
                        'resumo': data.get('resumo', ''),
                        'classificacao': data.get('classificacao', ''),
                        'metadata': data.get('metadata', {}),
                        'max_length': OPCOES['max_length'],
                        'language': OPCOES['language'],
                        'nivel_ensino': OPCOES['nivel_ensino'],
                        'status': 'ok',
                        'erro': ''
                    })
                else:
                    writer.writerow({
                        'headline': headline,
                        'title': title,
                        'text': text,
                        'resumo': '',
                        'classificacao': '',
                        'metadata': '',
                        'max_length': OPCOES['max_length'],
                        'language': OPCOES['language'],
                        'nivel_ensino': OPCOES['nivel_ensino'],
                        'status': 'erro',
                        'erro': f"HTTP {resp.status_code}: {resp.text}"
                    })
                contador += 1
                print(f"Processado {contador}: {title}")
            except Exception as e:
                writer.writerow({
                    'headline': headline,
                    'title': title,
                    'text': text,
                    'resumo': '',
                    'classificacao': '',
                    'metadata': '',
                    'max_length': OPCOES['max_length'],
                    'language': OPCOES['language'],
                    'nivel_ensino': OPCOES['nivel_ensino'],
                    'status': 'erro',
                    'erro': str(e)
                })
                contador += 1
                print(f"Erro no {contador}: {title} - {str(e)}")

if __name__ == '__main__':
    main() 