# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:53:34 2019

@author: Gui Pupio
"""

import xlwings as xw
from tkinter import filedialog, Tk
from os import getcwd as curPath
from util import insereTextoLento, initBrowser, login_rico
from getpass import getpass


def navegacao(file: str):
    # Acessa link contendo links para as empresas
    browser = initBrowser(r'https://www.rico.com.vc/login/')
    login = input('Usuario: ')
    login_rico(browser=browser, user=login, password=getpass())

    browser.get(r'https://www.rico.com.vc/dashboard/acoes/')
    campo_busca = browser.find_element_by_xpath(
        r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[1]/div/div/input')

    wkb = xw.Book(r'C:\Users\Gui Pupio\Desktop\Pessoal\FIIsDIvidendYield.xlsx')
    sht = wkb.sheets[0]

    for linha in range(1, sht.cells(1, 1).end('down').row):
        insereTextoLento(browser, r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[1]/div/div/input', sht.cells(
            linha, 1).value.split('-')[-1].strip())
        sht.cells(linha, 'D').value = browser.find_element_by_xpath(
            r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[3]/div[1]/table/tbody/tr/td[2]').text

        variacao = browser.find_element_by_xpath(
            r'/html/body/section/div/div[2]/div/div/section/div[6]/div[2]/form/div[1]/div[3]/div[1]/table/tbody/tr/td[3]')

        sht.cells(linha, 'E').value = variacao.text
        # if 'red' in variacao.get_attribute('class'):
        #    sht.cells(linha,'E').value = '-' +  sht.cells(linha,'E').value


if __name__ == "__main__":
    UpLevel = Tk()
    UpLevel.withdraw()

    # files que serão compactados - Todos devem ter a extensão '.xlsx'
    baseFile = filedialog.askopenfilename(
        initialdir=curPath(), title="Selecione o arquivo referente à base")

    # Destroi o tkinter gerado acima..
    UpLevel.destroy()
    navegacao(file=baseFile)
