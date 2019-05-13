# fixed imports
from time import sleep
import socket, json, threading, sys, GameLogic, traceback, hashlib, os

from bge import logic, events


# need to push 2 #


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
        self.stoptrap = True  # if true, don't send.
        self.scene = GameLogic.getCurrentScene()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ipaddr = "192.168.2.2"

        self.s.connect((self.ipaddr, 5555))

        print("Connected to server")
        self.sender({"cmd": "marco!"})
        threading.Thread(target=self.listener).start()
        # get self object

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
            datalist = []
            if "}{" in data:
                print("\n\n{}\n\n".format(data))
                data = data.split("}{")
                for d in data:
                    if d[0] != "{":
                        d = "{" + d
                    if d[-1] != "}":
                        d = d + "}"
                    if str(d).count("{") < str(d).count("}"):
                        d = "{" + d
                    elif str(d).count("{") > str(d).count("}"):
                        d = d + "}"

                    data = d
                    datalist.append(data)

                print("ROOM: HAD TO FILTER")
            else:
                datalist.append(data)

            for data in datalist:
                data = json.loads(data)
                print("data is: {}".format(data))
                keylist = list(data.keys())
                print(keylist)
                for key in keylist:
                    if key == "role":
                        # self.playobj = self.scene.objects["Cube"]
                        self.role = data[key]
                        # self.playobj = self.scene.objects["Player"]
                        print("ROLE IS: " + self.role)
                        # link role to self

                        if self.role == "defender":
                            print("adding defender")
                            self.scene.addObject("defenderPlayer", "defspawn")
                            self.playobj = self.scene.objects["defenderPlayer"]
                            self.playobj = self.scene.objects["defenderCamera"]
                            print("switching def cam")
                            self.scene.active_camera = self.scene.objects["defenderCamera"]
                        if self.role == "attacker":
                            print("adding attacker")
                            self.scene.addObject("attackerCamera", "attspawn")
                            self.scene.addObject("defenderPlayer", "defspawn")
                            self.scene.active_camera = self.scene.objects["attackerCamera"]
                            self.playobj = self.scene.objects["attackerCamera"]
                        self.playobj["role"] = self.role
                        # declare enemy role
                        if self.role == "attacker":
                            self.enemyrole = "defender"
                        else:
                            self.enemyrole = "attacker"

                        self.sender({"cmd": "search"})

                    if key == "player":  # get player dict
                        self.playerdicts.append(data[key])

                    if key == "room":
                        # print("room")
                        portnumber = data[key]
                        # print("closing old socket!")

                        # totally different socket to avoid mixups
                        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        # print("Created new socket!")
                        self.s2.connect((self.ipaddr, portnumber))
                        print("connected to room")
                        # print(self.s2)
                        self.roomset = True  # socket switch
                        # room init
                        roominitdict = {"role": self.role, "name": "{}Player".format(self.role)}
                        message = {
                            "roominit": roominitdict}  # this is the playerobject for the server, so add name, role, whatevs. can be in it's own dict.(if so, change server)
                        try:
                            self.sender(message)
                        except Exception:
                            traceback.print_exc()

                    if key == "spawn":  # this needs to be expanded for multiple types. DONE!
                        print("got spawn request")
                        print(data)
                        spawndict = data[key]  # msg
                        stypes = list(spawndict.keys())  # player/minion/tower

                        for stype in stypes:
                            print(stype)

                            # print(playerdict) # {'player': {"attacker": {'name': 'testplayer', 'role': 'attacker'}}
                            if stype == "attacker" or stype == "defender":
                                playerdict = spawndict[stype]
                                print("spawndict: " + str(playerdict))

                                print(self.role)
                                try:
                                    # playerdict = playerdict[self.enemyrole]
                                    print(playerdict)
                                    role = playerdict["role"]
                                    print("self is:" + self.role)
                                    name = playerdict["name"]
                                    print(self.enemyspawned)
                                    print(role != self.role)
                                    if not self.enemyspawned and role != self.role:
                                        print("Adding object!! \n\n---------\n\n")
                                        self.scene.addObject(
                                            name)  # will be role/type in the future # you can add a location (with findbyobject)
                                        enemyobj = self.scene.objects[name]

                                        enemyobj["name"] = name
                                        enemyobj["role"] = role
                                        self.enemyspawned = True
                                except Exception:
                                    traceback.print_exc()
                            if stype == "minion":
                                print("SPAWNING MINION")
                                miniondict = spawndict[stype]
                                location = miniondict["location"]  # e.g. "5"
                                miniontype = miniondict["name"]
                                print(miniontype, location)
                                self.scene.addObject(miniontype, location)

                    if key == "move":
                        print("got move request")
                        playerrole = data[key][0]
                        print("looking for" + playerrole)
                        directionkey = data[key][1]
                        obj = self.getobjectbyid(playerrole)  # role is used as id here
                        if obj != None:
                            self.move(directionkey, obj)
                        else:
                            print("couldn't find object. here is the list")

                    if key == "shooting":
                        life_time = 120
                        velocity = 15
                        arrow = self.scene.objectsInactive["Arrow"]
                        defender = self.scene.objects["defenderPlayer"]
                        new_arrow = self.scene.addObject(arrow, defender, life_time)
                        new_arrow.setLinearVelocity((0, velocity, 0), True)

        except Exception:
            print("Processing error!")
            print(data)
            traceback.print_exc()

    def getobjectbyid(self, id):
        print("getting id")
        for object in self.scene.objects:  # changed from objects to objectsInactive in a bid to increase performance

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
        mouse = logic.mouse
        wkey = logic.KX_INPUT_ACTIVE == keyb.events[events.WKEY]
        akey = logic.KX_INPUT_ACTIVE == keyb.events[events.AKEY]
        skey = logic.KX_INPUT_ACTIVE == keyb.events[events.SKEY]
        dkey = logic.KX_INPUT_ACTIVE == keyb.events[events.DKEY]
        mouseClick = logic.KX_INPUT_JUST_ACTIVATED == mouse.events[events.LEFTMOUSE]
        if wkey:
            #          print("Sending w")
            self.sender({"keypress": "w", "role": self.role})
            self.stoptrap = False  # now stop is allowed to be sent.
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
        if mouseClick:
            if self.role == "defender":
                self.sender({"shooting": "click", "role": self.role})
            self.stoptrap = False

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
            if self.roomset:  # to switch to the second socket
                self.s2.send(bytes(json.dumps(message), "utf-8"))
                # print(self.s2)
            elif not self.roomset:
                self.s.send(bytes(json.dumps(message), "utf-8"))
                # print(self.s)

            # print(self.s)

            print("sent message")
        except Exception as e:
            traceback.print_exc()
        except KeyboardInterrupt:
            # self.s.close()
            pass


networking = Networking()


def main():
    networking.detectmovement()
