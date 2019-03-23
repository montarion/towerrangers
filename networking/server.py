import socket, random, json, threading
from time import sleep

class Server:
    def __init__(self):
        host = "localhost"
        port = 6000
        addr = (host, port)

        self.connectiondict = {}
        self.rolelist = ["attacker", "defender"]
        self.role = "empty"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.s.setblocking(False)
        self.s.bind(addr)
        self.s.listen(5000)
        self.processing = False



    def assign(self, conn):
        if len(self.connectiondict) != 1:
            # no one in it yet
            print("first to get assigned")
            print("choosing role")
            self.role = self.rolelist[random.randint(0,1)]
            self.connectiondict[self.role] = conn
        else:
            print("second to get assigned")
            if self.role == self.rolelist[0]:
                self.role = self.rolelist[1]
            else:
                self.role = self.rolelist[1]
        msg = {"role": self.role}
        print(self.role)
        self.sender(conn, msg)
        print("role chosen and sent")
        #conn.close()

    def listen(self):
        print("listening..")

        while True:
            print(self.processing)
            if not self.processing:
                self.conn, ipaddr = self.s.accept()
                print("accepted from " + str(ipaddr))
                self.processing = True
            print("listening for messages...")

            data = str(self.conn.recv(1024))[2:-1]
            print(data)
            self.process(data)


    def sender(self, conn, msg):
        try:
            conn.send(bytes(json.dumps(msg), "utf-8"))
        except Exception as e:
            print(e)


    def process(self, data):
        data = json.loads(data)
        keylist = list(data.keys())
        print(keylist)
        for key in keylist:
            if key == "cmd":
                if data[key] == "marco!":
                    print(data)
                    print("got new!")
                    self.assign(self.conn)
                    # matchmaking
                if data[key] == "search":
                    # send to room
                    portnumber = random.randint(60000, 65000)
                    msg = {"room": portnumber}
                    self.sender(self.conn, msg)
                    self.conn.close()
                    self.processing = False
                    threading.Thread(target=self.room, args=[portnumber]).start()
                    print("Thread started")
                    # spawn new listener and shit ( on new thread) DONE
                    # close this connection DONE
                    pass


    def room(self, portnumber):
        print("IN ROOM")
        host = "localhost"
        port = portnumber
        addr = (host, port)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(5)

        conn, ipaddr = s.accept()
        print("accepted from " + str(ipaddr))
        while True:
            print("waiting for keypresses")
            data = str(conn.recv(1024))[2:-1]
            data = json.loads(data)
            keylist = list(data.keys())
            print(keylist)
            for key in keylist:
                # check if ready
                if key == "keypress":
                    # keypress stuff, send to everyone and such
                    pass

Server().listen()