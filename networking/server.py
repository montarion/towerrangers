import socket, random, json, threading, traceback
from time import sleep

class Server:
    def __init__(self):
        host = "localhost"
        port = 5555
        addr = (host, port)

        self.connectiondict = {}
        self.tempdict = {}
        self.roledict = {}
        self.rolelist = ["attacker", "defender"]
        self.role = "empty"

        self.roomdict = {1: [0, 60000]} # looks like {1: [0players/1player/2players, portnumber]}
        threading.Thread(target=self.room, args=[1, 60000]).start()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.s.setblocking(False)
        self.s.bind(addr)
        self.s.listen(50)
        self.processing = False



    def assign(self, conn):
        print(len(self.roledict))
        if len(self.roledict) != 1:
            # no one in it yet
            print("first to get assigned")
            self.role = self.rolelist[random.randint(0,1)]
            print("first role is: " + self.role)

            self.roledict[self.role] = [conn]
            self.connectiondict[self.role] = [conn]
        else:
            print("second to get assigned")
            print("second role is: " + self.role)
            if self.role == self.rolelist[0]:
                self.role = self.rolelist[1]
            else:
                self.role = self.rolelist[1]
            self.connectiondict[self.role] = [conn]
            # clear roles
            self.roledict = {}
        msg = {"role": self.role}

        self.sender(conn, msg)
        print("role chosen and sent")

        #conn.close()

    def listen(self):
        print("listening..")

        while True:
            if not self.processing:
                print("listening for messages...")
                self.conn, ipaddr = self.s.accept()
                print("MAIN: accepted from " + str(ipaddr))
                self.processing = True

            data = str(self.conn.recv(1024))[2:-1]

            if len(data) > 2:
                print("DATA IS: " + data)
                self.process(data)


    def sender(self, conn, msg):
        try:
            conn.sendall(bytes(json.dumps(msg), "utf-8"))
        except Exception as e:
            traceback.print_exc()

    def process(self, data):
        data = json.loads(data)
        keylist = list(data.keys())
        #print(keylist)
        for key in keylist:
            if key == "cmd":
                if data[key] == "marco!":
                    print("\n\n------------MARCO------------------\n\n")
                    print(data)
                    print("got new!")
                    self.assign(self.conn)
                    # matchmaking
                if data[key] == "search":
                    print("\n\n------------SEARCH------------------\n\n")

                    # send to room
                    for roomnumber in self.roomdict:
                        #print("ROOM NUMBER ON LINE 92 IS::: ")
                        #print(self.roomdict)
                        #print(roomnumber)
                        print("PEOPLE IN ROOM {}: {}".format(roomnumber, self.roomdict[roomnumber][0]))
                        if self.roomdict[roomnumber][0] == 0:
                            print("ADDING FIRST PERSON TO ROOM")
                            targetroom = roomnumber
                            portnumber = self.roomdict[roomnumber][1]
                            msg = {"room": portnumber}
                            self.sender(self.conn, msg)
                            print("sent room message")
                            self.roomdict[roomnumber][0] = 1
                            self.processing = False
                        elif self.roomdict[roomnumber][0] == 1:
                            print("ADDINMG SECOND PERSON TO ROOM")
                            targetroom = roomnumber
                            portnumber = self.roomdict[roomnumber][1]
                            msg = {"room": portnumber}
                            self.sender(self.conn, msg)
                            print("sent room message")


                            # make room full
                            self.roomdict[roomnumber][0] = 2
                            print("FILLED THE ROOM!")
                            #print(self.roomdict)
                            self.processing = True

                        elif self.roomdict[roomnumber][0] == 2:
                            print("soemthing went wrong I Think")
                            print(self.roomdict[roomnumber][0])

                            # make new room

                            # number of rooms is
                            numberOfRooms = len(self.roomdict)
                            print(numberOfRooms)
                            print("Creating new room with number: {}".format(numberOfRooms + 1))
                            portnumber = random.randint(60000, 65000)
                            msg = {"room": portnumber}
                            # because you can't add length to dictionaries while looping
                            self.tempdict[numberOfRooms + 1] = [1, portnumber]
                            threading.Thread(target=self.room, args=[numberOfRooms + 1, portnumber]).start()
                            #print("Thread started")
                            self.sender(self.conn, msg)
                            #self.conn.close()
                            self.processing = False

                        if len(self.tempdict) > 0:
                            self.roomdict = self.tempdict
                        print("ROOMDICT")
                        print(self.roomdict)

                    # spawn new listener and shit ( on new thread) DONE
                    # close this connection DONE
                    self.processing = False


    def room(self, roomnumber, portnumber):
        processing = False

        host = "localhost"
        port = portnumber
        addr = (host, port)
        roomfull = False
        roomconndict = {}

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)


        while True:
            print("\n\n------------ROOM--{}----------------\n\n".format(str(roomnumber)))
            #mechaniscm to make sure we always accept keypresses when full
            if roomfull:
                processing = True
            #print(self.connectiondict)
            #print("ROOMDICT IS: {}".format(self.roomdict[roomnumber]))
            #print(self.roomdict[roomnumber])
            #print("roomdict number is {}".format(self.roomdict[roomnumber][0]))

            #print(self.roomdict)
            #print(processing)
            if not processing:
                print("ROOM: accepting...")
                #print(self.roomdict)
                conn, ipaddr = s.accept()
                print("THREAD: accepted from " + str(ipaddr))

                processing = True
            else:
                if self.roomdict[roomnumber][0] != 2:
                    print(self.roomdict[roomnumber])
                    print("Waiting for other player...")
                    #processing = False
                if self.roomdict[roomnumber][0] == 2:
                    print("THREAD: ROOM {} IS FULL".format(roomnumber))
                    #processing = True
                    roomfull = True

                print("waiting for keypresses")
                data = str(conn.recv(1024))[2:-1]
                data = json.loads(data)
                keylist = list(data.keys())
                print(keylist)
                for key in keylist:
                    # check if ready
                    if key == "roominit":
                        print("ROOMINIT: {}".format(data[key]))
                        if not data["role"] in roomconndict:
                            roomconndict[data["role"]] = conn
                        # spawn other units already there
                        playerobject = {"name": "testplayer"}
                        msg = {"spawn": playerobject} # {"spawn": {playerobject}}
                        self.sender(conn, msg)
                        #processing = False
                        processing = True
                    if key == "keypress":
                        directionkey = data[key]
                        print(directionkey)
                        msg = {"move": [data["role"], directionkey]}

                        for player in roomconndict: # {"attacker": <socket>}
                            self.sender(roomconndict[player], msg)
                        # keypress stuff, send to everyone and such

                #processing = False
Server().listen()