import logging
import socketserver

logger = logging.getLogger(__name__)

HOST = "0.0.0.0"
PORT = 50000
BUFFER = 4096


class TrughputServer(socketserver.BaseRequestHandler):
    """We simply send the data back to the sender!"""
    def handle(self):
        data = self.request.recv(BUFFER)
        self.request.sendall(data)

        logger.info(f"Recieved and returned data from {self.client_address[0]}")


if __name__ == "__main__":
    with socketserver.UDPServer((HOST, PORT), TrughputServer) as server:
        server.serve_forever()
