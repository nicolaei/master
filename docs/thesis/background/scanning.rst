Scanning
========

The aim of scanning in this thesis is to be able to share information about our
local network with the clustering algorithm. Without this information, the
algorithm won't be able to accurately create clusters.

Scanning in :cite:`IEEE802.11` is handled via management frames, and can be
done in one of two ways: Active- or passive scanning.

Passive scanning, from a STA's perspective, is simply to listen for
*beacon frames* that are sent out periodically by all APs. These frames contain

 *  *A timestamp*; indicating when the frame was sent (according to the APs
    synchronization timer.

 *  *A beacon interval*; telling the STAs the period between each beacon
    transmission in TUs (a time period of 1024µ).

 *  *The capability information*; Various information about the AP, such as
    it's SSID and more. Extensions to 802.11 has also typically added some
    information to this field.

Active scanning on the other hand is initiated by the STAs themselves. This
process contains two management frames *probe requests* and *probe responses*.

The *probe request* is sent by an STA and either targets a single access point,
or broadcast to all APs. This is done by specifying the target APs SSID in
the frame. Leaving the SSID field empty means that the frame is considered as
a broadcast frame.

*Probe responses* on the other hand are sent by access points that receive the
*probe request*. These frames' content is almost identical to beacon frames,
though they do contain some more information than beacon frames. This
information isn't really relevant for what I wish to accomplish with this
thesis, so I won't outline it.

.. todo::

    Hmmm, not quite sure if I should actually outline what that information
    is, and then say that it's not relevant instead.

.. [*]  Information about active and passive scanning is gathered from
        :cite:`IEEE802.11Handbook`.


Differences between active and passive scanning
-----------------------------------------------

While both active and passive scanning are means to achieve the same result,
they have different impacts on the network and use differing amount of time
to discover all nodes on the network. The impact of them in regards to
discovery latency and network impact is widely studied.



Discovery time
##############

Even though both active and passive scanning will converge towards
discovering all nodes in the network, there is a significant time-difference
between these two approaches. This difference is especially significant in
high density WLAN deployments.

In addition to this there is always going to be some variance in the
discovery time due to the fact that there are always going to be large
variations in the wireless medium. Since multiple STAs share the same medium,
they'll have to share access to the medium.

In :cite:`APDiscovery` the authors analyzed the scanning process in IEEE802.11
networks in an urban setting, which typically means high density of APs in
the given area. The main takeaway from this study is that you'll need
multiple scans to discover as many APs as possible, and even then you're not
guaranteed to find all of the access points in your vicinity.

In their tests, they found that the scanning timer for a probe request
[#timer]_ had a lot to say about your ability to discover other APs. In general,
the longer the timer, the better the chance of discovering other access points.
Though over 100ms the benifit quickly diminish, as very few or no probe
responses were recieved after this time and the discovered APs mainly came
from normal beacon frames.

In addition to the length of the timer, they also found that the amount of
scans mattered a lot to the discovery (see the figure that I haven't added
yet). Even after 100 scans, the study found that up to 15% of all APs were
not discovered.

.. [#timer] Write about scanning timers

.. todo::

    Remember to add figures from :cite:`APDiscovery`!


Network Impact
##############

According to :cite:`ActiveScanPerformance` up to 90% of all probe responses
carry redundant information, and up to 60 percent of all management traffic
in a WLAN can be probe traffic. This is especially true for heavily utilized
channels (over 50% utilization), which typically exist in urban
environments.

This heavy utilization takes a special toll on real time applications such as
VoIP and games. Why? Well, there are two aspects to this: The client-side
impact and the network-wide impact.

The client-side issues with active scans are quite apparent. In
:cite:`ActiveScanPermformance`, they set up a client to run an active scan
every minute. While running these active scans they were continuously pinging
another host over the WLAN to measure the impact these active scans have on
the latency. The result was that every minute, when the active scans where
initialized, a large spike in latency occurred. This spike had a tail of
latency that lasted a few seconds. This kind of latency spike is problematic,
 as it has a impact of real time applications like games and VoIP.

.. todo::

    Add figure from :cite:`ActiveScanPerformance` that shows the spike in
    latency during active scans.

In addition to each individual client, :cite:`ActiveScanPerformance` also takes
a look at how active scanning impacts the network as a whole. The main takeaway
here is that due to the low data rate of probe traffic, it consumes airtime
that could have been better utilized by normal application data.

In networks with low utilization, this might not have shouch a large impact.
But in networks with high utilization, this low data rate traffic will factor
negativly on goodput in the network and will negatively affect other clients
that are not currently scanning.


Channel overlapping
-----------------------------------

In addition to their findings about :ref:`Discovery Time` in
:cite:`APDiscovery`, the authors also highlighted that due to channel
overlapping scanning, say channel 1, will also discover APs on channel 2.

This will help with discovery of access points, since a scan can potentially
discover as many as 40% of APs in adjacent channels. See the figure from the
study for percentages of adjecent channels.

.. todo::

    Figure out if this will be a problem for the clustering algorithm. Will
    it be supplied with false data? Where one AP is reported as being on
    channel 1, while in reality being on channel 2?
