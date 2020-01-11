from os import getcwd as curPath
from pathlib import Path
from platform import system as sistema_operacional
from time import sleep

from selenium import webdriver


def initBrowser(url: str, chromeDriverPath=Path(curPath()).parent.__str__() + '/chromedriver/' + sistema_operacional().lower() + r'/chromedriver') -> webdriver.Chrome:
    """
    INPUT:
        url (str): Pagina que o browser deve abrir
        chromeDriverPath (str): Path ate o chromedriver, Default: path atual
    """
    # Gera browser
    browser = webdriver.Chrome(executable_path=chromeDriverPath)
    # Acessa link contendo links para as empresas
    browser.get(url)
    return browser

def insereTextoLento(browser: webdriver.Chrome, xpath_texto: str, texto: str, delay_escrita: float =0.08, delay_retorno: float =2.5) -> None:
    """
    INPUT:
        browser: webdriver.Chrome
        xpath_texto(str): xpath do local onde o texto sera inserido
        texto (str): Texto que deve ser inserido
        delay_escrita (float): tempo de espera (em segundos) entre digitar cada caracter, Default: 0.08
        delay_retorno (float): tempo de espera (em segundos) para retornar, apos digitar tds os caracteres, Default: 2.5
    """
    browser.find_element_by_xpath(xpath_texto).clear()
    # Inserimos os caracteres com Delay, pq o site nao reconhece quando escrevemos muito rapido
    for char in texto:
        browser.find_element_by_xpath(xpath_texto).send_keys(char)
        sleep(delay_escrita)
    sleep(delay_retorno)
