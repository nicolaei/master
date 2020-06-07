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
   
Access Point Scan Results
-------------------------

As mentioned in [Discovery strategies], the access points measure the amount of
times unique access points were discovered against their percived strenght.

In this section you'll see the results of the three main different
discovery strategies and how well they picked up the access points that are in 
its proximity. For all discovery graphs you'll see two curves overlayed. These
show the expected _Rice_ and _Reighley_ fading, which was talked about in [Scanning
IEEE802.11 networks].

In the next parts we'll take a look at the following measurement runs:

 * Full Scan
 
 * Selective Scan (channels 1, 3, 5, 7, 9 and 11)
 
 * Selective Scan (channels 1, 6, and 11)
 
 * Smooth Scan (300ms intervals)
 
 * Smooth Scan (600ms intervals)
 
 * Smooth Scan (1200ms intervals)
 
For each of these measurement runs about 100 scans were conducted to be able to
get a good view of how scanning affects both clients performance and access point 
result. In addition to this, we will be using _full scan_ as our baseline due to
it commonly being used in modern Wi-Fi deployments.

### Discovery Accuracy

#### Full Scan { .unnumbered }

To start off, we have our baseline: the full scan. As mentioned in previous
chapters. This scan type is, as expected, discovering a lot of access points.
See figure {@fig:fullscanresults} and table {@tbl:amountfull}. The results from
this scan will be used for comparing both selective scan and smooth scan. 

Scan Type                 **AP 0**     **AP 1**     **AP 2**
---------------------     --------     --------     --------
**Full Scan**                54           69           61     

Table: Unique Access points discovered accross 100 full scans for APs 1, 2 and 3. 
       {#tbl:amountfull}
       
![Access Points Discovered for a "full" scan](static/ap_full_scan.png){#fig:fullscanresults}

Overall we see that signals without line of sight nicely follows the reighley 
curve. Though there are also some access points that have a high chance of 
discovery, even when their signal strenght is low. These access points most 
likely have line of sight to the access point that is scanning. A naive manual
verification of these access point's location confirms this. [^manualverify]

[^manualverify]: Manual verification was partly done by looking at the SSID of
the access points and corelating them to nearby shops, and partly by trying to 
walk around with a WiFi scanner app. Preferably, we would know the possition of 
all access points, but the resources for this wasn't avaliable.


#### Selective Scan { .unnumbered }

Next up we have selective scanning. As expected, this result discoveres less 
access points but took less time overall. The first test, scanning channels 1,
6 and 11, discovered the least amount of close access points. These access points
were probably on a separate channel during our scan.

An alternative selective scan implementation, which results are found in figure
{@fig:selectivescanresult}, scans every other channel instead. This also takes
shorter time than the other discovery methods, but still does not discover
all the access points avaliable.

Out of all the scanning methods, selective scan is thus the method that gives
the worst results, but it has a significant speed increase.

In section {@sec:channeloverlap} we took a look at how channel overlapping might 
help our results in the selective scanning, but it seems like this might not be
the case in this implementation, which can be seen by looking at the amount of
access points discovered.

Unfortunattely it is hard to pinpoint excactly why we're not getting the benifits
of channel overlapping, which was talked about in [@APDiscovery]. It might be 
because of driver or hardware implementation that is filtering out signals from
adjacent channels.

Channels Scanned          **AP 0**     **AP 1**     **AP 2**
---------------------     --------     --------     --------
**1, 6, 11**                 30           27           29 
**1, 3, 5, 7, 9, 11**        26           18           32 

Table: Access points discovered accross all scans accross the different 
       access points for selective scan. { #tbl:amountselective }

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth]{static/ap_selective_main_scan.png}
        
        \caption{Scanning channels 1, 6 and 11}
        \label{fig:selectivescanresultsmain}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth]{static/ap_selective_alt_scan.png}
        
        \caption{Scanning channels 1, 3, 5, 7, 9 and 11}
        \label{fig:selectivescanresultsalt}
    \end{subfigure}
      
    \caption{
        Access points discovered for selective scan accross all three access points
    }
    \label{fig:selectivescanresult}
\end{figure}


#### Smooth Scan { .unnumbered }

In the next three figures, we will take a look at smooth scanning from 300 to 1200 ms
intervals.

In table {@tbl:amountsmooth}, as well as in figure {@fig:smoothscanresults} we 
can see that the interval doesn't have a significant impact on discovery.
Arguably, the difference between them is within a margin of error that can be
expected from the changing environment that the measurments were conducted in.
E.g. some of the external access points could probably have been obstructed by
items within an apartment or something similar. [^apartmentreasoning]

[^apartmentreasoning]: As mentioned in the section about methodic problems;
the experiments were conducted in an urban environment without control of
most of the access points.

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
       different access points for smooth scan. {#tbl:amountsmooth}

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth]{static/ap_smooth_300_scan.png}
        
        \caption{300ms interval}
        \label{fig:smoothscanresults300}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth]{static/ap_smooth_600_scan.png}
        
        \caption{600ms interval}
        \label{fig:smoothscanresults600}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth]{static/ap_smooth_1200_scan.png}
        
        \caption{1200ms interval}
        \label{fig:smoothscanresults1200}
    \end{subfigure}
      
    \caption{Access points discovered for smooth scan results
               accross all three access points}
    \label{fig:smoothscanresults}
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


### Interpreting and analyzing the results

The six scanning algorithm result-sets for the access points shows how the scans
picked up different access points. As you might notice, the strength of the signal
isn't everything that matters for being able to discover an access point. Two access
points that have the same average signal strength might not be discovered the
same amount of times.

This phenomenon is most likely because some access points that are might be
obstructed while others are not, which fits nicely with _Rice_ and _Rayleigh
Fading_ as all measurements have taken place in an urban environment. The 
overlayed Rice and Rayleigh curves in the graphs shows this.

As expected, the different discovery methods take different amounts of time to
execute. These findings reflect findings of previous studies, for example where
smooth scanning is slower than alternative discovery methods. Though in the end,
this doesn't have an impact on our results, but it is worth to highlight in cases
where this thesis is used in solutions where measurement time is critical.


Client Results
--------------

Now we will be taking a deep dive into how the scans affected the clients. 
As discussed in [Measurement strategies], the clients measured both their latency 
and goodput to the access point they were connected to. This should give us a 
good overview of how the discovery methods affected the clients.

For all of these results, you'll see the latency and goodput measured whenever
the link was avaliable. In adition you'll see a blue vertical line that represents
when a scan finished on the access point that the client was connected to. Due
to problems with the clock on the Raspberri Pi, this isn't 100% accurate but
still usefull as a guide. This issue is discussed in [Methodic problems]. It is
worth restating that this issue shouldn't affect our final results, as the lines
are just used as guides. It does however mean that it will be slightly harder to
separate normal noise from the scan impact.


### Overall impact of scanning

\todo{
    Show close-ups of a single scan for each graph type
}

To get the best overview possible, we will be looking at both latency and goodput
graphs next to each other as these are closely related.

Seeing that over 100 scans have been conducted for each algorithm, we will be
looking at 8 results where enviornmental noise seems to be rather minimal for
each example. This should give us a good overview of the overall impact of the
algorithms, while still being able to weight inn possible variability in the
results.

#### Full Scan { .unnumbered }

In the excerpt from the full scan, you'll notice that the latency
hovers between 100 and 300 ms for quite a few seconds, which is substantial for 
real time applications such as VoIP and online video games.

![Client latency for full scan](static/cli_full_scan_latency.png){#fig:clifulllatency}

![Client goodput for full scan](static/cli_full_scan_goodput.png){#fig:clifullgoodput}

In addition, as expected, the goodput follows suit with the worst spikes ending
up almost hitting zero MB/s of goodput.

#### Selective Scan { .unnumbered }

Selective scanning decreases the max and average latency that the client will
experience, which echos [@citation] that states that latency lineary increeses
for each channel scanned. This effect can be obeserved here. 

In the examples for scanning channels 1, 6 and 11 the peak latency ends up being
around half of full scan, hovering at around 100 ms and maxing out at around 
150ms. In contrast to the full scan, the latency spikes are a lot shorter
duration compared to the full scan implementation, which we can see as a clear
benifit in our goodput results.

![Client latency for selective (1, 6, 11) scan](static/cli_selective_main_latency.png){#fig:cliselectivemainlatency}

![Client goodput for selective (1, 6, 11) scan](static/cli_selective_main_goodput.png){#fig:cliselectivemaingoodput}

As for the selective scan which skips every even-numbered channel, we can spot
roughly the same results here. The peak latency is hovering around 100 to 150ms,
but the goodput is not hit as badly as the full scan results. However, the 
goodput for this scanning method does end up taking a slightly worse hit.

![Client latency for selective (skip 1) scan](static/cli_selective_alt_latency.png){#fig:cliselectivealtlatency}

![Client goodput for selective (skip 1) scan](static/cli_selective_alt_goodput.png){#fig:cliselectivealtgoodput}


#### Smooth Scan { .unnumbered }

During smooth scan, it seems like clients are largely unaffected by the scans
conducted by the AP it's connected to.

In figures {@fig:clismooth300laten} trough {@fig:clismooth1200good} we can
observe that the latency and goodput results does not have any periodic spikes.
This is in contrast to the observations in the full and selective scan algorithms,
where we can see periodic spikes in latency.

In these results we can only see sporadic spikes in latency and dips in goodput.
It is likely these spikes were results of the environment where we conducted 
the tests or do to RF noise.

![Client latency for a "smooth" scan with 300ms intervals](static/cli_smooth_300_latency.png){#fig:clismooth300laten}

![Client goodput for a "smooth" scan with 300ms intervals](static/cli_smooth_300_goodput.png){#fig:clismooth300good}

![Client latency for a "smooth" scan with 600ms intervals](static/cli_smooth_600_latency.png){#fig:clismooth600laten}

![Client goodput for a "smooth" scan with 600ms intervals](static/cli_smooth_600_goodput.png){#fig:clismooth600good}

![Client latency for a "smooth" scan with 1200ms intervals](static/cli_smooth_1200_latency.png){#fig:clismooth1200laten}

![Client goodput for a "smooth" scan with 600ms intervals](static/cli_smooth_1200_goodput.png){#fig:clismooth1200good}


### Interpreting and analyzing the results

* Why are clients largly unaffected by the scans?

    * Probably due to the timing. Backed up by the results in 
      [@SelectingScanningParameters], [@ProactiveScan], and [@PracticalSchemes].
      
* Why are selective scans way less effected?

    * The linear time difference.
    
    * Future work can confirm how long the time difference is.

* Why are goodput affected by the latency?

    * Because goodput and troughput is a function of data delivered over X time.

