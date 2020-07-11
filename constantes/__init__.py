from platform import system as sistema_operacional

def carregar_configuracao(arquivo: str):
    """Carregar <arquivo> retornando um dicionário.

    Args:
        arquivo (str): path completo ate o arquivo de configuracao

    Returns:
        dict: dicionario contendo as configuracoes lidas no arquivo
    """
    configuracao = {}
    with open(arquivo, 'r') as _file:
        for linha in _file.readlines():
            _linha = linha.strip()
            # Ignora comentarios
            if _linha.startswith('#') or len(_linha) == 0:
                continue 
            
            chave, valor = _linha.split('=', 1)

            if chave == 'MEUS_FIIS':
                try:
                    valor = list(map(lambda fii: fii.strip(), valor.split(',')))
                except Exception:
                    pass
            
            configuracao[chave] = valor
    
    return configuracao


SEP_DIR = '/' if sistema_operacional().lower() == 'linux' else '\\'

PATH_USER_FILE = SEP_DIR.join(['.', 'user.properties'])

DICT_USER_CONFIGS = carregar_configuracao(PATH_USER_FILE)


