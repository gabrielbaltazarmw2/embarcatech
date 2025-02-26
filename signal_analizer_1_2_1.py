import network
import socket
import time
from machine import Pin, ADC, I2C, SoftI2C
from ssd1306 import SSD1306_I2C
import sys

# 📡 Configuração Wi-Fi
SSID = "VIVOFIBRA-8378"      # Substitua pelo seu Wi-Fi
PASSWORD = "banda365"        # Substitua pela senha do Wi-Fi
UDP_IP = "192.168.15.171"    # IP do servidor que receberá os parâmetros
UDP_PORT = 5005              # Porta do servidor

# 🎛 Configuração do display OLED
OLED_WIDTH = 128
OLED_HEIGHT = 64
I2C_SDA = Pin(14)
I2C_SCL = Pin(15)

i2c = SoftI2C(sda=I2C_SDA, scl=I2C_SCL, freq=400000)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

# 🎮 Configuração do joystick
VRX_PIN = 27  # Eixo X para ajuste dos parâmetros
VRY_PIN = 26  # (Não utilizado neste exemplo)
vrx = ADC(Pin(VRX_PIN))

# 🎛 Configuração dos botões
BOTAO_A = Pin(5, Pin.IN, Pin.PULL_UP)  # Botão A para alternar o parâmetro ativo
BOTAO_B = Pin(6, Pin.IN, Pin.PULL_UP)  # Botão B para alternar o modo (sinal/portadora)

# 🔢 Parâmetros iniciais
forma_onda = "senoidal"  # "senoidal" ou "quadrada"
freq_sinal = 1           # Frequência do sinal
i_mod = 1.0              # Índice de modulação
fase_sinal = 0           # Fase do sinal (em graus)
offset_sinal = 0         # Offset do sinal
freq_portadora = 50      # Frequência da portadora

# 🔢 Limites dos parâmetros
min_freq = 1
max_freq = 50
min_i_mod = 0.1
max_i_mod = 5.0
min_fase = 0
max_fase = 360
min_offset = 0.0
max_offset = 5.0
min_portadora = 1
max_portadora = 200

# Variáveis para armazenar os valores anteriores (para envio apenas se houver mudanças)
forma_onda_anterior = forma_onda
freq_sinal_anterior = freq_sinal
i_mod_anterior = i_mod
fase_sinal_anterior = fase_sinal
offset_sinal_anterior = offset_sinal
freq_portadora_anterior = freq_portadora

# Variáveis de controle de estado
modo_variavel = "sinal"  # "sinal" ou "portadora"
parametro_atual = "forma"  # Inicia selecionando a forma de onda

# 📟 Função para atualizar o display OLED
def atualizar_display():
    oled.fill(0)
    if modo_variavel == "sinal":
        # Exibe os parâmetros do sinal
        oled.text("Sinal: {}".format(forma_onda), 0, 0)
        oled.text("Freq: {} Hz".format(freq_sinal), 0, 10)
        oled.text("i_mod: {:.1f}".format(i_mod), 0, 20)
        oled.text("Fase: {} deg".format(fase_sinal), 0, 30)
        oled.text("Offset: {:.1f}".format(offset_sinal), 0, 40)
        oled.text("-> {}".format(parametro_atual), 0, 50)
    else:
        # Exibe somente o parâmetro da portadora
        oled.text("Portadora:", 0, 20)
        oled.text("{} Hz".format(freq_portadora), 0, 30)
    oled.show()

# 📡 Função para enviar parâmetros via Wi-Fi
def enviar_parametros():
    mensagem = "{},{},{:.1f},{},{:.1f},{}".format(forma_onda, freq_sinal, i_mod, fase_sinal, offset_sinal, freq_portadora)
    sock.sendto(mensagem.encode(), (UDP_IP, UDP_PORT))
    print("Parâmetros enviados:", mensagem)

# 🏁 Função para conectar ao Wi-Fi
def conectar_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    print("Conectando ao Wi-Fi...")
    while not wifi.isconnected():
        time.sleep(1)
    print("Conectado! IP:", wifi.ifconfig()[0])
    return wifi

# 🏁 Função para inicializar o display com mensagem
def inicializar_display(mensagem):
    oled.fill(0)
    oled.text(mensagem, 0, 20)
    oled.show()

# 🏁 Função para alternar o parâmetro ativo
def alternar_parametro():
    global parametro_atual
    if modo_variavel == "sinal":
        if parametro_atual == "forma":
            parametro_atual = "frequencia"
        elif parametro_atual == "frequencia":
            parametro_atual = "i_mod"
        elif parametro_atual == "i_mod":
            parametro_atual = "fase"
        elif parametro_atual == "fase":
            parametro_atual = "offset"
        else:
            parametro_atual = "forma"
        atualizar_display()

# 🏁 Função para alternar o modo (sinal/portadora)
def alternar_modo():
    global modo_variavel
    if modo_variavel == "sinal":
        modo_variavel = "portadora"
    else:
        modo_variavel = "sinal"
    atualizar_display()

# 🏁 Função para ajustar parâmetros com o joystick
def ajustar_parametros(valor_x):
    global forma_onda, freq_sinal, i_mod, fase_sinal, offset_sinal, freq_portadora
    if modo_variavel == "sinal":
        if parametro_atual == "forma":
            if valor_x > 45000:
                forma_onda = "quadrada" if forma_onda == "senoidal" else "senoidal"
                time.sleep(0.3)
        elif parametro_atual == "frequencia":
            if valor_x > 45000 and freq_sinal < max_freq:
                freq_sinal += 1
            elif valor_x < 20000 and freq_sinal > min_freq:
                freq_sinal -= 1
        elif parametro_atual == "i_mod":
            if valor_x > 45000 and i_mod < max_i_mod:
                i_mod += 0.1
                time.sleep(0.25)
            elif valor_x < 20000 and i_mod > min_i_mod:
                i_mod -= 0.1
                time.sleep(0.25)
        elif parametro_atual == "fase":
            if valor_x > 45000 and fase_sinal < max_fase:
                fase_sinal += 1
            elif valor_x < 20000 and fase_sinal > min_fase:
                fase_sinal -= 1
        elif parametro_atual == "offset":
            if valor_x > 45000 and offset_sinal < max_offset:
                offset_sinal += 0.1
                time.sleep(0.25)
            elif valor_x < 20000 and offset_sinal > min_offset:
                offset_sinal -= 0.1
                time.sleep(0.25)
    else:
        if valor_x > 45000 and freq_portadora < max_portadora:
            freq_portadora += 1
        elif valor_x < 20000 and freq_portadora > min_portadora:
            freq_portadora -= 1

# 🏁 Função para verificar e enviar mudanças
def verificar_e_enviar_mudancas():
    global forma_onda_anterior, freq_sinal_anterior, i_mod_anterior, fase_sinal_anterior, offset_sinal_anterior, freq_portadora_anterior
    if (forma_onda != forma_onda_anterior or freq_sinal != freq_sinal_anterior or 
        i_mod != i_mod_anterior or fase_sinal != fase_sinal_anterior or 
        offset_sinal != offset_sinal_anterior or freq_portadora != freq_portadora_anterior):
        atualizar_display()
        enviar_parametros()
        forma_onda_anterior = forma_onda
        freq_sinal_anterior = freq_sinal
        i_mod_anterior = i_mod
        fase_sinal_anterior = fase_sinal
        offset_sinal_anterior = offset_sinal
        freq_portadora_anterior = freq_portadora

# 🏁 Inicialização do display com "Conectando..."
inicializar_display("Conectando...")

# 📡 Conectar ao Wi-Fi
wifi = conectar_wifi()

# Atualiza o display com "Wifi Conectado"
inicializar_display("Wifi Conectado")
time.sleep(2)

# 🔌 Configuração do socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 🏁 Loop principal
while True:
    # Verifica se o botão A foi pressionado para alternar o parâmetro ativo
    if BOTAO_A.value() == 0:
        alternar_parametro()
        time.sleep(0.5)  # Debounce

    # Verifica se o botão B foi pressionado para alternar entre os modos
    if BOTAO_B.value() == 0:
        alternar_modo()
        time.sleep(0.5)  # Debounce

    # Leitura do joystick (eixo X)
    valor_x = vrx.read_u16()

    # Ajusta os parâmetros com base no joystick
    ajustar_parametros(valor_x)

    # Verifica se houve mudança e envia os parâmetros
    verificar_e_enviar_mudancas()

    time.sleep(0.001)

