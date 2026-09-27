from tkinter import *
from back import *
from PIL import Image, ImageTk
#bug ao excluir um digito no meio do dato como por exemplo o "2" de 12/13/1999, todos os outros digitos se movem para esquerda e o cursor vai pro final // possivel resolução, não deixar o cursor pular pro fimg

def _reformatar(entry, digitos, posicoes_separador, caractere_sep, cursor_digitos):
    novo = ''
    pos_final = 0
    contador_digitos = 0
    for i, d in enumerate(digitos):
        if i in posicoes_separador:
            novo += caractere_sep
        novo += d
        contador_digitos += 1
        if contador_digitos == cursor_digitos:
            pos_final = len(novo)
    entry.delete(0, END)
    entry.insert(0, novo)
    entry.icursor(pos_final)


def mascara_data(event):
    entry = event.widget
    texto = entry.get()
    pos_cursor = entry.index(INSERT)

    # quantos dígitos existem antes da posição atual do cursor
    digitos_antes_cursor = sum(1 for c in texto[:pos_cursor] if c.isdigit())

    digitos = [c for c in texto if c.isdigit()][:8]  # DD MM AAAA
    anterior = getattr(entry, '_qtd_digitos', 0)

    if event.keysym == 'BackSpace' and len(digitos) == anterior:
        digitos = digitos[:-1]
        digitos_antes_cursor = max(0, digitos_antes_cursor - 1)

    entry._qtd_digitos = len(digitos)
    _reformatar(entry, digitos, (2, 4), '/', digitos_antes_cursor)


def mascara_hora(event):
    entry = event.widget
    texto = entry.get()
    pos_cursor = entry.index(INSERT)

    digitos_antes_cursor = sum(1 for c in texto[:pos_cursor] if c.isdigit())

    digitos = [c for c in texto if c.isdigit()][:4]  # HH MM
    anterior = getattr(entry, '_qtd_digitos', 0)

    if event.keysym == 'BackSpace' and len(digitos) == anterior:
        digitos = digitos[:-1]
        digitos_antes_cursor = max(0, digitos_antes_cursor - 1)

    entry._qtd_digitos = len(digitos)
    _reformatar(entry, digitos, (2,), ':', digitos_antes_cursor)


def somente_digitos_e_separador(char_permitido):
    """Filtro leve via validatecommand: barra letras/símbolos indesejados
    antes mesmo do KeyRelease disparar a máscara."""
    def validar(texto_proposto):
        return all(c.isdigit() or c == char_permitido for c in texto_proposto)
    return validar


class reginter:
    def __init__(self, master=None):

        vcmd_data = (master.register(somente_digitos_e_separador('/')), '%P')
        vcmd_hora = (master.register(somente_digitos_e_separador(':')), '%P')

        self.fontePadrao = ("Arial", "10")
        # conteiners
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        for attr in ["hora1conteiner", "hora2conteiner", "hora3conteiner", "hora4conteiner"]:
            f = Frame(master)
            f["padx"] = 20
            f.pack()
            setattr(self, attr, f)

        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()

        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()

        Label(self.primeiroContainer, text="registro de ponto",
              font=self.fontePadrao, width=20).pack(side=TOP)

        Label(self.segundoContainer, text="nome do funcionario",
              font=self.fontePadrao).pack(side=LEFT)
        self.nome = Entry(self.segundoContainer, width=20, font=self.fontePadrao)
        strnome = bNome()
        self.nome.insert(0, strnome)
        self.nome.pack(side=LEFT)

        Label(self.terceiroContainer, text="data",
              font=self.fontePadrao, width=14).pack(side=LEFT)
        self.data = Entry(self.terceiroContainer, validate='key',
                           validatecommand=vcmd_data, font=self.fontePadrao, width=20)
        self.data.pack(side=LEFT)
        self.data.bind('<KeyRelease>', mascara_data)

        campos = [
            ("hora1conteiner", "hora1", "inicio turno"),
            ("hora2conteiner", "hora2", "inicio break"),
            ("hora3conteiner", "hora3", "fim break"),
            ("hora4conteiner", "hora4", "fim turno"),
        ]
        for container_attr, entry_attr, label_text in campos:
            container = getattr(self, container_attr)
            Label(container, text=label_text,
                  font=self.fontePadrao, width=14).pack(side=LEFT)
            entry = Entry(container, validate='key', validatecommand=vcmd_hora,
                          font=self.fontePadrao, width=20)
            entry.pack(side=LEFT)
            entry.bind('<KeyRelease>', mascara_hora)
            setattr(self, entry_attr, entry)

        Button(self.quintoContainer, text="salvar", font=("Calibri", "12"),
               width=15, command=self.registrar).pack()
        Button(self.quintoContainer, text="voltar", font=("Calibri", "12"),
               width=15, command=master.destroy).pack()

    def registrar(self):
        nome = self.nome.get()
        data = self.data.get()
        h1 = self.hora1.get()
        h2 = self.hora2.get()
        h3 = self.hora3.get()
        h4 = self.hora4.get()
        registro(nome, data, h1, h2, h3, h4)


class interface:
    def __init__(self, master=None):
        # Conteiner master
        self.master = master
        self._janelaRegistro = None
        self._janelaMenu = None
        self._janelaBuscar = None

        # conteiner menor
        self.widget = Frame(master)
        self.widget.pack()

        self.bott = Frame(master)
        self.bott["padx"] = 15
        self.bott.pack()

        self.busca = Frame(master)
        self.busca["pady"] = 10
        self.busca.pack()

        # 2. Abre a imagem usando o Pillow
        imagem_original = Image.open("linha_menu.png")

        # 3. Define o novo tamanho (Largura, Altura) e redimensiona
        novo_tamanho = (12, 20)
        imagem_reduzida = imagem_original.resize(novo_tamanho)

        # 4. Converte a imagem do Pillow para o formato do Tkinter
        imagem_tkinter = ImageTk.PhotoImage(imagem_reduzida)

        Label(self.widget, text="deseja registrar novos pontos?",
              font=("Verdana", "12", "italic", "bold")).pack(side=LEFT)
        Button(self.widget, image=imagem_tkinter, width=14, height=16,
               command=self.menuP).pack(side=RIGHT, padx=11)

        Button(self.bott, text="registrar", font=("Calibri", "12"),
               width=15, command=self.registro).pack(side=BOTTOM)

        Button(self.busca, text="buscar", font=("Calibri", "12"),
               width=15, command=self.buscar).pack(side=TOP)

    def menuP(self):
        if self._janelaMenu is not None and self._janelaMenu.winfo_exists():
            self._janelaMenu.lift()
            return

        class menu:
            def __init__(self, master=None):
                self.nomeWig = Frame(master)
                self.nomeWig.pack()

                Label(self.nomeWig, text="alterar nome padrão",
                      font=("Verdana", "12", "italic", "bold")).pack(side=TOP)

                Label(self.nomeWig, text="seu nome:",
                      font=("Verdana", "12", "italic", "bold")).pack(side=LEFT)
                self.nomeEN = Entry(self.nomeWig, width=20, font=("arial", "10"))
                self.nomeEN.pack(side=RIGHT)

                Button(self.nomeWig, text="salvar", command=self.salvar_nome).pack()

            def salvar_nome(self):
                usuario = self.nomeEN.get()
                nome(usuario)

        self._janelaMenu = Toplevel(self.master)
        self._janelaMenu.title("menu")
        menu(self._janelaMenu)

    def buscar(self):

        if self._janelaBuscar is not None and self._janelaBuscar.winfo_exists():
            self._janelaBuscar.lift()
            return

        class busc:
            def __init__(self, master=None):
                self.buscJanela = Frame(master)
                self.buscJanela.pack(padx=10, pady=10)

                Label(self.buscJanela, text="Deseja buscar por dia, mês ou ano?",
                      font=("Verdana", "12", "italic", "bold")).pack()

                self.opcaoBusca = StringVar(value="dia")

                frameOpcoes = Frame(self.buscJanela)
                frameOpcoes.pack(pady=5)

                Radiobutton(frameOpcoes, text="Dia", variable=self.opcaoBusca,
                            value="dia", command=self.atualizarPlaceholder).pack(side="left")
                Radiobutton(frameOpcoes, text="Mês", variable=self.opcaoBusca,
                            value="mes", command=self.atualizarPlaceholder).pack(side="left")
                Radiobutton(frameOpcoes, text="Ano", variable=self.opcaoBusca,
                            value="ano", command=self.atualizarPlaceholder).pack(side="left")

                self.entryBusca = Entry(self.buscJanela, font=("Verdana", "12"), justify="center")
                self.entryBusca.pack(pady=10)
                self.entryBusca.bind("<KeyRelease>", self.aplicarMascara)

                self.atualizarPlaceholder()

            def atualizarPlaceholder(self):
                # Limpa o campo ao trocar de opção, pois o formato muda
                self.entryBusca.delete(0, "end")

            def aplicarMascara(self, event=None):
                texto = "".join(filter(str.isdigit, self.entryBusca.get()))
                opcao = self.opcaoBusca.get()

                if opcao == "dia":
                    texto = texto[:8]
                    if len(texto) >= 5:
                        texto = f"{texto[:2]}/{texto[2:4]}/{texto[4:]}"
                    elif len(texto) >= 3:
                        texto = f"{texto[:2]}/{texto[2:]}"
                elif opcao == "mes":
                    texto = texto[:6]
                    if len(texto) >= 3:
                        texto = f"{texto[:2]}/{texto[2:]}"
                else:  # ano
                    texto = texto[:4]

                self.entryBusca.delete(0, "end")
                self.entryBusca.insert(0, texto)

        self._janelaBuscar = Toplevel(self.master)
        self._janelaBuscar.title("em produção")
        self._janelaBuscar.geometry("400x180")
        busc(self._janelaBuscar)

    def registro(self):
        # Reaproveita janela se já estiver aberta
        if self._janelaRegistro is not None and self._janelaRegistro.winfo_exists():
            self._janelaRegistro.lift()
            return

        self._janelaRegistro = Toplevel(self.master)  # Toplevel, não Tk()
        self._janelaRegistro.title("Registro de Ponto")
        reginter(self._janelaRegistro)