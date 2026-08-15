from pathlib import Path


pasta_atual = Path(__file__).resolve().parent



def registro (nome,data,h1,h2,h3,h4):
    mes=data[3:5]
    ano=data[6:]
    caminho_arquivo = pasta_atual / "dados" / f"{nome}_{mes}_{ano}.txt"
    try:
        with open(caminho_arquivo,"a") as arq:
            ponto_completo=f"{nome}_{data}_{h1}_{h2}_{h3}_{h4}\n"
            arq.write(ponto_completo)
    except FileNotFoundError:
        with open(caminho_arquivo,"w") as arq:
            pass
        caminho = Path(f"{pasta_atual}/{caminho_arquivo}")

        # parents=True : cria todas as pastas pais que estiverem faltando
        # exist_ok=True: evita erros caso a pasta já exista
        caminho.mkdir(parents=True, exist_ok=True)

def nome(nome):

    caminho="nomeUnico.txt"
    try:
        with open(caminho,"w") as arq:
            arq.write(nome)

    finally:
        pass

def bNome():
    nomeus = "usuario"
    caminho="nomeUnico.txt"
    
    with open(caminho,"r") as arq:
        nomeus=arq.read()
        print(nomeus) 
        return nomeus



