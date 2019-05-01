# -*- coding: utf-8 -*-
"""
Created on Wed May 1 10:22:34 2019

@author: Guilherme Pupio
"""
from tkinter import filedialog, Tk
from os import getcwd as curPath
from selenium import webdriver
import pandas

def initBrowser(url:str):
    # Gera browser
    browser = webdriver.Chrome(executable_path=curPath() + r'/chromedriver')
    # Acessa link contendo links para as empresas
    browser.get(url)
    return browser
    

def obtem_dict_FII(browser):
    informacoes = {
        'Codigo': [],
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
        linha += 1
    return informacoes
        

if __name__ == "__main__":
    # Gera Browser
    browser= initBrowser(url= r'https://fiis.com.br/lista-por-codigo/')
    codigo_FIIs = obtem_dict_FII(browser)