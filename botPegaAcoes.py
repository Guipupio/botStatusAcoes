# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 21:46:34 2019

@author: Guilherme Pupio
"""

import xlwings as xw
from tkinter import filedialog, Tk
from os import getcwd as curPath
from selenium import webdriver
from string import ascii_uppercase as letrasAlfabeto
from datetime import datetime
from time import sleep
from util import get_path_janela_dialogo, initBrowser

def completaExcel(browser, sht, sht2 = None):
    linha = 2
    limit = sht.cells(1,1).end('down').row
    coluna = sht.cells(1,1).end('right').column
    data = datetime.now()
    sht.cells(1, coluna).value = str(data.day) + '/' + str(data.month) + '/' + str(data.year)
    while linha <=  limit:
        try:
            # Acessamos a pagina da acao
            browser.get(sht.cells(linha, 'A').hyperlink)
            
            # Alteramos o frame ate chegar ao da tabela
            browser.switch_to.frame('ctl00_contentPlaceHolderConteudo_iframeCarregadorPaginaExterna')
            browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0].get_attribute('id'))
            
            num_add = 0
            linhaTabela = 2
            elementos =[]
            sleep(7)
            
            # Pegando dados refentes aa primeira acao
            elementos.append(browser.execute_script('''return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr.ticker.active.quote-ticker-inited > td.symbol-short-name-container').textContent'''))
            elementos.append(browser.execute_script('''return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr.ticker.active.quote-ticker-inited > td.symbol-last').textContent'''))
            elementos.append(browser.execute_script('''return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr.ticker.active.quote-ticker-inited > td.symbol-change').textContent'''))
            
            # Inserindo na planilha
            for coluna in list(range(0,3)):
                sht2.cells(linha, coluna+2).value = elementos[coluna]
            
            linhaTabela = 2
            while True:
                elementos = []
                elementos.append(browser.execute_script("return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr:nth-child("+str(linhaTabela) +") > td.symbol-short-name-container').textContent"))
                elementos.append(browser.execute_script("return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr:nth-child("+str(linhaTabela) +") > td.symbol-last').textContent"))
                elementos.append(browser.execute_script("return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr:nth-child("+str(linhaTabela) +") > td.symbol-change').textContent"))
                
                # Se texto nao encontrado, quebramos o loop
                if any(map(lambda text: text == '\xa0', [el for el in elementos])):
                    break
                                                                                         
                                                                                         
                #sht2.range(str(linha) + ":" + str(linha)).api.Insert(-4161)
                #sht2.cells(linha, 'A').add_hyperlink(sht.cells(linha + 1, 'A').hyperlink, sht.cells(linha + 1, 'A').value)
                linha += 1
                limit += 1
                
                for coluna in list(range(0,3)):
                    sht2.cells(linha, coluna+2).value = elementos[coluna]
                    
                linhaTabela += 1
        except:
            pass
        linha += 1

def getInfobasica(browser, sht):
    linha = 2
    limit = sht.cells(1,1).end('down').row
    while linha <=  limit:
        try:
            # Acessamos a pagina da acao
            browser.get(sht.cells(linha, 'A').hyperlink)
            
            # Alteramos o frame ate chegar ao da tabela
            browser.switch_to.frame('ctl00_contentPlaceHolderConteudo_iframeCarregadorPaginaExterna')
            browser.switch_to.frame(browser.find_elements_by_tag_name('iframe')[0].get_attribute('id'))
            
            num_add = 0
            linhaTabela = 2
            elementos =[]
        
            sleep(7)
            # Pegando dados refentes aa primeira acao
            elementos.append(browser.execute_script('''return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr.ticker.active.quote-ticker-inited > td.symbol-short-name-container').textContent'''))
            elementos.append(browser.execute_script('''return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr.ticker.active.quote-ticker-inited > td.symbol-last').textContent'''))
            elementos.append(browser.execute_script('''return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr.ticker.active.quote-ticker-inited > td.symbol-change').textContent'''))
            
            # Inserindo na planilha
            for coluna in list(range(0,3)):
                sht.cells(linha, coluna+2).value = elementos[coluna]
            
            linhaTabela = 2
            while True:
                elementos = []
                elementos.append(browser.execute_script("return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr:nth-child("+str(linhaTabela) +") > td.symbol-short-name-container').textContent"))
                elementos.append(browser.execute_script("return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr:nth-child("+str(linhaTabela) +") > td.symbol-last').textContent"))
                elementos.append(browser.execute_script("return document.querySelector('#miniwidget > div.pages > div > table > tbody > tr:nth-child("+str(linhaTabela) +") > td.symbol-change').textContent"))
                
                # Se texto nao encontrado, quebramos o loop
                if any(map(lambda text: text == '\xa0', [el for el in elementos])):
                    break
                                                                                         
                                                                                         
                sht.range(str(linha) + ":" + str(linha)).api.Insert(-4161)
                sht.cells(linha, 'A').add_hyperlink(sht.cells(linha + 1, 'A').hyperlink, sht.cells(linha + 1, 'A').value)
                num_add += 1
                limit += 1
                
                for coluna in list(range(0,3)):
                    sht.cells(linha, coluna+2).value = elementos[coluna]
                    
                linhaTabela += 1
        except:
            pass
        linha += 1 + num_add

def getNomeLink(browser, sht ):
    linha = 1
    sht.cells(linha, 'A').value = 'Nome'
    sht.cells(linha, 'B').value = 'Sigla'
    sht.cells(linha, 'C').value = 'Valor R$'
    sht.cells(linha, 'D').value = 'Change'
    try:
        while True:            
            item = browser.find_element_by_xpath('//*[@id="ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_grdEmpresa_ctl01"]/tbody/tr['+ str(linha) +']/td[1]/a')
            sht.cells(linha+1, 'A').add_hyperlink(address=item.get_attribute('href'), text_to_display= item.text)
            linha += 1
    except Exception:
        pass

def navegacao(file: str):

    browser = initBrowser(url = 'http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm')
    # Mudamos de iframe
    browser.switch_to.frame('bvmf_iframe')
    # Clicamos para aparecer todas as acoes
    browser.find_element_by_xpath('//*[@id="ctl00_contentPlaceHolderConteudo_BuscaNomeEmpresa1_btnTodas"]').click()
    
    if file == '':
        wkb = xw.Book()
        sht = wkb.sheets[0]
        getNomeLink(browser, sht)
        getInfobasica(browser, sht) 
        wkb.save(r'C:\Users\Gui Pupio\Desktop\Pessoal\python' + r'\base-' +str(data.day) + '-' + str(data.month)+ '-' + str(data.year))
    else:
        wkb = xw.Book(file)
        sht = wkb.sheets[0]
        wkb.sheets.add(name= 'TEMP', after = sht)
        sht2 = wkb.sheets['TEMP']
        completaExcel(browser, sht, sht2)
        wkb.save()      

        
if __name__ == "__main__":
    
    baseFile = get_path_janela_dialogo(initialdir = curPath(),title = "Selecione o arquivo referente à base")    
    navegacao(file= baseFile)
    
    