Introduction
============

Background
----------

Today, only 53.6% the global population is online [@DigitalDevelopment2019]. 
This statistic has been increasing every year, and shows no sign of stopping.
Seeing that most consumer equipment today ship without ports for wired
connections, it's safe to assume that the majority of todays users are using
Wi-Fi as their primary way of connecting to the internet.

Though with the increasing availiability in developing countries and increasing
urbanization around the world, the availiable channels for Wi-Fi deployments are
getting increasingly congested.

With this problem in mind, it is necessary to figure out how access points can
have a good overview of the local wirless space to select the best channel
for themselves and to collaborate with their peers for optimal channal usage.

In this thesis I aim to figure out how to scan the local wireless topology for
active wireless access points and their signal strength, without affecting
clients connected to the access point. By being able to scan more often,
access points should be able to more easily collaborate between each other in a
decentralized or centralized manner.


Scope (Problem Statement?)
--------------------------

In this section I'll be discussing what _is_ and what _is not_ in the scope of
this thesis. The goal, as discussed in the introduction, is to find a way to
give the channel allocation algorithm all the information it needs to select the
best channel for a given access point.


### What am I trying to figure out?

At a glance it would seem rather simple to find other access points in a
network with a simple scan, but this might not be the case. The implementation
will have to keep network performance and discovery accuracy in mind.

The definition of this thesis is thus:

**How do you scan a IEE802.11 network from an access point without affecting the
performance of the connected STAs while still ensuring accurate results?**


### What problems does this solve?

In urban areas, there are typically a lot of access points competing for the
same radio frequencies. Some access points will automatically select their
channel at random, some will try to do an exhaustive scan of the local area.
Scanning can increase latency with as much as ten-fold in some cases
[@ActiveScanningParameters].

Implementing my approach can help to minimize the package loss and latency
introduced by interference, which is common to see in urban 2.4 GHz
deployments where channel availability is generally low.

By beig able to scan the network more often - _without affecting the
connected clients_ - I hope that any future implementers can scan more often to
select the best channel for their access point. Another possibility is for
multiple access points to collaborate using this information.

\todo{
    This last paragraph with talk about usecase should be moved to the
    discussion or conclusion.
}
