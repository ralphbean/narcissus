Narcissus - Realtime visualizations of web server hits
------------------------------------------------------

.. figure:: narcissus/raw/master/narcissus/public/images/narcissus-caravaggio.jpg
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
  WebSockets to `polymaps <http://polymaps.org/>`_.
* Realtime graphs of what countries are downloading what content with `d3
  <http://d3js.org>`_.
* `Ømq (zeromq) <http://www.zeromq.org/>`_ on the backend.
* **Fast**.  No polling.

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

There are three processes that make up narcissus:

* The web app that serves the initial map.
* The websocket server, a.k.a the Moksha Hub, that serves the realtime
  data stream
* The data collection script that feeds the Moksha Hub.

The Web App
~~~~~~~~~~~

Set up the WSGI app::

    $ mkvirtualenv narc
    $ pip install narcissus.app

Grab a default config file::

    $ wget https://raw.github.com/ralphbean/narcissus/develop/narcissus.app/development.ini

And start that development-grade web server::

    $ ~/.virtualenvs/narc2/bin/narcissus.app-serve

You can also you apache with ``mod_wsgi`` to serve this if you wanted to do it
more permanently.

.. TODO -- docs on mod_wsgi would be nice.

The Moksha Hub
~~~~~~~~~~~~~~

Assuming you're running the web app and the Moksha Hub on the same
machine, you can share the virtualenv as well and just run::

    $ workon narc
    $ pip install narcissus.hub
    $ ~/.virtualenvs/narc2/bin/moksha-hub

The Data Collection Script
~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming you want to visualize the logs of a lighttpd server, you can
run::

    $ tail -f /var/log/lighttpd/access.log | \
        narcissus-zeromq-source --targets=tcp://0.0.0.0:11987

The development.ini file tells the moksha-hub to connect
to ``tcp://0.0.0.0:11987`` from which it will start getting your raw
lighttpd logs.  Those are then processed and stats are forwarded via
WebSockets to anyone viewing the web app.

IRC
---

Try us in ``#moksha`` on ``irc.freenode.net``.

Authors
-------

* Ralph Bean <rbean@redhat.com>

  * http://threebean.org

* Luke Macken <lmacken@redhat.com>

  * `lewk.org <http://lewk.org>`_

* Lee Burton <lburton@mrow.org>

  * `mrow.org <http://mrow.org>`_


Powered by
----------

.. image:: http://mokshaproject.github.com/mokshaproject.net/img/moksha-logo.png
   :align: left
   :scale: 100 %
   :alt: Moksha
   :target: https://fedorahosted.org/moksha/
