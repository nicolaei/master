------------
Introduction
------------

In this thesis, I intend to take a look at a subsection of a larger project
addressing interference in 802.11 wireless networks :cite:`IEEE802.11`. This
project tries to solve the problem with a decentralized algorithm where every
access point in a given neighborhood discovers each other and communicates
over back haul. The algorithm will assign a channel, and antenna power output,
to each access point, to minimize interference.

What this thesis aims to solve is scanning the local area for active
wireless nodes, so that the algorithm can do it's work.


Thesis definition
=================

.. todo::

    Define the thesis


Motivation
==========

.. todo::

    What is the motivation behind this thesis?

     * Helping the main project!

Scope
=====

In this section I'll be discussing whats is and what is not in the scope of
this thesis. The goal, as discussed in the introduction, is to find a way to
give the channel allocation all the information it needs to select the best
channel for a given access point.

Outside of the scope
--------------------

The following is not in the scope of this thesis.

Hardware-spesific solutions
###########################

.. todo::

    Cite some article that has a hardware specific solution?

Hardware-specific solutions will not be looked into in this article, as the
aim is to use existing infrastructure and equipment to implement the algorithm.
In addition to this, hardware spesific solutions will be more costly for vendors
and can thus be unfavorable.
