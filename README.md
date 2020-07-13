# Dependencias:
- Python3.7+
- Chrome versão 83.x

## Outras Versoes do Chrome
- Atualize o chromeDriver instalado em `chromedriver/plataforma/chromedriver`, conforme sua versao de Chrome
> https://chromedriver.chromium.org/downloads

## Dependencias python
- Instale os pacotes necessarios com:
```shell
python -m pip install requirements.txt
```

# Fundos Imobiliarios

## Buscar Informações
- Para gerar um arquivo CSV com as informacoes atuais dos FIIs brasileiros execute:
```shell
python main.py -gf 1
```
## Gerar analise
- Para Plotar uma imagem com as ultimas informacoes buscadas:
```shell
python main.py -pf -1
```
## Gerar analise apenas dos seus FIIS
- Insira no arquivo `user.properties` os nomes dos seus FIIs conforme o padrão definido em `user.properties`
- Para Plotar uma imagem com as ultimas informacoes buscadas de apenas os seus FIIs:
```shell
python main.py -pf -1 --only-mine 1
```

## Exemplo completo inicial

```shell
python main.py -gf 1 -pf -1 
```

# Ações
- Em desenvolvimento.. ta um lixo por enquanto


