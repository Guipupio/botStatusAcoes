from csv import QUOTE_ALL, writer
from os import listdir
from shutil import move

tamanho_campos = {
    "TIPREG": 2,
    "DATA": 8,
    "CODBDI": 2,
    "CODNEG": 12,
    "TPMERC": 3,
    "NOMRES": 12,
    "ESPECI": 10,
    "PRAZOT": 3,
    "MODREF": 4,
    "PREABE": 13,
    "PREMAX": 13,
    "PREMIN": 13,
    "PREMED": 13,
    "PREULT": 13,
    "PREOFC": 13,
    "PREOFV": 13,
    "TOTNEG": 5,
    "QUATOT": 18,
    "VOLTOT": 18,
    "PREEXE": 18,
    "INDOPC": 1,
    "DATVEN": 8,
    "FATCOT": 7,
    "PTOEXE": 13,
    "CODISI": 12,
    "DISMES": 3,
}

def formata_valores(string: str):
    if string.isnumeric() and len(string) == 8:
        return string[0:4] + "-" + string[4:6] + "-" + string[6:]
    elif string.isnumeric(): return int(string)
    else: return string

def linha2lista(linha: str, tamanhos: list) -> list:
    """
        Recebe uma Linha de informaçao 

        OUTPUT:
            Lista com o texto da linha separado pelos tamanhos
    """
    inicio = 0
    infos = []
    for tamanho in tamanhos:
        fim = inicio + tamanho
        infos.append(formata_valores(linha[inicio:fim].strip()))
        inicio = fim
    
    return infos

if __name__ == "__main__":

    # Diretorio com os arquivos TXT
    root_raiz = '/home/pupio/COTACAO_HISTORICA/{dir}/'
    # Lista com o nome do todos os arquivos do diretorio
    list_files = listdir(root_raiz.format(dir='raw'))

    for filename in list_files:
        print('Iniciando transformacao para {}'.format(filename))
        # Abre arquivo para registrar infos csv
        with open(root_raiz.format(dir='csv') + filename[:-3] + 'csv', 'w', newline='', encoding = "ISO-8859-1") as csv_file:
            csv = writer(csv_file, quoting=QUOTE_ALL)
            csv.writerow(list(tamanho_campos.keys()))

            # Le arquivo
            with open(root_raiz.format(dir='raw') + filename, 'r', encoding = "ISO-8859-1") as file:
                # Obtem o conteudo do arquivo, removendo
                data = file.readlines()[1:-2]
                for line in data:
                    csv.writerow(linha2lista(line, tamanho_campos.values()))
        
        move(root_raiz.format(dir='raw') + filename, root_raiz.format(dir='OK') + filename)