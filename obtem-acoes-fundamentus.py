from datetime import datetime
from os.path import exists
from time import sleep

from numpy import resize
from pandas import DataFrame as DF
from pandas import read_csv

from browser.browser import Browser

URL_BASE_FUNDAMENTUS = 'http://fundamentus.com.br/resultado.php?setor={setor}'
TOTAL_SETORES = 42

FUNCAO_LISTA_VALORES = """let listaInfosSelenium = []; \\
    $("{jquery_element}").each(function(){{  \\
        listaInfosSelenium.push(this.{atributo});  \\
    }}); \\
    return listaInfosSelenium"""


def string2float(string: str) -> float:
    try:
        if "%" in string:
            return float(string[0:-1])/100
        else:
            return float(string)
    except ValueError:
        return string

def obtem_info_colunas(browser, tabela_id: str) -> (list, int):
    """
        Objetivo: Obter Headers da tabela 

        OUTPUT:
            tuple (list, int)
            list -> nome das colunas
            int - > Numero de colunas
    """
    jquery_element = '#{tabela_id} > thead > tr:first > th'.format(tabela_id=tabela_id)

    # constroi funcao para obter o nome das headers
    browser.constroiFuncaoNaPagina('get_headers_info_selenium', FUNCAO_LISTA_VALORES.format(jquery_element=jquery_element, atributo='innerText'))
    #  Executa função, para obter a lista
    nome_colunas = [coluna.lower() for coluna in browser.execute_script(""" return get_headers_info_selenium() """)]

    return nome_colunas, len(nome_colunas)


def dados_tabela_2_dict(browser, tabela_id: str, nome_headers: list, num_colunas: int, setor: int) -> dict:
    
    jquery_element = '#{tabela_id} > tbody > tr > td'.format(tabela_id=tabela_id)

    # constroi funcao para obter o texto de cada campo da tabela
    browser.constroiFuncaoNaPagina(nome='get_table_body_info_selenium', corpo_funcao=FUNCAO_LISTA_VALORES.format(jquery_element=jquery_element, atributo='innerText'))
    #  Executa função, para obter a lista
    list_texto_tabela = browser.execute_script(""" return get_table_body_info_selenium() """)

    list_texto_tabela = list(map(lambda coluna: coluna.replace('.', '').replace(',', '.'), list_texto_tabela))
    
    # Temos um vetor 1 x num_colunas*num_linhas -> Redimensionamos para: num_linhas x num_colunas
    if len(list_texto_tabela) == 0:
        return dict({nome_info: [] for nome_info in nome_headers},**{'setor': []})
    elif len(list_texto_tabela) > num_colunas:
        lista_ativos = resize(list_texto_tabela, (-1, num_colunas))
    else:
        lista_ativos = resize(list_texto_tabela, (1, num_colunas))

    dados = {nome_info: list(map(string2float, lista_ativos[:, index])) for index, nome_info in enumerate(nome_headers) }

    dados['setor'] = [setor for _ in range(len(lista_ativos))]

    return dados


def vasculha_setores(browser, tabela_id: str) -> dict:
    conjunto_info = {}

    try:
        for setor in list(range(1,TOTAL_SETORES +1)):

            # Atualiza Browser para o setor correspondente
            browser.get(URL_BASE_FUNDAMENTUS.format(setor=setor))
            
            if not browser.existejQueryNaPagina():
                browser.insereJqueryNaPagina()
                sleep(1.5)

            if not conjunto_info:
                nome_headers, num_colunas = obtem_info_colunas(browser, tabela_id)
                conjunto_info = dict({coluna: [] for coluna in nome_headers}, **{'setor' : []})
            
            infos_parciais = dados_tabela_2_dict(browser, tabela_id, nome_headers, num_colunas, setor)
            
            for info in conjunto_info.keys():
                conjunto_info[info].extend(infos_parciais[info])
            
    except Exception as erro:
        print(erro)

    return conjunto_info

if __name__ == '__main__':
    browser = Browser()
    try:
        dict_infos = vasculha_setores(browser, tabela_id='resultado')
        df_info = DF(dict_infos)
        str_agora = datetime.now().strftime("%d_%m_%Y")
        df_info.to_csv('base_csv/relatorio_' + str_agora + '.csv', sep=';', decimal=',', float_format="%.6f")


    except Exception as erro:
        print(erro)
    
    finally:
        browser.close()
        browser.quit()
