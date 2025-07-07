import os
import json
import tkinter as tk
from tkinter import messagebox
import subprocess

config_path = os.path.join(os.path.dirname(__file__), "config_email.json")

def salvar_config(e_remetente, senha, e_destinatario, smtp):
    dados = {
        "remetente": e_remetente,
        "senha": senha,
        "destinatario": e_destinatario,
        "smtp": smtp
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)
    return True

def abrir_gui_configuracao():
    def on_salvar():
        if not (entry_rem.get() and entry_senha.get() and entry_dest.get() and entry_smtp.get()):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        salvar_config(entry_rem.get(), entry_senha.get(), entry_dest.get(), entry_smtp.get())
        root.destroy()
        iniciar_monitoramento()

    root = tk.Tk()
    root.title("Configurar E-mail do Monitor")
    root.geometry("400x220")
    root.resizable(False, False)

    tk.Label(root, text="E-mail Remetente:").pack()
    entry_rem = tk.Entry(root, width=40)
    entry_rem.pack()

    tk.Label(root, text="Senha do App:").pack()
    entry_senha = tk.Entry(root, width=40, show="*")
    entry_senha.pack()

    tk.Label(root, text="E-mail Destinatário:").pack()
    entry_dest = tk.Entry(root, width=40)
    entry_dest.pack()

    tk.Label(root, text="Servidor SMTP:").pack()
    entry_smtp = tk.Entry(root, width=40)
    entry_smtp.insert(0, "smtp.gmail.com")
    entry_smtp.pack()

    tk.Button(root, text="Salvar e Iniciar Monitor", command=on_salvar).pack(pady=10)
    root.mainloop()

def iniciar_monitoramento():
    caminho = os.path.join(os.path.dirname(__file__), "monitor_servicos.py")
    subprocess.run(["python", caminho], shell=True)

# Checagem e execução
if not os.path.exists(config_path):
    abrir_gui_configuracao()
else:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if all(k in cfg and cfg[k].strip() for k in ("remetente", "senha", "destinatario", "smtp")):
            iniciar_monitoramento()
        else:
            abrir_gui_configuracao()
    except Exception:
        abrir_gui_configuracao()
