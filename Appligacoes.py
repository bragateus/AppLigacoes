import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import os

# Caminho para o arquivo onde o contador será salvo
diretorio_atual = os.path.dirname(os.path.realpath(__file__))
caminho_arquivo = os.path.join(diretorio_atual, 'historico_ligacoes.txt')

# Função para carregar os contadores e dados do arquivo
def carregar_contador():
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()
            dados = []
            for linha in linhas:
                dados.append(linha.strip())
            return dados
    else:
        return []

# Função para salvar os contadores e dados no arquivo
def salvar_contador(contador, leads, reunioes, ramal, reset=False):
    data_atual = datetime.now().strftime('%d-%m-%Y')
    hora_atual = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    ramal = entry_ramal.get()

    dados = carregar_contador()
    nova_entrada = f"---{data_atual}---"
    existe_data = False

    # Procurar se a data já existe no arquivo
    for i in range(len(dados)):
        if dados[i] == nova_entrada:
            existe_data = True
            dados[i + 1] = f"LA: {contador}"
            dados[i + 2] = f"L: {leads}"
            dados[i + 3] = f"R: {reunioes}"
            dados[i + 4] = f"Ramal: {ramal}"
            dados = dados[:i + 5]
            break

    # Se a data não existir, adiciona uma nova entrada
    if not existe_data:
        dados.append(nova_entrada)
        dados.append(f"LA: {contador}")
        dados.append(f"L: {leads}")
        dados.append(f"R: {reunioes}")
        dados.append(f"Ramal: {ramal}")
        dados.append("---Histórico de ligações do dia---")

    if not reset:
        dados.append(f"{hora_atual} - Ligações: {contador} - Leads: {leads} - Reuniões: {reunioes}")
    else:
        dados.append(f"{hora_atual} - Contador resetado")

    # Salva os dados atualizados no arquivo
    with open(caminho_arquivo, 'w') as f:
        for linha in dados:
            f.write(f"{linha}\n")

# Função para carregar os valores do histórico ao iniciar o programa
def carregar_valores_iniciais():
    global contador, leads, reunioes
    dados = carregar_contador()
    data_atual = datetime.now().strftime('%d-%m-%Y')
    for i in range(len(dados)):
        if dados[i] == f"---{data_atual}---":
            contador = int(dados[i + 1].split(":")[1].strip())
            leads = int(dados[i + 2].split(":")[1].strip())
            reunioes = int(dados[i + 3].split(":")[1].strip())
            
            break

# Função para incrementar o contador
def contar_ligacao():
    global contador, leads, reunioes
    contador += 1
    leads = int(entry_leads.get()) if entry_leads.get().isdigit() else 0
    reunioes = int(entry_reunioes.get()) if entry_reunioes.get().isdigit() else 0
    label_contador.config(text=f"Ligações: {contador}")
    salvar_contador(contador, leads, reunioes, entry_ramal.get())

# Função para resetar o contador
def resetar_contador():
    global contador, leads, reunioes
    resposta = messagebox.askyesno("Confirmar Reset", "Você realmente deseja resetar o contador?")
    if resposta:
        contador = 0
        leads = 0
        reunioes = 0
        label_contador.config(text=f"Ligações: {contador}")
        salvar_contador(contador, leads, reunioes, entry_ramal.get(), reset=True)

# Função para abrir o histórico em uma nova janela
def abrir_historico():
    historico_window = tk.Toplevel(janela)
    historico_window.title("Histórico de Ligações")
    historico_window.geometry("400x300")
    historico_window.configure(bg=corFundo)

    # Área de texto rolável para exibir o histórico
    texto_historico = scrolledtext.ScrolledText(historico_window, wrap=tk.WORD, width=50, height=15, font=("Arial", 12), bg=corEntry, fg=corClara)
    texto_historico.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    try:
        with open(caminho_arquivo, "r") as arquivo:
            historico = arquivo.read()
            texto_historico.insert(tk.END, historico)
    except FileNotFoundError:
        texto_historico.insert(tk.END, "Nenhum histórico encontrado.")

# Função para alternar entre dark mode e light mode
def alternar_tema():
    global corFundo, corEntry, corFonte, corClara, corBotao, corReset
    if corFundo == "#1f1f1f":  # Se estiver no modo escuro, muda para claro
        corFundo = "white"
        corEntry = "#f0f0f0"
        corFonte = "#0084d6"
        corClara = "black"
        corBotao = "#0084d6"
        corReset = "#ff4d4d"
    else:  # Se estiver no modo claro, muda para escuro
        corFundo = "#1f1f1f"
        corEntry = "#4f4f4f"
        corFonte = "#0084d6"
        corClara = "white"
        corBotao = "#0084d6"
        corReset = "#ff4d4d"

    # Aplicar as novas cores aos elementos da interface
    janela.configure(bg=corFundo)
    frame_ramal.configure(bg=corFundo)
    label_ramal.configure(bg=corFundo, fg=corFonte)
    entry_ramal.configure(bg=corEntry, fg=corClara)
    label_contador.configure(bg=corFundo, fg=corClara)
    frame_leads.configure(bg=corFundo)
    label_leads.configure(bg=corFundo, fg=corFonte)
    entry_leads.configure(bg=corEntry, fg=corClara)
    frame_reunioes.configure(bg=corFundo)
    label_reunioes.configure(bg=corFundo, fg=corFonte)
    entry_reunioes.configure(bg=corEntry, fg=corClara)
    botao_contar.configure(bg=corBotao, fg=corClara)
    botao_resetar.configure(bg=corReset, fg=corClara)
    botao_historico.configure(bg=corBotao, fg=corClara)
    botao_tema.configure(bg=corBotao, fg=corClara)

# Função para arrastar a janela
def iniciar_arrastar(event):
    janela._offset_x = event.x
    janela._offset_y = event.y

def parar_arrastar(event):
    del janela._offset_x
    del janela._offset_y

def arrastar_janela(event):
    x = janela.winfo_pointerx() - janela._offset_x
    y = janela.winfo_pointery() - janela._offset_y
    janela.geometry(f"+{x}+{y}")

# Inicialização da janela principal
janela = tk.Tk()
janela.title("Contador de Ligações")
janela.geometry("180x300")
janela.configure(bg="#1f1f1f")

# Configura a janela para ficar sempre no topo
janela.wm_attributes("-topmost", 1)

# Posiciona a janela no canto inferior direito da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
largura_janela = 180
altura_janela = 300
x = largura_tela - largura_janela
y = altura_tela - altura_janela
janela.geometry(f"+{x}+{y}")

# Permite arrastar a janela clicando no fundo branco
janela.bind("<ButtonPress-1>", iniciar_arrastar)
janela.bind("<ButtonRelease-1>", parar_arrastar)
janela.bind("<B1-Motion>", arrastar_janela)

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
corReset = "#ff4d4d"
corVerde = "#28b310"
corAzulClaro = "#bbcedc"

fonte_principal = ""

# Carregar valores iniciais do histórico
carregar_valores_iniciais()

# Frame para o campo do ramal
frame_ramal = tk.Frame(janela, bg=corFundo)
frame_ramal.pack(pady=10)

# Label e Entry para o número do ramal
label_ramal = tk.Label(frame_ramal, text="Ramal:", font=("Arial", 10), bg=corFundo, fg=corFonte)
label_ramal.pack(side=tk.LEFT, padx=5)

entry_ramal = tk.Entry(frame_ramal, font=("Arial", 12), width=4, bg=corEntry, fg=corClara)
entry_ramal.pack(side=tk.LEFT)

# Label para mostrar o contador
label_contador = tk.Label(janela, text=f"Ligações: {contador}", font=("Arial", 16), bg=corFundo, fg=corClara)
label_contador.pack(pady=5)

# Frame para Leads
frame_leads = tk.Frame(janela, bg=corFundo)
frame_leads.pack(pady=5)

# Frame para Reuniões
frame_reunioes = tk.Frame(janela, bg=corFundo)
frame_reunioes.pack(pady=5)

# Label e Entry para Leads
label_leads = tk.Label(frame_leads, text="Leads:", font=("Arial", 10), bg=corFundo, fg=corFonte)
label_leads.pack(side=tk.LEFT, padx=5)

entry_leads = tk.Entry(frame_leads, font=("Arial", 12), width=2, bg=corEntry, fg=corClara)
entry_leads.pack(side=tk.LEFT)
entry_leads.insert(0, str(leads))  # Carrega o valor inicial de leads

# Label e Entry para Reuniões
label_reunioes = tk.Label(frame_reunioes, text="Reuniões:", font=("Arial", 10), bg=corFundo, fg=corFonte)
label_reunioes.pack(side=tk.LEFT, padx=5)

entry_reunioes = tk.Entry(frame_reunioes, font=("Arial", 12), width=2, bg=corEntry, fg=corClara)
entry_reunioes.pack(side=tk.LEFT)
entry_reunioes.insert(0, str(reunioes))  # Carrega o valor inicial de reuniões

# Botão para contar ligações
botao_contar = tk.Button(janela, text="Ligação Feita", font=("Arial", 12), bg=corBotao, fg=corClara, command=contar_ligacao)
botao_contar.pack(pady=5)

# Botão para resetar o contador
botao_resetar = tk.Button(janela, text="Resetar Contador", font=("Arial", 10), bg=corReset, fg=corClara, command=resetar_contador)
botao_resetar.pack(pady=5)

# Botão para abrir o histórico
botao_historico = tk.Button(janela, text="Abrir Histórico", font=("Arial", 10), bg=corBotao, fg=corClara, command=abrir_historico)
botao_historico.pack(pady=5)

# Botão para alternar tema
botao_tema = tk.Button(janela, text="Tema", font=("Arial", 8), bg=corBotao, fg=corClara, command=alternar_tema)
botao_tema.pack(pady=2)

# Iniciar a interface gráfica
janela.mainloop()


