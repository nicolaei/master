---
title: Master Essay
date: 2019-07-30
author: Nicolas Harlem Eide
---


Introduction
============

With this essay, I intend to take a look at a subsection of a larger project
addressing interference in 802.11 wireless networks. This project tries to 
solve the problem with a decentralized algorithm where every access point in 
a given neighborhood discovers each other and communicates over backhaul.

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
