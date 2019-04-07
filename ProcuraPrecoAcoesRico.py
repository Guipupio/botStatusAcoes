# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:53:34 2019

@author: Gui Pupio
"""

import xlwings as xw
from tkinter import filedialog, Tk
from os import getcwd as curPath
from selenium import webdriver
from string import ascii_uppercase as letrasAlfabeto
from datetime import datetime
from time import sleep

def insereTextoLento(browser: webdriver.Chrome, xpath_texto: str, texto: str):
    browser.find_element_by_xpath(xpath_texto).clear()

    # Inserimos os caracteres com Delay, pq o site nao reconhece quando escrevemos muito rapido
    for char in texto:
        browser.find_element_by_xpath(xpath_texto).send_keys(char)
        sleep(0.08)
    sleep(2.5)

def navegacao(file: str):

    # Gera browser
    browser = webdriver.Chrome(executable_path=r'C:\Users\Gui Pupio\Desktop\Pessoal\python' + r'\chromedriver.exe')
    
    # Acessa link contendo links para as empresas
    browser.get(r'https://www.rico.com.vc/login/')
    insereTextoLento(browser, r'//*[@id="loginForm"]/div[1]/input', 'gpupio')
    browser.find_element_by_xpath(r'//*[@id="loginForm"]/button').submit()
    insereTextoLento(browser, r'//*[@id="login-component"]/div/div[2]/div/div[1]/div/form/div[1]/input', '')
    
    
    browser.get(r'https://www.rico.com.vc/dashboard/acoes/')
    campo_busca = browser.find_element_by_xpath(r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[1]/div/div/input')
    
    wkb = xw.Book(r'C:\Users\Gui Pupio\Desktop\Pessoal\FIIsDIvidendYield.xlsx')
    sht = wkb.sheets[0]
    
    for linha in range(1,sht.cells(1,1).end('down').row):
        insereTextoLento(browser,r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[1]/div/div/input', sht.cells(linha,1).value.split('-')[-1].strip())
        sht.cells(linha,'D').value = browser.find_element_by_xpath(r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[3]/div[1]/table/tbody/tr/td[2]').text
        
        variacao = browser.find_element_by_xpath(r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[3]/div[1]/table/tbody/tr/td[3]')
        
        sht.cells(linha,'E').value = variacao.text
        #if 'red' in variacao.get_attribute('class'):
        #    sht.cells(linha,'E').value = '-' +  sht.cells(linha,'E').value
        
if __name__ == "__main__":
    UpLevel = Tk()
    UpLevel.withdraw()
    
    #files que serão compactados - Todos devem ter a extensão '.xlsx'
    baseFile = filedialog.askopenfilename(initialdir = curPath(),title = "Selecione o arquivo referente à base")
   
    #Destroi o tkinter gerado acima..
    UpLevel.destroy()    
    navegacao(file= baseFile)