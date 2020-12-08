import socket
import pickle

HEADER = 64
class Client :
    def __init__(self) :
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try :
            self.client.connect(self.ADDR)
            self.connected = True
        except :
            print("[WinError 10061] No connection could be made because the target machine actively refused it")
            self.connected = False

    def send(self,msg):
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

# if __name__ == "__main__" :
#     from Scripts.main_game import Game, GameData 

#     gd = GameData()
#     gd.savedata()
#     input()
#     print("reached")
#     gd.wipe_data()