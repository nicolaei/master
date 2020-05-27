Results
=======

In this chapter I will present my findings, discuss them and elaborate on how
this impacts my problem statement.


<!--
Guiding points while writing:

 * Present my findings
 
 * Organize, classify and analyze the data
 
 * Interpret and explain the findings.
 
 * Check if these findings are in line with what I expected from the work I 
   talked about in the introduction?
-->
   
Access Point Scan results
-------------------------

As mentioned in [Discovery strategies] in an earlier chapter, the access points 
measure the amount of times an access point was discovered against it's percived
strenght.

In this section you'll see the results of the three main different
discovery strategies and how well they picked up the access points that are in 
its proximity.

In the next parts we'll take a look at the following measurement runs:

 * Full Scan
 
 * Selective Scan (channels 1, 3, 5, 7, 9 and 11)
 
 * Selective Scan (channels 1, 6, and 11)
 
 * Smooth Scan (300ms intervals)
 
 * Smooth Scan (600ms intervals)
 
 * Smooth Scan (1200ms intervals)
 
 
<!-- TODO: Write about removing results below 2 discoveries. -->


### Discovery Accuracy

#### Full Scan { .unnumbered }

To start off, we have our base-line: the full scan. As mentioned in previous
chapters. This scan type is, as expected, discovering a lot of access points.
See figure {@fig:fullscanresults} and table {@tbl:amountfull}.

Scan Type                 **AP 0**     **AP 1**     **AP 2**
---------------------     --------     --------     --------
**Full Scan**                54           69           61     

Table: Access points discovered accross all scans accross the 
       different access points for full scan. {#tbl:amountfull}
       
![Access Points Discovered for a "full" scan](static/ap_full_scan.png){ #fig:fullscanresults }

Overall we see that signals without line of sight nicely follows the reighley 
curve. Though there are also some access points that have a high chance of 
discovery, even when their signal strenght is low. These access points most 
likely have line of sight to the access point that is scanning. A naive manual
verification of these access points loaction confirms this. [^manualverify]

[^manualverify]: Manual verification was partly done by looking at the SSID of
the access points and partly by trying to walk around with a WiFi scanner app.
Preferably, we would know the possition of all access points, but the resources
for this wasn't avaliable.


#### Selective Scan { .unnumbered }

Next up we have the selective scan. As expected, this result discoveres less 
access points but took less time overall. The first test, scanning channels 1,
6 and 11, discovered the least amount of close access points. These access points
were probably on a separate channel during our scan.

An alternative selective scan implementation, which results are found in figure
{@fig:selectivescanresultalt}, scans every other channel instead. This also takes
shorter time than the other discovery methods, but still does not discover
all the access points avaliable.

Out of all the scanning methods, selective scan is thus the least performant, but
has a significant speed increase.

In {@sec:channeloverlap} we took a look at how channel overlapping might help
our results in the selective scanning, but it seems like this might not be the
case in this implementation, which can be seen by looking at the amount of access
points discovered.

Unfortunattely it is hard to pinpoint excactly why we're not getting the benifits
of channel overlapping. It might be because of driver or hardware implementation
that is filtering out signals from adjacent channels.

Channels Scanned          **AP 0**     **AP 1**     **AP 2**
---------------------     --------     --------     --------
**1, 6, 11**                 30           27           29 
**1, 3, 5, 7, 9, 11**        26           18           32 

Table: Access points discovered accross all scans accross the different 
       access points for selective scan. { #tbl:amountselective }

\begin{figure}
  \centering
  
  \begin{subfigure}{.75\textwidth}
    \centering
    \includegraphics[width=\textwidth]{static/ap_selective_main_scan.png}
    \label{fig:selectivescanresultsmain}
    \caption{Channels 1, 6 and 11}
  \end{subfigure}
  
  \begin{subfigure}{.75\textwidth}
    \centering
    \includegraphics[width=\textwidth]{static/ap_selective_alt_scan.png}
    \label{fig:selectivescanresultsalt}
    \caption{Channels 1, 3, 5, 7, 9 and 11}
  \end{subfigure}
  
  \label{fig:smoothscanresults}
  \caption{Access points discovered for selective scan accross all three access points}
\end{figure}


#### Smooth Scan { .unnumbered }

In the next three figures, we will take a look at smooth scanning from 300 to 1200 ms
intervals.

In table {@tbl:amountsmooth}, as well as in {@fig:smoothscanresults} we can see
that the interval doesn't have a significant impact on discovery. Arguably, the
difference between them is within a margin of error that can be expected from
the changing environment that the measurments were conducted in. E.g. some of
the external access points could probably have been obstructed by items within
an apartment or something similar.

Overall, the performance here is quite good. Though as discussed in the section
on Smooth Scanning in [Possible Measurement Strategies and Discovery Methods],
the time it took to run these scans is significantly longer. We will be looking
more into the timing differences in the next section.

Interval         **AP 0**     **AP 1**     **AP 2**
------------     --------     --------     --------
**300 ms**          49           47           44
**600 ms**          43           50           52
**1200 ms**         43           40           48

Table: Access points discovered accross all scans accross the 
       different access points for smooth scan. { #tbl:amountsmooth }

\begin{figure}[p]
  \centering
  
  \begin{subfigure}[b]{.75\textwidth}
    \centering
    \includegraphics[width=\textwidth]{static/ap_smooth_300_scan.png}
    \label{fig:smoothscanresults300}
    \caption{300ms interval}
  \end{subfigure}
  
  \begin{subfigure}[b]{.75\textwidth}
    \centering
    \includegraphics[width=\textwidth]{static/ap_smooth_600_scan.png}
    \label{fig:smoothscanresults600}
    \caption{600ms interval}
  \end{subfigure}
  
  \begin{subfigure}[b]{.75\textwidth}
    \centering
    \includegraphics[width=\textwidth]{static/ap_smooth_1200_scan.png}
    \label{fig:smoothscanresults1200}
    \caption{1200ms interval}
  \end{subfigure}
  
  \label{fig:smoothscanresults}
  \caption{Access points discovered for smooth scan results
           accross all three access points}
\end{figure}


### Timing

As expected, there are major timing differences between the different scannning
methods. Table {@tbl:timing} outlines the mean times for every scan method.

Scan Type                        Time
--------------------------       ------
**Full Scan**                    3.47s
**Selective Scan (1, 6, 11)**    0.18s
**Selective Scan (Skip 1)**      0.35s
**Smooth Scan (300ms)**          4.98s
**Smooth Scan (600ms)**          8.88s
**Smooth Scan (1200ms)**         17.62s

Table: Mean total time for completing a scan {#tbl:timing}

For each of these scan types, the standard deviation of the total time taken is
rather low at just a $+-10$ milliseconds appart. This is rather insignificant.

In addition to this, it's worth noting that while smooth scans take significantly
longer to complete, they don't spend all that time actually scanning. For each of
the smooth scans only 

$$timeSpent - (channelsScanned * interval)$$

seconds are spent on doing the actuall scanning. Using this information, we can
recalculate the mean timings above.

Scan Type                        Time
--------------------------       -----
**Full Scan**                    3.47s
**Selective Scan (1, 6, 11)**    0.18s
**Selective Scan (Skip 1)**      0.35s
**Smooth Scan (300ms)**          1.68s
**Smooth Scan (600ms)**          2.28s
**Smooth Scan (1200ms)**         4.42s

Table: Mean total time for completing a scan
       (adjusted for scanning intervals) {#tbl:alttiming}

With this in mind, we can see that table {@tbl:alttiming} shows results that are
more similar to each other.

\todo{
    Hmm, it's strange that these timings are so seemingly unrelated. Maybe do
    another run with the access points to verify this? These timings were measured
    independent of the main scan runs anyways.
}


### Interpreting and analyzing the results

The five scanning algorithm result-sets for the access points shows how the scans
picked up different access points. As you might notice, the strength of the signal
isn't everything that matters for being able to discover an access point. Two access
points that have the same average signal strength might be discovered less.

This phenomenon is most likely because access points that are further away might
be obstructed while others are not. This fits nicely with _Rice_ and _Rayleigh
Fading_ as all measurements have taken place in an urban environment. This will
be clearer once we look at the probability of discovery graphs, where both rice
and raleigh curves have been added to further show this.

As expected, the different discovery methods take different amounts of time to
execute. These findings reflect findings of previous studies, for example where
smooth scanning is slower than alternative discovery methods. Though in the end,
this doesn't have an impact on our results, but it is worth to highlight in cases
where this thesis is used in solutions where measurement time is critical.

\todo{
    While I believe that this statement is true, this has to be confirmed when I have
    the graph. Confirm that the timing has no effect on the actual results by looking
    at the final graph.
}




### Comparing the results

![Comparison of results between all discoveries](static/ap_all.png){#fig:all-discoveries}

In [@fig:all-discoveries] you can see that 

 *   Compare the results that were shown off above

     *   Which results are most promising?

     *   Are any of them worse than the others?


Client Latency Results
----------------------

The latency is where the results get more interesting. In this subsection we'll take
a deep dive in how the different discovery methods affect the clients on the network.

A quick recap: As mentioned in [Measuring Points], the client's are measuring both
latency and goodput to the access point. This should give us a good overview of
how the scans affect the clients.

\todo{
    So far only latency has been measured! Need to measure goodput as well.
}

For all of these results, you'll see the latency graphed every 250ms, and a
blue vertical line that indicates every time a scan is triggered by the access point.
Be aware that this blue line isn't 100% accurate due to some issue with clock-skew
on my Raspberry Pi's. This should however _not_ affect the results at all, these
lines are only indicators to help finidng when a scan happened. 


### The results 

\todo{
    Show close-ups of a single scan for each graph type
}

Like the [Access Point Scan results], I will be starting off with our baseline:
the full scan. In the excerpt from the full scan, you'll notice that the latency
hovers between 100 and 150 ms for quite a few seconds, which is quite substantial
for real time applications such as VoIP and online video games.

![Client impact for "full" scan](static/cli_full_scan.png)

Selective scanning decreases the max and average latency that the client will
experience, which echos [@citation] that states that latency lineary increeses
for each channel scanned. This effect can clearly be obeserved here. For example
the scan which only scans 1, 7 and 11 avereages around 50 ms of latency.

![Client impact for a simple "selective" scan on ch 1, 7 and 11](static/cli_selective_scan_1_7_11.png)
![Client impact for a alternating "selective" scan](static/cli_selective_scan_even.png)

Lastly we have the smooth scans which all seamingly hover between 50 and 100 ms
during scan periods. But the smaller inpact in latency is carried on for a bit longer
due to the fact that we have intervals between each scan.

In my results, the latency of of longer intervals than 300ms are seemingly not
effective for minimizing client latency. In some cases, the latency is even
larger than the 300ms run! 

\todo{
    Analze how much longer each scan runs by looking at only a single scan.
}

\todo{
    Check for packet loss in the scans!!!
}

![Client impact for a "smooth" scan with 300ms intervals](static/cli_smooth_300_scan.png)
![Client impact for a "smooth" scan with 600ms intervals](static/cli_smooth_600_scan.png)
![Client impact for a "smooth" scan with 1200ms intervals](static/cli_smooth_1200_scan.png)
    

### Comparing the results

\todo{
    Create a graph or table comparing max latency peaks and their duration for each
    scanning method. This can include mean and avg of the max latencies. That should
    be the easiest to implement as we have the when the scan happens.
}

 *   Compare the results that were shown off above

     *   Which results are most promising?
    
     *   Which results are to be avoided?


A full comparison between AP and Client results
-----------------------------------------------

In this section I will be looking at the results, keeping in mind the results of both
the Access Point discovery and the Client side impact.

