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

As noted in [Possible Measurement Strategies and Discovery Methods], using a
minimum and maximum channel time 

As suggested in for possible future work to improve scanning results or client latency
can be to investigate the use of different Min- and MaxCT strategies. I originally
outlined two strategies for this thesis, but due to implementation constraints I
was not able to test them.

By looking at documentation found on `iw`'s [@iw] kernel page, these changes probably
had to be done in the driver.


Scanning Triggers
-----------------

As noted in the Method chapter, scanning triggers might be worthwile to 
investigate further. Scanning isn't neccesarry to do that often, as the
local access points might not move often enough to warrant a scan.

Instead, something like a trigger to scan only when traffic is low might be a
good idea to investigate for future research.

This could be acomplished by looking at a survey dump, which the linux kernel
provides [@SurveyDump]. A survey dump gives the access point the possibility of
looking at the status of the current channel. This tool provides the amount of 
time that:

 * the channel was active
 * the channel was busy
 * was used to recieve data
 * was used to transmit data
 
By utilizing this data, an implementer can determine when it is a good time to
start a scan based on previous activity levels. By doing this it would be possible
to avoid periods of the day that has heavy useage.
