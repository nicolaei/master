FROM ciena/mininet:latest

# Mininet is looking for this controller, but Open vSwitch has changed how it
# packages it :(
RUN apt-get update \
    && apt-get install -y --no-install-recommends openvswitch-testcontroller \
    && ln /usr/bin/ovs-testcontroller /usr/bin/controller

COPY src /src

CMD ["/src/topology.py"]
