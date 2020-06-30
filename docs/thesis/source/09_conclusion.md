Conclusion
==========

In this thesis, we have looked at how we can enable active channel selection
by actively scanning the local environment with an access point. We have seen how
three different scanning strategies impact the accuracy of scans, and how these
scanning strategies impact the performance of clients on the network.

In our tests, we have checked the performance and impact of _full scan_, the "normal"
scanning strategy mostly used today; _selective scan_, an optimistic approach that
tries to scan less; and _smooth scan_, a full scan implementation that spreads
scanning of each channel into distinct periods with intervals in between.

Out of these strategies, *smooth scan* is a promesing approach that shows high
accuracy while there is close to no impact on clients. We've seen how this 
approach compares to other two other scanning strategies; *full scan* and 
*selective scan*. The improvements from these two strategies are quite major.
In a full scan scenario, a client had to endure around 150ms latency for over
a period of time, while in the smooth scan scenario the latency during scanning
was close to zero.

As we have also talked about in the discussion and future work, it is possible to 
get even better performance out of these alternate scanning strategies by 
implementing them on the driver level. In adition to this future implementors
can probably improve on these results by modifying the minimum and maximum
channel time (as previously suggested by [@SelectingScanningParameters] and
[@APDiscovery] for client based scans) or even introduce a secondary radio to
use for dedicated scanning of the network (as previously suggested by
[@SeamlessHandoff]).

These results are overall exciting and show that it is possible to give users a
better experience on modern day networks by scanning the network to do active 
channel switching.


References
==========