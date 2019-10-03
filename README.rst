Using ResFi for distributed discovery of a local wireless network
=================================================================

Using on Windows
----------------

Because I hate my life, I'm trying to run everything under Windows. Turns out
that isn't so easy :D

You'll have to have the following components:

    * VirtualBox with the supplied Mininet WiFi image
    * PuTTy (For x11 forwarding)
    * VcXsrv (For viewing x11 content)

PuTTy is going to be the tool that does all the X11 forwarding, regardless of
which other terminal you're using. If you're not using PuTTy, you won't be
able to get X11-forwarding working, as it is not supported by PowerShell :(


Running ResFi
-------------

Resfi needs some dependencies that are not in the mininet vm by default.
These arn't specified as needing to be installed in the guide either.

Run :code:`install_deps.sh` to install these dependencies.

Furthermore, you'll also need to edit :code:`framework/config.py`. Change the
line with the option :code:`CONNECTOR="linux"` to :code:`CONNECTOR="mininet"`.