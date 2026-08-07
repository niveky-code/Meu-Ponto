
from tkinter import *
from back import *
from PIL import Image, ImageTk



def limitar_text(a):
    try:
        if len(a) <= 10:
            if (len(a) < 3):
                if (a[2].isdigit()):
                    return False
            if (len(a) < 6 ):
                if(a[5].isdigit()):
                    return False
            return all(c.isdigit() or c == '/' for c in a)
    except IndexError:
        print("erro")

    
    return False

def limitar_text_hora(a):
    if len(a) <= 5:
        if (len(a) > 2) and (a[2].isdigit()):
            return False
        if len(a) < 3:
            for item in a:
                num = int(item)
                if (len(a) < 2 and num > 2):
                    
                    return False
                if (len(a) > 1) and len(a) < 3:
                    if (num > 3) and not (a[0] == '1' or a[0] == '0'):
                        return False
        if len(a) > 3:
            num = int(a[3])
            if (len(a) == 4 and num > 5):
                return False
        return all(c.isdigit() or c == ':' for c in a)
    return False




class reginter:
    def __init__(self, master=None):
        vcmd1 = (master.register(limitar_text_hora), '%P')
        self.fontePadrao = ("Arial", "10")
        #conteiners
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()

        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        for attr in ["hora1conteiner","hora2conteiner","hora3conteiner","hora4conteiner"]:
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
        self.nome.pack(side=LEFT)

        vcmd = (self.terceiroContainer.register(limitar_text), "%P")
        Label(self.terceiroContainer, text="data",
              font=self.fontePadrao, width=14).pack(side=LEFT)
        self.data = Entry(self.terceiroContainer, validate='key',
                          validatecommand=vcmd, font=self.fontePadrao, width=20)
        self.data.insert(0,"00/00/0000")
        self.data.pack(side=LEFT)

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
            entry = Entry(container, validate='key', validatecommand=vcmd1,
                          font=self.fontePadrao, width=20)
            entry.pack(side=LEFT)
            setattr(self, entry_attr, entry)

        Button(self.quintoContainer, text="enviar", font=("Calibri", "12"),
               width=15, command=self.registrar).pack()
        Button(self.quintoContainer, text="voltar", font=("Calibri", "12"),
               width=15, command=master.destroy).pack()

    def registrar(self):
        nome  = self.nome.get()
        data  = self.data.get()
        h1    = self.hora1.get()
        h2    = self.hora2.get()
        h3    = self.hora3.get()
        h4    = self.hora4.get()
        registro(nome, data, h1, h2, h3, h4) 
    
 

class interface:
    def __init__(self, master=None):
        #Conteiner master
        self.master = master
        self._janela = None
        self._janelaMenu = None
        #conteiner menor
        self.widget = Frame(master)
        self.widget.pack()

        self.bot = Frame(master)
        self.bot["padx"] = 15
        self.bot.pack()
        # 2. Abre a imagem usando o Pillow
        imagem_original = Image.open("linha_menu.png")

        # 3. Define o novo tamanho (Largura, Altura) e redimensiona
        novo_tamanho = (12, 20)
        imagem_reduzida = imagem_original.resize(novo_tamanho)

        # 4. Converte a imagem do Pillow para o formato do Tkinter
        imagem_tkinter = ImageTk.PhotoImage(imagem_reduzida)


        Label(self.widget, text="deseja registrar novos pontos?",
              font=("Verdana", "12", "italic", "bold")).pack(side=LEFT)
        Button(self.widget,image=imagem_tkinter,width=14,height=16,
               command=self.menuP ).pack(side=RIGHT,padx=11)

        Button(self.bot, text="registrar", font=("Calibri", "12"),
                       width=15, command=self.registro).pack(side=BOTTOM)
        
        

        
    def menuP(self):
        if self._janelaMenu is not None and self._janelaMenu.winfo_exists():
            self._janelaMenu.lift()
            return
        class menu:
            def __init__(self,master=None):
                self.nomeWig=Frame(master)
                self.nomeWig.pack()

                Label(self.nomeWig, text="seu nome:",
                  font=("Verdana", "12", "italic", "bold")).pack(side=LEFT)
                self.nomeEN = Entry(self.nomeWig, width=20, font=("arial","10"))
                self.nomeEN.pack(side=RIGHT)


        self._janelaMenu = Toplevel(self.master)
        self._janelaMenu.title("menu")
        menu(self._janelaMenu)
                

    def registro(self):
        # Reaproveita janela se já estiver aberta
        if self._janela is not None and self._janela.winfo_exists():
            self._janela.lift()
            return

        self._janela = Toplevel(self.master)  # Toplevel, não Tk()
        self._janela.title("Registro de Ponto")
        reginter(self._janela)




