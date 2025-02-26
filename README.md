# **Projeto: Sistema de Análise de Sinais e Modulação AM**

Este projeto consiste em um sistema embarcado para controle e análise de sinais modulados em AM (Amplitude Modulada), com uma interface gráfica para visualização em tempo real. O sistema é composto por duas partes principais: o **sistema embarcado** (que roda em um microcontrolador) e a **interface gráfica** (que roda em um desktop).

---

## **Estrutura do Projeto**

### **Arquivos Necessários**
1. **Microcontrolador (Raspberry Pi Pico W)**:
   - `signal_analizer_1_2_1.py`: Código principal do sistema embarcado.
   - `ssd1306.py`: Biblioteca para controle do display OLED.
   - **MicroPython**: Deve estar instalado no microcontrolador.

2. **Desktop**:
   - `signal_analizer_1_2_2.py`: Código da interface gráfica.
   - **Python**: Deve estar instalado no desktop.

---

## **Instruções de Configuração**

### **1. Configuração do Microcontrolador**
1. **Instale o MicroPython**:
   - Siga as instruções oficiais para instalar o MicroPython na Raspberry Pi Pico W: [Instalação do MicroPython](https://micropython.org/download/rp2-pico/).

2. **Transfira os arquivos para o microcontrolador**:
   - Conecte a Raspberry Pi Pico W ao computador via USB.
   - Use uma ferramenta como o **Thonny IDE** para transferir os arquivos `signal_analizer_1_2_1.py` e `ssd1306.py` para o microcontrolador.
   - Certifique-se de que o arquivo `signal_analizer_1_2_1.py` seja renomeado para `main.py` para que seja executado automaticamente ao iniciar o microcontrolador.

3. **Conecte os periféricos**:
   - Conecte o display OLED, o joystick e os botões conforme descrito no código e na documentação do projeto.

4. **Execute o sistema embarcado**:
   - Reinicie o microcontrolador. O sistema embarcado deve iniciar automaticamente, exibindo os parâmetros no display OLED e aguardando conexão Wi-Fi.

---

### **2. Configuração da Interface Gráfica no Desktop**
1. **Instale o Python**:
   - Certifique-se de que o Python (versão 3.7 ou superior) está instalado no seu desktop. Você pode baixá-lo em: [Python.org](https://www.python.org/).

2. **Instale as dependências**:
   - Abra um terminal ou prompt de comando e instale as bibliotecas necessárias usando o comando:
     ```bash
     pip install numpy pyqtgraph
     ```

3. **Execute a interface gráfica**:
   - Navegue até o diretório onde o arquivo `signal_analizer_1_2_2.py` está localizado.
   - Execute o código com o comando:
     ```bash
     python signal_analizer_1_2_2.py
     ```

4. **Conecte-se ao sistema embarcado**:
   - Certifique-se de que o microcontrolador e o desktop estão na mesma rede Wi-Fi.
   - A interface gráfica se conectará automaticamente ao sistema embarcado via UDP e começará a exibir os gráficos em tempo real.

---

## **Funcionalidades**

### **Sistema Embarcado**
- Ajuste de parâmetros via joystick e botões:
  - Forma de onda (senoidal ou quadrada).
  - Frequência do sinal modulante.
  - Índice de modulação.
  - Fase e offset do sinal.
  - Frequência da portadora.
- Exibição dos parâmetros no display OLED.
- Transmissão dos parâmetros via Wi-Fi para a interface gráfica.

### **Interface Gráfica**
- Visualização em tempo real:
  - Sinal modulante e sua fase.
  - Espectro de frequência.
  - Sinal modulado AM e seu espectro.
- Organização dos gráficos em abas para fácil navegação.

---

## **Requisitos de Hardware**

### **Microcontrolador**
- Raspberry Pi Pico W.
- Display OLED 128x64 (comunicação I2C).
- Joystick analógico KY023.
- Dois botões para interação.
- Fonte de alimentação (pilha de lítio ou USB).

### **Desktop**
- Qualquer computador com Python instalado.
- Conexão Wi-Fi para comunicação com o microcontrolador.

---

## **Considerações Finais**

Este projeto foi desenvolvido com foco educacional, permitindo o estudo prático de modulação AM e conceitos de telecomunicações. A combinação de hardware acessível e software de código aberto torna essa solução replicável e adaptável a diferentes necessidades.

Para dúvidas ou sugestões, sinta-se à vontade para entrar em contato! 🚀  

**#Engenharia #Telecomunicações #Python #MicroPython #IoT #EducaçãoTecnológica #Projetos #Inovação**
