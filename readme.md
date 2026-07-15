# Simulador RISC-V Pipeline (GUI)

Este software é um simulador didático projetado para visualizar a execução de instruções da arquitetura RISC-V em um pipeline clássico de 5 estágios (IF, ID, EX, MEM, WB). A aplicação conta com uma interface gráfica (GUI) interativa para acompanhar o fluxo das instruções e o estado do processador a cada ciclo de clock.

---

## 👤 Autor e Informações
* **Autor:** Luiz Carlos da Silva Souza
* **Data:** Julho de 2025
* **Linguagem:** Python 3
* **Interface Gráfica:** Tkinter (GUI)

---

## 🛠️ Requisitos
O simulador foi desenvolvido utilizando apenas recursos nativos do Python, dispensando a instalação de bibliotecas complexas de terceiros:

* **Python 3.6** ou superior.
* **Tkinter** (já vem incluído por padrão na instalação do Python na maioria dos sistemas operacionais).

---

## 🚀 Como Executar

1. Abra o terminal na pasta raiz onde o projeto está salvo.
2. Execute os comandos:
  ```bash```
  ```python simulador_riscv.py```

3. A janela gráfica abrirá exibindo a interface com 3 botões principais de controle:
* **`Carregar .asm`** ➔ Abre a janela para selecionar o seu arquivo de código Assembly RISC-V (`.asm`).
* **`Próximo ciclo`** ➔ Avança manualmente um ciclo de clock do pipeline para acompanhar a evolução das instruções nos estágios.
* **`Abrir saida.out`** ➔ Abre o relatório de texto gerado com o histórico detalhado de toda a simulação.

---

## 📝 Formato dos Arquivos `.asm`

O arquivo de entrada deve conter instruções em formato texto (Assembly RISC-V), sendo aceita uma instrução por linha (comentários são permitidos utilizando a sintaxe padrão).

### Instruções Suportadas

| Tipo de Instrução | Operações Disponíveis |
| **Aritméticas** | `ADD`, `SUB`, `MUL`, `DIV`, `REM` |
| **Lógicas** | `AND`, `OR`, `XOR` |
| **Deslocamento** | `SLL`, `SRL` |
| **Imediatas** | `ADDI` |
| **Memória** | `LW`, `SW` |
| **Pseudo-instruções** | `NOP` |

### Exemplo de Código Válido

```assembly
ADDI x1, x0, 10
ADDI x2, x0, 20
ADD x3, x1, x2
SW x3, 0(x0)
LW x4, 0(x0)
```

---

## 📊 Arquivo de Saída (`saida.out`)

A cada ciclo de clock executado, o arquivo `saida.out` é atualizado automaticamente com as seguintes informações, organizadas por separadores para facilitar a leitura:

* O estágio atual de cada instrução dentro do pipeline de 5 estágios.
* O valor de todos os registradores internos (`x0` a `x31`).
* O mapa da memória RAM (mostrando apenas as posições modificadas/não zeradas).

---

## ⚠️ Observações Importantes

* **Registrador Zero (`x0`):** O registrador `x0` é rigidamente tratado como constante `0` (conforme a especificação da arquitetura RISC-V).
* **Divisão por Zero:** Operações de divisão por zero (`DIV` ou `REM` com divisor nulo) são tratadas para retornar `0` de forma segura, evitando falhas na execução.
* **Acessos à Memória:** Tentativas de acesso inválido ou fora dos limites da memória são ignoradas silenciosamente pelo simulador.
* **Hazards de Dados:** O simulador **não realiza a detecção automática de hazards de dados** (não implementa adiantamento ou bolhas automáticas). Para garantir o funcionamento correto e evitar inconsistências de dados, insira instruções `NOP` manualmente entre instruções dependentes.