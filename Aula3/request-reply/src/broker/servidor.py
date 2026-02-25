import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://broker:5556")

tasks = []

while True:
    msg = socket.recv_string()
    print(f"Mensagem recebida: {msg}", flush=True)
    cmd, sep, rest = msg.partition(":")
    cmd = cmd.strip().upper()

    if cmd == "ADD" and sep:
        task = rest.strip()
        tasks.append(task)
        resp = f"OK ADDED {len(tasks)-1}"
    elif cmd == "REMOVE" and sep:
        arg = rest.strip()
        if arg.isdigit():
            idx = int(arg)
            if 0 <= idx < len(tasks):
                removed = tasks.pop(idx)
                resp = f"OK REMOVED {removed}"
            else:
                resp = "ERROR index out of range"
        else:
            try:
                tasks.remove(arg)
                resp = f"OK REMOVED {arg}"
            except ValueError:
                resp = "ERROR task not found"
    elif cmd == "LIST":
        if tasks:
            lines = [f"{i}: {t}" for i, t in enumerate(tasks)]
            resp = "\n".join(lines)
        else:
            resp = "EMPTY"
    else:
        resp = "ERROR unknown command"

    socket.send_string(resp)

