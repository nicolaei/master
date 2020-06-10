Discussion
==========

\todo{
    Alternative title: "Scanning from the access point with minimal impact"
}

Now we will be discussing the results from the previous chapter. We will be
looking into how this relates to and reflects the theory and earlier research 
that has been presented, as well as how these discoveries might be used in future
applications and research. 


Increasing accuracy with multiple scans {#sec:multiplescans}
---------------------------------------

As we've seen from the [Access Point Scan Results], an AP is not guaranteed to
be discovered with a single scan [^fading]. Thus, it is neccesary to use multiple 
scans to increase the likelyhood of discovering all access points that needs to
be taken in account when choosing a channel.

[^fading]: As discussed in earlier chapters and seen in the results, the curves 
that determine the likelyhood of discovery can be explained with the _Reighley_ 
and _Ricean_ fading models.

The amount of scans that needs to be run has to be determined on a per deployment
basis. The characterisitiscs of the local radio environment for every deployment
might vary slightly and there is a performance-to-accuracy benifit that needs
to be accounted for; Is it most important to not disturb clients or to get a
detailed image of the local network?

However, it is worth noting that scanning multiple times might cause an even
more noticable negative impact on clients if a non-optimal scanning strategy, 
such as full scan, is used. Multiple stutters can become rather noticable and 
annoying for users. To leviate this, an implementation can either spread the 
scans over a longer time period, or even better: utilize a more optimal scanning 
strategy such as smooth scanning.


Temporal spread of channel scanning with smooth scan
----------------------------------------------------

As hyphotezised, spreading the scanning of channels temporally by adding a
backoff period between each channel proved to keep client latency low, while
keeping similar results as the full scan. This reflects the findings in
[@PracticalSchemes] rather nicely. In this study they found that by employing
smooth scan in client scanning, packet loss and delay will be greatly reduced.
[^noteonpacketloss]

[^noteonpacketloss]: Regarding packet loss, it is worth noting that none of the 
scans in the results showed any sign of packet loss due to scanning.
[@PracticalSchemes] was written in 2007, so buffer overflow in clients and access
points might have been more of an issue back then than now.

It is however worth reinstating that there might be micro latency issues that the
results might not highlight due to the variablity in the environment. This should
probably be looked into by futher research. 

Though all in all, these results do seem to reflect nicely on the problem statement
that was defined in the introduction. It is possible to scan the wireless network
without affecting the clients.

### Scan accuracy and performance

As shown in the results, the discovery accuracy of the smooth scan was comparable
to the full scan implementation. This, together with the fact that smooth scan 
had a minimal impact on the client's performance, this strategy seems like a good 
way to conduct scans from access points.

\todo{
    The argument in the paragraph below feels kinda week.
}

However, the scans might not show a correct picture of the local environment if
there are a lot of mobile access points in one location. For example at a cafe 
or outdoors. The data from the scan might show a large amount of mobile access
points, and a possible channel selection might be done based on an environment
that might not exist a few hours later. This can probably be leviated by scanning
and switching channels more often, i.e. every hour.

In addition to the accuracy of the results, the time to complete a complete scan
was also recorded in the tests. Smooth scan was the slowest of the three purposed
strategies, but seeing that these scans are done from an access point that won't
be moving, it shouldn't be a problem.

There is an edge case for mobile hotspots, however. Since these access points
are able to move, they need to keep the time to scan lower. In a previous study
on mobile hotspots in urban environments of $50 APs/km^2$, it was found that for 
a mobile hotspot moving at $16.2 km/h$, $32.4 km/h$, $64.8 km/h$ or $97.2 km/h$ 
the optimal scanning periods were 10, 7, 5 or 4 seconds respectively 
[@MobileHotspots]. These timings are well within the measured times of a single 
pass of a smooth scans, but if an implementation chose to run with multiple scans,
as argued in section {@sec:multiplescans}, it might become a problem.

However, it could also be argued that these devices do not benefit from actively
switching between channels, as their environment is constantly changing. 
Especially for mobile devices where battery capacity is limited. Though this is
out of scope for this thesis and should probably be looked into by future research.



### On the issue of time

\todo{
    Find a source to quote about what the requirements for VoIP, games and
    remote vehicle operations are.
}


### The impact of multiple clients
    
 * More research should probably be done with a large amount of clients to
   verify that these results are able to scale.


### In a 5 GHz environment

While the experiments in this thesis only looked at the 2.4 GHz spectrum, it is
likely that these results will be able to transfeer to the 5 GHz spectrum.
However, the time it takes to complete a single scan will increase significantly.

The 5 GHz spectrum offers a greater amount of channels than the 2.4 GHz spectrum,
and with that the time to complete a single run of all channels might pose a
problem. Though, as noted previously, as long as the access point scans multiple
times, this shouldn't pose a problem as potential missing access points from one
scan can be picked up in later scans.

The notion of running multiple scans that take longer time might prove
problematic for applications that are especially time sensitive. Here we're not
thinking about VoIP and similar, but next generation applications that require
especially low latency such as remotely operated veichles. Though more reasearch is
needed in a more predictable environment to see if this is going to be a problem.

\todo{
    Find a citation for how low latency is needed for remotely operated veichles.
    This is just intuition right now and based on what I've heard from 5G marketing
    videos.
}


Optimizing the approach
-----------------------

 * The way I've been doing my scans could be way more optimized by
   doing them in the driver. For example the selective scan ends up (after
   my understanding) switching back and forth between listening and serving
   while scanning. This is because I'm just using the IW tool.
   Though however, the results still show that there is a benifit in client
   latency when it comes to this.
  
 * Move min and max channel time sections from [Future Work] to this chapter?
 
 * Move extra radio operation on a separate channel from [Future Work] to
   this chapter?


<!--
In this chapter you discuss the results of your study/project.

 - Is it possible to generalise?
 
 - Make comparisons with other studies
 
 - Are there alternative explanations?
 
 - What are the strong and weak aspects of the paper?
 
 - What are the practical implications?
 
 - Is more research needed?
 
 - Make recommendations (to be applied in practice).
-->


<!--
Critisism
---------
Valid critisism to my approach can be:
    * The variability in my environment
    * The equipment used might not be optimal.
    * The way I've been doing my scans could be way more optimized by
      doing them in the driver. For example the selective scan ends up (after
      my understanding) switching back and forth between listening and serving
      while scanning. This is because I'm just using the IW tool.
      Though however, the results still show that there is a benifit in client
      latency when it comes to this.
-->

<!--

Recomendations
--------------

-->