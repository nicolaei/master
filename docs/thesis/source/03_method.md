Method
======

In this chapter I'll be talking about my methods for experiments and how I
implemented the experiments.

Setup
-----

To get my results I need to gather data. This data will be gathered via two
methods: A simulation setup and a real-world setup.

### Simulation

To test various use-cases I'll be using emulation to do rapid testing of
mechanism to check if they are viable. Ones a setup is deemed viable in my
simulation environment I will be moving on to the real-world setup with my
tasks.

The simulation's are done in a fork of the network-emulator Mininet called
Mininet-Wifi. This enables me to do tests in an environment that doesn't
require real world parts.

There are limitations to this approach that are important to be wary off
though, such as Mininet-Wifi's limited interference model[^interference], which 
is rather basic at the time of writing. This limitation means that some
results might be dramatically different from it's real world counterpart.

[^interference]: https://github.com/intrig-unicamp/mininet-wifi/issues/134

\todo{
    When actual tests are done, confirm the quote about results being
    dramatically different from the real world counterpart.
}


### Real-world

In the real-world setup I will be using Raspberry Pi's as both make-shift
clients and access points. These relatively inexpensive units have an onboard
WiFi chipset that will be used.

The Raspberry Pi's have the following specifications:

 - [ ] TODO: Get the Raspberry Pi's and their specifications.

This setup was tested and used in an isolated room at the norwegian defence
institute of technology.

\todo{
    Once tests are completed, make sure that this is correct.
}

Data points
-----------

During my tests, I've tried to gather the following data to verify the
effectiveness of my results:

- Client latency
- Client goodput
- Percent of access points discovered
- Speed of discovery

[^goodput]: Goodput is the application-level throughput.

These data points will help me figure out which methods are best fit for
discovering a high percentage of access points at a high speed, while still
letting clients utilize the network like normal.

\todo{
    Remember to add citations to articles for the resoning behind these
    datapoints.
}

### Client latency & client goodput

These datapoints will be used to measure how a given algorithm affects the
clients on the network. As [@ActiveScanPerformance] mentions, a large amount
of probe traffic can negatively impact the network's clients.

To summarize: These measurement points main objective is to make sure that our
chosen algorithm does not harm our networks performance too negatively.


### Percent of access points discovered & speed of discovery

While client latency and goodput from the chosen algorithms are important, it
is also very important to make sure that we're discovering as many access
points as possible and doing it as fast as possible.

Worth noting is that the faster we're doing the discovery, the less probe
requests will be occupying the network, and thus improving the client's latency.
