Requirements and Problem Areas
==============================

Simply scanning the local topology may sound like a simple endevour, but there
are some caviats that need to be considered to get accurate results while still
letting clients use the network freely.

In this chapter we will take a quick look at conserns and problems that need
to be thought about when selecting and implementing strategies for scanning as
well as requirements that have to be mett to keep a level of service for clients
and access points.

Requirements
------------

Now we will be taking a look at what requirements we need to forfill to keep our
promise of keeping scanning accuracy high while effecting the clients as little
as possible.


### Do client's have to rediscover the access point?

When an access point switches channels, will all its clients will lose 
connection and have to re-discover and re-connect to the access point?
If an access point scans channels for to long, the client might end up thinking
that the connection is lost and try to go trough a scan of it's own to reconnect
to the network. This can increse used airtime on the network with unnececary
management packets, and lead to lower bandwidth for all clients.

If this does become a problem, it might be extra important to schedule scans
at optimal times of day with little network traffic.

### Can the access point send data while scanning?

If it is not possible for the access point to send data while scanning, then
another problem will arise: *How can we make sure that the client's are able
to continue using the network when the clustering algorithm asks for the
current status of the network?*.

If we can't transmit og receive data during the whole duration of the scan,
we might even need to schedule the discovery period to periods where the
network is less utilized, or find a way to decrease the consecutive time that is
spendt scanning.

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


