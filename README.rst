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

**TODO** - need new pip-based instructions

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
