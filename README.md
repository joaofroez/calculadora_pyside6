# Calculadora com PySide6

Uma calculadora de desktop simples e funcional desenvolvida em **Python** com a biblioteca **PySide6** para a interface gráfica.  
O projeto inclui funcionalidades básicas, potenciação e um histórico de operações interativo.

---

## ✨ Funcionalidades Principais

- **Operações básicas:** Realiza cálculos de adição, subtração, multiplicação e divisão.  
- **Potenciação:** Suporte para operações de exponenciação (`^`).  
- **Histórico Interativo:** Armazena as operações realizadas em um painel que pode ser aberto e fechado.  
  - Clicar em um item do histórico recupera o resultado e a expressão, permitindo continuar os cálculos a partir daquele ponto.  
- **Interface Gráfica:** Desenvolvida com PySide6, apresentando um design limpo e responsivo com um tema escuro moderno.  
- **Controle via Teclado:** Permite a inserção de números e operações diretamente pelo teclado, incluindo atalhos como:  
  - **Enter** → Resultado  
  - **Backspace** → Apagar  
  - **Esc** → Limpar a tela  

---

## 🚀 Tecnologias Utilizadas

- **Python 3.x**  
- **PySide6** – Biblioteca para a construção da interface gráfica (bindings oficiais do Qt para Python).  
- **QDarkStyle** – Para aplicação de um tema escuro elegante na aplicação.
---
# 📂 Estrutura do Projeto

O projeto está organizado nos seguintes arquivos principais para manter o código limpo e modular:

- **main.py**: Ponto de entrada da aplicação. Inicializa a janela principal e todos os componentes da interface.  
- **main_window.py**: Define a classe `MainWindow`, que é a janela principal da aplicação.  
- **display.py**: Contém a classe `Display`, que gerencia o visor da calculadora onde números e resultados são exibidos.  
- **buttons.py**: Define a lógica dos botões, a grade de botões (`ButtonsGrid`) com toda a lógica dos cálculos, e o botão que controla o histórico.  
- **history.py**: Implementa o painel de histórico (`HistoryFrame`) e a lista de operações (`HistoryList`) com seu respectivo modelo de dados.  
- **info.py**: Define o `QLabel` que exibe a expressão completa da operação atual acima do display principal.  
- **utils.py**: Funções utilitárias para validação de números, verificação de strings e formatação de expressões.  
- **variables.py**: Armazena constantes utilizadas no projeto, como tamanhos de fonte, cores e caminhos de arquivos.  
- **style.py**: Configura o tema (QSS) da aplicação, utilizando a biblioteca **qdarkstyle** e estilos customizados.  

---

# 🔮 Melhorias Futuras

- [ ] Adicionar mais operações matemáticas (raiz quadrada, porcentagem, etc.).  
- [ ] Implementar um sistema de temas (claro, escuro) com a opção de troca em tempo real.  
- [ ] Adicionar mais atalhos de teclado para todas as operações.  
- [ ] Melhorar o tratamento de números muito grandes ou pequenos (notação científica).  
- [ ] Empacotar a aplicação em um executável para facilitar a distribuição (usando **PyInstaller** ou **cx_Freeze**).  
