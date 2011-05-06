Narcissus - Realtime visualizations of web server hits
------------------------------------------------------
.. figure:: narcissus/raw/master/moksha/public/narcissus/images/narcissus-caravaggio.jpg
   :align: right
   :scale: 50 %
   :alt: Narcissus wastes a bunch of time.

   Narcissus wastes a bunch of time.

.. split here

What is this?
-------------
This is ``narcissus``.  It is a web application that visualizes web server hits
as they happen in real time.

Features:

* IP addresses converted to latitude/longitude, then streamed via
  `orbited <http://http://orbited.org/>`_ and plotted on `polymaps
  <http://polymaps.org/>`_.
* Realtime graphs of url-hit distribution with `jQuery flot
  <http://code.google.com/p/flot/>`_.
* Colorized raw logs streamed to the browser by way of `ccze
  <http://freshmeat.net/projects/ccze/>`_ and `ansi2html
  <http://pypi.python.org/pypi/ansi2html>`_.
* `AMQP (Advanced Message Queueing Protocol)
  <http://www.amqp.org/confluence/display/AMQP/Advanced+Message+Queuing+Protocol>`_
  from logs to browser.
* **Fast**.  Little to no handshaking overhead.

The Story
---------
``narcissus`` was written on April 15th, 2011 at the `hackfest` hosted by the
FOSSBox at `Rochester Institute of Technology <http://www.rit.edu>`_.

We knew that `mirror.rit.edu <http://mirror.rit.edu>`_ was cool, fast, and was
the site with the heaviest traffic on RIT's entire network, but looking at a
mirror frontpage or silently updating your Linux distribution in the background
is not very flashy--not something to phone home about. We wanted to make
something cool. Something that would show the 'big picture' of the Open Source
world. We feel we did that with ``narcissus``.

The RIT FOSSbox is the launch pad for all things Free & Open Source Software
(FOSS) at RIT. It is parented both by the `Center for Student Innovation
<http://www.rit.edu/academicaffairs/centerforstudentinnovation/>`_ (physically)
and the `Lab for Technological Literacy's <http://ltl.rit.edu>`_ `FOSS@RIT
Initiative <http://foss.rit.edu>`_ (virtually). They have great `staff
<http://foss.rit.edu/people>`_, `mentors <http://foss.rit.edu/mentors>`_, and
students who all work on `amazing stuff <http://foss.rit.edu/projects>`_.  If
you read their `history <http://foss.rit.edu/history>`_ you can learn all sorts
of neat things about their work on the One Laptop Per Child project.

The ``narcissus`` authors got together and got the proof-of-concept (and some
bling-bling) working in a single afternoon but really it was the space, time,
and environment provided by the FOSSbox that made it possible.

This project could **not** have happened without the hard work of `Remy
DeCausemaker <https://opensource.com/users/remyd>`_, the "FOSSBoss" and
backbone of the FOSSbox. He and his students have made countless contributions
at cost to self that push the limits in the art of software development and
code culture on campus, and should be recognized therefore. Together with `Luke
Macken <http://lewk.org>`_, `RJ Bean <http://threebean.wordpress.com`_, the
power of `Moksha <http://fedorahosted.org/moksha>`_, and the support of the
Grey Beards, RIT has become a real center of gravity for the FOSS Movement.

Live Demo
---------
You can see ``narcissus`` running live at `narcissus.rc.rit.edu
<http://narcissus.rc.rit.edu>`_.

The Research Computing department at the Rochester Institute of Technology runs
that ``narcissus`` instance.  It is pointed at their **very** active `FOSS mirror
<http://mirror.rit.edu>`_.  (That site is the highest-traffic site at RIT!)

Source
------
Get the source from `github.com <http://github.com/ralphbean/narcissus>`_.

Running
-------
On your machine that will host `narcissus`, say, ``monitoring.host.org``,
create ``~/.fabricrc`` with the following content::

    narcissus_source_location = ~/narc/narcissus
    moksha_source_location = ~/narc/moksha

Then run the following commands::

    $ mkdir narc && cd narc
    $ git clone git://github.com/ralphbean/narcissus.git
    $ git clone git://github.com/ralphbean/moksha.git

    $ sudo yum -y install fabric

    $ cd moksha
    $ fab -H localhost boostrap
    $ sudo service qpidd start

    $ cd ../narcissus
    $ fab -H localhost install

    $ cd ../moksha
    $ fab -H localhost restart

In the same place, you may want to run the following command, which can help you
figure out what's up (if anything is 'up')::

    $ fab -H localhost wtf

Finally, on the machine that is being monitored, say, ``monitored.host.org``,
run the following to setup the narcissus `sending` script::

    $ sudo su -
    $ yum install inotail python-qpid

    $ mkdir narc && cd narc
    $ git clone git://github.com/ralphbean/narcissus.git

And to run it and send stuff to your `monitoring` host::

    $ inotail -f /var/log/lighttpd/access.log | \
        ./narcissus/scripts/amqp-log-sender.py --target=monitoring.host.org

``inotail`` is faster than ``tail``, btw.

Gotchas
-------
- Watch out for iptables on ports 9000, 5672, 8080, and 8000.

IRC
---
Try us in ``#moksha`` on ``irc.freenode.net``.

Authors
-------
* Ralph Bean <ralph.bean@gmail.com>

  * `threebean.wordpress.com <http://threebean.wordpress.com>`_

* Luke Macken <lmacken@redhat.com>

  * `lewk.org <http://lewk.org>`_

* Lee Burton <lburton@mrow.org>

  * `mrow.org <http://mrow.org>`_


.. split here

Powered by
----------
.. image:: narcissus/raw/master/moksha/public/narcissus/images/moksha.png
   :align: left
   :scale: 100 %
   :alt: Moksha
   :target: https://fedorahosted.org/moksha/
