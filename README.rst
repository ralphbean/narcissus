Narcissus - Realtime visualizations of web server hits
------------------------------------------------------

.. figure:: narcissus/raw/master/narcissus-caravaggio.jpg
   :align: right
   :scale: 50 %
   :alt: Narcissus wastes a bunch of time.

   Narcissus wastes a bunch of time.

.. split here

Source
------

Get the source from `github.com <http://github.com/ralphbean/narcissus>`_.


Features
--------

* IP addresses converted to latitude/longitude plotted
  on `polymaps <http://polymaps.org/>`_ as they happen.
* Realtime graphs of url-hit distribution.
* `AMQP (Advanced Message Queueing Protocol)
  <http://www.amqp.org/confluence/display/AMQP/Advanced+Message+Queuing+Protocol>`_
  from logs to browser.  *Fast*.  Little to no handshaking overhead.

Live Demo
---------

* TODO -- please check back!

Running
-------

Create ``~/.fabricrc`` with the following content::

    narcissus_source_location = ~/narc/narcissus
    moksha_source_location = ~/narc/narcissus/moksha-proper

.. parsed-literal::

    $ sudo yum -y install fabric
    $ cd narc/moksha
    $ fab -H localhost boostrap
    $ cd ../narcissus
    $ fab -H localhost install
    $ cd ../moksha
    $ fab -H localhost stop start

Authors
-------
* Ralph Bean <ralph.bean@gmail.com>
* Luke Macken <lmacken@redhat.com>
* Lee Burton <lburton@mrow.org>

.. split here

Powered by
----------

.. image:: narcissus/raw/master/moksha.png
   :align: left
   :scale: 100 %
   :alt: Moksha
   :target: https://fedorahosted.org/moksha/
