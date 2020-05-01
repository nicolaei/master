import logging
import socketserver

logger = logging.getLogger(__name__)

HOST = "0.0.0.0"
PORT = 50000


class TrughputServer(socketserver.BaseRequestHandler):
    """We simply send the data back to the sender!"""
    def handle(self):
        data = self.request[0]
        self.request[1].sendto(data, self.client_address)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )

    logger.info("Starting troughput server")
    with socketserver.UDPServer((HOST, PORT), TrughputServer) as server:
        logger.info("Waiting for requests...")
        server.serve_forever()
