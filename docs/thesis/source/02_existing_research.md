Scanning IEEE802.11 networks
============================

The aim of scanning the local IEE802.11 topology in this thesis is to be able
to provide information about adjacent nodes to channel allocation algorithms.
With this information any given channel allocation algorithm should be able to
give the access point a channel with the same or less congestion.

In this chapter we will be exploring how a IEEE802.11 scan works and existing
research on scanning strategies for IEE802.11 networks.

The anatomy of a IEEE802.11 scan
---------------------------------

Scanning in IEEE802.11 [@IEEE802.11] is handled via management frames, and can
be done in one of two ways: active or passive scanning.

**Passive scanning**, from a STA's perspective, is simply to listen for
*beacon frames* that are sent out periodically by all APs. These frames contain:

 *  *A timestamp*; indicating when the frame was sent (according to the APs
    synchronization timer.

 *  *A beacon interval*; telling the STAs the period between each beacon
    transmission in TUs[^tu-definition].

 *  *The capability information*; Various information about the AP, such as
    it's SSID and more. Extensions to 802.11 has also typically added some
    information to this field.

[^tu-definition]: TU (time unit) is a period of 1024μs.

**Active scanning** however, is initiated by the STAs themselves. This
process contains two management frames *probe requests* and *probe responses*.

The *probe request* is sent by an STA and either targets a single access point,
or broadcast to all APs. This is done by specifying the target APs SSID in
the frame. Leaving the SSID field empty means that the frame is considered as
a broadcast frame.

*Probe responses* are sent by access points that receive the *probe request*.
These frames' content is almost identical to beacon frames, though they do 
contain some more information than the probe request's frames.  This information
isn't really relevant for what I wish to accomplish in this thesis, so I won't
outline it [^beacon-information].

[^beacon-information]: If you're interested in the rest of the information that
    can be found in a beacon frame, please consult [@802.11Handbook, p. 52-53].

The window in which the station that sent out the *probe request* is
listening for *probe responses* is called the *scanning timer*. This timer
has two components:

 * *Minimum Channel Time (MinCT)*: The minimum amount of time a station will 
   listen to the channel for a response from access points.

 * *Max Channel Time (MaxCT)*: The maximum amount of time a station will listen 
   to a channel for a response from an access point. This timer only activates 
   if a probe response is received before MinCT.

The min- and maxCT timer pair decides for how long the station will listen in on
a channel after sending a probe request. See {+@fig:activescanexample} how an 
example of how active scan works, where all of these concepts are incorporated.


\begin{figure}
    \begin{subfigure}[b]{\linewidth}
        \begin{tikzpicture}[scale=1]
            \node at (0,0) (start) {};
            \node at (3.5,0) (min) {};
            \node at (8,0) (max) {};
            \node at (10,0) (end) {};
            
            \draw [|->] (start) -- (end);
            
            \draw [->] (start) -- (1, 2) node [midway, above, sloped] 
                {\footnotesize Probe Request};
            \draw [->] (1, 2) -- (3, 0) node [midway, above, sloped] 
                {\footnotesize Probe Response (AP 1)};
            \draw [->] (3, 2) -- (6, 0) node [midway, above, sloped] 
                {\footnotesize Probe Response (AP 2)};
            \draw [decorate, decoration={zigzag}] [->] 
                (5, 2) -- (9, 0) node [midway, above, sloped] 
                {\footnotesize Probe Response (AP 3)};
            
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (start) -- (min) node [midway, yshift=-1.5em] {$MinCT$};
            
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (min) -- (max) node [midway, yshift=-1.5em] {$MaxCT$};
        \end{tikzpicture}
        
        \caption{
            A successfull scan where a probe response was recived before $MinCT$
            ended. In this senario both AP1 and AP2 would be discovered, but
            not AP3.
        }
        \label{fig:activescansuccess}
    \end{subfigure}
    
    \begin{subfigure}[b]{\linewidth}
        \begin{tikzpicture}[scale=1]
            \node at (0,0) (start) {};
            \node at (3.5,0) (min) {};
            \node at (8,0) (max) {};
            \node at (10,0) (end) {};
            
            \draw [|->] (start) -- (end);
            
            \draw [->] (start) -- (1, 2) node [midway, above, sloped] 
                {\footnotesize Probe Request};
            \draw [decorate, decoration={zigzag}] [->] 
                (2, 2) -- (4, 0) node [midway, above, sloped] 
                {\footnotesize Probe Response (AP 1)};
            \draw [decorate, decoration={zigzag}] [->] 
                (3, 2) -- (6, 0) node [midway, above, sloped] 
                {\footnotesize Probe Response (AP 2)};
            \draw [decorate, decoration={zigzag}] [->] 
                (5, 2) -- (9, 0) node [midway, above, sloped] 
                {\footnotesize Probe Response (AP 3)};
            
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (start) -- (min) node [midway, yshift=-1.5em] {$MinCT$};
            
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (min) -- (max) node [midway, yshift=-1.5em] {$MaxCT$};
        \end{tikzpicture}
        
        \caption{
            An unsuccessful scan where no access points are discovered. In this 
            scenario, no access points would be discovered because all responses
            came after $MinCT$, and thus the $MaxCT$ period will never occur.
        }
        \label{fig:activescanfail}
    \end{subfigure}
    
    \caption{
        Examples of active scanning, with both an successful and unsuccessful scan.
    }
    \label{fig:activescanexample}
\end{figure}


Scanning in modern day IEE802.11 networks
-----------------------------------------

While the aim of this thesis is to use scanning to discover other APs from
our own AP, the main use of scanning in IEEE802.11 networks is for clients 
(STAs) to find access points to connect to and keep their connection alive. 
These are the two typical use-cases found in the wild today [@WifiScanFaq]:

 * When disconnected; finding available APs to connect to or ask for
   specific APs that the STA has connected to before.

 * While connected; finding APs with the same SSID as the one that the STA
   is currently connected to, but with a better signal. This is typically
   used for mobile STAs to improve service while roaming.

In addition to this, some access points have the ability to trigger a scan in
order to figure out which channel might be the least congested in the area. With
this information, the access point might choose to switch channel.

Lastly, mobile devices may also use IEEE802.11 beacons to enhance their
positioning service by using a database of known access point poisitions such as
Mozilla Location Services [@MozillaLocationServices]. It's also worth noting
that these services typically use other sources such as bluetooth or GPS to
further increase accuracy.


Differences between active and passive scanning
-----------------------------------------------

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
](static/probe_vs_beacon.png){ width=40%; #fig:probevsbeacons }

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


### Network impact

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
 From [@ActiveScanPerformance]](static/probe_latency.png){ width=60%; #fig:probelatency }

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


Channel overlapping {#sec:channeloverlap}
-------------------

In addition to their findings about [Discovery Time](@sec:Discovery Time)) in
[@APDiscovery] the authors also highlighted that due to channel overlapping,
an STA that is scanning a channel $i$ has a propability of also discovering
access points on channels up to two channels away.

This can help with discovery of access points, since a scan can potentially
discover as many as 40% of APs in adjacent channels. See {@fig:channeloverlap}
for percentages of adjecent channels.

![Percent of access points discovered in adjacent channels 
  (From [@APDiscovery])](static/channel_overlap.png){ #fig:channeloverlap }
