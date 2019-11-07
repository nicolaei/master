Scanning
========

.. todo::

    Remember to add how I'll be scanning. Could be ResFi.

To accomplish the scanning I will be using Python 2.7 together with *some
library or something else*.

The aim of doing the scanning is to be able to share information about our
local network with the clustering algorithm. Without this information, the
algorithm won't be able to accurately create clusters.

Possible problem areas
----------------------

While just doing a scan might sound like a simple project, but there are a
few parameters that needs to be considered to make sure that the program does
not interrupt the clients.

Client's have to rediscover the access point
#############################################

.. todo::

    Find a citation for the fact that clients will lose their connection when
    the access point switches channel.

    Also, a bit clunky language here :(

    Maybe the title of this section should be a question to be consistent
    with the other subsections?

When the access point switches channels, all it's clients will lose connection
and have to re-discover and re-connect to the access point
:cite:`Citation Needed`. If the access point switches channels to quickly,
the clients may end up losing connection for such a long time that it might
become an annoyance to the users. To leviate this, I will have to figure out
what the best possible time period is.

Can the access point send data while scanning?
##############################################

If it is not possible for the access point to send data while scanning, then
another problem will arise: *How can we make sure that the client's are able
to continue using the network when the clustering algorithm asks for the
current status of the network?*.

If we can't transmit og receive data during the whole duration of the scan,
we might even need to schedule the discovery period to periods where the
network is less utilized.

What if some other access points are also scanning?
###################################################

.. todo::

    I'm not quite sure about this section. I need to find some literature or
    do some measurements that support that access points that are scanning
    might not be able to do RX or TX.

    The program is also going to be using active beacons, so maybe this needs
    to be rephrased?

In the case that multiple access points are trying to do a scan of the network
at the same time, our program might need to do multiple passes to be certain
that it collects information about all the other access points around it.

Because of this, I'll have to figure out:

*   How many passes are enough to be certain that we've collected information
    about all other access points in our neighbourhood?

*   Is it possible to be more smart about the scanning? Can - for example -
    some randomization of when the scan happens or be used?


Getting the scanning up and running
-----------------------------------

.. todo::

    Do the actual scanning
