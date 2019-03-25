import socket, random, json


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
        self.s.bind(addr)
        self.s.listen(5000)


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
        self.sender(conn, msg)
        print("role chosen and sent")
        conn.close()
    def listen(self):

        while True:
            print("listening..")
            self.conn, ipaddr = self.s.accept()
            print("accepted from " + str(ipaddr))
            data = str(self.conn.recv(1024))[2:-1]
            print(data)
            self.process(data)

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
            if key == "keypress":
                # keypress stuff, send to everyone and such
                pass


    def sender(self, conn, message):
        conn.sendall(bytes(json.dumps(message), encoding="utf-8"))


Server().listen()
