This package contains the "wsgi" components for `narcissus
<https://github.com/ralphbean/narcissus>`_.

Narcissus is a web application that visualizes web server hits
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
