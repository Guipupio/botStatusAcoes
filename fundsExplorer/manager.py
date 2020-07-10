from browser.browsers import ChromeBrowser
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math

def generate_csv_current_data(path_save_csv: str = None) -> None:
    # Instancia o Browser
    browser = ChromeBrowser()
    # Acessa fundsExplorer
    browser.get_url('https://www.fundsexplorer.com.br/ranking')

    # Obtem dados da tabela
    dict_dataTable = browser.dados_tabela_2_dict(tabela_id="table-ranking")

    # Cria um DataFrame
    df_fiis = pd.DataFrame(dict_dataTable)

    # Exporta para CSV
    df_fiis.to_csv(path_save_csv,index=False)

    # Fecha Browser
    browser.quit()

def analisa_fiis(path_to_csv: str):
    # Obtem data Frame
    df = pd.read_csv(path_to_csv)
    
    # obtem apenas os p/vpa positivos
    df_filtrado = df[df['p/vpa'] > 0]
    
    # Obtem os setores dos FIIS
    list_setores = df_filtrado.setor.unique()
    num_setores = len(list_setores)
    isqrt_num_setores = math.isqrt(num_setores)
    
    num_plots_vertical = num_plots_horizontal = isqrt_num_setores
    
    # Adicionamos mais uma linha nos plots
    if  isqrt_num_setores ** 2 != num_setores:
        num_plots_vertical += 1
    
    plt.style.use('dark_background')
    # Gera subplot das dimensoes necessarias
    fig, subplots = plt.subplots(num_plots_vertical, num_plots_horizontal,  figsize=(30,20), dpi=400)
    
    for idx, setor in enumerate(list_setores):
        
        # Filtra por setor
        _df = df_filtrado[df_filtrado.setor == setor]

        # Remove os FIIs com P/VPA muito grandes
        _df = _df[_df['p/vpa'] < 20]
        
        # obtem dados do Setor
        y = _df['dy (12m)\nmédia'] * 100
        x = _df['p/vpa']

        # Define indices do subplot
        idx_v = int(idx/num_plots_horizontal)
        idx_h = idx % num_plots_horizontal

        # Plota FIIs
        subplots[idx_v][idx_h].scatter(x, y)

        # Adiciona nome dos FIIs
        for codigo, _x, _y in zip(_df['código\ndo fundo'], x, y):
            subplots[idx_v][idx_h].annotate(codigo, (_x,_y), fontsize=5, fontstretch=1000, color=(0.3, 0.3,0.3), rotation=45, ha='left', rotation_mode='anchor')

        # Labels do subplot
        subplots[idx_v][idx_h].set_title(setor)
        subplots[idx_v][idx_h].set_xlabel("P/VPA")
        subplots[idx_v][idx_h].set_ylabel("% DY (12M) Médio")
    
    fig.tight_layout(pad=2.5)
    fig.suptitle('Análise FIIs por Setores', fontsize=16)
    
    fig.savefig(f"Analise-{path_to_csv.split('/')[-1][:-4]}.png")
    
    plt.show()