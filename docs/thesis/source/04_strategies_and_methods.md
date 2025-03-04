Possible Measurement and Discovery Strategies 
=============================================

In this chapter we will be looking at previous research regarding discovery
strategies and how to measure these. These will be used as a basis in the next 
chapter, where we will be looking at how the experiments have been implemented.

These methods aim to measure and discover the optimal way to get a good overview
of the local topology, while not impacting the clients connected to the
access point.


Measurement strategies 
----------------------

During the tests, the following data has been gathered to verify the
effectiveness of the results:

- Client latency
- Client goodput [^goodput]
- Probability of access point discovery 
- Speed of access point discovery

[^goodput]: _Goodput_ is the application-level throughput.

These data points will help to figure out which methods are best fit for
discovering a high percentage of access points, while still letting clients 
utilize the network like normal.


### Client measurements

Client latency and goodput will be used to measure how a given algorithm affects
the clients on the network. With these two measurements combined we can see how
much impact each scanning method has on both real-time and non-real-time applications.

As [@ActiveScanPerformance] mentions, a large amount of probe traffic can
negatively impact the network's clients, and when access points are scanning they
won't be able to transmit or recive traffic from the clients.

To summarize: The main objective of these measurement points is to make sure
that we can choose an algorithm that has the least negative impact on our
client's performance.


### Access point measurements 

While client latency and goodput from the chosen algorithms are important, it
is also important to make sure that we're discovering all access points that are 
in proximity to possibly be able to affect the performance of our access point.
To acomplish this we will have to measure the probability of discovery against 
the percived strength of the signal.

It is worth noting that the less time we are spending on _active_ scanning, the
less chance there is that the connected clients will lose packets
[@ActiveScanPerformance]. This is because the clients have to queue up messages 
that did not get an ACK from the recipient when using TCP, or packets that simply 
gets dumped when using UDP. To measure this, we will be looking at the total time
spend scanning for access points.

To further visualize the accuracy of our scans, every access point result graph
will have an approximated _Ricean_ and _Rayleigh_ fading curve overlayed to 
visualize the expected probability of discovery for a given access point.

Simply put, both Ricean and Rayleigh fading are stochastic models for radio 
propagation anomalies caused by partial cancellation of a signal by itself. The
two fading models are utilized for two different scenarios 
[@RayleighFading] [@RicianFading]:

 * _Ricean fading_ occurs when one of the signal paths are much stronger than
   the others. This is typically associated with signals that have line of sight,
   or one of the reflections of the signal are particularly strong.
 
 * _Reyleigh fading_ models signals where there is no dominant signal path. 
   This is usefull for modeling signals without line of sight, which are typical
   in urban environments.


Discovery strategies {#sec:discoverystrategies}
--------------------

Discovery strategies are a well discussed topic within IEEE802.11 literature, 
but these are mainly aimed at clients trying to discover access points.

Any given scanning algorithm must find the best trade-off between:

 *  The time spent to probe for APs
 
 *  The number of discovered APs
 
 *  The discovery of at least one candidate AP after a full scan

When scanning from a client, an ideal scanning algorithm seeks to discover the 
maximum number of APs in the shortest period [@SelectingScanningParameters]. 
This is due to the mobile nature of clients. Take, for example, a scenario where 
a client is moving down a hallway. If the conenction to the current access point
gets too poor, and it needs to roam to the next one a scan is triggered. In this
case, a scanning algorithm that is to slow might cause the client to not discover 
any access points before it loses the connection.

However, when scanning from an access point this mobility limitation does not 
cause an issue. Access points are not mobile [^mobile-access-points], and for the
problem that this thesis aims to solve speed is not as important as the accuracy 
of the scan. Because of this, we don't have to consider the time spent looking 
for access points.

[^mobile-access-points]: There is an exception here: Mobile phones can work as
    hotspots. This is a typical usecase in cafes and similar. However, this edge
    case is out of the scope of this thesis. Besides, these mobile hotspots are
    typically only around for a limited amount of time. I.e. while a guest is
    at a cafe.

Now, we will be looking at multiple discovery strategies that has been outlined
in previous research.
 
\begin{figure}
    \begin{subfigure}[b]{\linewidth}
        \begin{tikzpicture}[scale=1]
            \node at (0,0) (start) {};
            \node at (0,0) (ch1) {};
            \node at (1,0) (ch2) {};
            \node at (2,0) (ch3) {};
            \node at (3,0) (ch4) {};
            \node at (4,0) (ch5) {};
            \node at (5,0) (ch6) {};
            \node at (6,0) (ch7) {};
            \node at (7,0) (ch8) {};
            \node at (8,0) (ch9) {};
            \node at (9,0) (ch10) {};
            \node at (10,0) (ch11) {};
            \node at (11,0) (end) {};
            
            \draw [|-|] (start) -- (end);
            
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch1) -- (ch2) node [midway, yshift=-1.5em] {$CH 1$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch2) -- (ch3) node [midway, yshift=1.5em] {$CH 2$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch3) -- (ch4) node [midway, yshift=-1.5em] {$CH 3$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch4) -- (ch5) node [midway, yshift=1.5em] {$CH 4$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch5) -- (ch6) node [midway, yshift=-1.5em] {$CH 5$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch6) -- (ch7) node [midway, yshift=1.5em] {$CH 6$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch7) -- (ch8) node [midway, yshift=-1.5em] {$CH 7$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch8) -- (ch9) node [midway, yshift=1.5em] {$CH 8$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch9) -- (ch10) node [midway, yshift=-1.5em] {$CH 9$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch10) -- (ch11) node [midway, yshift=1.5em] {$CH 10$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch11) -- (end) node [midway, yshift=-1.5em] {$CH 11$};
        \end{tikzpicture}
        \caption{Representation of a full scan}
    \end{subfigure}
    
    \begin{subfigure}[b]{\linewidth}
        \begin{tikzpicture}[scale=1]
            \node at (0,0) (start) {};
            \node at (0,0) (ch1) {};
            \node at (1,0) (ch3) {};
            \node at (2,0) (ch5) {};
            \node at (3,0) (ch7) {};
            \node at (4,0) (ch9) {};
            \node at (5,0) (ch11) {};
            \node at (6,0) (ch11_end) {};
            \node at (11,0) (end) {};
            
            \draw [|-|] (start) -- (end);
            
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch1) -- (ch3) node [midway, yshift=-1.5em] {$CH 1$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch3) -- (ch5) node [midway, yshift=1.5em] {$CH 3$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch5) -- (ch7) node [midway, yshift=-1.5em] {$CH 5$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch7) -- (ch9) node [midway, yshift=1.5em] {$CH 7$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch9) -- (ch11) node [midway, yshift=-1.5em] {$CH 9$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch11) -- (ch11_end) node [midway, yshift=1.5em] {$CH 11$};
        \end{tikzpicture}
        \caption{Representation of a selective scan}
    \end{subfigure}

    \begin{subfigure}[b]{\linewidth}
        \begin{tikzpicture}[scale=1]
            \node at (0,0) (start) {};
            \node at (0,0) (ch1) {};
            \node at (1,0) (ch1_end) {};
            \node at (3,0) (ch2) {};
            \node at (4,0) (ch2_end) {};
            \node at (6,0) (ch3) {};
            \node at (7,0) (ch3_end) {};
            \node at (9,0) (ch4) {};
            \node at (10,0) (ch4_end) {};
            \node at (11,0) (end) {};
            
            \draw [->] (start) -- (end);
            
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch1) -- (ch1_end) node [midway, yshift=-1.5em] {$CH 1$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch2) -- (ch2_end) node [midway, yshift=1.5em] {$CH 2$};
            \draw [decorate, decoration={brace, amplitude=10pt, mirror}] 
                (ch3) -- (ch3_end) node [midway, yshift=-1.5em] {$CH 3$};
            \draw [decorate, decoration={brace, amplitude=10pt}] 
                (ch4) -- (ch4_end) node [midway, yshift=1.5em] {$CH 4$};
        \end{tikzpicture}
        \caption{
            Representation of a smooth scan. 
            Scans continue after the end of the figure.
        }
    \end{subfigure}
    
    \caption{
        Representation of the three scanning strategies. The X-axis is time.
    }
\end{figure}



### Full scan

This approach will be used as the baseline, seeing as it is the simplest and
most common way for most clients to scan the network.

With a full scan, the access point will be going trough all channels, in
order and without pause.


### Selective Scanning

According to [@APDiscovery], some percentage of access points in adjacent
channels will be discovered while in a given channel due to channel overlapping.
In addition to this, most 2.4 GHz Wi-Fi deployments only operate on the three
non-overlapping channels; 1, 6 and 11.

Seeing that our main goal is to find access points that are in proximity to the
current access point, it's possible that we can find many of these while
scanning fewer channels. This could give a huge boost in speed if successful.

This approach should substantially decrease the time spent on doing a full scan,
as (according to [@SeamlessHandoff]) the fact that when scanning the station
that is scanning has to wait for a response for up to 100ms. This implies
that scanning time increases proportional to the number of channels that are
being scanned. Reducing the number of channels scanned, will thus reduce the
total time of the scan.


### Smooth Scanning

Smooth scanning utilizes a temporaly spaced approach where channels are scanned 
in multiple batches. Each channel is assigned to a group, and in between the
groups the access point will return to "normal" operations where it will
serve clients. 

Both the group size and time between each scan is configurable, and has their
trade-offs. This will be discussed further in the next section about parameters.

This approach has previously been explored in
[@SelectingScanningParameters], [@ProactiveScan], and [@PracticalSchemes].
Though in these cases, it was specifically tested on the client.

The use of intervals of normal operations in these papers prove quite
beneficial for the client's latency, goodput and packet loss, though at the
expense of scanning speed. This longer scanning period should hopefully not have
any impact when scanning as the access-point.


Parameters
----------

In addition to changing up the strategies, there are also a few parameters
that can be changed within every strategy for more optimal results. These 
parameters might be set adaptively or statically, depending on the operator's wishes.

Based on previous research ([@APDiscovery] [@ProactiveScan] 
[@SelectingScanningParameters]), the following parameters are the most impactfull
when it comes to time and accuracy. In addition to this, it's reasonable to
assume that these will have some sort of impact on a client's goodput.

 *  *Minimum number of scans*: The amount of scans of the whole channel sequence
    that should be performed before the scan is finished.
 
 *  *Smooth scan interval*: The amount of time to wait between each scan 

 *  *Smooth scan group size*: The number of channels to scan per period
 
 *  *Scanning Trigger*: When to start a scan
 
 *  *Max and min channel time*: The amount of time to stay on each channel


### Minimum number of scans

As [@APDiscovery] notes, all access points will most likely not be discovered 
with just one scan of the entire frequency space. By specifying a minimum number 
of scans we make sure that more access points in the vicinity are found before
submitting the results of the scan. 


### Smooth scanning interval

As mentioned in [Smooth Scanning], it is possible to adjust the time
spent serving clients in between each scanning group. This parameter is a
trade off between the latency and package loss of clients, and the speed of the
total scan.

[@ProactiveScan] has done research regarding which interval to choose. The
longer the interval is, the more time clients will have to send packets that
were cued up during the last scan. Though these longer intervals will
increase the total time of our scan. However, the results of the scan should not
be effected by the longer scan time.


### Smooth scanning group size 

The size of the groups in smooth scanning is another trade off between client
packet loss and total scan duration.

[@ProactiveScan] has also done research regarding this parameter. The larger the
group size, the faster the total scan will be, though the trade-off comes at
the expense of clients in form of possible packet loss.


### Scanning Trigger

When to start scanning is important. In an extreme case, all access points can
start scanning at the same time, which would both congest the medium, and since
they are all listening and probably not replying, we could end up not discovering
any other access point.

In typical client handoff schemes, the scan is triggered when the RSSI to the
connected access point is low or when trying to find a network to connect to.
Both of these triggers do not exist when searching from an access point, 
because it is not connected to another access point, nor does it need to find
another access point to establish an uplink. 

There is also a question of how often the access points should scan to keep a
accurate view of its neighbourhood. I hypothesize that new access points will not
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
 
 *  **Traffic based trigger**: Using periods of low traffic as a trigger could
    also be a possible solution. Though here we also introduce the risk of
    scanning at the wrong time. Seeing that workplaces and homes usually empty
    and fill up at the same time, we could risk having access points scanning at
    the same time.
    
    In addition to this, only scanning when there is low traffic could risk
    getting inaccurate results because other access points might be turned off.


[^turned-off]: Some consumer access points are can turned off during a specified
               period. For example in households where parents wish to limit 
               access to the internet during the night.


### Min and Max Channel Time

Minimum and maximum channel time is mentioned in a lot of literature
regarding Wi-Fi. This parameter can change whether or not the scanning node
spend too much time on a channel or if it does not spend enough time.

For example [@SelectingScanningParameters] suggests having a set of minimum and maximum
channel times for each available channel. This way we can optimize the time
spent on each channel depending on weather or not there have previously been
seen access points, or if the access points on a channel typically spend longer
time to reply.

By using minimum and maximum channel time, client latency can be reduced for each
channel scanned. Reducing the total time of a scan and possibly improving goodput
and latency. Two prevelant strategies from literature are:

 *  **Scanning with a constant Min-/MaxCT for all channels**: This means that
    the channel time will not change for each individual channel. [@APDiscovery]
    showed that higher timers yield higher discovery rates.
 
 *  **Scanning with a variable Min-/MaxCT for each channel**: As suggested in
    [@SelectingScanningParameters], a variable Min-/MaxCT for each channel
    is an approach that might yield high results, while still keeping time on
    less populated channels low.
