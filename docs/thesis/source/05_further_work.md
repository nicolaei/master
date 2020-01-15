Further Work
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
access points has been removed from the area [^mobile-aps].

This approach might be useful in cases where a centralized or decentralized
system is in charge of channel allocation, rather than the single access point.

[^mobile-aps]: Mobile access points in the form of smart phones might become
    more prevent in the future, and they might not have a strong enough signal
    to actively cause a problem for other clients on the network. Though this is
    just a hypothesis, so more research has to be done to confirm this.
