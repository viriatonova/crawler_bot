# Crawler bot

Prova de conceito para web crawler e scraper

## Índice

1. [Dependências](#dependencias)
2. [Setup](#setup)
2. [Modo de uso](#modo-de-uso)

## Dependencias

- [Python](https://www.python.org/)
- [Google Chrome](https://www.google.com/intl/pt-BR/chrome/)
- [Chromedriver](https://chromedriver.chromium.org/downloads)

## Setup 

- Estutura de pastas do projeto:

    ```text
        crawler_bot/
        ├── bot/
        │   └── entity/
        ├── out/
        └── chromedriver
    ```
- Download `Chromedriver` e coloque no diretório `root` do projeto
- Crie e ative o ambiente virtual python, e, em seguida instale as dependências do projeto:
    ```bash
        $ python -m venv venv
        $ source venv/bin/activate
        $ pip install -r requirements.txt
    ```

## Modo de uso

- Navegue até o diretório `root` do projeto
- Comando de CLI do projeto:
    - -r : `definir região`
    - -s : `[OPICIONAL] definir formato para salvar os dados`
    ```bash
        python main.py -r China # sem o parâmentro -s imprime os dados na tela 
        python main.py -r Brazil -s json
        python main.py -r Chile -s csv
    ```