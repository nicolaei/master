# See https://svn.python.org/projects/python/trunk/Demo/sockets/throughput.py

# ! /usr/bin/env python

# Test network throughput.
#
# Usage:
# 1) on host_A: throughput -s [port]                    # start a server
# 2) on host_B: throughput -c  count host_A [port]      # start a client
#
# The server will service multiple clients until it is killed.
#
# The client performs one transfer of count*BUFSIZE bytes and
# measures the time it takes (roundtrip!).
import logging
import sys
import time
from socket import *

logger = logging.getLogger(__name__)

MY_PORT = 50000 + 42
BUFSIZE = 1024


def main():
    if len(sys.argv) < 2:
        usage()
    elif sys.argv[1] == "-s":
        server()
    elif sys.argv[1] == "-c":
        client()
    else:
        usage()


def usage():
    sys.stdout = sys.stderr

    logger.info("Usage:    (on host_A) throughput -s [port]")
    logger.info("and then: (on host_B) throughput -c count host_A [port]")

    sys.exit(2)




if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s"
    )
    main()
