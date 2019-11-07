Scanning
========

The aim of scanning in this thesis is to be able to share information about our
local network with the clustering algorithm. Without this information, the
algorithm won't be able to accurately create clusters.

Active- vs passive scanning
---------------------------

Scanning in :cite:`IEEE802.11` is handled via management frames, and can be
done in one of two ways: Active- or passive scanning.

Passive scanning, from a STA's perspective, is simply to listen for
*beacon frames* that are sent out periodically by all APs. These frames contain

 *  *A timestamp*; indicating when the frame was sent (according to the APs
    synchronization timer.

 *  *A beacon interval*; telling the STAs the period between each beacon
    transmission in TUs (a time period of 1024µ).

 *  *The capability information*; Various information about the AP, such as
    it's SSID and more. Extensions to 802.11 has also typically added some
    information to this field.

Active scanning on the other hand is initiated by the STAs themselves. This
process contains two management frames *probe requests* and *probe responses*.

The *probe request* is sent by an STA and either targets a single access point,
or broadcast to all APs. This is done by specifying the target APs SSID in
the frame. Leaving the SSID field empty means that the frame is considered as
a broadcast frame.

*Probe responses* on the other hand are sent by access points that receive the
*probe request*. These frames' content is almost identical to beacon frames,
though they do contain some more information than beacon frames. This
information isn't really relevant for what I wish to accomplish with this
thesis, so I won't outline it.

.. todo::

    Hmmm, not quite sure if I should actually outline what that information
    is, and then say that it's not relevant instead.

.. [*]  Information about active and passive scanning is gathered from
        :cite:`IEEE802.11Handbook`.

