import sys
import socket
import struct
import select
import random


class Server:
    def __init__(self, server_addr, server_port):
        self.server_addr = server_addr
        self.server_port = server_port

        self.initVariables()
        self.initSocket(self.server_addr, self.server_port)

    def startServer(self):

        self.sock.listen(5)
        timeout = 1.0

        self.serverLogic(0, 0, timeout)
        # conn.close()
        self.sock.close()

    def serverLogic(self, conn, addr, timeout):
        packer = struct.Struct("c i")
        while True:
            try:

                if not self.is_number_guessed:
                    readables, _, _ = select.select(self.inputs, [], [], timeout)

                    for s in readables:
                        if s is self.sock:
                            connection, client_info = self.sock.accept()
                            # print("Csatlakozott valaki: {}:{}".format(*client_info))
                            self.inputs.append(connection)
                        else:
                            self.msg = s.recv(packer.size)
                            if not self.msg:
                                s.close()
                                # print("A kliens lezarta a kapcsolatot")
                                self.inputs.remove(s)
                                continue
    
                            self.parsed_msg = packer.unpack(self.msg)
                            # print(
                            #     "A kliens msg: {} {}".format(
                            #         self.parsed_msg[0].decode(), self.parsed_msg[1]
                            #     )
                            # )
                            
                            # print('guessed number: {}, parsed_msg: {}' .format(self.guessed_number, self.parsed_msg[1]))
                            # print(self.parsed_msg[0] == '=')
                            if self.parsed_msg[1] == self.guessed_number and self.parsed_msg[0].decode() == '=':
                                self.is_number_guessed = True
                                self.sendMessageToClient(0, 'Y', s, packer)
                                self.inputs.remove(s)
                            elif self.parsed_msg[1] != self.guessed_number and self.parsed_msg[0].decode() == '=':
                                self.sendMessageToClient(0, 'K', s, packer)
                            elif (self.parsed_msg[1] > self.guessed_number and self.parsed_msg[0].decode() == '<') or (self.parsed_msg[1] < self.guessed_number and self.parsed_msg[0].decode() == '>'):
                                self.sendMessageToClient(0, 'I', s, packer)
                            elif (self.parsed_msg[1] < self.guessed_number and self.parsed_msg[0].decode() == '<') or (self.parsed_msg[1] > self.guessed_number and self.parsed_msg[0].decode() == '>'):
                                self.sendMessageToClient(0, 'N', s, packer)

                else:
                    for s in self.inputs:
                        if s is not self.sock:
                            self.sendMessageToClient(0, 'V', s, packer)
                            s.close()
                            self.inputs.remove(s)

                    break

                for s in self.inputs:
                    if s.fileno() == -1:
                        self.inputs.remove(s)

            except KeyboardInterrupt:
                for s in self.inputs:
                    s.close()
                # print("Server closing")
                break

    def sendMessageToClient(self, number, char, s, packer):
        self.msg = packer.pack(char.encode(), number)
        s.sendall(self.msg)

    # osztaly valtozoinak inicializalasa
    def initVariables(self):
        self.guessed_number = random.randint(0, 100)
        self.msg = ''
        self.pasrsed_msg = []
        self.equality = ["<", ">", "="]
        self.is_number_guessed = False

    # socket valtozoinak inicializalasa
    def initSocket(self, server_addr, server_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((server_addr, server_port))
        self.inputs = [self.sock]
        self.sock.listen(5)


server = Server(sys.argv[1], int(sys.argv[2]))
server.startServer()
