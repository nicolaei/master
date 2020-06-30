Requirements and Problem Areas
==============================

Scanning the local topology may sound like a simple endevour, but there are some
caveats that need to be considered to get accurate results while still letting
clients use the network freely.

In this chapter we will take a quick look at concerns and problems that need
to be thought about when selecting and implementing strategies for scanning as
well as requirements that have to be met to keep a level of service for clients
and access points.

Quality of Service 
------------------

The main job of an access point is to be an uplink to its clients. When a user
is using their computer they expect that they don't lose connectivety in the
middle of a large download or in a voice meeting with an important client.
Because of this, keeping a good _quality of service_ will be a major concern.

Due to the nature of what we're trying to implement here, there are some
concerns regarding keeping this quality of service.

For example when an access point switches channels, will all its clients 
lose connection and have to re-discover and re-connect to the access point?
If an access point scans channels for to long, the client might end up thinking
that the connection is lost and try to go through a scan of its own to reconnect
to the network. This can increase used airtime on the channel with unnececary
management packets, and lead to lower bandwidth for all clients. Which again 
might also affect the results of the scans that we are trying to do in the first
place.

If this becomes a problem, it might be extra important to schedule scans
at optimal times of day with little network traffic.

In addition to this, if it is not possible for the access point to send data 
while scanning, then another problem will arise: *How can we make sure that the
clients are able to continue using the network when a channel allocation 
algorithm asks for the current status of the network?*.

If we can't transmit or receive data during the whole duration of the scan, we 
might need to schedule the discovery period to when the network is less utilized, 
or find a way to decrease the consecutive time that is spent scanning.


Scan Accuracy
-------------

Making sure that our scans accuratly depict the local area is also important.
Because, if our scan data is missing important access points the following
channel allocation algorithm might choose a sub-optimal channel for our access point.

To resolve this issue, the scan accuracy is of uttermost importance as well.

To keep scanning accuracy high, it might mean that we need to spend more time on
scanning. For example, in the case that multiple access points are trying to do
a scan of the network at the same time, our program might need to do multiple
scanning passes to be certain that it collects information about all the other
access points.


Weighting requirements against each other
-----------------------------------------

_Scan accuracy_ and _quality of service_ create two opposing forces. To be more
accurate we might have to do more scanning (which will be discussed in later 
chapters), while quality of service might suffer from the increased scanning activity.

The combination of these two requirements is a parameter that needs to be thought
about to make sure that optimal results are achived in a real world implementation.
