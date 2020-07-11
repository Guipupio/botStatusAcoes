import math

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from browser.browsers import ChromeBrowser
from util import SEP_DIR


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


def gera_cor_relativa_vacancia(vacancia: float) -> tuple:
    if not math.isnan(vacancia):
        # Retorna mistura de Verde com Vermelho, variando a intensidade de acordo com a Vacancia 
        return (math.sqrt(vacancia), (1- vacancia) ** 2, 0, (0.5 + abs(vacancia-0.5)) ** 2)
    else:
        # Retorna um Cinza
        return (0.5, 0.5, 0.5, 1)        


def plota_fiis(path_to_csv: str, setor_auto_fit = False):
    # Obtem data Frame
    df = pd.read_csv(path_to_csv, na_values=np.nan)
    
    # obtem apenas os p/vpa positivos
    df_filtrado = df[df['p/vpa'] > 0]
    # Remove items absurdamente valorizados
    df_filtrado = df_filtrado[df_filtrado['p/vpa'] < 20]

    df_filtrado = pd.DataFrame({
            'dy': df_filtrado['dy (12m)\nmédia'] * 100,
            'setor': df_filtrado['setor'],
            'p/vpa': df_filtrado['p/vpa'],
            'ativo': df_filtrado['código\ndo fundo'],
            'vacancia': df_filtrado['vacância\nfísica']
            })
    
    # Obtem os setores dos FIIS
    list_setores = list(filter(lambda x: type(x) is str, df_filtrado.setor.unique()))
    num_setores = len(list_setores)
    isqrt_num_setores = math.isqrt(num_setores)

    num_plots_vertical = num_plots_horizontal = isqrt_num_setores
    
    # Adicionamos mais uma linha nos plots
    if  isqrt_num_setores ** 2 != num_setores:
        num_plots_vertical += 1

    # Obtem maximo DY
    max_dy = df_filtrado.dy.max()
    # Obtem maximo V/VPA
    max_p_vpa = df_filtrado['p/vpa'].max()
    min_p_vpa = df_filtrado['p/vpa'].min()

    kwargs_subplot = {}
    if not setor_auto_fit:
        kwargs_subplot = dict(
            kwargs_subplot,
            **{
                'x_range': (min_p_vpa, max_p_vpa),
                'y_range': (-0.1, max_dy + 0.2),
                }
        )
    
    # Plota imagem no modo Dark
    plt.style.use('dark_background')

    # Gera subplot das dimensoes necessarias
    fig, subplots = plt.subplots(num_plots_vertical, num_plots_horizontal,  figsize=(20,10), dpi=200)
    
    for idx, setor in enumerate(list_setores):
        
        # Filtra por setor
        _df = df_filtrado[df_filtrado.setor == setor]

        # obtem dados do Setor
        y = _df['dy']
        x = _df['p/vpa']
        nome_ativos = _df['ativo']

        # Define indices do subplot
        idx_v = int(idx/num_plots_horizontal)
        idx_h = idx % num_plots_horizontal

        # Plota FIIs
        preenche_subplot(subplots, idx_v, idx_h, x, y, _df, setor, nome_ativos, **kwargs_subplot)
    
    fig.tight_layout(pad=2.5)
    fig.suptitle('Análise FIIs por Setores', fontsize=14)
    
    fig.savefig(f"Analise-{path_to_csv.split(SEP_DIR)[-1][:-4]}.png")


def preenche_subplot(subplots, idx_v: int, idx_h: int, x: iter, y: iter, _df, setor: str, nome_ativos: iter, x_range: tuple = None, y_range: tuple =  None):
    # Plota FIIs
    subplots[idx_v][idx_h].scatter(x, y, c=_df.vacancia.apply(gera_cor_relativa_vacancia), label=nome_ativos)
    # subplots[idx_v][idx_h].legend()
    # Adiciona nome dos FIIs
    for codigo, _x, _y in zip(_df['ativo'], x, y):
        subplots[idx_v][idx_h].annotate(codigo, (_x,_y), fontsize=5, fontstretch=1000, color=(0.9, 0.9, 0.9, 1), rotation=45, ha='left', rotation_mode='anchor')

    # Labels do subplot
    subplots[idx_v][idx_h].set_title(setor)
    subplots[idx_v][idx_h].set_xlabel("P/VPA")
    subplots[idx_v][idx_h].set_ylabel("% DY (12M) Médio")
    subplots[idx_v][idx_h].set_ylim(y_range)
    subplots[idx_v][idx_h].set_xlim(x_range)