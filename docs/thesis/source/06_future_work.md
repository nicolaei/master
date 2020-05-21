Future Work
============

In this section I'll outline similar approaches and other work that can build
on my findings.

Caching
-------

Using a cache might be beneficial to lower the time used for the total scan and
is something that might be useful to look at.

This approach is based on an assumption that access points rarely or never move,
and that new access points are rarely introduced [^mobile-aps].


Persistent connection
---------------------

Keeping a persistent connection to the access points that have been discovered
can also help with reducing the amount of times an access point has to perform
a scan of the network.

Assuming that access points rarely or never move, and new ones are rather
rarely introduced this persistent connection can be used to check if any
access points has been removed from the area.

This approach might be useful in cases where a centralized or decentralized
system is in charge of channel allocation, rather than the single access point.

[^mobile-aps]: Mobile access points in the form of smart phones might become
    more prevent in the future, and they might not have a strong enough signal
    to actively cause a problem for other clients on the network. Though this is
    just a hypothesis, so more research has to be done to confirm this.
    
    
Extra radio operating on a separate channel
-------------------------------------------

In [@SeamlessHandoff] the authors suggest having an extra radio on the
access point to improve handoff between access points. Using this extra
radio, access points discover each other using an exclusive discovery channel.

The approach outlined in [@SeamlessHandoff] showed that the time spent on
scanning would remain approximately the same, but the packet loss was greatly
reduced. I also hypothesize that this approach would allow for less impact on
the clients, seeing that the discovery of other access points would not
happen on the same channel that clients are operating on.

This approach was considered for testing in the thesis, but ultimately decided
against due to the extra equipment needed for adoption. For this method to be
effective, most access points need to have this extra radio.


Min and Max Channel Time
------------------------

Minimum and maximum channel time is mentioned in a lot of literature
regarding Wi-Fi. This parameter can change weather or not the scanning node
spend too much time on a channel or if it doesn't spend enough time.

For example [@SelectingScanningParameters] suggests having a set of minimum and maximum
channel times for each available channel. This way we can optimize the time
spent on each channel depending on weather or not there have previously been
seen access points, or if the access points on a channel typically spend longer
time to reply.

A suggestion for possible future work to improve scanning results or client latency
can be to investigate the use of different Min- and MaxCT strategies. I originally
outlined two strategies for this thesis, but due to implementation constraints I
was not able to test them.

 *  **Scanning with a constant Min-/MaxCT for all channels**: This means that
    the channel time won't change for each individual channel. [@APDiscovery]
    showed that higher timers yield higher discovery rates, but since I'm also
    interested in the impact towards clients, I will be using the same set of
    timers that they used.
 
 *  **Scanning with a variable Min-/MaxCT for each channel**: As suggested in
    [@SelectingScanningParameters], a variable Min-/MaxCT for each channel
    is an approach that might yield high results, while still keeping time on
    less populated channels low.


Scanning Triggers
-----------------

As noted in the Method chapter, scanning triggers might be worthwile to 
investigate further. Scanning isn't neccesarry to do that often, as the
local access points might not move often enough to warrant a scan.

Instead, something like a trigger to scan only when traffic is low might be a
good idea to investigate for future research.


