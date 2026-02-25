import zmq
import threading

def subscribe_time():
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.setsockopt_string(zmq.SUBSCRIBE, "P1")
    sub.connect("tcp://proxy:5556")
    
    print("Subscriber(Time) connected and subscribed to P1", flush=True)
    while True:
        message = sub.recv_string()
        print(f"Subscriber(Time) received: {message}", flush=True)
    
    sub.close()
    context.term()

def subscribe_random():
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.setsockopt_string(zmq.SUBSCRIBE, "P2")
    sub.connect("tcp://proxy:5556")
    
    print("Subscriber(Random) connected and subscribed to P2", flush=True)
    while True:
        message = sub.recv_string()
        print(f"Subscriber(Random) received: {message}", flush=True)
    
    sub.close()
    context.term()

def subscribe_both():
    context = zmq.Context()
    sub = context.socket(zmq.SUB)
    sub.setsockopt_string(zmq.SUBSCRIBE, "P1")
    sub.setsockopt_string(zmq.SUBSCRIBE, "P2")
    sub.connect("tcp://proxy:5556")
    
    print("Subscriber(Both) connected and subscribed to P1 and P2", flush=True)
    while True:
        message = sub.recv_string()
        print(f"Subscriber(Both) received: {message}", flush=True)
    
    sub.close()
    context.term()

if __name__ == "__main__":
    t1 = threading.Thread(target=subscribe_time, daemon=True)
    t2 = threading.Thread(target=subscribe_random, daemon=True)
    t3 = threading.Thread(target=subscribe_both, daemon=True)
    
    t1.start()
    t2.start()
    t3.start()
    
    t1.join()
    t2.join()
    t3.join()
