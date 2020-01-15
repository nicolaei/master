Introduction
============

Background
----------

In this thesis, I intend to take a look at a subsection of a larger project
addressing interference in 802.11 wireless networks :cite:`IEEE802.11`. This
project tries to solve the problem with a decentralized algorithm where every
access point in a given neighborhood discovers each other and communicates
over back haul. The algorithm will assign a channel, and antenna power output,
to each access point, to minimize interference.

What this thesis aims to solve is scanning the local area for active
wireless nodes, so that the algorithm can do it's work.


Scope (Problem Statement?)
--------------------------

In this section I'll be discussing what is and what is not in the scope of
this thesis. The goal, as discussed in the introduction, is to find a way to
give the channel allocation all the information it needs to select the best
channel for a given access point.


### What am I trying to figure out?

At a glance it would seem rather simple to find other access points in a
network with a simple scan, but this might not be the case. The implementation
will have to keep network performance and discovery accuracy in mind.

The definition of this thesis is thus:

**How do you scan a IEE802.11 network from an access point without affecting the
performance of the connected STAs while still ensuring accurate results?**


### What problems does this solve?

By being able to scan a network continuously for other access points, it is
possible for any given access point to change channels when needed. This can
help to minimize the package loss and latency introduced by interference,
which is common to see in urban 2.4 GHz deployments where channel availability
is generally low.

This information can also be further shared with other nodes on the network or
a centralized channel allocation system.


### Outside of the scope

\todo{
    Could possibly be in the conclusion or discussion section.
}


The following is not in the scope of this thesis.

#### Hardware-spesific solutions

\todo{
    Cite some article that has a hardware specific solution?
}

Hardware-specific solutions will not be looked into in this article, as the
aim is to use existing infrastructure and equipment to implement the algorithm.
In addition to this, hardware spesific solutions will be more costly for vendors
and can thus be unfavorable.
