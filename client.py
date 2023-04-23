import sys
import socket
import random
import struct
import time

class Client:
    def __init__(self, server_addr, server_port):
        self.server_addr = server_addr
        self.server_port = server_port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        

        self.initVariables()

    def startClient(self):
        self.sock.connect((self.server_addr, self.server_port))
        self.clientLogic()
        self.sock.close()

    # clientLogic fuggveny, ami a talalgatast csinalja a barkobabol
    def clientLogic(self):
        print(self.number_to_guess)
        print ('initial guess: min: {} max: {} guessed: {}'.format(self.min, self.max, self.number_to_guess))
        packer = struct.Struct("c i")
        equ = self.equality[random.randint(0, len(self.equality) - 2)]

        self.msg = packer.pack(equ.encode(), self.number_to_guess)
        self.sock.sendall(self.msg)

        self.msg = self.sock.recv(packer.size)
        self.pasrsed_msg = packer.unpack(self.msg)

        while self.pasrsed_msg[0].decode() != 'K' or self.pasrsed_msg[0].decode() != 'Y' or self.pasrsed_msg[0].decode() != 'V':
            if (self.pasrsed_msg[0].decode() == 'I' and equ == '<') or (self.pasrsed_msg[0].decode() == 'N' and equ == '>'):
                self.max = self.number_to_guess
                self.number_to_guess = random.randint(self.min, self.max)
                print ('min: {} max: {} guessed: {}'.format(self.min, self.max, self.number_to_guess))

                time.sleep(random.randint(1,5))
                self.sendMessage(self.number_to_guess, equ, packer)
                self.recieveMessage(packer)

            elif self.pasrsed_msg[0].decode() == 'I' and equ == '>' or (self.pasrsed_msg[0].decode() == 'N' and equ == '<'):
                self.min = self.number_to_guess
                self.number_to_guess = random.randint(self.min, self.max)
                print ('min: {} max: {} guessed: {}'.format(self.min, self.max, self.number_to_guess))

                time.sleep(random.randint(1,5))
                self.sendMessage(self.number_to_guess, equ, packer)
                self.recieveMessage(packer)

        print('kliens vege!')

    # helper fuggveny, hogy ne legyen kodismetlen uzenet kuldesnel
    def sendMessage (self, number_to_guess, equ, packer):
        equ = self.equality[random.randint(0, len(self.equality) - 2)]
        if self.max == self.min:
            equ = '='
        self.msg = packer.pack(equ.encode(), number_to_guess)
        self.sock.sendall(self.msg)

    # helper fuggveny, hogy ne legyen kodismetlen uzenet fogadasnal
    def recieveMessage(self, packer):
        self.msg = self.sock.recv(packer.size)
        self.pasrsed_msg = packer.unpack(self.msg)

    # osztaly valtozoinak inicializalasa
    def initVariables(self):
        self.min = 0
        self.max = 100
        self.number_to_guess = random.randint(0, 100)
        self.msg = ''
        self.pasrsed_msg = []
        self.equality = ["<", ">", "="]


        
client = Client(sys.argv[1], int(sys.argv[2]))
client.startClient()