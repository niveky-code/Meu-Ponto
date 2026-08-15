
import tkinter as tk

janela = tk.Tk()
janela.geometry("400x300")

# Variável que vai guardar a opção escolhida
resposta = tk.StringVar(value="")  # começa vazia

opcoes = [
    ("Alternativa A", "a"),
    ("Alternativa B", "b"),
    ("Alternativa C", "c"),
    ("Alternativa D", "d"),
]

tk.Label(janela, text="Qual é a capital do Brasil?", font=("Arial", 12, "bold")).pack(pady=10)

for texto, valor in opcoes:
    tk.Radiobutton(
        janela,
        text=texto,
        variable=resposta,
        value=valor
    ).pack(anchor="w", padx=20)

def verificar():
    print("Selecionado:", resposta.get())

tk.Button(janela, text="Confirmar", command=verificar).pack(pady=10)

janela.mainloop()