import zmq
import random
from datetime import datetime
from time import sleep
import threading

def publish_time():
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://proxy:5555")
    sleep(0.5)
    
    while True:
        message = f"P1 {datetime.now().isoformat()}"
        print(f"P1 sending: {message}", flush=True)
        pub.send_string(message)
        sleep(1)
    
    pub.close()
    context.term()

def publish_random():
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.connect("tcp://proxy:5555")
    sleep(0.5)
    
    while True:
        number = random.randint(1, 6)
        message = f"P2 {number}"
        print(f"P2 sending: {message}", flush=True)
        pub.send_string(message)
        sleep(1)
    
    pub.close()
    context.term()

if __name__ == "__main__":
    t1 = threading.Thread(target=publish_time, daemon=True)
    t2 = threading.Thread(target=publish_random, daemon=True)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
