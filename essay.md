---
title: Master Essay
date: 2019-07-30
author: Nicolas Harlem Eide
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

What this masters thesis aims to solve is scanning the local area for active
wireless nodes, so that the algorithm can do it's work.

The problem
-----------

There is one main issue I'll have to look at while trying to find a 
solution to the problem.

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


Methods and Technologies
========================

ResFi will be the main technology I'll be looking at to solve the task at 
hand. It is a Python framework for Distributed Radio Resource Management of
Residential WiFi Networks [@resfi].

Quantitative measurements will be utilized to answer the questions in 
[the outlining of the problem](#The problem). This will be done by creating a
physical network with live WiFi routers.


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

I intend to solve the task at hand with a few tools:

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
positives (as a bloom filter is a type of hash map) [@bloom-filter-explenation].

This might sound like a standard hash map, but it is not. The difference is that 
Bloom filters have a smaller footprint as they don't store the elements 
themselves. Instead, they check if a value is *certainly not* present.

ResFi
-----

As ResFi is a Python framework [@resfi], any code in this project will be 
developed with Python 3.
