Future Work
============

This chapter outlines similar approaches and other work that can build on the
findings in this thesis.

Caching
-------

Using a cache might be beneficial to lower the time used for the total scan and
is something that might be useful to look at.

This approach is based on an assumption that access points rarely or never move,
and that new access points are rarely introduced [^mobile-aps].

[^mobile-aps]: Mobile access points in the form of smart phones might become
    more prevent in the future, and they might not have a strong enough signal
    to actively cause a problem for other clients on the network. Though this is
    just a hypothesis, so more research has to be done to confirm this.


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

As noted in [Possible Measurement and Discovery Strategies], using a minimum and
maximum channel to shorten scan times might be helpfull to further improve the 
client latency. 

Originally there were two strategies outlined for this thesis, but due to
implementation constraints these were not tested. By looking at documentation
found on `iw`'s page on the linux kernel documentation [@iw], these changes 
probably has to be done in the driver.


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
to avoid periods of the day that has heavy Wi-Fi usage.


Improving channel selection by checking channel congestion
----------------------------------------------------------

While this thesis mainly looked at how to do scanning while not impacting client
latency, there are more methods that probably can be experimented with to further
improve channel selection. Looking at the congestion on a given channel in addition
to the amount of access points on it might yield even better results for channel
selection.

By using the _survey dump_ that was outlined in the previous section, future work 
can measure the usage of a given channel. Using this information together with 
the amount of access points that are active on the channel can help the channel
allocation algorithm to more intelligently select a channel that is both least
populated and least congested.


Using neighbour reports
-----------------------

In IEEE802.11k, a feature called "neighbor reports" were added to speed up scanning.
These reports enable clients to send a request to their access point for a report
about neighboring APs [@CiscoNeighborReport].

While this is mainly aimed at client to access point, rather than access point
to client or access point to access point, it might be worth investigating if 
this is feasable to use for an even more detailed overview of the local 
wireless space.
