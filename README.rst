Overview
========

.. image:: https://scrutinizer-ci.com/g/stakkr-org/docker-clean/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/stakkr-org/docker-clean
.. image:: https://travis-ci.com/stakkr-org/docker-clean.svg?branch=master
   :target: https://travis-ci.com/stakkr-org/docker-clean
.. image:: https://img.shields.io/pypi/l/docker-clean.svg
   :target: https://pypi.python.org/pypi/docker-clean
.. image:: https://api.codeclimate.com/v1/badges/0d084cbb66933be59317/maintainability
   :target: https://codeclimate.com/github/stakkr-org/docker-clean/maintainability
   :alt: Maintainability
.. image:: https://api.codeclimate.com/v1/badges/0d084cbb66933be59317/test_coverage
   :target: https://codeclimate.com/github/stakkr-org/docker-clean/test_coverage
   :alt: Test Coverage


Docker-Clean
============

Command line tool to clean docker containers, images, volumes and networks
that are not in use currently (started).


.. code:: bash

    Usage: docker-clean [OPTIONS]

      Clean Docker containers, images, volumes and networks that are not in use

    Options:
      -f, --force                           Do it
      -c, --containers / --no-containers    Remove containers
      -i, --images / --no-images            Remove images
      -V, --volumes / --no-volumes          Remove volumes
      -n, --networks / --no-networks        Remove networks
      --help                                Show this message and exit.



Development
===========

Setup your env
--------------

To develop, you have to create a virtual environment :

.. code:: bash

    $ git clone git@github.com:stakkr-org/docker-clean.git docker-clean
    $ cd docker-clean
    $ python3 -m venv venv
    $ source venv/bin/activate
    # For Windows use "venv\Scripts\activate"


Then install docker-clean and its dependencies :

.. code:: bash

    $ python -m pip install --upgrade pip
    $ python -m pip install -e .
    $ python -m pip install -r requirements-dev.txt


Run Tests
---------

.. code:: bash

    $ py.test
