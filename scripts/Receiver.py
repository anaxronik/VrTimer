import socket


class Receiver:
    def __init__(self):
        udp_port = 5678
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', udp_port))

        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
            print(sock)
        sock.close()

if __name__ == '__main__':
    Receiver()
