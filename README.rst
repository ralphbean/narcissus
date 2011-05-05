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
