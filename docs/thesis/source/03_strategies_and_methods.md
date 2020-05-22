Possible Measurement Strategies and Discovery Methods
=====================================================

In this chapter I'll be talking about which methods that I will be using in my
experiments and how I implemented these methods.

These methods aim to measure and discover the optimal way to get a good overview
of the local topology, while not impacting the clients connected to the
access point.


Measurement strategies 
----------------------

During my tests, I've tried to gather the following data to verify the
effectiveness of my results:

- Client latency
- Client goodput [^goodput]
- Probability of access point discovery 
- Speed of access point discovery

[^goodput]: _Goodput_ is the application-level throughput.

These data points will help me figure out which methods are best fit for
discovering a high percentage of access points, while still letting clients 
utilize the network like normal.


### Client measurements

Client latency and goodput will be used to measure how a given algorithm affects
the clients on the network. With these two measurements combined we can see how
much impact each scanning method has on both real-time and non-real-time .

As [@ActiveScanPerformance] mentions, a large amount of probe traffic can
negatively impact the network's clients, and when access points are scanning they
won't be able to recive traffic from the clients.

To summarize: The main objective of these measurement points is to make sure
that we can choose an algorithm that has the least negative impact on our
client's performance.


### Access point measurements 

While client latency and goodput from the chosen algorithms are important, it
is also important to make sure that we're discovering as many access points as
possible, as accurately as possible. To acomplish this we will have to measure 
the probability of discovery against the percived strength of the signal.

It's worth noting that the less time we're spending on _active_ scanning, the
smaller the chance is that we will be missing packets due to buffer overflows
on the client [@ActiveScanPerformance]. To measure this, we will be looking
at the total time spend scanning for access points.


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


### Min and Max Channel Time

Minimum and maximum channel time is mentioned in a lot of literature
regarding Wi-Fi. This parameter can change weather or not the scanning node
spend too much time on a channel or if it doesn't spend enough time.

For example [@SelectingScanningParameters] suggests having a set of minimum and maximum
channel times for each available channel. This way we can optimize the time
spent on each channel depending on weather or not there have previously been
seen access points, or if the access points on a channel typically spend longer
time to reply.

By using minimum and maximum channel time, client latency can be reduced for each
channel scanned. Reducing the total time of a scan and possibly improving goodput
and latency. Two prevelant strategies from literature are:

 *  **Scanning with a constant Min-/MaxCT for all channels**: This means that
    the channel time won't change for each individual channel. [@APDiscovery]
    showed that higher timers yield higher discovery rates, but since I'm also
    interested in the impact towards clients, I will be using the same set of
    timers that they used.
 
 *  **Scanning with a variable Min-/MaxCT for each channel**: As suggested in
    [@SelectingScanningParameters], a variable Min-/MaxCT for each channel
    is an approach that might yield high results, while still keeping time on
    less populated channels low.
