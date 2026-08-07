import tkinter as tk
from PIL import Image, ImageTk

# 1. Cria a janela do Tkinter
#janela = tk.Tk()
#janela.title("Imagem Redimensionada")

# 2. Abre a imagem usando o Pillow
imagem_original = Image.open("linha_menu.png")

# 3. Define o novo tamanho (Largura, Altura) e redimensiona
novo_tamanho = (14, 16)
imagem_reduzida = imagem_original.resize(novo_tamanho)

# 4. Converte a imagem do Pillow para o formato do Tkinter
imagem_tkinter = ImageTk.PhotoImage(imagem_reduzida)

# 5. Coloca a imagem em um Label e exibe na janela
#rotulo = tk.Label(janela, image=imagem_tkinter)
#rotulo.pack(padx=20, pady=20)

# Mantém a janela aberta
#janela.mainloop()
