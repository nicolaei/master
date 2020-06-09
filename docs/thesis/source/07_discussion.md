Discussion
==========

\todo{
    Alternative title: "Scanning from the access point with minimal impact"
}

Now we will be discussing the results from the previous chapter. We will be
looking into how this relates to and reflects the theory and earlier research 
that has been presented, as well as how these discoveries might be used in future
applications and research. 


Increasing accuracy with multiple scans
---------------------------------------

As we've seen from the [Access Point Scan Results], an AP is not guaranteed to
be discovered with a single scan [^fading]. Thus, it neccesary to have multiple 
scan passes to increase the likelyhood of discovering all access points that 
needs to be taken in account when choosing a channel.

[^fading]: As discussed in earlier chapters and seen in the results, the curves 
that determine the likelyhood of discovery can be explained with the _Reighley_ 
and _Ricean_ fading models.

The amount of passes that needs to be run needs to be determined on a per deployment
basis. The characterisitiscs of the local radio environment for every deployment
might vary slightly and there is a performance-to-accuracy benifit that needs
to be accounted for; Is it most important to not disturb clients or to get a
detailed image of the local network?

However, it is worth noting that scanning multiple times might cause an even
more noticable negative impact on clients if a non-optimal scanning strategy such 
as full scan is used. Multiple stutters can become rather notisable and annoying
for users. To leviate this, an implementation can either spread the scan pases
over a longer time period, or even better: utilize a more optimal scanning strategy
such as smooth scanning.


Temporal spread of channel scanning with smooth scan
----------------------------------------------------

As hyphotezised, spreading the scanning of channels temporally by adding a
backoff period between each channel proved to keep client latency low, while
keeping similar results as the full scan. This reflects the findings in
[@PracticalSchemes] rather nicely, where they found that when employing smooth scan
in client scanning, packet loss and delay will be greatly reduced. [^noteonpacketloss]

[^noteonpacketloss]: Regarding packet loss, it is worth keeping in mind that none
of the scans in the results showed any sign of packet loss due to scanning.
[@PracticalSchemes] was written in 2007, so buffer overflow in clients and access
points might have been more of an issue back then than now.

It is however worth reinstating that there might be micro latency issues that the
results might not highlight due to the variablity in the environment. This should
probably be looked into by futher research. 

Though all in all, these results do seem to reflect nicely on the problem statement
that was defined in the introduction. It is possible to scan the wireless network
without affecting the clients.

### Access Point Accuracy

As shown in the resutls, the discovery accuracy of the smooth scan was comparable
to the full scan implementation. This, together with the fact that smooth scan 
had a minimal impact on the client's performance, this strategy seems like a good 
way to conduct scans from access points.
 
 * Smooth scan has comparable results to full scan in relation to amount of
   neighbouring access points discovered.
   
    * Anecdotally, most applications of access points doesn't require a the scan
      results to be quick. In clients, this requirements is there because mobile
      devices need to find a new access point while on the move. Having a 20-30
      second gap where there is no connection is not acceptable in those situations.
      
    * It would however not be a good idea to spread the scans over a to long
      timespan, even though it is possible. This is because that if the
      environment was to change
      
    * *Weakness of smooth scan*: In situations where there are a lot of mobile
      access points (for example in a cafe or in an outdoors environment), the
      scan might get corrupted data if the scan goes on for too long. Mobile
      access points might come in to view for a few seconds. 
      
        * Due to this, the access point might want ****to do multiple scans before
          switching channels to get a more accurate reading of the local network.
          
            * This should not affect clients, as we have discovered, smooth scanning
              from an access point has minimal impact on the clients that are
              connected to it.


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