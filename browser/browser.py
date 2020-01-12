from os import getcwd as curPath
from platform import system as sistema_operacional
from time import sleep

from selenium import webdriver

class Browser(webdriver.Chrome):

    def __init__(self, chromeDriverPath = curPath() + '/chromedriver/' + sistema_operacional().lower() + r'/chromedriver', *args, **kwargs) -> webdriver.Chrome:
        """
            INPUT:
                chromeDriverPath (str): Path ate o chromedriver, Default: path atual
        """
        # Inicializa Browser com chromeDriverPath, default
        super(Browser, self).__init__(chromeDriverPath, *args,**kwargs)

    def insereTextoLento(self, xpath_texto: str, texto: str, delay_escrita: float =0.08, delay_retorno: float =2.5) -> None:
        """
        INPUT:
            self: webdriver.Chrome
            xpath_texto(str): xpath do local onde o texto sera inserido
            texto (str): Texto que deve ser inserido
            delay_escrita (float): tempo de espera (em segundos) entre digitar cada caracter, Default: 0.08
            delay_retorno (float): tempo de espera (em segundos) para retornar, apos digitar tds os caracteres, Default: 2.5
        """
        self.find_element_by_xpath(xpath_texto).clear()
        # Inserimos os caracteres com Delay, pq o site nao reconhece quando escrevemos muito rapido
        for char in texto:
            self.find_element_by_xpath(xpath_texto).send_keys(char)
            sleep(delay_escrita)
        sleep(delay_retorno)

    def existejQueryNaPagina(self) -> bool:
        CRIACAO_FUNCAO_GET_JQUERY = """
            var script = document.createElement('script');
            script.text = 'function get_jquery_selenium(){ \
                try { \
                    return jQuery.fn.jquery \
                } \
                catch(err){ \
                    return "ERRO" \
                } \
            }';
            document.getElementsByTagName('head')[0].appendChild(script);
        """
        self.execute_script(CRIACAO_FUNCAO_GET_JQUERY)

        SENTENCA_JQUERY = "return get_jquery_selenium()"

        jQuery = self.execute_script(SENTENCA_JQUERY)
        if jQuery ==  'ERRO':
            return False
        else: 
            return True

    def insereJqueryNaPagina(self) -> None:
        SENTENCA_JQUERY ="""
        var script = document.createElement('script');
        script.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
        script.type = 'text/javascript';
        document.getElementsByTagName('head')[0].appendChild(script); 
        """
        self.execute_script(SENTENCA_JQUERY)