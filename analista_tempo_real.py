import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
from pymongo import MongoClient

# 1. Configuração Global (Conecta só uma vez)
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['guardian_grid']
    colecao = db['leituras_sensor']
    print("Conectado ao MongoDB.")
except Exception as e:
    print(f"Erro: {e}")
    exit()

# Prepara a janela do gráfico
plt.style.use('seaborn-v0_8-darkgrid') # Estilo visual
fig = plt.figure(figsize=(16, 7))

# 2. Função de Atualização do Gráfico
def atualizar_grafico(i):
    # Limpa a tela anterior para não poluir visualmente
    plt.clf()
    
    # Busca os dados mais recentes do MongoDB
    # Pega os últimos 100 registros para análise
    dados_mongo = list(colecao.find({}, {'_id': 0, 'voltagem': 1, 'timestamp': 1}).sort('_id', -1).limit(100))
    
    if not dados_mongo:
        return

    df = pd.DataFrame(dados_mongo)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # Cria uma coluna de voltagem anterior para o gráfico de espaço de fase
    df['voltagem_anterior'] = df['voltagem'].shift(1)

    # --- GRÁFICO 1: Linha do Tempo (Esquerda) ---
    ax1 = plt.subplot(1, 2, 1)
    
    # Linha principal
    plt.plot(df['timestamp'], df['voltagem'], color='#00ff88', linewidth=2, label='Tensão da Rede')
    
    # Detecta apagões para destacar em vermelho
    apagoes = df[df['voltagem'] == 0]
    if not apagoes.empty:
        plt.scatter(apagoes['timestamp'], apagoes['voltagem'], color='#ff0055', s=100, zorder=5, label='RUPTURA DETECTADA')

    plt.title('Monitoramento em Tempo Real: Voltagem', fontsize=14, fontweight='bold')
    plt.ylabel('Voltagem (V)')
    plt.xlabel('Tempo (Recente)')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Rotaciona as datas para não encavalar
    plt.xticks(rotation=45)

    # --- GRÁFICO 2: Espaço de Fase (Direita) ---
    ax2 = plt.subplot(1, 2, 2)
    
    # Aqui usamos scatterplot. Se o sistema estiver saudável, os pontos ficam aglomerados nas pontas.
    # Se houver apagão, eles caem para o (0,0).
    sns.scatterplot(
        x=df['voltagem_anterior'], 
        y=df['voltagem'], 
        hue=df['voltagem'], 
        palette='viridis', 
        s=80, 
        edgecolor='black',
        legend=False,
        ax=ax2
    )

    plt.title('Topologia da Catástrofe (Atratores)', fontsize=14, fontweight='bold')
    plt.xlabel('Voltagem (t-1)')
    plt.ylabel('Voltagem (t)')
    
    # Linha de perigo
    plt.axvline(x=50, color='red', linestyle='--', alpha=0.3)
    plt.text(10, 200, 'ESTABILIDADE', color='green', fontsize=10)
    plt.text(5, 10, 'COLAPSO', color='red', fontsize=10, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()

# 3. Rodando a Animação
print(" Iniciando Monitoramento em Tempo Real...")
# Intervalo de 1000ms (1 segundo) entre atualizações
ani = FuncAnimation(fig, atualizar_grafico, interval=1000)

plt.show()
