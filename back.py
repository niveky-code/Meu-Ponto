import re
from pathlib import Path


pasta_atual = Path(__file__).resolve().parent
pasta_dados = pasta_atual / "dados"


def criar_pasta_nome(nome):
    # troca caracteres que o Windows não aceita em nome de pasta
    pasta_nome = re.sub(r'[<>:"/\\|?*]', "_", nome.strip())
    if pasta_nome:
        (pasta_dados / pasta_nome).mkdir(parents=True, exist_ok=True)


def registro(nome, data, h1, h2, h3, h4):
    mes = data[3:5]
    ano = data[6:]
    nomedUs =nome.strip()
    pasta_dados.mkdir(parents=True, exist_ok=True)
    criar_pasta_nome(nome)

    caminho_arquivo = pasta_dados/ nomedUs / f"{nome}_{mes}_{ano}.txt"
    with open(caminho_arquivo, "a", encoding="utf-8") as arq:
        arq.write(f"{nome}_{data}_{h1}_{h2}_{h3}_{h4}\n")


def nome(nome):
    nome = nome.strip()

    pasta_dados.mkdir(parents=True, exist_ok=True)
    with open(pasta_dados / "nomeUnico.txt", "w", encoding="utf-8") as arq:
        arq.write(nome)

    criar_pasta_nome(nome)


def bNome():
    nomeus = "usuario"
    caminho = pasta_dados / "nomeUnico.txt"
    try:
        with open(caminho, "r", encoding="utf-8") as arq:
            nomeus = arq.read().strip()
            return nomeus
    except FileNotFoundError:
        return nomeus