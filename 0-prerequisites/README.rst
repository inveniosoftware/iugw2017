Part 0: Prerequisites
=====================

The IUGW2017 tutorials will use prepared virtual machines (VMs) in order to
ensure that all participants have homogeneous working environment.

Install system tools
--------------------

We shall use some system tools such as ``wget`` or ``ssh`` that you already have
probably installed if you use GNU/Linux or macOS platforms.

On MS Windows, we recommend to use:

- install wget from `<https://eternallybored.org/misc/wget/>`_

- install OpenSSH client (not server!) from `<https://www.mls-software.com/opensshd.html>`_ (see for example `this blog post <http://www.simplehelp.net/2016/03/13/how-to-ssh-from-windows-10/>`_

Install VirtualBox
------------------

First you need to install `VirtualBox <https://www.virtualbox.org/>`_ which is
available for various platforms:

- For MS Windows and macOS, you can download VirtualBox from
  `<https://www.virtualbox.org/wiki/Downloads>`_.

- For GNU/Linux distributions you can install VirtualBox via your distribution
  package manager.

We tested various VirtualBox versions such as 5.0.26 or 5.1.16.

Install Vagrant
---------------

We use `Vagrant <https://www.vagrantup.com/>`_ to automatise certain VM
operations.

- For MS Windows, you can download Vagrant from
  `<https://www.vagrantup.com/downloads.html>`_.

- For macOS, you can install Vagrant via ``brew``.

- For GNU/Linux distributions you can install Vagrant via your distribution
  package manager.

We tested various Vagrant versions such as 1.9.2.

Download VMs
------------

Let us now import prepared VM boxes using Vagrant.

You can use your USB stick:

.. code-block:: console

   $ sudo mount /dev/sdb1 /mnt
   $ vagrant box add -n iugw2017-base-web /mnt/iugw2017-base-web.box
   $ vagrant box add -n iugw2017-demosite-web /mnt/iugw2017-demosite-web.box
   $ vagrant box add -n iugw2017-demositewithcustomdata-web /mnt/iugw2017-demositewithcustomdata-web.box

You can also download the boxes via web. Note that there is about 2.6 GB to
transfer:

.. code-block:: console

   $ vagrant box add -n iugw2017-base-web https://cernbox.cern.ch/index.php/s/AGmVB7rxld7xTQ1/download
   $ vagrant box add -n iugw2017-demosite-web https://cernbox.cern.ch/index.php/s/fu6cge3xhmByBdz/download
   $ vagrant box add -n iugw2017-demositewithcustomdata-web https://cernbox.cern.ch/index.php/s/4kpARUBZywt0sVD/download

This will create three VM images ready to be used:

- ``iugw2017-base-web`` that contains a bare base operating system with required
  services such Elasticsearch, PostgreSQL, RabbitMQ, Redis.

- ``iugw2017-demosite-web`` that contains full Invenio demo site instance.

- ``iugw2017-demositewithcustomdata-web`` that contains full Invenio demo site
  instance after the beautification tutorial and the custom data model tutorial.

The first base VM image is the one upon which the whole tutorial series is
executed. The second and the third demo site VM images are included as a
reference only in case it may be helpful to quickly start an already pre-built
demo site.

Download tutorial sources
-------------------------

Next, create a working space on your laptop:

.. code-block:: console

   $ mkdir ~/iugw2017-tutorials
   $ cd ~/iugw2017-tutorials

and copy the tutorial sources from the USB key:

.. code-block:: console

   $ cp -a /mnt/iugw2017 .
   $ cd iugw2017

or clone them from GitHub:

.. code-block:: console

   $ git clone https://github.com/inveniosoftware/iugw2017
   $ cd iugw2017

Start VM
--------

We are now ready to boot the VM:

.. code-block:: console

    $ vagrant up

This will boot the base box.

Note that if you would like to boot the full demo site box, you can simply alter
``Vagrantfile`` beforehand:

.. code-block:: console

   $ sed -i'' -e 's,iugw2017-base-web,iugw2017-demosite-web,g' Vagrantfile

Log into VM
-----------

You should be now able to login into your VM:

.. code-block:: console

   $ vagrant ssh
   vagrant> cat /etc/debian_version
   jessie/sid

If it worked, good! You are now ready for the first tutorial.
