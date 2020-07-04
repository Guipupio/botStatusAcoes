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
    
    # Gera subplot das dimensoes necessarias
    fig, subplots = plt.subplots(num_plots_vertical, num_plots_horizontal,  figsize=(20,10), dpi=200)
    
    for idx, setor in enumerate(list_setores):
        
        # Filtra por setor
        _df = df_filtrado[df_filtrado.setor == setor]
        
        # obtem dados do Setor
        y = _df['dy (12m)\nmédia']
        x = _df['p/vpa']

        # Define indices do subplot
        idx_v = int(idx/num_plots_horizontal)
        idx_h = idx % num_plots_horizontal

        # Plota FIIs
        subplots[idx_v][idx_h].scatter(x, y)

        # Labels do subplot
        subplots[idx_v][idx_h].set_title(setor)
        subplots[idx_v][idx_h].set_xlabel("P/VPA")
        subplots[idx_v][idx_h].set_ylabel("DY (12M) Médio")
        
    fig.tight_layout(pad=3.0)
    fig.suptitle('Análise FIIs por Setores', fontsize=16)
    
    fig.savefig("Analise.png")
    plt.show()