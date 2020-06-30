Results
=======

In this chapter we will look at the findings from the experiments, discuss them 
and elaborate on how this impacts the problem statement.

   
Access Point Scan Results
-------------------------

As mentioned in section {@sec:discoverystrategies}, the access points measure the
amount of times unique access points were discovered against their percived strength.

In this section you will see the results of the three main different
discovery strategies and how well they picked up the access points that are in 
its proximity. For all discovery graphs you will see two curves overlayed. These
show the expected _Rice_ and _Reighley_ fading, which was talked about in 
previous chapters.

In the next sections we will take a look at the following measurement runs:

 * Full Scan
 
 * Selective Scan (channels 1, 3, 5, 7, 9 and 11)
 
 * Selective Scan (channels 1, 6, and 11)
 
 * Smooth Scan (300ms intervals)
 
 * Smooth Scan (600ms intervals)
 
 * Smooth Scan (1200ms intervals)
 
For each of these measurement runs about 100 scans were conducted to be able to
get a good view of how scanning affects both clients performance and access point 
result. In addition to this, the _full scan_ will be used as a baseline due to
it commonly being used in modern Wi-Fi deployments.

### Discovery Accuracy

#### Full Scan { .unnumbered }

To start off, we have our baseline: the full scan. This scan type is, as expected,
discovering a lot of access points. We can see from table {@tbl:amountfull} that
there are a lot of access points in the area where we scanned from.

The numbers from this won't tell us much on their own however. It's first when 
we put them up against the next tests that we will see how the performance of the
other strategies measure up against the full scan. For now, we can assume that 
the amounts for each of the access points are the maximum amount of access points
that can be seen from the location of AP 0, AP 1 and AP 2 respectivly.[^measurement]

[^measurement]: While we can assume that this is around the maximum, as stated in
    the methodic problems section, these tests were done in an appartment in the
    middle of a city so changes might happen between tests.

Scan Type                 **AP 0**     **AP 1**     **AP 2**
---------------------     --------     --------     --------
**Full Scan**                43           56           63     

Table: Unique Access points discovered accross 100 full scans. The columns define 
       the access point that was scanning, and the numbers are the amount of 
       unique access points that were discovered by the given access point.
       {#tbl:amountfull}

In addition to the total amount of access points found, it is also interesting
to see how likely it is that we are to discover an access point, given the percived
signal strength. This relationship can be seen in figure {@fig:fullscanresults},
and in addition we can see the variation in the observed signal strength via the
bars going left to right of each point. These bars are limited to the 95th 
percentile to weed out outliers in the dataset.
       
![Access points discovered for a "full" scan](static/ap_full_scan.png){#fig:fullscanresults}

Overall we see that signals without line of sight nicely follows the reighley 
curve. Though there are also some access points that have a high chance of 
discovery, even when their signal strenght is low. These access points most 
likely have line of sight to the access point that is scanning, which is modeled
by the rice curve. A naive manual verification of these access point's location
confirms this. [^manualverify]

[^manualverify]: Manual verification was partly done by looking at the SSID of
    the access points and corelating them to nearby shops, and partly by trying 
    to walk around with a Wi-Fi scanner app. Preferably, we would know the 
    possition of all access points, but the resources for this wasn't avaliable.

In the sections next sections, about selective and smooth scan, we will be using 
the results from this scan to compare the performance.


#### Selective Scan { .unnumbered }

Next up we have selective scanning. As expected, this result discoveres less 
access points but took less time overall. The first test, scanning channels 1,
6 and 11, discovered the least amount of access points, as seen in table
{@tbl:amountselective}. Quite a few of the access points in the area were on
channels that were not within the specified channels of our scans.

In figure {@fig:selectivescanresultsmain} the top left of the graph is quite 
empty, in contrast to all other result sets. The access points that normally show 
up in this section of the graphs are AP 0 through AP 2, but these were not configured 
to run on channel 1, 6 or 11, which can explain why we do not observe them.

An alternative selective scan implementation, which results are found in figure
{@fig:selectivescanresultsalt}, scans every other channel instead. This also takes
shorter time than the other discovery methods, but still does not discover
all the access points avaliable. In the case of AP 0 and 1 it even discovers less 
than with the approach that only scanned channels 1, 6 and 11. This might be 
because it did not scan channel 6, which is a typical channel for access points 
to use.

Out of all the scanning methods, selective scan is the method that gives the 
worst results, but it has a significant speed increase.

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
**1, 6, 11**              30 (70%)     27 (48%)     29 (46%)
**1, 3, 5, 7, 9, 11**     26 (60%)     18 (32%)     32 (51%) 

Table: Access points discovered accross all scans accross the different 
       access points for selective scan. The percentages are relative to the
       amount of access points found in the full scan. {#tbl:amountselective}

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

Now we will take a look at smooth scanning from 300 to 1200 ms intervals.

These tests seem to perform quite similar as the full scan in terms of the amount
of access points discovered. As can be seen in table {@tbl:amountsmooth}, AP 0
discovers the same amount of access points as our full scan experiment. AP 1 and
AP 2 also performs better than the results in the selective scan, but does not
live up to the results from AP 0. Why only AP 0 discovers the same amount as
the full scan approach is hard to say, but might be because the environment had
changed.

As for the probability of discovery, we're seeing almost exactly the same sort
of results as in the full scan. In figure {@fig:smoothscanresults} we can see
yet again that the results match up with what we'd expect from Reyleigh and 
Ricean fading.

We can also can see that the interval doesn't have a significant impact on 
discovery accuracy. Arguably, the difference between them is within a margin of 
error that can be expected from the changing environment that the measurments 
were conducted in. E.g. external access points could probably have been 
obstructed by items within an apartment or something similar. [^apartmentreasoning]

[^apartmentreasoning]: As mentioned in the section about methodic problems;
the experiments were conducted in an urban environment without control of
most of the access points.

Overall, the performance here is quite good. Though as discussed in the section
on Smooth Scanning in [Possible Measurement and Discovery Strategies],
the time it took to run these scans is significantly longer. We will be looking
more into the timing differences in the next section.

Interval         **AP 0**      **AP 1**     **AP 2**
------------     ---------     --------     --------
**300 ms**       49 (114%)     47 (84%)     44 (69%)
**600 ms**       43 (100%)     50 (89%)     52 (82%)
**1200 ms**      43 (100%)     40 (71%)     48 (76%)

Table: Access points discovered accross all scans accross the 
       different access points for smooth scan. The percentages are relative to 
       the amount of access points found in the full scan. {#tbl:amountsmooth}

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

Scan Type                                   Time
--------------------------------------      ------
**Full Scan**                               0.74s
**Selective Scan (1, 6, 11)**               0.18s
**Selective Scan (1, 3, 5, 7, 9, 11)**      0.35s
**Smooth Scan (300ms)**                     4.98s
**Smooth Scan (600ms)**                     9.19s
**Smooth Scan (1200ms)**                    17.62s

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
**Full Scan**                    0.74s
**Selective Scan (1, 6, 11)**    0.18s
**Selective Scan (Skip 1)**      0.35s
**Smooth Scan (300ms)**          0.78s
**Smooth Scan (600ms)**          0.79s
**Smooth Scan (1200ms)**         0.82s

Table: Mean total time for completing a scan
       (adjusted for scanning intervals) {#tbl:alttiming}

With this in mind, we can see that table {@tbl:alttiming} shows results that are
more similar to each other, but there is still a small difference for smooth scan.
This difference is probably due to implementation overhead.


### Interpreting and analyzing the results

The six scanning algorithm result-sets for the access points shows how the scans
picked up different access points. As you might notice, the strength of the signal
isn't everything that matters for being able to discover an access point. Two access
points that have the same average signal strength might not be discovered the
same amount of times.

This phenomenon is most likely caused by _Rice_ and _Rayleigh fading_. As all
measurements have taken place in an urban environment, the likelyhood of different
objects, cars, or similar moving in the way of the signal and slightly obstructing
the access points is large due to the long time-frame that has been used for these
test. 

In addition to this, the variance in the signals (the horizontal bars) seem to
decrease as they move further towards the lower left in all the experiments.
This is mostly a result of the weak access points only being measured a few
times in total, so the sample size is small. Since the experiments were conducted
over such a long time-frame (a few days), there were a lot of possibilities for
changes in the environment that the experiments were conducted in. Due to this, 
the larger spikes in difference might be as a result of obstructions or similar. 

There is also a difference between AP 0, AP 1 and AP 2 when it comes to the 
relative amount of access points found when compared to the full scan. 
Consistently there is about a 15-30 percentage point difference between the 
results of AP 0, as compared to AP 1 and 2. Again, it is likely that this is 
caused by the difference in environment as the full scan measurements were done 
a few days after the selective and smooth scan runs.

Lastly, as expected, the different discovery methods take different amounts of 
time to execute. These findings reflect findings of previous studies, for example 
where smooth scanning is slower than alternative discovery methods. Though in the 
end, the speed of the scan doesn't have an impact on our results, but it is worth
to highlight in cases where this thesis is used in solutions where measurement 
time is critical.


Client Results
--------------

Now we will be taking a deep dive into how the scans affected the clients. 
As discussed in previous sections about measurement strategies, the clients measured 
both their latency and goodput to the access point they were connected to. This 
should give us a good overview of how the discovery methods affected the clients. 
No scanning was done from the clients during these trails.

For all of these results, you will see the latency and goodput measured whenever
the link was avaliable. In adition you will see a blue vertical line for every
two minutes that represents when a scan finished on the access point that the 
client was connected to. Due to problems with the clock on the Raspberri Pi, 
this is not 100% accurate but still usefull as a guide. This issue is discussed 
in [Methodic problems]. It is worth restating that this issue shouldn't affect our
final results, as the lines are just used as guides. It does however mean that it
will be slightly harder to separate normal noise from the scan impact.


### Overall impact of scanning

To get the best overview possible, we will be looking at both latency and goodput
graphs next to each other as these are closely related.

Seeing that over 100 scans have been conducted for each algorithm, we will be
looking at eight results where enviornmental noise seems to be rather minimal for
each example. This should give us a good overview of the overall impact of the
algorithms, while still being able to weight inn possible variability in the
results.

#### Full Scan { .unnumbered }

In the excerpt from the full scan in figure {@fig:clifull}, you will notice that the 
latency hovers between 100 and 300 ms for over a second, which is substantial for 
real time applications such as VoIP and online video games. Spikes of over 400 ms 
in latency was also observed.

This nicely fits with the results from [@ActiveScanPerformance] where the client 
itself was scanning the local network, and observed the same pattern of latency 
issues while scanning.

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_full_scan_latency.png}
        
        \caption{
            Client latency. The spikes are a result of the access point scanning 
            the network, and thus not allowing traffic.
        }
        \label{fig:clifulllatency}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_full_scan_goodput.png}
        
        \caption{
            Client goodput.
        }
        \label{fig:clifullgoodput}
    \end{subfigure}
      
    \caption{
        Client latency and goodput results for full scan.
    }
    \label{fig:clifull}
\end{figure}

In addition, as expected, the goodput follows suit with the worst spikes ending
up almost hitting zero MB/s of goodput. This is expected as throughput and goodput
is linked to the latency.

#### Selective Scan { .unnumbered }

Selective scanning decreases the max and average latency that the client will
experience, which echos [@SeamlessHandoff] that states that latency lineary 
increeses for each channel scanned.

In the examples for scanning channels 1, 6 and 11 the peak latency ends up being
around half of full scan, hovering at around 100 ms and maxing out at around 
150ms. In contrast to the full scan, the latency spikes are a lot shorter
duration compared to the full scan implementation, which we can see as a clear
benifit in our goodput results.

\todo{Reference to the figures in the paragraph above!}

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_selective_main_latency.png}
        
        \caption{
            Client latency. The spikes here are lower than the full scan, but 
            still severe enough to be noticable for real time applications.
        }
        \label{fig:cliselectivemainlatency}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_selective_main_goodput.png}
        
        \caption{
            Client goodput. The dips in goodput are smaler in this case, 
            but might be noticable for users.
        }
        \label{fig:cliselectivemaingoodput}
    \end{subfigure}
      
    \caption{
        Client latency and goodput results for selective scan on channels 1, 6 and 11.
    }
    \label{fig:cliselectivemain}
\end{figure}

As for the selective scan which skips every even-numbered channel, we can spot
roughly the same results here. The peak latency is hovering around 100 to 150ms,
but the goodput is not hit as badly as the full scan results. However, the 
goodput for this scanning method does end up taking a slightly worse hit than
selective scan on channels 1, 6 and 11.

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_selective_alt_latency.png}
        
        \caption{
            Client latency. The latency spikes seems to show roughly the same 
            pattern as the results for channels 1, 6 and 11. 
        }
        \label{fig:cliselectivealtlatency}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_selective_alt_goodput.png}
        
        \caption{
            Client goodput
        }
        \label{fig:cliselectivealtgoodput}
    \end{subfigure}
      
    \caption{
        Client latency and goodput results for selective scan on 
        channels 1, 3, 5, 7, 9 and 11.
    }
    \label{fig:cliselectivealt}
\end{figure}

Though for both selective scans, there are sometimes scan periods where the 
latency seems to not be affected by the scan. This can be seen in the third last
period of figure {@fig:cliselectivemainlatency} and in the middle of figure
{@fig:cliselectivealtlatency}. Why this is, is unclear. It might have to do with
the environment the scans were conducted in, or due to some fault.


#### Smooth Scan { .unnumbered }

During smooth scan, it seems like clients are largely unaffected by the scans
conducted by the AP it's connected to.

In figures {@fig:clismooth300} trough {@fig:clismooth1200} we can
observe that the latency and goodput results does not have any periodic spikes.
This is in contrast to the observations in the full and selective scan algorithms,
where we can see periodic spikes in latency.

In these results we can only see sporadic spikes in latency and dips in goodput.
It is likely these spikes were results of the environment where we conducted 
the tests or due to RF noise.

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_smooth_300_latency.png}
        
        \caption{
            Client latency. In these results the spikes in latency seems random,
            suggesting that they're caused by the environment or other factors, 
            and not the scanning itself.
        }
        \label{fig:clismooth300laten}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_smooth_300_goodput.png}
        
        \caption{
            Client goodput
        }
        \label{fig:clismooth300good}
    \end{subfigure}
      
    \caption{
        Client latency and goodput results for smooth scan with 300 ms intervals
    }
    \label{fig:clismooth300}
\end{figure}

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_smooth_600_latency.png}
        
        \caption{
            Client latency
        }
        \label{fig:clismooth600laten}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_smooth_600_goodput.png}
        
        \caption{
            Client goodput
        }
        \label{fig:clismooth600good}
    \end{subfigure}
      
    \caption{
        Client latency and goodput results for smooth scan with 600 ms intervals
    }
    \label{fig:clismooth600}
\end{figure}

\begin{figure}
    \centering
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_smooth_1200_latency.png}
        
        \caption{
            Client latency
        }
        \label{fig:clismooth1200laten}
    \end{subfigure}
      
    \begin{subfigure}[b]{\textwidth}
        \centering
        \includegraphics[width=\textwidth,center]{static/cli_smooth_1200_goodput.png}
        
        \caption{
            Client goodput
        }
        \label{fig:clismooth1200good}
    \end{subfigure}
      
    \caption{
        Client latency and goodput results for smooth scan with 1200 ms intervals
    }
    \label{fig:clismooth1200}
\end{figure}


### Interpreting and analyzing the results

We have now looked at how the six different scans have affected the clients. As
expected, the full scan is the worst strategy to utilize from the clients
point of view. It ends up disturbing the client's performance in such a manner
that it would be obvious to any real-time application users.

As we've seen, the selective scan strategies gets shorter and lower spikes of
latency than the full scan. However, the smooth scans ends up stealing the 
show with what looks like no latency introduced by the scanning, regardless of 
parameters used.

This reduction of client latency nicely matches what we've come to expect from
the studies on how clients are affected when they scan ([@PracticalSchemes]), 
as layed out in previous chapters. These results show that with shorter interuptions, 
comes less latency. For smooth scanning this reduced interuption comes from
the fact that there is a break between every channel scanned, while the selective
scan achieved the shorter interuption time by just scanning fewer channels.
