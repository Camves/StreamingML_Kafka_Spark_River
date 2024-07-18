import sys
import subprocess

arquivos = ['teste_river\kafka_carregar_dados.py', 'teste_river\streaming_learning.py']
processos = []

for arquivo in arquivos:
    processo = subprocess.Popen([sys.executable, arquivo])
    processos.append(processo)

for processo in processos:
    processo.wait()