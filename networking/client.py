#fixed imports
from time import sleep
import socket, json, threading, sys, GameLogic, traceback


from bge import logic, events
import HASH.py


### THIS IS THE CLIENT ###


class Networking:
    def __init__(self):
        self.obj = logic.getCurrentController()
        self.owner = self.obj.owner
        print("Initializing network..")
        self.lastsent = ""
        self.role = "unknown"
        self.enemyrole = "unknown"
        self.playerdicts = []
        self.roomset = False
        self.enemyspawned = False
        self.stop = "µ"
        self.stoptrap = True # if true, don't send.
        self.scene = GameLogic.getCurrentScene()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        hostname = socket.gethostname()    
        self.ipaddr = socket.gethostbyname(hostname)
        self.s.connect((self.ipaddr, 5555))
        
        # hash
        nameUser = "marco!"
        hash_object = hashlib.sha256(nameUser.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        
        print("Connected to server")
        self.sender({"cmdTEST": nameUser})
        #self.sender({"cmdTEST": 'marco!'})
        print(self.sender({"cmd": 'nameUser'}))
        threading.Thread(target=self.listener).start()
        # get self object
        self.obj = self.scene.objects["Cube"]



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
            # filter bad dicts
            if "}{" in data:
                data = data.split("}{")[0] + "}"
                print("HAD TO FILTER")
            data = json.loads(data)
            keylist = list(data.keys())
            for key in keylist:
                if key == "role":
                    # hardcoding for test HARDCODED
                    self.role = data[key]

                    print("ROLE IS: " + self.role)
                    # link role to self
                    self.obj["role"] = self.role
                    # declare enemy role
                    if self.role == "attacker":
                        self.enemyrole = "defender"
                    else:
                        self.enemyrole = "attacker"

                    self.sender({"cmd": "search"})
                if key == "player": # get player dict
                    self.playerdicts.append(data[key])
                #if key == "move":
                #    name = data[key][0]
                #    keypress = data[key][1] # list looks like [str(name), str(keypress)]
                #    #self.move(keypress, )
                if key == "room":
                    #print("room")
                    portnumber = data[key]
                    #print("closing old socket!")

                    # totally different socket to avoid mixups
                    self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #print("Created new socket!")
                    self.s2.connect((self.ipaddr, portnumber))
                    print("connected to room")
                    #print(self.s2)
                    self.roomset = True # socket switch
                    # room init
                    message = {"roominit": self.role} # this is the playerobject for the server, so add name, role, whatevs. can be in it's own dict.(if so, change server)
                    try:
                        self.sender(message)
                    except Exception:
                        traceback.print_exc()

                    #self.move("w", self.obj)
                if key == "spawn":
                    print("got spawn request")
                    playerdict = data[key]

                    #print(playerdict) # {"attacker":{"name":"testplayer", "role":"attacker"}}
                    role = playerdict[self.enemyrole]["role"] # again, hardcoded.
                    name = playerdict[role]["name"]
                    if not self.enemyspawned:
                        self.scene.addObject("testplayer") # will be role/type in the future
                        enemyobj = self.scene.objects["testplayer"]
                        enemyobj["name"] = name
                        enemyobj["role"] = role
                        self.enemyspawned = True

                if key == "move":
                    print("got move request")
                    playerrole = data[key][0]
                    print("looking for" + playerrole)
                    directionkey = data[key][1]
                    obj = self.getobjectbyid(playerrole) # role is used as id here
                    self.move(directionkey, obj)
        except Exception:
            print("Processing error!")
            print(data)
            traceback.print_exc()


    def getobjectbyid(self, id):
        print("getting id")
        for object in self.scene.objects:

            try:
                if object["role"] == id:
                   return object
            except:
                pass

    def move(self, keypress, playerobject):
        # SPEEDS NEED TO BE TIMES 2 IF IT'S NOT YOURSELF. network crap I guess..
        print(playerobject)
        if keypress == "w":
            playerobject.applyMovement((0, 0.1, 0), True)
        if keypress == "a":
            playerobject.applyMovement((-0.1, 0, 0), True)
        if keypress == "s":
            playerobject.applyMovement((0, -0.1, 0), True)
        if keypress == "d":
            playerobject.applyMovement((0.1, 0, 0), True)
        if keypress == self.stoptrap:
            playerobject.applyMovement((0, 0, 0), True)

    def spawnobject(self):
        # needs a "player"dict containing name, type, spawnlocation, and if type=minion, a goal.
        pass

    def detectmovement(self):
        keyb = logic.keyboard
        wkey = logic.KX_INPUT_ACTIVE == keyb.events[events.WKEY]
        akey = logic.KX_INPUT_ACTIVE == keyb.events[events.AKEY]
        skey = logic.KX_INPUT_ACTIVE == keyb.events[events.SKEY]
        dkey = logic.KX_INPUT_ACTIVE == keyb.events[events.DKEY]
        if wkey:
            #          print("Sending w")
            self.sender({"keypress": "w", "role": self.role})
            self.stoptrap = False # now stop is allowed to be sent.
        if akey:
            #            print("Sending a")
            self.sender({"keypress": "a", "role": self.role})
            self.stoptrap = False  # now stop is allowed to be sent.
        if skey:
            self.sender({"keypress": "s", "role": self.role})
            self.stoptrap = False  # now stop is allowed to be sent.
        if dkey:
            # print("Sending d")
            self.sender({"keypress": "d", "role": self.role})
            self.stoptrap = False  # now stop is allowed to be sent.
        else:
            if not self.stoptrap:  # if not stoptrap, send. else(just used it), don't send.
                # print sending stoptrap
                self.sender({"keypress": self.stop, "role": self.role})
                self.stoptrap = True
        sleep(0.0001)

    def sender(self, message, role=""):
        print(message)
        if role != "":
            message["role"] = role
        else:
            message["role"] = self.role


        print("Trying to send", message)
        print(self.roomset)
        try:
            if self.roomset: # to switch to the second socket
                self.s2.send(bytes(json.dumps(message), "utf-8"))
                print(self.s2)
            elif not self.roomset:
                self.s.send(bytes(json.dumps(message), "utf-8"))
                print(self.s)

            print(self.s)

            print("sent message")
        except Exception as e:
            traceback.print_exc()
        except KeyboardInterrupt:
            #self.s.close()
            pass

networking = Networking()


def main():
    networking.detectmovement()

