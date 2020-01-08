from selenium import webdriver
from os import getcwd as curPath
from pathlib import Path
from platform import system as sistema_operacional

def initBrowser(url: str, chromeDriverPath=Path(curPath()).parent.__str__() + '/chromedriver/' + sistema_operacional().lower() + r'/chromedriver'):
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

