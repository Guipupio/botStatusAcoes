from os.path import exists
from time import sleep

from browser.browser import Browser

URL_BASE_FUNDAMENTUS = 'http://fundamentus.com.br/resultado.php?setor={setor}'
TOTAL_SETORES = 42

FUNCAO_LISTA_VALORES = """let listaInfosSelenium = []; \\
    $("{jquery_element}").each(function(){{  \\
        listaInfosSelenium.push(this.{atributo});  \\
    }}); \\
    return listaInfosSelenium"""

# browser.current_url

def obtem_mapeamento_info_colunas(browser, conjunto_info: dict, tabela_id: str) -> dict:
    """
        Objetivo: Mapear o número da coluna com o texto buscado
    """
    jquery_element = '#{tabela_id} > thead > tr:first > th'.format(tabela_id=tabela_id)

    # constroi funcao para obter o nome das headers
    browser.constroiFuncaoNaPagina('get_headers_info_selenium', FUNCAO_LISTA_VALORES.format(jquery_element=jquery_element, atributo='innerText'))
    #  Executa função, para obter a lista
    nome_colunas = browser.execute_script(""" return get_headers_info_selenium() """)

    return {coluna: indice for indice, coluna in enumerate(nome_colunas)}

def vasculha_setores(browser, tabela_id: str, **informacoes_buscadas):
    conjunto_info = {info.lower(): [] for info in informacoes_buscadas.keys()}

    # Força a busca conter ao menos o nome da ação (papel) e o seu valor (cotação)
    conjunto_info = dict(conjunto_info, **{'papel': [], 'cotação' :[]})

    mapeamento_info_colunas = {}

    for setor in list(range(1,TOTAL_SETORES +1)):

        
        # Atualiza Browser para o setor correspondente
        browser.get(URL_BASE_FUNDAMENTUS.format(setor=setor))
        
        if not browser.existejQueryNaPagina():
            browser.insereJqueryNaPagina()

        if not mapeamento_info_colunas:
            obtem_mapeamento_info_colunas(browser, conjunto_info, tabela_id)

if __name__ == '__main__':
    browser = Browser()
    try:
        vasculha_setores(browser, tabela_id='resultado')
    except Exception as erro:
        print(erro)
        browser.close()
        browser.quit()
