Implementation
==============

Now we will take a look at the strategies and parameters that have been tested 
and how the these have been implemented in code and hardware. In addition to that 
we will be talking about difficulties that have risen from the implementation 
and during the execution of these experiments. 

Scanning Strategies
-------------------

\todo{Write an intro to this section!}

### Full Scan

As mentioned in the previous chapter, this approach will simply go through all
channels in one go. Meaning that we go from channel 1 to 12 without any breaks. 
This is how a typical scan works with most modern implementations.

The full scan results are used as a base-line test for comparisons.


### Selective Scanning

Two strategies will be tested for the selective channel approach.
As mentioned in the previous chapter, according to [@APDiscovery], some
percentage of adjacent channels will be discovered while in any given channels
due to channel overlapping.

 *  **Scanning channels 1, 6 and 11**: These are the only channels that don't
    overlap with each other in the normal 2.4 GHz space.
 
 *  **Scanning every alternating channel**: This means scanning channels 1, 3, 5,
    7, 9, and 11. If scanning every alternating channel is feasible, it might 
    halve our total scanning time seeing that the time to scan is proportional 
    to the amount of channels scanned [@SeamlessHandoff].


### Smooth Scanning

The smooth scanning implementation has been tested with static smooth scanning
parameters based on [@ProactiveScan] and [@PracticalSchemes]'s results. These 
articles showed that lower group size and higher intervals are beneficial for
latency and packet loss. Seeing that we are not dependent on a low time-to-scan,
the client's latency and goodput is prioritized. 

The following intervals will be tested, with 1 channel per group:

 * 300 miliseconds
 
 * 600 miliseconds
 
 * 1200 miliseconds
 

Scanning Parameters
-------------------

To make sure that results are as comparable as possible, the parameters have
been kept as static as possible between each test.

### Minimum number of scans

[@APDiscovery] discovered that to get the most accurate view of the local
topology, multiple scans are neccesary. To get a good view of the probability
of dicsovery for each scanning setup, the implementation will be scanning every
two minutes for a minimum of three hours. 

### Scanning triggers

As hinted at above the experiments will only be testing one trigger type, 
*clock based triggers*. It might be a worthwile endevor for future work to
investigate traffic based triggers and other triggers to find more optimal times 
to scan at.

It can also be argued that due to the low amount of traffic that the access points
will be experiencing (max two clients), the traffic based trigger might not make
a huge difference due to the low amount of clients.

Hardware and dependencies
-------------------------

To do the actual measurements, the tests will be using Raspberry Pi 4 Model B (4 GB) 
as make-shift access points and clients.

Both clients and the access points are using Raspian 10 (Buster), which are based
on the popular Linux distribution Debian (Buster).

All Raspberries were deployed at consistent locations in a area of approximately
50sqm. See figure {@fig:aplayout} for an aproximation on placement. In this 
figure the clients number corresponds to the access point it is connected to. 
There are no clients connected to AP 1.

![Layout of access points and clients during scans](static/ap_layout.png){ height=45% #fig:aplayout }

### Access Point Setup

The nodes that function as access points are using `hostapd` as the access point
software. This allows for easy-setup of everything from SSID to the selected channel.

For the sake of consistensy all access points have the same settings accross
all experiments. The selected channel was the one with the least assigned APs
in my area.


### Client Setup

Unlike the access points, the clients are using `wpa_supplicant` to connect to 
the access points. A single client never changes which access point it is 
connected to during any of the experiments, and the will not be scanning during
the experiments.


Measurements and collecting data
--------------------------------

To do the actual measurements, the following tools have been used:

 * `sockets` to collect data about how the client's connection is affected by 
   the scans that the access points are doing.
  
 * `iw` to conduct scans from the access points.
 
 * `python` to collect data from `sockets` and `iw`, as well as writing this 
   data to disk. All data is also timestamped to make it easier to spot the
   corralations between ping-spikes and the actuall scan (ping-spikes can happen
   unrelated to scans due to interference).

### Latency and goodput measurement

To measure latency and goodput a `socket` server is set up on the access points,
which the client connects to over UDP. UDP was selected to avoid potential backoff
and overhead which an TCP implementation would cause. Packets are sent from the
client as soon as the medium is avaliable for aditional data, and each packet is 
numbered to make sure that timing is matched to the correct packet.

By only checking latency and goodput between the client and access point, instead
of a remote host, we make sure that only the connection between the two nodes
are measured. In contrast, if we tried to measure between a remote server and
the client we might end up measuring the uplink to the internet instead.


### Scanning setup

Scans are triggered at 2 minute intervals and use `iw`, a linux tool to show
and manipulate wireless devices and their configuration [@iw], to initiate and
gather information about the scans.

To see how performant the scanning algorithms were, multiple scans were conducted
over the course of a few hours. Discovered access points with less than two
discoveries over the total scanning period  have been discarded as these were 
typically mobile access-points that passed by the measuring environment.


Methodic problems
-----------------

During the implementation process a few issues were discovered. In the following
sections I will be outlining some of these problems and how they could have been
mitigated.

### The Raspberry Pi's lack of a hardware clock

During the implementation, it turned out that the Raspberry Pi does not have a
hardware clock. This paired with the fact that the Raspberry Pis did not have
an uplink towards the internet to sync with NTP ment that the clocks on the 
devices were inaccurate (typically shifting up to a minute or two during a few 
hours of scanning).

Due to this, programatic corelation between when a scan occured and the resulting
latency proved problematic. To leviate this, in the results I will be manually
corelating the results. Future works might be able to leviate this problems by
keeping all access points and clients connected with an uplink to sync to an NTP
server or use hardware that has an hardware clock.
   
   
### The lack of customization of MinCT and MaxCT in CFG80211

While working on the implementation, it became clear that the Linux API for
configuring 802.11 devices, CFG802.11, did not support changing the min- and max
channel time parameters.

Because of this, no experiments on the minimum and maximum channel time has been
done through any of the tests, and the default implementation on the Rasperry Pi
4 is being used. It was not possible to figure out what these values were, so
these are unkown at the time of writing. 

However, seeing that existing research has been able to modify this on other
devices, further reserach could probably solve this by modifying drivers. 

### Problems with doing measurements in an appartment

Originally these measurements were planned to be ran in an dedicated environment
at _Kjeller ITS_, but due to COVID-19 that was not avaliable. Thus, the 
experiments had to be conducted in my appartment which is in the middle of Oslo.
This introduced some issues, outlined below:

 * There is more chance of interference due to the appartment being in the middle
   of a high density residential area.
 
 * There was constant movement in the appartment and thus line of sight between 
   some of the access points would at times be broken. In addition, a clothing 
   rack would be in the general area which chould have affected the results.

