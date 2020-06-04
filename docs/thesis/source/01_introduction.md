Introduction
============

Background
----------

Today, only 53.6% the global population is online [@DigitalDevelopment2019]. 
This statistic has been increasing every year, and shows no sign of stopping.
Seeing that most consumer equipment today ship without ports for wired
connections, it's safe to assume that the majority of todays users are using
Wi-Fi as their primary way of connecting to the internet.

Though there are only 12 avaliable channels on the 2.4GHz band, where only three
of these are considered to be "usable" due to channel overlap. The 5 GHz band has
more channels, but suffer from shorter range due to the shorter wavelength, 
so more access points might have to be deployed for good coverage.

Due to a limited amount of channels and an increasing availiability of the internet
in developing countries, as well as urbanization around the world, the Wi-Fi
channels that are avaliable for deployments are getting increasingly congested.

With this problem in mind, it is necessary to figure out how access points can
have a good overview of the local wirless space to select a channel for 
themselves and to collaborate with their peers for channal usage.

\todo{
    Do you have an article I can cite regarding the statement about cooperation
    below @Madeleine?
}

Cooperating on the channel allocation problem outperforms non cooperative methods.
In these methods the channel allocation problem can be considered from a 
graph colouring perspective where the vertices are Wi-Fi networks, and the 
edges are neighbouring networks which interfere with each other. 

In this thesis I aim to figure out how to scan the local wireless topology for
active wireless access points and their signal strength, without affecting
clients connected to the access point. By being able to scan more often,
access points should be able to more easily collaborate between each other in a
decentralized or centralized manner.


Scope
-----

In this section I'll be discussing what _is_ and what _is not_ in the scope of
this thesis. The goal, as discussed in the introduction, is to find a way to
give the channel allocation algorithm all the information it needs to select the
channel for a given access point.


### What am I trying to figure out?

The channel allocation algorithm needs data about neighbouring access points
to figure out which channel the access point should be serving on. To do this
it has to do a scan, but as we will see in later chapters this comes with a cost
of client network performance.

In addition, the scanning algorithm must not sacrifice the accuracy of the results
to achieve this. If only some nearby access points that could cause interference
are found, we risk not improving the network performance after a potential
channel switch, or worse; harming the network performance.

In short, the implementation will have to keep both network performance and 
discovery accuracy in mind.

The definition of this thesis is thus:

**How do you scan a IEE802.11 network from an access point without affecting the
performance of the connected clients while still ensuring accurate results?**


### What problems does this solve?

In urban areas, there are typically a lot of access points competing for the
same radio frequencies. Some access points will automatically select their
channel at random, some will try to do an exhaustive scan of the local area.
Scanning can increase latency with as much as ten-fold in some cases
[@ActiveScanPerformance].

By being able to scan the network _without affecting the
connected clients_ I hope that any future implementers are able to use scanning
to select the best channel for their access point. Another possibility is for
multiple access points to collaborate using this information.


Outline
-----------

Continuing into the next chapters we will be gaining more insight into the world
of scanning in IEEE802.11 and how we can use scans from an access point.

 - **Scanning in IEEE802.11 networks** - How scanning works and current 
   practices within the field

 - **Requirements and Problem Areas** - Further discussing the requirmenents
   that needs to be met when scanning from an access point and possible problems
   that we might face.
 
 - **Possible Measurement Strategies and Discovery Methods** - A look into
   different scanning strategies from existing litterature and how to measure
   if we're meeting the defined requirements.
 
 - **Implementation** - A look into how the experiments were implemented.
 
 - **Results** - The results from the implemented experiments
 
 - **Future Work** - A walktrough of issues and ideas that future works can look at.
 
 - **Conclsion** - Conclusion based on the results and subsequent discussion.

