import socket, random, json, threading
from time import sleep

class Server:
    def __init__(self):
        host = "localhost"
        port = 6000
        addr = (host, port)

        self.connectiondict = {}
        self.roledict = {}
        self.rolelist = ["attacker", "defender"]
        self.role = "empty"

        self.roomdict = {1: [0, 60000]} # looks like {1: [0players/1player/2players, portnumber]}
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
                print("accepted from " + str(ipaddr))
                self.processing = True

            data = str(self.conn.recv(1024))[2:-1]
            print("DATA IS: " + data)
            if len(data) > 2:
                self.process(data)


    def sender(self, conn, msg):
        try:
            conn.send(bytes(json.dumps(msg), "utf-8"))
        except Exception as e:
            print(e)


    def process(self, data):
        data = json.loads(data)
        keylist = list(data.keys())
        #print(keylist)
        for key in keylist:
            if key == "cmd":
                if data[key] == "marco!":
                    print(data)
                    print("got new!")
                    self.assign(self.conn)
                    # matchmaking
                if data[key] == "search":
                    print("IN SEARCH")
                    tempdict = {}
                    # send to room
                    print(self.roomdict)
                    for roomnumber in self.roomdict:
                        if self.roomdict[roomnumber][0] == 1:
                            #print(roomnumber)
                            targetroom = roomnumber
                            portnumber = self.roomdict[roomnumber][1]
                            msg = {"room": portnumber}
                            self.sender(self.conn, msg)
                            print("sent room message")

                            self.conn.close()
                            # make room full
                            self.roomdict[roomnumber][0] = 2
                            self.processing = False
                        elif self.roomdict[roomnumber][0] == 2:
                            self.processing = False
                            pass
                        else:
                            # make new room
                            print("Creating new room")
                            # number of rooms is
                            numberOfRooms = len(self.roomdict)
                            portnumber = random.randint(60000, 65000)
                            msg = {"room": portnumber}
                            # because you can't add length to dictionaries while looping
                            tempdict[numberOfRooms + 1] = [1, portnumber]
                            threading.Thread(target=self.room, args=[numberOfRooms + 1, portnumber]).start()
                            print("Thread started")
                            self.sender(self.conn, msg)
                            self.conn.close()
                            self.processing = False
                        self.roomdict = tempdict

                    # spawn new listener and shit ( on new thread) DONE
                    # close this connection DONE
                    pass


    def room(self, roomnumber, portnumber):
        processing = False
        print("IN ROOM: " + str(roomnumber))
        host = "localhost"
        port = portnumber
        addr = (host, port)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)


        print(self.connectiondict)
        while True:
            print(processing)
            if not processing:
                conn, ipaddr = s.accept()
                print("accepted from " + str(ipaddr))
                processing = True
            print("waiting for keypresses")
            data = str(conn.recv(1024))[2:-1]
            data = json.loads(data)
            keylist = list(data.keys())
            print(keylist)
            for key in keylist:
                # check if ready
                if key == "roominit":
                    print(data[key])
                    # spawn other units already there
                    playerobject = {"name": "testplayer"}
                    msg = {"spawn": playerobject} # {"spawn": {playerobject}}
                    self.sender(conn, msg)
                    processing = False
                if key == "keypress":
                    directionkey = data[key]
                    print(directionkey)
                    msg = {"move": directionkey}
                    self.sender(conn, msg)
                    # keypress stuff, send to everyone and such
                    pass
            #processing = False
Server().listen()