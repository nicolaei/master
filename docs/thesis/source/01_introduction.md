Introduction
============

Today, only 53.6% the global population is online [@DigitalDevelopment2019]. 
This statistic has been increasing every year, and shows no sign of stopping.
Seeing that most consumer equipment today ship without ports for wired
connections, it's safe to assume that the most users today are using Wi-Fi as 
their primary way of connecting to the internet.

And even though there are only 12 avaliable channels on the 2.4GHz band, only three
of these are considered to be "usable" due to channel overlap. The 5 GHz band has
more channels, but suffer from shorter range due to the shorter wavelength, 
so more access points might have to be deployed for good coverage.

Due to the limited amount of channels and the ever-increasing urbanization
around the world, the Wi-Fi channels that are avaliable for deployments are 
getting increasingly congested.

With this problem in mind, it is necesarry to figure out how to give access points
a good overview over the local wireless space in order to select a channel for
themselves or to collaborate with their peers for channel usage.

In this thesis I aim to figure out how to scan the local wireless topology for
active wireless access points and their signal strength, without affecting
clients connected to the access point. By being able to scan more often,
access points should be able to more easily collaborate between each other in a
decentralized or centralized manner.


The problem at hand
-------------------

Any channel allocation algorithm needs data about neighbouring access points
to figure out which channel the access point should be serving on. To do this
it has to do a scan, but as we will see in later chapters this comes with a cost
of client network performance.

In addition, the scanning algorithm must not sacrifice the accuracy of the results
to achieve this. If only some nearby access points that could cause interference
are found, we risk not improving the network performance after a potential
channel switch, or worse; harming the network performance.

In short, implementations have to keep both network performance and discovery
accuracy in mind when scanning the network.

Thus, the definition of this thesis is:

**How do you scan a IEE802.11 network from an access point without affecting the
performance of the connected clients while still ensuring accurate results?**

To solve this problem we will be looking at previous research that has been done
to help clients better scan the local network and applying it to scanning from
access points. Through experiments, we will also be looking at how these methods 
effect the results, and how they impact the clients.

In addition to this we will be discussing probable strategies to further add to
the findings in this thesis, such as when to scan or other methods that can give
access points even more information about the utilization of the local network.


The need for a solution
-----------------------

In urban areas, there are typically a lot of access points competing for the
same radio frequencies. Some access points will automatically select their
channel at random, some will try to do an exhaustive scan of the local area.
This scanning can increase latency with as much as ten-fold in some cases
[@ActiveScanPerformance].

By being able to scan the network _without affecting the connected clients_ it
is possible that future implementers can to use scanning to select more optimal 
channels for their access point. This can help reduce overcrowding on selected
channels by making the acccess points select a channel that is less congested 
at any given time.

Another possibility is for multiple access points to collaborate using this 
information. Earlier studies [@mishra2005weighted] [@baid2015understanding]
have shown that cooperating to solve the channel allocation problem outperforms
any non-cooperative methods.

By thinking of the channel allocation problem from a graph coloring perspective,
where verticies are Wi-Fi networks and edges are neighbouring netwroks which can
interfeer with each other [@mishra2005weighted], multiple access points can 
cooperate to find good channel allocations.

The problems that this thesis aims to solve can help any strategy, cooperative
or otherwise, to get the information they need without disturbing clients with
large interruptions in service during scans. By using the methods tested in this
thesis, any future implementors can hopfully utilize the limited channel space 
in todays network to their full potential.


Outline
-------

Continuing into the next chapters we will be gaining more insight into the world
of scanning in IEEE802.11 and how we can use scans from an access point.

 - **Scanning in IEEE802.11 networks** - How scanning works and current 
   practices within the field

 - **Requirements and Problem Areas** - Further discussing the requirmenents
   that needs to be met when scanning from an access point and possible problems
   that we might face.
 
 - **Possible Measurement and Discovery Strategies** - A look into different 
   scanning strategies from existing litterature and how to measure if we're 
   meeting the defined requirements.
 
 - **Implementation** - A look into how the experiments were implemented.
 
 - **Results** - The results from the implemented experiments
 
 - **Discussion** - Looking at how the results can be utilized
 
 - **Future Work** - A walktrough of issues and ideas that future works can look at.
 
 - **Conclsion** - Conclusion based on the results and subsequent discussion.

