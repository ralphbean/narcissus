Narcissus - Realtime visualizations of web server hits
------------------------------------------------------

.. figure:: narcissus/raw/master/moksha/public/narcissus/images/narcissus-caravaggio.jpg
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

Research Computing at RIT runs a `narcissus` instance pointed at
http://mirror.rit.edu at http://narcissus.rc.rit.edu.

Running
-------

Create ``~/.fabricrc`` with the following content::

    narcissus_source_location = ~/narc/narcissus
    moksha_source_location = ~/narc/moksha

.. parsed-literal::

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

Authors
-------
* Ralph Bean <ralph.bean@gmail.com>
* Luke Macken <lmacken@redhat.com>
* Lee Burton <lburton@mrow.org>

.. split here

Powered by
----------

.. image:: narcissus/raw/master/moksha/public/narcissus/images/moksha.png
   :align: left
   :scale: 100 %
   :alt: Moksha
   :target: https://fedorahosted.org/moksha/
