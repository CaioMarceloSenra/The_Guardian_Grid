import pandas as pd
from pymongo import MongoClient
import time
import os

# 1. Configurações da Exportação
ARQUIVO_SAIDA = "dados_guardian.csv"
INTERVALO_ATUALIZACAO = 5 # Segundos entre cada salvamento

try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["guardian_grid"]
    collection = db["leituras_sensor"]
    print(" Conectado ao MongoDB para exportação.")
except Exception as e:
    print(f" Erro de conexão: {e}")
    exit()

print(f" INICIANDO EXPORTAÇÃO CONTÍNUA PARA: {ARQUIVO_SAIDA}")
print("Mantenha essa janela aberta para alimentar o Power BI.")
print("Pressione CTRL+C para parar.")

while True:
    try:
        # 2. Busca todos os dados do MongoDB
        # O parâmetro {'_id': 0} diz pro Mongo não trazer o ID criptografado
        cursor = collection.find({}, {'_id': 0})
        dados = list(cursor)

        if dados:
            # 3. Transforma em Tabela
            df = pd.DataFrame(dados)

            # Converte a coluna de timestamp para datetime 
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # 4. Salva o CSV (Sobrescreve o anterior)
            # index=False é vital para não criar uma coluna de números desnecessária
            df.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig') 
            
            print(f" Atualizado! {len(df)} registros salvos em {ARQUIVO_SAIDA}")
        else:
            print(" Banco vazio. Aguardando dados...")

    except PermissionError:
        print(" ERRO: O arquivo CSV está aberto no Excel/Power BI? Feche-o para permitir a gravação!")
    except Exception as e:
        print(f" Erro inesperado: {e}")

    # Respira um pouco para não fritar o HD
    time.sleep(INTERVALO_ATUALIZACAO)
