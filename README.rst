badger
======

Commandline Interface to create svg badges.

Install
-------

.. code:: bash

    pip install badger

Usage (Commandline)
-------------------

Simplest use case of static label and value.

.. code:: bash

    badger version v1.2.3

Percentage mode, with color picked relative to where in the 0-100 range
the value is.

.. code:: bash

    badger -p coverage 60%

Usage (Package)
---------------

.. code:: python

    from badger import Badge, PercentageBadge

    badge = Badge("version", "v1.2.3")
    badge.save("test.svg")

    percentage_badge = PercentageBadge("coverage", 60)
    badge.save("percentage-test.svg")

Disclaimer
==========

Code heavily copied from https://github.com/dbrgn/coverage-badge, badge
design originally from https://github.com/badges/shields