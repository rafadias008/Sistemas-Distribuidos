import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://broker:5555")

commands = [
    "ADD:Comprar leite",
    "ADD:Estudar Python",
    "ADD:Enviar relatório",
    "ADD:Fazer o jogo do Fagner",
    "LIST",
    "REMOVE:1",
    "LIST",
    "REMOVE:0",
    "LIST"
]

for cmd in commands:
    print(f"Enviando: {cmd}")
    socket.send_string(cmd)
    mensagem = socket.recv_string()
    print(f"Resposta: {mensagem}")
    time.sleep(0.2)

print("Fim das tarefas.")
