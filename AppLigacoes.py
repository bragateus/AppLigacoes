import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox, colorchooser
from tkinter import PhotoImage 
import random
import webbrowser  


# Determinar o diretório base (onde o executável ou script está localizado pra teste)
if getattr(sys, 'frozen', False):  # É executável?
    diretorio_base = os.path.dirname(sys.executable)
else:  # Caso contrário, usa o diretório do script
    diretorio_base = os.path.dirname(os.path.realpath(__file__))

# Caminho para os arquivos
caminho_arquivo = os.path.join(diretorio_base, 'historico_ligacoes.txt')
caminho_anotacoes = os.path.join(diretorio_base, 'anotacoes.txt')

# Função para verificar e criar os arquivos, se precisar
def verificar_ou_criar_arquivo(caminho):
    if not os.path.exists(caminho):
        with open(caminho, 'w') as f:
            f.write("")  # Cria o arquivo vazio novo

# Verificar e criar os arquivos necessários
verificar_ou_criar_arquivo(caminho_arquivo)
verificar_ou_criar_arquivo(caminho_anotacoes)

# Variáveis globais
contador = 0
leads = 0
reunioes = 0

# Cores iniciais (dark mode)
corFundo = "#1f1f1f"
corEntry = "#4f4f4f"
corFonte = "#0084d6"
corClara = "white"
corBotao = "#0084d6"
corBotaoMenos = "#42505A" 
corReset = "#ff4d4d"
corLinks = "#454546"

# Função para carregar os contadores do jeito certo
def carregar_contador():
    global contador, leads, reunioes
    if not os.path.exists(caminho_arquivo):
        return
    
    data_atual = datetime.now().strftime('%d-%m-%Y')
    
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
        
    # Procurar a data atual no arquivo (começa do final para melhor performance)
    for i in range(len(linhas)-1, -1, -1):
        if linhas[i].strip() == f"---{data_atual}---":
            if i+4 < len(linhas):  
                try:
                    contador = int(linhas[i+1].split(":")[1].strip())
                    leads = int(linhas[i+2].split(":")[1].strip())
                    reunioes = int(linhas[i+3].split(":")[1].strip())
                except (IndexError, ValueError):
                    pass
            break

# Função pra Salvar os contadores
def salvar_contador(reset=False):
    global contador, leads, reunioes
    data_atual = datetime.now().strftime('%d-%m-%Y')
    hora_atual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    ramal = entry_ramal.get()

    # Carrega apenas as linhas necessárias
    linhas_existentes = []
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            linhas_existentes = f.readlines()

    nova_entrada = f"---{data_atual}---\n"
    existe_data = False
    indice_data = -1

    # Procura a data atual no txt
    for i, linha in enumerate(linhas_existentes):
        if linha.strip() == nova_entrada.strip():
            existe_data = True
            indice_data = i
            break

    # Novas linhas no txt
    linhas_novas = []
    if existe_data:
        linhas_novas = linhas_existentes[:indice_data]
        linhas_novas.extend([
            nova_entrada,
            f"LA: {contador}\n",
            f"L: {leads}\n",
            f"R: {reunioes}\n",
            f"Ramal: {ramal}\n",
        ])
    else:
        linhas_novas = linhas_existentes + [
            nova_entrada,
            f"LA: {contador}\n",
            f"L: {leads}\n",
            f"R: {reunioes}\n",
            f"Ramal: {ramal}\n",
        ]

    # Adiciona o registro atual
    if not reset:
        linhas_novas.append(f"{hora_atual} - Ligações: {contador} - Leads: {leads} - Reuniões: {reunioes}\n")
    else:
        linhas_novas.append(f"{hora_atual} - Contador resetado\n")

    # Escreve de volta no arquivo
    with open(caminho_arquivo, 'w') as f:
        f.writelines(linhas_novas)

# Função para salvar anotações
def salvar_anotacoes(text_widget):
    data_atual = datetime.now().strftime('%d-%m-%Y')
    with open(caminho_anotacoes, 'w') as f:
        f.write(f"---{data_atual}---\n")
        f.write(text_widget.get("1.0", tk.END))

# Função para abrir a janela de anotações
def abrir_anotacoes():
    anotacoes_window = tk.Toplevel(janela)
    anotacoes_window.title("Anotações")
    anotacoes_window.geometry("400x300")
    anotacoes_window.configure(bg=corFundo)

    # Configura a janela para ficar sempre no topo
    anotacoes_window.wm_attributes("-topmost", 1)

    texto_anotacoes = scrolledtext.ScrolledText(anotacoes_window, wrap=tk.WORD, width=50, height=15,
                                                font=("Arial", 12), bg=corEntry, fg=corClara)
    texto_anotacoes.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Carregar anotações do dia
    data_atual = datetime.now().strftime('%d-%m-%Y')
    if os.path.exists(caminho_anotacoes):
        with open(caminho_anotacoes, 'r') as f:
            linhas = f.readlines()
            if linhas and linhas[0].strip() == f"---{data_atual}---":
                texto_anotacoes.insert(tk.END, "".join(linhas[1:]))

    # Salvar automaticamente ao fechar a janela
    anotacoes_window.protocol("WM_DELETE_WINDOW", lambda: (salvar_anotacoes(texto_anotacoes), anotacoes_window.destroy()))

# Função para selecionar a cor do fundo e ajustar o contraste
def selecionar_cor():
    global corFundo, corFonte, corEntry, corClara
    cor_selecionada = colorchooser.askcolor(title="Selecione a cor de fundo")[1]
    if cor_selecionada:
        corFundo = cor_selecionada
        corFonte = "white" if sum(int(cor_selecionada[i:i+2], 16) for i in (1, 3, 5)) < 382 else "black"
        corEntry = "#4f4f4f" if corFonte == "white" else "#f0f0f0"
        corClara = corFonte
        atualizar_tema()

# Função para atualizar o tema de acordo
def atualizar_tema():
    elementos = [
        (janela, 'bg'), (frame_ramal, 'bg'), (label_ramal, 'bg'),
        (label_ramal, 'fg'), (entry_ramal, 'bg'), (entry_ramal, 'fg'),
        (label_contador, 'bg'), (label_contador, 'fg'), (frame_leads, 'bg'),
        (label_leads, 'bg'), (label_leads, 'fg'), (entry_leads, 'bg'),
        (entry_leads, 'fg'), (frame_reunioes, 'bg'), (label_reunioes, 'bg'),
        (label_reunioes, 'fg'), (entry_reunioes, 'bg'), (entry_reunioes, 'fg'),
        (frame_tema_cor, 'bg'),  
        (frame_ligacoes, 'bg'),  
        (frame_icones, 'bg'), (icone_github, 'bg'),(icone_linkedin, 'bg'),
    ]
    for elemento, atributo in elementos:
        if atributo == 'bg':
            elemento.config(bg=corFundo)
        elif atributo == 'fg':
            elemento.config(fg=corFonte)

# Função para incrementar +1 no número de leads
def adicionar_lead():
    global leads
    leads += 1
    entry_leads.delete(0, tk.END)
    entry_leads.insert(0, str(leads))
    salvar_contador()
    piscar_tela("#43b02a")
    x = botao_lead.winfo_rootx() - janela.winfo_rootx() + botao_lead.winfo_width() // 2
    y = botao_lead.winfo_rooty() - janela.winfo_rooty() + botao_lead.winfo_height() // 2


# Função para incrementar +1 no número de reuniões
def adicionar_reuniao():
    global reunioes
    reunioes += 1
    entry_reunioes.delete(0, tk.END)
    entry_reunioes.insert(0, str(reunioes))
    salvar_contador()
    piscar_tela("#43b02a")


# Função para piscar a tela com uma transição suave
def piscar_tela(cor_temporaria):
    cor_atual = janela.cget("bg")
    janela.configure(bg=cor_temporaria)
    janela.after(300, lambda: janela.configure(bg="#2d6f1e"))
    janela.after(450, lambda: janela.configure(bg="#215416"))
    janela.after(500, lambda: janela.configure(bg="#1f3f1f"))
    janela.after(600, lambda: janela.configure(bg="#172e16"))
    janela.after(700, lambda: janela.configure(bg=cor_atual))

# Função para contar ligações
def contar_ligacao():
    global contador
    contador += 1
    label_contador.config(text=f"Ligações: {contador}")
    salvar_contador()


# Função para diminuir -1 nos leads
def diminuir_lead():
    global leads
    if leads > 0:  # Evitar valores negativos
        leads -= 1
        entry_leads.delete(0, tk.END)
        entry_leads.insert(0, str(leads))
        salvar_contador()

# Função para diminuir -1 reuinões, 
def diminuir_reuniao():
    global reunioes
    if reunioes > 0:  
        reunioes -= 1
        entry_reunioes.delete(0, tk.END)
        entry_reunioes.insert(0, str(reunioes))
        salvar_contador()

# Função para diminuir -1 no número de ligações, sem valor negativo*
def diminuir_ligacao():
    global contador
    if contador > 0: 
        contador -= 1
        label_contador.config(text=f"Ligações: {contador}")
        salvar_contador()

# Função para resetar o contador com confirmação
def resetar_contador():
    global contador, leads, reunioes
    resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja resetar o contador?")
    if resposta:  # Se o usuário confirmar
        contador = 0
        leads = 0
        reunioes = 0
        entry_leads.delete(0, tk.END)
        entry_leads.insert(0, str(leads))
        entry_reunioes.delete(0, tk.END)
        entry_reunioes.insert(0, str(reunioes))
        label_contador.config(text=f"Ligações: {contador}")
        salvar_contador(reset=True)
        piscar_tela("#940106")

# função abrir historico
def abrir_historico():
    if not os.path.exists(caminho_arquivo):
        messagebox.showinfo("Histórico", "Nenhum histórico encontrado.")
        return

    historico_window = tk.Toplevel(janela)
    historico_window.title("Histórico de Ligações")
    historico_window.geometry("400x300")
    historico_window.configure(bg=corFundo)

    texto_historico = scrolledtext.ScrolledText(historico_window, wrap=tk.WORD, width=50, height=15,
                                                font=("Arial", 12), bg=corEntry, fg=corClara)
    texto_historico.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    with open(caminho_arquivo, 'r') as f:
        texto_historico.insert(tk.END, f.read())
    texto_historico.config(state=tk.DISABLED)

# alterar o tema
def alternar_tema():
    global corFundo, corFonte, corEntry, corClara
    if corFundo == "#1f1f1f":  # Dark mode
        corFundo = "#f0f0f0"
        corFonte = "black"
        corEntry = "#ffffff"
        corClara = "black"
    else:  # Light mode
        corFundo = "#1f1f1f"
        corFonte = "white"
        corEntry = "#4f4f4f"
        corClara = "white"
    atualizar_tema()

# Função para abrir o GitHub
def abrir_github():
    webbrowser.open("https://github.com/bragateus")  #GitHub

# Função para abrir o LinkedIn
def abrir_linkedin():
    webbrowser.open("https://www.linkedin.com/in/mateus-braga-lima") 

# Configuração da janela principal
janela = tk.Tk()
janela.title("Contador de Ligações")
janela.geometry("180x340")
janela.configure(bg=corFundo)
janela.wm_attributes("-topmost", 1)


# Posicionamento canto da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
janela.geometry(f"+{largura_tela-180}+{altura_tela-450}")

# Funções para arrastar a janela
janela.bind("<ButtonPress-1>", lambda e: (setattr(janela, '_offset_x', e.x), setattr(janela, '_offset_y', e.y)))
janela.bind("<ButtonRelease-1>", lambda e: (delattr(janela, '_offset_x'), delattr(janela, '_offset_y')))
janela.bind("<B1-Motion>", lambda e: janela.geometry(
    f"+{janela.winfo_pointerx()-janela._offset_x}+{janela.winfo_pointery()-janela._offset_y}"))

# Carrega os valores iniciais
carregar_contador()

# ------------- Interface do app tkinter------------
frame_ramal = tk.Frame(janela, bg=corFundo)
frame_ramal.pack(pady=10)

label_ramal = tk.Label(frame_ramal, text="Ramal:", font=("Arial", 10), bg=corFundo, fg=corFonte)
label_ramal.pack(side=tk.LEFT, padx=5)

entry_ramal = tk.Entry(frame_ramal, font=("Arial", 12), width=4, bg=corEntry, fg=corClara)
entry_ramal.pack(side=tk.LEFT)

label_contador = tk.Label(janela, text=f"Ligações: {contador}", font=("Arial", 16), bg=corFundo, fg=corClara)
label_contador.pack(pady=5)

frame_leads = tk.Frame(janela, bg=corFundo)
frame_leads.pack(pady=5)

label_leads = tk.Label(frame_leads, text="Leads:", font=("Arial", 10), bg=corFundo, fg=corFonte)
label_leads.pack(side=tk.LEFT, padx=5)

entry_leads = tk.Entry(frame_leads, font=("Arial", 12), width=2, bg=corEntry, fg=corClara)
entry_leads.pack(side=tk.LEFT)
entry_leads.insert(0, str(leads))

botao_lead = tk.Button(frame_leads, text="+1", font=("Arial", 10), bg=corBotao, fg=corClara, command=lambda: adicionar_lead())
botao_lead.pack(side=tk.LEFT, padx=5)

botao_lead_menos = tk.Button(frame_leads, text="-1", font=("Arial", 10), bg=corBotaoMenos, fg=corClara, command=lambda: diminuir_lead())
botao_lead_menos.pack(side=tk.LEFT, padx=5)

frame_reunioes = tk.Frame(janela, bg=corFundo)
frame_reunioes.pack(pady=5)

label_reunioes = tk.Label(frame_reunioes, text="Reuniões:", font=("Arial", 10), bg=corFundo, fg=corFonte)
label_reunioes.pack(side=tk.LEFT, padx=5)

entry_reunioes = tk.Entry(frame_reunioes, font=("Arial", 12), width=2, bg=corEntry, fg=corClara)
entry_reunioes.pack(side=tk.LEFT)
entry_reunioes.insert(0, str(reunioes))

botao_reuniao = tk.Button(frame_reunioes, text="+1", font=("Arial", 10), bg=corBotao, fg=corClara, command=lambda: adicionar_reuniao())
botao_reuniao.pack(side=tk.LEFT, padx=5)

botao_reuniao_menos = tk.Button(frame_reunioes, text="-1", font=("Arial", 10), bg=corBotaoMenos, fg=corClara, command=lambda: diminuir_reuniao())
botao_reuniao_menos.pack(side=tk.LEFT, padx=5)

# Frame para os botões de ligação
frame_ligacoes = tk.Frame(janela, bg=corFundo)
frame_ligacoes.pack(pady=5)

# Botão para incrementar +1 ligação
botao_contar = tk.Button(frame_ligacoes, text="+1 Ligação", font=("Roboto", 11), bg=corBotao, fg=corClara, command=contar_ligacao)
botao_contar.pack(side=tk.LEFT, padx=5)

# Botão para decrementar -1 ligação
botao_ligacao_menos = tk.Button(frame_ligacoes, text="-1 Ligação", font=("Roboto", 11), bg=corBotaoMenos, fg=corClara, command=diminuir_ligacao)
botao_ligacao_menos.pack(side=tk.LEFT, padx=5)

botao_resetar = tk.Button(janela, text="Resetar Contador", font=("Roboto", 10), bg=corReset, fg=corClara, command=resetar_contador)
botao_resetar.pack(pady=5)

botao_historico = tk.Button(janela, text="Abrir Histórico", font=("Roboto", 10), bg=corBotao, fg=corClara, command=abrir_historico)
botao_historico.pack(pady=5)

botao_anotacoes = tk.Button(janela, text="Anotações", font=("Roboto", 10), bg=corBotao, fg=corClara, command=abrir_anotacoes)
botao_anotacoes.pack(pady=5)

# Frame para os botões de Tema e Selecionar Cor
frame_tema_cor = tk.Frame(janela, bg=corFundo)
frame_tema_cor.pack(pady=2)

botao_tema = tk.Button(frame_tema_cor, text="Tema", font=("Roboto", 8), bg=corBotao, fg=corClara, width=8, command=alternar_tema)
botao_tema.pack(side=tk.LEFT, padx=2)

botao_cor = tk.Button(frame_tema_cor, text="Cor", font=("Roboto", 8), bg=corBotao, fg=corClara, width=8, command=selecionar_cor)
botao_cor.pack(side=tk.LEFT, padx=2)

# Carregar as imagens dos ícones git e linkedin
icone_github_img = PhotoImage(file="src/github.png").subsample(25, 25)  # ajuste de escala
icone_linkedin_img = PhotoImage(file="src/linkedin.png").subsample(25, 25)  # escala x,y

# Frame para os ícones do GitHub e LinkedIn
frame_icones = tk.Frame(janela, bg=corFundo)
frame_icones.pack(side=tk.BOTTOM, pady=4)

# Ícone do GitHub
icone_github = tk.Label(frame_icones, text=" GitHub", font=("Roboto", 8), bg=corFundo, fg=corLinks, cursor="hand2",
                        image=icone_github_img, compound=tk.LEFT) 
icone_github.pack(side=tk.LEFT, padx=4)
icone_github.bind("<Button-1>", lambda e: abrir_github())

# Ícone do LinkedIn
icone_linkedin = tk.Label(frame_icones, text=" LinkedIn", font=("Roboto", 8), bg=corFundo, fg=corLinks, cursor="hand2",
                          image=icone_linkedin_img, compound=tk.LEFT) 
icone_linkedin.pack(side=tk.LEFT, padx=4)
icone_linkedin.bind("<Button-1>", lambda e: abrir_linkedin())

# Iniciar o App
janela.mainloop()
