#fixed imports
from time import sleep
import socket, json, threading, sys, GameLogic, traceback


from bge import logic, events



### THIS IS THE CLIENT ###


class Networking:
    def __init__(self):
        self.obj = logic.getCurrentController()
        self.owner = self.obj.owner
        print("Initializing network..")
        self.lastsent = ""
        self.role = "unknown"
        self.playerdicts = []
        self.roomset = False
        self.scene = GameLogic.getCurrentScene()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ipaddr = "localhost"
        self.s.connect((self.ipaddr, 5555))
        print("Connected to server")
        self.sender({"cmd": "marco!"})
        threading.Thread(target=self.listener).start()
        print(self.scene.objects)

    def listener(self):
        print("Started listener")
        while True:
            try:
                if self.roomset:
                    data = str(self.s2.recv(1024))[2:-1]
                else:
                    data = str(self.s.recv(1024))[2:-1]

                
                if data:
                    print("RECEIVED: " + str(data))
                    self.process(data)
            except Exception as e:
                traceback.print_exc()
                if self.roomset:
                    self.s2.close()
                else:
                    self.s.close()
                print("LISTENER ERROR")
                break

    def process(self, data):
        try:
            data = json.loads(data)
            keylist = list(data.keys())
            print("keylist" + str(keylist))
            for key in keylist:
                if key == "role":
                    self.role = data[key]
                    print("ROLE IS: " + self.role)
                    self.sender({"cmd": "search"})
                if key == "player": # get player dict
                    self.playerdicts.append(data[key])
                if key == "move":
                    name = data[key][0]
                    keypress = data[key][1] # list looks like [str(name), str(keypress)]
                    #self.move(keypress, )
                if key == "room":
                    print("room")
                    portnumber = data[key]
                    print("closing old socket!")
                    print(self.s)
                    #self.s.close()

                    #sleep(1)
                    # totally different socket to avoid mixups
                    self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    print("Created new socket!")
                    self.s2.connect((self.ipaddr, portnumber))
                    print("connected to room")
                    print(type(self.s2))
                    self.roomset = True # socket switch
                    # room init
                    message = {"roominit": self.role}
                    try:
                        self.sender(message)
                    except Exception:
                        traceback.print_exc()

                    #self.move("w", self.obj)
                if key == "spawn":
                    print("got spawn request")
                    playerdict = data[key]
                    print(playerdict)
                    self.scene.addObject("testplayer")
                if key == "move":
                    print("got move request")
                    playerrole = data[key][0]
                    directionkey = data[key][1]
                    obj = self.getobjectbyname(playerrole)
                    self.move(directionkey, obj)
        except Exception:
            print("Processing error!")
            print(data)
            traceback.print_exc()


    def getobjectbyname(self, object):
        obj = self.scene.objects["testplayer"] # needs to be attacker/defender/minion. figure out how to change object name dynamically
        return obj

    def move(self, keypress, playerobject):
        if keypress == "w":
            playerobject.applyMovement((0, 0.1, 0), True)
        if keypress == "a":
            playerobject.applyMovement((-0.1, 0, 0), True)
        if keypress == "s":
            playerobject.applyMovement((0, -0.1, 0), True)
        if keypress == "d":
            playerobject.applyMovement((0.1, 0, 0), True)


    def detectmovement(self):
        keyb = logic.keyboard
        wkey = logic.KX_INPUT_ACTIVE == keyb.events[events.WKEY]
        akey = logic.KX_INPUT_ACTIVE == keyb.events[events.AKEY]
        skey = logic.KX_INPUT_ACTIVE == keyb.events[events.SKEY]
        dkey = logic.KX_INPUT_ACTIVE == keyb.events[events.DKEY]
        if wkey:
            #          print("Sending w")
            self.sender({"keypress": "w", "role": self.role})
        if akey:
            #            print("Sending a")
            self.sender({"keypress": "a", "role": self.role})
        if skey:
            self.sender({"keypress": "s", "role": self.role})
        if dkey:
            # print("Sending d")
            self.sender({"keypress": "d", "role": self.role})
        sleep(0.0001)

    def sender(self, message):
        message["role"] = self.role
        if message != self.lastsent:
            print("Trying to send", message)
            try:
                if self.roomset: # to switch to the second socket
                    self.s2.send(bytes(json.dumps(message), "utf-8"))
                elif not self.roomset:
                    self.s.send(bytes(json.dumps(message), "utf-8"))
                #print(self.s)
                print("sent message")
            except Exception as e:
                traceback.print_exc()
            except KeyboardInterrupt:
                #self.s.close()
                pass
            #self.lastsent = message

networking = Networking()


def main():
    networking.detectmovement()
