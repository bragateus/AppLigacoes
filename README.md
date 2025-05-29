# 📞 Contador de Ligações SDR

Um aplicativo simples pra equipes SDR (Sales Development Representatives) contarem e monitorarem suas ligações, leads e reuniões agendadas no dia-a-dia.

### Preview do App

![image](https://github.com/user-attachments/assets/59f4e1ac-dae2-402d-957e-6521e9a6b486)



## 🚀 Pra Que Serve?

- ✅ Contar todas as ligações feitas durante o dia
- ✅ Registrar leads qualificados
- ✅ Anotar reuniões agendadas
- ✅ Identificar ligações por ramal
- ✅ Histórico completo das atividades

## ⚙️ Como Instalar (Versão com o codigo_) 

1. Certifique-se que tem o Python instalado (versão 3.6 ou superior)
2. Baixe os arquivos do projeto
3. Instale as dependências:
```bash
pip install tkinter
```
## ⚙️ Como Instalar (Versão com Executável) 
1. Baixe o Arquivo compactado(.zip)
2. Extraia a pasta contida dentro.
3. Execute o Arquivo AppLigacões.exe

* O app demora um pouco para abrir, então assim que clicar para abirir esperar um pouco até a janela abrir no canto direito.

## 📲 Como Usar

1. **Configuração Inicial**:
   - Abra o app e digite seu ramal no campo indicado

2. **Durante as Ligações**:
   - Clique em "Ligação Feita" a cada chamada realizada
   - Atualize os campos de Leads e Reuniões quando conseguir

3. **Controles**:
   - `Resetar Contador`: Zera os números do dia (cuidado!).
   - `Abrir Histórico`: Visualiza todo seu histórico de ligações por dia.
   - `Tema`: Alterna entre modo claro e escuro.
   - `Cor`: Altera a cor do fundo da janela do app para uma cor personalizada.
   - `Anotações`: Abre uma janela para anotações, que fica sobreposta a outras janelas.

## 📊 O Que É Registrado

O app salva automaticamente:
- Data e hora de cada ligação
- Total de ligações por dia
- Leads qualificados
- Reuniões agendadas
- Ramal utilizado

Tudo organizado num arquivo `historico_ligacoes.txt` na mesma pasta do app.

## 💡 Dicas Pra Equipe SDR

1. Atualize os leads e reuniões imediatamente após conseguir
2. Use o histórico pra identificar seus melhores horários
3. Compare sua performance dia a dia
4. O ramal ajuda a identificar quem fez cada ligação

## 🛠️ Personalização

Você pode facilmente:
- Mudar as cores (editando as variáveis `corFundo`, `corBotao`, etc)
- Ajustar o tamanho da janela, arrastar para onde quiser da dela tela e sobreposição de janelas.
- Modificar o local onde o histórico é salvo

## 🚀 Melhorias Planejadas
 - Migrar para SQLite para persistência
 - Adicionar autenticação de usuário
 - Implementar relatórios gráficos
 - Adicionar exportação para Excel/CSV
 - ~Adicionar campo de escrita de observações~ ✅ 

## 🤝 Contribuição

Contribuições são bem-vindas! Só abrir um Pull Request.

---

Feito por Mateus Braga para Equipe de Vendas SDR - Mundivox
