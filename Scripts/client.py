import socket

HEADER = 64
class Client :
    def __init__(self) :
        """Setup socket connection."""
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = None
        self.connected = False

    def start_socket(self,server_ip:str) :
        self.SERVER = server_ip
        print(f"code showing in client side is {self.SERVER}")
        self.ADDR = (self.SERVER, self.PORT)
        print(f"address is {self.ADDR}")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            self.client.connect(self.ADDR)
            self.connected = True
            print("Connection Established with Server")
        except Exception as exception :
            print(exception)
            self.connected = False
            print("Connection Failed")
        return self.connected

    def send(self,msg:str):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def recieve(self) :
        re_msg = self.client.recv(5000).decode(self.FORMAT)
        return(re_msg)

    def end_conn(self) :
        Client.send(self,self.DISCONNECT_MESSAGE)
        print("[Connection Terminated]")

if __name__ == "__main__" :
    client = Client()
    client.start_socket("192.168.56.1")