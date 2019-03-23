import socket, json, threading, sys, GameLogic
from time import sleep
from bge import logic, events



### THIS IS THE CLIENT ###


class Networking:
    def __init__(self):
        self.obj = logic.getCurrentController()
        print("Initializing network..")
        self.lastsent = ""
        self.role = "unknown"
        self.playerdicts = []
        self.scene = GameLogic.getCurrentScene()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect(('localhost', 6000))
        print("Connected to server")
        self.sender({"cmd": "marco!"})
        threading.Thread(target=self.listener).start()
        print(self.scene.objects)

    def listener(self):
        print("Started listener")
        while True:
            try:
                data = str(self.s.recv(1024))[2:-1]
                if data:
                    print("RECEIVED: " + str(data))
                    self.process(data)
            except Exception as e:
                print(e)
                #self.s.close()
                #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                #self.s.connect(('localhost', 6000))
                break

    def process(self, data):
        data = json.loads(data)
        keylist = list(data.keys())
        print(keylist)
        for key in keylist:
            if key == "role":
                self.role = data[key]
                self.s.connect(('localhost', 6000))
            if key == "player": # get player dict
                self.playerdicts.append(data[key])
            if key == "move":
                name = data[key][0]
                keypress = data[key][1] # list looks like [str(name), str(keypress)]

                #self.move(keypress, )
    def move(self, keypress, playerobject):
        if keypress == "w":
            playerobject.applyMovement((0, -0.1, 0), True)

    def detectmovement(self):
        keyb = logic.keyboard

        wkey = logic.KX_INPUT_ACTIVE == keyb.events[events.WKEY]
        akey = logic.KX_INPUT_ACTIVE == keyb.events[events.AKEY]
        skey = logic.KX_INPUT_ACTIVE == keyb.events[events.SKEY]
        dkey = logic.KX_INPUT_ACTIVE == keyb.events[events.DKEY]

        if wkey:
            #          print("Sending w")
            self.sender({"keypress": "w"})
        if akey:
            #            print("Sending a")
            self.sender({"keypress": "a"})
        if skey:
            self.sender({"keypress": "s"})
        if dkey:
            # print("Sending d")
            self.sender({"keypress": "d"})

    def sender(self, message):
        message["role"] = self.role
        if message != self.lastsent:
            print("Trying to send", message)
            try:
                self.s.send(bytes(json.dumps(message), "utf-8"))
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                self.s.close()
            self.lastsent = message


networking = Networking()


def main():
    networking.detectmovement()
