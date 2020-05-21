Method
======

In this chapter I'll be talking about which methods that I will be using in my
experiments and how I implemented these methods.

These methods aim to measure and discover the optimal way to get a good overview
of the local topology, while not impacting the clients connected to the
access point.


Measuring points
----------------

During my tests, I've tried to gather the following data to verify the
effectiveness of my results:

- Client latency
- Client goodput [^goodput]
- Percent of access points discovered
- Speed of discovery

[^goodput]: _Goodput_ is the application-level throughput.

These data points will help me figure out which methods are best fit for
discovering a high percentage of access points at a high speed, while still
letting clients utilize the network like normal.

\todo{
    These measuring points could be grouped into two parts: Scan results and
    client impact.
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
points as possible, and doing it as fast as possible.

Worth noting is that the faster we're doing the discovery, the less probe
requests will be occupying the network, and thus improving the client's latency.


Discovery strategies
--------------------

Discovery strategies are a well discussed topic within IEEE802.11, but these
are mainly aimed at clients trying to discover access points.

Any given scanning algorithm must find the best trade-off between:

 *  The time spent to probe for APs
 
 *  The number of discovered APs
 
 *  The discovery of at least one candidate AP after a full scan

An ideal scanning algorithm seeks to discover the maximum number of APs in
the shortest period [@SelectingScanningParameters].
 
I'll be testing multiple discovery strategies that has been outlined in
various research articles in this thesis.
 
\todo{
    Write a section about each of the strategies and outline their apparent
    weaknesses that has been discussed in the given research articles.
}

### Full scan

This approach will be used as the baseline, seeing as it is the simplest and
most common way for most clients to scan the network.

With a full scan, the access point will be going trough all channels, in
order and without pause.


### Selective Scanning

According to [@APDiscovery], some percentage of access points in adjacent
channels will be discovered while in a given channel due to channel overlapping.

Seeing that our main goal is to find access points that are neighbouring the
current access point, it's possible that we can find many of these while
scanning fewer channels. This could give a huge boost in speed if successful.

This approach should substantially decrease the time spent on doing a full scan,
as (according to [@SeamlessHandoff]) the fact that when scanning the station
that is scanning has to wait for a response for up to 100ms. This implies
that scanning time increases proportional to the number of channels that are
being scanned. Reducing the number of channels scanned, will thus reduce the
total time of the scan.

![Percent of access points discovered in adjacent channels 
  (From [@APDiscovery])](static/channel_overlap.png){ width=75% }


### Smooth Scanning

Smooth scanning utilizes a staggered approach where channels are scanned in
multiple batches. Each channel is assigned to a group, and in between the
groups the access point will return to "normal" operations where it will
serve clients. 

Both the group size and time between each scan is configurable, and has their
trade-offs. For more on this, see [Parameters].

This approach has previously been explored in
[@SelectingScanningParameters], [@ProactiveScan], and [@PracticalSchemes].
Though in these cases, it was specifically tested on the client.

The use of intervals of normal operations in these articles prove quite
beneficial for the client's latency, goodput and packet loss, though at the
expense of scanning speed. This longer scanning period should hopefully not have
any impact when scanning as the access-point.

Parameters
----------

In addition to changing up the strategies, there are also a few parameters
that can be changed within every strategy for more optimal results.

These parameters might be set adaptively or statically, depending on the
operator's wish.

Based on previous research, the following parameters are the most impactfull
when it comes to time and accuracy. In addition to this, I assume that these
will have some sort of impact on a client's goodput.

 *  *Minimum number of scans*: How many scans (of the whole channel sequence)
    should be performed before the scan is finished.
 
 *  *Smooth scan interval*: How long to wait between each scan 

 *  *Smooth scan group size*: The number of channels to scan per period
 
 *  *Scanning Trigger*: When should the scans start?


### Minimum number of scans

This parameter is important to make sure that we have a reply from all access
points in our vicinity before sending of our results. As [@APDiscovery]
notes, all access points will most likely not be discovered with just one scan.


### Smooth scanning interval

As mentioned in [Smooth Scanning], there is a possibility to adjust the time
spent serving clients in between each scanning group. This parameter is a
trade off between the latency and package loss of clients, and the speed of the
total scan.

[@ProactiveScan] has done research regarding which interval to choose. The
longer the interval is, the more time clients will have to send packets that
were cued up during the last scan. Though these longer intervals will
increase the total time of our scan.


### Smooth scanning group size 

The size of the groups in smooth scanning is another trade off between client
packet loss and total scan duration.

[@ProactiveScan] has also done research regarding this parameter. The larger the
group size, the faster the total scan will be, though the trade-off comes at
the expense of clients in form of possible packet loss.


### Scanning Trigger

When to start scanning is important. In an extreme case, all access points can
start scanning at the same time, which would both congest the medium and since
they're all listening and probably not replying, we could end up not discovering
any other access point.

\todo{
    I'm not quite sure if access points don't reply while listening for
    responses. I'll have to verify this.
}

In typical client handoff schemes, the scan is triggered when the RSSI to the
connected access point is low or when trying to find a network to connect to.
Both of these triggers don't exist when searching from an access point, because
the client isn't connected to another access point, nor does it need to find
another one.

There is also a question of how often the access points should scan to keep a
accurate view of its neighbourhood. I hypothesize that new access points won't
be introduced and removed within a day. Though with the advent of sharing mobile
data over Wi-Fi, this assumption might be wrong. Mobile phones that share their
data are mobile, as opposed to traditional access points.

Some possible methods are:

 *  **Random timers**: Having the timing for a scan totally random opens for
    less possibility for collision. Pairing this with the number of scans, it
    seems very likely that it would help give an accurate overview of the
    access point's current neighbourhood.
 
 *  **Clock based timer**: Basing the scan times of the clock could be a good
    solution for avoiding times with high traffic, but it introduces the risk
    of always scanning at the same time as another access point or scanning
    while another access point is turned off [^turned-off].
 
 *  **Traffic based trigger**: Having times of low traffic be the trigger could
    also be a possible solution. Though here we also introduce the risk of
    scanning at the wrong time. Seeing that workplaces and homes usually empty
    and fill up at the same time, we could risk having access points scanning at
    the same time.
    
    In addition to this, only scanning when there is low traffic could risk
    getting inaccurate results because other access points might be turned off
    or getting a different signal strength due to lower traffic.
    
\todo{
    I'm not quite sure about what I'm saying about different signal strength
    here. Does it actually work like that?
}


[^turned-off]: Some consumer access points have the ability to be turned off
               during a specified period. For example in households where
               parents wish to limit access to the internet during the night.


Implementation
--------------

In the following section we will be taking a look at how the tests were 
implemented and executed. 

### Scanning Strategies

#### Full Scan

The full scan is used as a base-line test for comparisons. 

As mentioned earlier, this approach will simply go through all channels in one 
go. Meaning that we go from channel 1 to 12 without any breaks. This is how a 
typical scan works with most modern implementations.

#### Selective Scanning

With the selective channel approach I will be testing two approaches.
As mentioned earlier in this chapter, according to [@APDiscovery], some
percentage of adjacent channels will be discovered while in any given channels
due to channel overlapping.

 *  **Scanning channels 1, 6 and 11**: These are the only channels that don't
    overlap with each other in the normal 2.4 GHz space.
 
 *  **Scanning every alternating channel**: If scanning every alternating
    channel is feasible, it might halve our total scanning time seeing that
    the time to scan is proportional to the amount of channels scanned
    [@SeamlessHandoff].


#### Smooth Scanning

The smooth scanning implementation has been tested with static smooth scanning
parameters based on [@ProactiveScan] and [@PracticalSchemes]'s results. These 
articles showed that lower group size and higher intervals are beneficial for
latency and packet loss. Seeing that we're not dependent on a low time-to-scan,
I want to prioritize the clients goodput. 

The following parameter configurations will be tested:

 * **1 channel per group, 300 miliseconds intervals**
 
 * **1 channel per group, 600 miliseconds intervals**
 
 * **1 channel per group, 1200 miliseconds intervals**
 

### Scanning Parameters

To make sure that results are comparable I will try to keep the parameters as
static as possible between each test. This section will not cover the smooth
scan interval and smooth scan group size. See the [implementation section about
smooth scanning](Smooth Scanning) for that information.

#### Minimum number of scans

[@APDiscovery] discovered that to get the most accurate view of the local
topology, multiple scans are neccesary. To get a good view of the probability
of dicsovery for each scanning setup, the implementation will be scanning every
2 minutes for a minimum of three hours. 

#### Scanning triggers

As hinted at above I will only be testing one trigger type, *clock based triggers*.
It might be a worthwile endevor for future work to investigate traffic based
triggers and other triggers to find more optimal times to scan at.

It can also be argued that due to the low amount of traffic that my access points
will be experiencing (max two clients), the traffic based trigger might not make
a huge difference due to the low amount of clients.

### Setup

To do the actual measurements, I will be using Raspberry Pi 4 Model B (4 GB) as
make-shift access points and clients. The RPi 4 has a built in Wi-Fi antenna 
which supports both 2.4 and 5 GHz.

Both clients and the access points are using Raspian 10 (Buster), which are based
on the popular Linux distribution Debian (Buster).

All Raspberries were deployed at consistent locations in a area of approximately
50sqm. See figure {@fig:aplayout} for an aproximation on placement. In this 
figure the clients number corresponds to the access point it is connected to. 
`AP 1` does not have any connected clients.

![Layout of access points and clients during scans](static/ap_layout.png){ height=45% #fig:aplayout }

#### Access Point Setup

The nodes that function as access points are using `hostapd` as the access point
software. This allows for easy-setup of everything from SSID to the selected channel.

For the sake of consistensy all access points have the same settings accross
all experiments. The selected channel was the one with the least assigned APs
in my area.


#### Client Setup

In similar vains ast the access points, the clients are using `wpa_supplicant` 
to connect to the access points. A single client never changes which access point 
it is connected to during any of the experiments.


### Measurements and collecting data

To do the actual measurements, I will be using:

 * `sockets` to collect data about how the client's connection is affected by 
   the scans that the access points are doing.
  
 * `iw` to conduct scans from the access points.
 
 * `python` to collect data from `socekt`s and `iw`, as well as writing this 
   data to disk. All data is also timestamped to make it easier to spot the
   corralations between ping-spikes and the actuall scan (ping-spikes can happen
   unrelated to scans due to interference).

#### Latency and goodput measurement

To measure latency and goodput a `socket` server is set up on the access points,
which the client connects to over UDP. UPD was selected to avoid potential backoff
from an TCP implementation. Packets are sent as soon as the channel is avaliable
for aditional sends. Each packet is numbered to make sure that timing is matched
to the correct packet.

By only checking latency and goodput between the client and access point, instead
of a remote host, we make sure that only the connection between the two nodes
are measured. In contrast, if we tried to measure between a remote server and
the client we might end up measuring the uplink to the internet instead.


#### Scanning setup

Scans are triggered at 2 minute intervals and use `iw`, a linux tool to show
and manipulate wireless devices and their configuration [@iw], to initiate and
gather information about the scans.

To see how performat the scanning algorithms were, multiple scans were conducted
over the course of a few hours. Discovered access points with less than 2 results
have been discarded as these were typically mobile access-points that passed by
the measuring environment.


### Methodic problems

During the implementation process a few issues were discovered. In the following
sections I will be outlining some of these problems and how they could have been
mitigated.

#### The Raspberry Pi's lack of a hardware clock

During the implementation, it turned out that the Raspberry Pi does not have a
hardware clock. This paired with the fact that the Raspberry Pis did not have
an uplink towards the internet ment that the clocks on the devices were really
inaccurate (typically shifting up to a minute or two during a few hours of
scanning).

Due to this, programatic corelation between when a scan occured and the resulting
latency proved problematic. To leviate this, in the results I will be manually
corelating the results. Furture works might be able to leviate this problems by
keeping all access points and clients connected with an uplink to sync to an NTP
server or use hardware that has an hardware clock.

#### Problems with doing measurements in an appartment

Originally these measurements were planned to be ran in an dedicated environment
at _Kjeller ITS_, but due to COVID-19 that was not avaliable. Thus, the 
experiments had to be conducted in my appartment which is in the middle of Oslo.
This introduced some issues, outlined below:

 * There is more chance of interference due to the appartment being in the middle
   of a high density residential area.
 
 * There was constant movement in the appartment and thus LoS between some of the
   access points would at times be broken. In addition a clothing rack would be
   in the general area which chould have affected the results.

