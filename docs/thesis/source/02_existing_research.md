Existing research and current practices
=======================================

Scanning
--------

The aim of scanning the local IEE802.11 topology in this thesis is to be able
to provide information about adjacent nodes to channel allocation algorithms.
With this information any given channel allocation algorithm should be able to
give the access point an optimal channel.

Scanning in IEEE802.11 [@IEEE802.11] is handled via management frames, and can
be done in one of two ways: Active- or passive scanning.

Passive scanning, from a STA's perspective, is simply to listen for
*beacon frames* that are sent out periodically by all APs. These frames contain

 *  *A timestamp*; indicating when the frame was sent (according to the APs
    synchronization timer.

 *  *A beacon interval*; telling the STAs the period between each beacon
    transmission in TUs[^tu-definition].

 *  *The capability information*; Various information about the AP, such as
    it's SSID and more. Extensions to 802.11 has also typically added some
    information to this field.

[^tu-definition]: TU (time unit) is a period of 1024p.

Active scanning on the other hand is initiated by the STAs themselves. This
process contains two management frames *probe requests* and *probe responses*.

The *probe request* is sent by an STA and either targets a single access point,
or broadcast to all APs. This is done by specifying the target APs SSID in
the frame. Leaving the SSID field empty means that the frame is considered as
a broadcast frame.

*Probe responses* on the other hand are sent by access points that receive the
*probe request*. These frames' content is almost identical to beacon frames,
though they do contain some more information than the probe request's frames. 
This information isn't really relevant for what I wish to accomplish in this
thesis, so I won't outline it [^beacon-information].

[^beacon-information]: If you're interested in the rest of the information that
    can be found in a beacon frame, please consult [@802.11Handbook, p. 52-53].

The window in which the station that sent out the *probe request* is
listening for *probe responses* is called the *scanning timer*. This timer
has two components:

 * *Minimum Channel Time*: The minimum amount of time a station will listen to
   the channel for a response from access points.

 * *Max Channel Time*: The maximum amount of time a station will listen to a
   channel for a response from an access point. This timer only activates if a
   probe response is received before MinCT.

The min- and maxCT timer pair decides for how long the station will listen in on
a channel after sending a probe request. 

\begin{figure}
    \begin{tikzpicture}[scale=1]
        \node at (0,0) (start) {};
        \node at (3,0) (min) {};
        \node at (10,0) (max) {};
        
        \draw [|->] (start) -- (max);
        \draw [->] (start) -- (1, 2) node [midway, above, sloped] 
            {\footnotesize Probe Request};
        \draw [->] (2, 2) -- (4, 0) node [midway, above, sloped] 
            {\footnotesize Probe Response (AP 1)};
        \draw [->] (3, 2) -- (6, 0) node [midway, above, sloped] 
            {\footnotesize Probe Response (AP 2)};
        
        \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
            (start) -- (min) node [midway, yshift=-1.5em] {$MinCT$};
        
        \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
            (min) -- (max) node [midway, yshift=-1.5em] {$MinCT$};
    \end{tikzpicture}
\caption{A scenario where no probe response was resieved before $MinCT$. In
         this case, no access points would be discovered because all responses
         came after $MinCT$, and thus the $MaxCT$ period will never occur.}
\end{figure}

### Current use of scanning in IEEE802.11 networks

While the aim of this thesis is to use scanning to discover other APs from
our own AP, the main use of scanning in IEEE802.11 networks is for
clients (STAs) to find access points to connect to. Typical use-cases are:

 * When disconnected; finding available APs to connect to or ask for
   specific APs that the STA has connected to before.

 * When connected; finding APs with the same SSID as the one that the STA
   is currently connected to, but with a better signal. This is typically
   used for mobile STAs to improve service while roaming.


### Differences between active and passive scanning

While both active and passive scanning are means to achieve the same result,
they have different impacts on the network and use differing amount of time
to discover all nodes on the network. The impact of them in regards to
discovery latency and network impact is widely studied.


### Discovery time

Even though both active and passive scanning will converge towards
discovering all nodes in the network, there is a significant time-difference
between these two approaches. This difference is especially significant in
high density WLAN deployments.

In addition to this there is always going to be some variance in the
discovery time due to the fact that there are always going to be large
variations in the wireless medium. Since multiple STAs share the same medium,
they'll have to share access to the medium.

In [@APDiscovery] the authors analyzed the scanning process in IEEE802.11
networks in an urban setting, which typically means high density of APs in
the given area. The main takeaway from this study is that you'll need
multiple scans to discover as many APs as possible, and even then you're not
guaranteed to find all the access points in your vicinity.

![Probe responses vs beacon frames. Here you can clearly see the how
 probe responses almost disappear after 100ms. Taken from [@APDiscovery]
](static/probe_vs_beacon.png){ width=40% }

In their tests, they found that the scanning timer for a probe request
had a lot to say about your ability to discover other APs. In general,
the longer the timer, the better the chance of discovering other access points.
Though over 100ms the benefit quickly diminish, as very few or no probe
responses were received after this time, and the discovered APs mainly came
from normal beacon frames.

In addition to the length of the timer, they also found that the amount of
scans mattered a lot to the discovery (see the figure that I haven't added
yet). Even after 100 scans, the study found that up to 15% of all APs were
not discovered.

\todo{
    Why are some access points discovered, while others are not?
    Which APs are these (like, is it the distance that matters)?
    Maybe it's their distance (ie. quality of the connection).
}


### Network Impact

According to [@ActiveScanPerformance] up to 90% of all probe responses
carry redundant information, and up to 60 percent of all management traffic
in a WLAN can be probe traffic. This is especially true for heavily utilized
channels (over 50% utilization), which typically exist in urban
environments.

This heavy utilization takes a special toll on real-time applications such as
VoIP and games. Why? Well, there are two aspects to this: The client-side 
impact, and the network-wide impact.

The client-side issues with active scans are quite apparent. In
[@ActiveScanPerformance], they set up a client to run an active scan
every minute. While running these active scans they were continuously pinging
another host over the WLAN to measure the impact these active scans have on
the latency. The result was that every minute, when the active scans was 
initialized, a large spike in latency occurred. This spike had a tail of
latency that lasted a few seconds. This kind of latency spike is problematic,
as it has an impact on real-time applications like games and VoIP.

![Scanning can have quite an effect on a client's latency. Every time a
 client scans, it's latency can increase as much as 10 fold.
 From [@ActiveScanPerformance]](static/probe_latency.png){ width=60% }

I hypothesize that this effect will be even stronger ones access points start
scanning as well, seeing that this won't just effect the access point, but
all of it's connected clients as well.

In addition to each individual client, [@ActiveScanPerformance] also takes
a look at how active scanning impacts the network as a whole. The main takeaway
here is that due to the low data rate of probe traffic, it consumes airtime
that could have been better utilized by normal application data.

In networks with low utilization, this might not have such a large impact.
However, in networks with high utilization, this low data rate traffic will
factor negatively on goodput[^goodput] in the network and will negatively affect
other clients that are not currently scanning.

[^goodput]: _Goodput_ is the application-level throughput.


### Channel overlapping

In addition to their findings about [Discovery Time](@sec:Discovery Time)) in
[@APDiscovery] the authors also highlighted that due to channel overlapping,
an STA that is scanning a channel $i$ has a propability of also discovering
access points on channels up to two channels away.

This will help with discovery of access points, since a scan can potentially
discover as many as 40% of APs in adjacent channels. See the figure from the
study for percentages of adjecent channels.

![Percent of access points discovered in adjacent channels 
  (From [@APDiscovery])](static/channel_overlap.png){ width=75% }


Possible problem areas
----------------------

Simply scanning the local topology may sound like a simple endevour, but there
are some caviats that need to be considered to get accurate results while still
letting clients use the network freely.

### Client's have to rediscover the access point

\todo{
    Find a citation for the fact that clients will lose their connection when
    the access point switches channel.
    
    This might also be a non-problem if we utilize smooth scanning.
}
\todo{
    Maybe the title of this section should be a question to be consistent
    with the other subsections?
}

When an access point switches channels, all its clients will lose connection
and have to re-discover and re-connect to the access point [Citation Needed].
If the access point switches channels to quickly, the clients may end up
losing connection for such a long time that it might become an annoyance to
the users. To leviate this, I will have to figure out what the best possible
time period is.

### Can the access point send data while scanning?

If it is not possible for the access point to send data while scanning, then
another problem will arise: *How can we make sure that the client's are able
to continue using the network when the clustering algorithm asks for the
current status of the network?*.

If we can't transmit og receive data during the whole duration of the scan,
we might even need to schedule the discovery period to periods where the
network is less utilized.

### What if some other access points are also scanning?

\todo{
    I'm not quite sure about this section. I need to find some literature or
    do some measurements that support that access points that are scanning
    might not be able to do RX or TX.

    The program is also going to be using active beacons, so maybe this needs
    to be rephrased?
}

In the case that multiple access points are trying to do a scan of the network
at the same time, our program might need to do multiple scanning passes to be
certain that it collects information about all the other access points.

Because of this, I'll have to figure out:

*   How many passes are enough to be certain that we've collected information
    about all other access points in our neighbourhood?

*   Is it possible to be more smart about the scanning? Can - for example -
    some randomization of when the scan happens or be used?


