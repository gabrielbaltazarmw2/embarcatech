import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
import socket

# Configuração do PyQtGraph
app = QtWidgets.QApplication([])

# Janela principal
win_main = QtWidgets.QMainWindow()
win_main.setWindowTitle('Sistema de Modulação AM')
win_main.resize(1200, 800)

# Widget central e layout de abas
central_widget = QtWidgets.QWidget()
win_main.setCentralWidget(central_widget)
layout = QtWidgets.QVBoxLayout(central_widget)

# Abas para organizar os gráficos
tab_widget = QtWidgets.QTabWidget()
layout.addWidget(tab_widget)

# Primeira aba: Sinal Modulante e Espectro
tab1 = QtWidgets.QWidget()
tab_widget.addTab(tab1, "Sinal Modulante e Espectro")
layout_tab1 = QtWidgets.QVBoxLayout(tab1)

# Gráfico do sinal original
plot_time = pg.PlotWidget(title="K + mx(t)")
curve_time = plot_time.plot(pen='y', name="Sinal Original")
layout_tab1.addWidget(plot_time)

# Adiciona um TextItem para exibir os parâmetros
display_text = pg.TextItem("", anchor=(0, 0))
display_text.setPos(0, 1)  # Posiciona no canto superior esquerdo do gráfico
plot_time.getPlotItem().addItem(display_text)

# Gráfico do espectro de frequência
plot_freq = pg.PlotWidget(title="Espectro de Frequência (FFT)")
curve_freq = plot_freq.plot(pen='c')
plot_freq.setXRange(0, 200)
layout_tab1.addWidget(plot_freq)

# Gráfico da fase do sinal
plot_fase = pg.PlotWidget(title="Fase do Sinal")
curve_phase = plot_fase.plot(pen='r', name="Fase do Sinal")
layout_tab1.addWidget(plot_fase)

# Segunda aba: Modulação AM
tab2 = QtWidgets.QWidget()
tab_widget.addTab(tab2, "Modulação AM")
layout_tab2 = QtWidgets.QVBoxLayout(tab2)

# Gráfico do sinal modulado no domínio do tempo
plot_am_time = pg.PlotWidget(title="Sinal Modulado no Domínio do Tempo")
curve_am_time = plot_am_time.plot(pen='y', name="Sinal Modulado")
layout_tab2.addWidget(plot_am_time)

# Gráfico do espectro da modulação AM
plot_am_freq = pg.PlotWidget(title="Espectro da Modulação AM")
curve_am_freq = plot_am_freq.plot(pen='m')
layout_tab2.addWidget(plot_am_freq)

# Configuração do socket UDP
UDP_IP = "0.0.0.0"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Parâmetros iniciais
forma_onda = "senoidal"  # "senoidal" ou "quadrada"
frequencia_atual = 1     # Hz (sinal modulante)
i_mod = 1.0              # Índice de modulação
teta = 0                 # Fase (em radianos)
offset = 0               # Offset do sinal
fc = 50                  # Hz (portadora)
fs = 400                 # Taxa de amostragem
N = 400                  # Número de pontos
tempo = np.linspace(0, 1, N)

modo_variavel = "sinal"  # "sinal" exibe os parâmetros do sinal; "portadora" exibe a portadora

# Função para gerar o sinal (senoidal ou quadrada)
def gerar_onda(tempo, frequencia, i_mod, teta, offset):
    if forma_onda == "senoidal":
        return offset + i_mod * np.cos(2 * np.pi * frequencia * tempo + teta)
    else:  # forma_onda == "quadrada"
        return offset + i_mod * np.sign(np.cos(2 * np.pi * frequencia * tempo + teta))

# Função para calcular a fase do sinal
def calcular_fase(tempo, frequencia, teta):
    return (2 * np.pi * frequencia * tempo + teta) % (2 * np.pi)

# Função para receber parâmetros via UDP (mensagem com 6 valores)
def receber_parametros():
    global forma_onda, frequencia_atual, i_mod, teta, offset, fc
    try:
        sock.settimeout(0.01)
        data, _ = sock.recvfrom(1024)
        dados = data.decode().strip().split(',')
        if len(dados) == 6:
            nova_forma = dados[0].strip()
            nova_freq_sinal = int(dados[1])
            novo_i_mod = float(dados[2])
            nova_fase = float(dados[3])
            novo_offset = float(dados[4])
            nova_freq_portadora = int(dados[5])
            if nova_forma in ["senoidal", "quadrada"]:
                forma_onda = nova_forma
            if 1 <= nova_freq_sinal <= 50:
                frequencia_atual = nova_freq_sinal
            if 0.1 <= novo_i_mod <= 5.0:
                i_mod = novo_i_mod
            if 0 <= nova_fase <= 360:
                teta = np.radians(nova_fase)
            if 0.0 <= novo_offset <= 5.0:
                offset = novo_offset
            if 1 <= nova_freq_portadora <= 200:
                fc = nova_freq_portadora
            print("Parâmetros recebidos: Forma = {}, Sinal = {} Hz, i_mod = {:.1f}, Fase = {}°, Offset = {:.1f}, Portadora = {} Hz".format(
                forma_onda, frequencia_atual, i_mod, nova_fase, offset, fc))
    except (socket.timeout, ValueError):
        pass

# Atualiza o "display" dos parâmetros sobreposto no gráfico
def atualizar_display():
    if modo_variavel == "sinal":
        texto = ("Sinal: {}\nFreq: {} Hz\n"
                 "i_mod: {:.1f}\nFase: {}°\nOffset: {:.1f}"
                ).format(forma_onda, frequencia_atual, i_mod, int(np.degrees(teta)) % 360, offset)
    else:
        texto = "Portadora: {} Hz".format(fc)
    display_text.setText(texto)

# Função para calcular a FFT
def calcular_fft(sinal):
    return np.abs(np.fft.fft(sinal))[:N//2] / N

# Função para atualizar os gráficos
def atualizar_graficos():
    global onda, fase_sinal
    receber_parametros()
    
    onda = gerar_onda(tempo, frequencia_atual, i_mod, teta, offset)
    fase_sinal = calcular_fase(tempo, frequencia_atual, teta)
    
    # Sinal modulado AM
    onda_modulada = onda * np.cos(2 * np.pi * fc * tempo)
    
    # Cálculo da FFT
    fft_sinal = calcular_fft(onda)
    fft_modulado = calcular_fft(onda_modulada)
    
    curve_time.setData(tempo, onda)
    curve_phase.setData(tempo, fase_sinal)
    curve_freq.setData(np.fft.fftfreq(N, d=1/fs)[:N//2], fft_sinal)
    curve_am_time.setData(tempo, onda_modulada)
    curve_am_freq.setData(np.fft.fftfreq(N, d=1/fs)[:N//2], fft_modulado)
    
    atualizar_display()

# Permite alternar o modo ("sinal" ou "portadora") ao pressionar a tecla B
def keyPressEvent(event):
    global modo_variavel
    if event.key() == QtCore.Qt.Key_B:
        modo_variavel = "portadora" if modo_variavel == "sinal" else "sinal"
        atualizar_display()

win_main.keyPressEvent = keyPressEvent

# Timer para atualização dos gráficos
timer = QtCore.QTimer()
timer.timeout.connect(atualizar_graficos)
timer.start(10)

# Exibe a janela principal
win_main.show()

if __name__ == '__main__':
    try:
        app.exec_()
    except KeyboardInterrupt:
        print("Encerrando...")