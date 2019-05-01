# -*- coding: utf-8 -*-
"""
Created on Wed May 1 10:22:34 2019

@author: Guilherme Pupio
"""

from selenium import webdriver
import pandas
from datetime import datetime
from util import initBrowser, login_rico, insereTextoLento
from getpass import getpass

NOW = datetime.now().strftime("%d/%m")
    

def obtem_dict_FII(browser):
    informacoes = {
        'Codigo': [],
        'Nome':[],
    }
    linha = 2
    while True:
        ignora=False
        try:
            codigo = browser.find_element_by_xpath('//table/tbody/tr[' + str(linha) + ']/td[1]')
        except Exception as error:
            print("\n\n\n\n")
            print(error)
            break
        # Verifica se ha *IQ* ou *BL*
        try:
            if len(codigo.find_elements_by_xpath(".//sup")) > 0:
                for sup in codigo.find_elements_by_xpath(".//sup"):
                    if sup.text in ('*IQ*',):
                        ignora=True
        except Exception as error:
            pass
        # Obtem uma lista com os codigos dos FII
        if not ignora:
            informacoes['Codigo'].append(codigo.find_element_by_xpath(".//a").text)
            nome = browser.find_element_by_xpath('//table/tbody/tr[' + str(linha) + ']/td[2]/a').text
            informacoes['Nome'].append(nome)
        linha += 1
    return informacoes

def pesquisa_valores(browser, informacoes):
    # Abre pagina da Rico
    password = getpass()
    browser.get('https://www.rico.com.vc/login/')
    browser.maximize_window()
    # Loga na Pagina da Rico
    login_rico(browser, 'gpupio', password)
    try:
        browser.find_element_by_xpath('/html/body/div[8]/div/div[5]/a[1]').click()
    except Exception:
        pass
    
    browser.get(r'https://www.rico.com.vc/dashboard/acoes/')
    campo_busca = '/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[1]/div/div/input'
    
    informacoes['Valor R$ - ' + NOW] = []
    informacoes['Variacao - ' + NOW] = []
    
    for codigo in informacoes['Codigo']:
        insereTextoLento(browser, campo_busca, codigo)
        valor = float(browser.find_element_by_xpath(r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[3]/div[1]/table/tbody/tr/td[2]').text.replace('.','').replace(',','.').replace('R$','').replace(' ',''))
        informacoes['Valor R$ - ' + NOW].append(valor)
        informacoes['Variacao - ' + NOW].append(browser.find_element_by_xpath(r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[3]/div[1]/table/tbody/tr/td[3]').text)
    
    return informacoes

def export_csv(informacoes:dict):
    df_fiis = pandas.DataFrame.from_dict(informacoes)
    df_ordenado = df_fiis.sort_values(['Valor R$ - ' + NOW, 'Variacao - ' + NOW])
    df_ordenado.to_csv(path_or_buf=curPath() + r'/FIIs_' + NOW.replace('/','-') + '.xls', index=False)

if __name__ == "__main__":
    # Gera Browser
    print("Inicio")
    browser= initBrowser(url= r'https://fiis.com.br/lista-por-codigo/')
    print("Obtendo Codigo e Nome dos FIIs")
    codigo_FIIs = obtem_dict_FII(browser)
    print("Obtendo Valores associados aos COdigos")
    dados_FII = pesquisa_valores(browser, codigo_FIIs)
    print("Exportando Valores")
    export_csv(dados_FII)
    
    