# -*- coding: utf-8 -*-
"""
Created on Mon May  1 12:53:34 2019

@author: Gui Pupio
"""

from selenium import webdriver
from time import sleep
from os import getcwd as curPath
from tkinter import filedialog, Tk


def login_rico(browser, user:str, password:str):
    insereTextoLento(browser, r'//*[@id="loginForm"]/div[1]/input',  user)
    browser.find_element_by_xpath(r'//*[@id="loginForm"]/button').submit()
    # Aguarda 5 segundos a pagina renderizar
    sleep(5)
    #Obtem Botoes de senha
    botoes = browser.find_elements_by_class_name('btn-blue-xlight')
    if len(botoes) != 6:
        raise ErroLoginRico("Provavelmete Houve alteracoes na forma de Login. Verifique!")
    for digito in password:
        for botao in botoes:
            if digito in botao.text:
                botao.click()
                continue
    browser.find_element_by_xpath(r'//*[@id="login-component"]/div/div[2]/div/div[1]/div/form/button').submit() 
            
def get_path_janela_dialogo(initPath = None, multiplos_arquivos= False, titulo='Selecione o arquivo'):
    """
    INPUT:
        initPath (opcional): Define diretorio que a janela sera aberta
        multiplos_arquivos: 
            Default: False
            True: para poder selecionar multiplos arquivos
        titulo:
            Titulo que aparece na janela de Dialogo 
    OUTPUT:
        caminho do Arquivo (str)
    """
    UpLevel = Tk()
    UpLevel.withdraw()
    parametros ={}
    if initPath:  
        parametros['initialdir'] = initPath
    if titulo:
        parametros['title'] = titulo
    
    if multiplos_arquivos:
        baseFile = filedialog.askopenfilenames(initialdir = curPath(),title = titulo)  
    else:
        baseFile = filedialog.askopenfilename(initialdir = curPath(),title = titulo)
    
    #Destroi o tkinter gerado acima..
    UpLevel.destroy()
    return baseFile
        
    
def initBrowser(url:str, chromeDriverPath=curPath() + r'/chromedriver'):
    # Gera browser
    browser = webdriver.Chrome(executable_path=chromeDriverPath)
    # Acessa link contendo links para as empresas
    browser.get(url)
    return browser

def insereTextoLento(browser: webdriver.Chrome, xpath_texto: str, texto: str):
    browser.find_element_by_xpath(xpath_texto).clear()
    # Inserimos os caracteres com Delay, pq o site nao reconhece quando escrevemos muito rapido
    for char in texto:
        browser.find_element_by_xpath(xpath_texto).send_keys(char)
        sleep(0.08)
    sleep(2.5)
    


class ErroLoginRico(Exception):
    pass