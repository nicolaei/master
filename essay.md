---
title: "Using ResFi for distributed discovery of a local wireless network"
subtitle: "A part of a larger project for better channel assignment in WiFi"
date: 2019-07-01
author: Nicolas Harlem Eide
documentclass: ifimaster 
---


Introduction
============

With this essay, I intend to take a look at a subsection of a larger project
addressing interference in 802.11 wireless networks [@IEEE802.11]. This project 
tries to solve the problem with a decentralized algorithm where every 
access point in a given neighborhood discovers each other and communicates 
over back haul.

The algorithm will assign a channel and antenna power output to each access 
point, to minimize interference.

What this thesis aims to solve is scanning the local area for active
wireless nodes, so that the algorithm can do it's work.

The problem
-----------

There are two main issues I'll have to look at while trying to find a 
solution to the task at hand.

**How can we scan the network with minimal disruption to the connected 
  clients?**

This can be split into some sub-questions:

*   Can we do measurements and act as an AP at the same time?

*   How can we scan the network without filling the local space with probing 
    requests?

*   How do we scan the local network with minimal disruption to the connected
    clients?

There is also another question that has to be solved, related to the minimal 
disruption question:

**How do we pass information about the network between routers?**

This question also have a few sub-questions "built in".

*   How can we pass possibly large-ish amounts of information with as little 
    data as possible?

*   Can we ensure that the data we're receiving is correct?
    Someone might have ill intent when answering our probe requests


Methods and Technologies
========================

Quantitative measurements will be utilized to answer the questions in 
[the outlining of the problem](#The problem). This will be done by creating a
physical network with live WiFi routers.

To actually solve the problem, I will be using the following technologies:

*   [Bloom filters] - A compact and efficient way of knowing what data is *not* 
                      present.
                  
*   [ResFi] - A python framework for communicating with other nodes trough
              back haul.

Bloom filters
-------------

I will experiment with bloom filters [@bloom-filters] to exchange data about 
the local wireless network between nodes.

Bloom filters are useful as they're able to reduce network look-ups for 
non-existent keys in the set of nodes. If a key isn't in the bloom filter, 
it's definitily not on the network. But there is still a chance of false 
positives [@bloom-filter-explenation].

This might sound like a standard hash map, but it is not. The difference is that 
Bloom filters have a smaller footprint as they don't store the elements 
themselves. Instead, they check if a value is *certainly not* present.

ResFi
-----

ResFi is a Python framework for enabling creation of distributed Radio 
Resource Management (RRM) functionality in Residential or residental 802.11 
WLAN deployments. It uses the radio interface of all APs to efficiently 
discover adjacent ones. After this initial discovery, the APs public IPs are 
exchanged and a connection is made via the southbound interface [@resfi].

As ResFi is a Python framework, any code in this project will be 
developed with Python. 


Existing Works
==============

There are some existing work covering ResFi and distributed orchestration 
that I intend to utilize in this thesis.

Understanding the Role of Active Scans For Their Better Utilization In Large-Scale WiFi Networks [@active-resfi-scans]
----------------------------------------------------------------------------------------------------------------------

This article focuses on how active scanning, which is one of the main 
components of ResFi's discovery phase, might affect the local WLAN's 
performance.

It highlights:

*   that  active scans increase latency quite a lot for _all_ clients on a 
    network, and that this latency will even stay for a few seconds after the
    actual probe request [@active-resfi-scans p. 32]. Which will not play out
    nicely on high impact WiFi deployments [@active-resfi-scans p. 121].
    
*   that all current solutions to decrease scanning delays require some 
    change to hardware or driver [@active-resfi-scans p. 123].
  


How do I intend to solve the task?
===================================

With the help of [ResFi] and [Bloom filters] I will hopefully be able to find
a viable solution to establish and sustain communication between access points 
in proximity of each other.

Local Network Discovery Methods
-------------------------------

Evolutionary algorithms might be utilized to find a good model for maximizing
the speed and accuracy of the discovery, while still keeping the possible 
impact from probe requests [@active-resfi-scans] low.

Different enviornments call for differing strategies when it comes to minimizing
the amount of latency introduced from our active scanning, and actually 
discovering what access points live on a given channel. If we're really 
unlucky we might even not discover any accesspoints, because they're all 
scanning for other access points!

Though this could also be over engineering, and any simple algorithm with 
exponential backoff might suffice. Only the measurements will tell!

Needless to say, there is a large chance that we'll have to do multiple scans
on the network to get a true idea about what the local area might look like.

Measuring
---------

With the help of a physical network and emulated networks for testing I will
be measuring what kind of effect my changes are doing, and what the best 
strategy might be.

For emulated networks I'll be working with Mininet, as that is already 
supported by ResFi.