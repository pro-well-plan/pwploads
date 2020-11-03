Adding load cases
=================

Before adding a load case, a proper trajectory must be included for the casing
since this is required for calculating some forces. To do this, you can use `well_profile`_.

Install it using pip:

.. code-block:: bash

    $ pip install pwploads

.. code-block:: python

    >>> import well_profile as wp
    >>> trajectory = wp.load('trajectory1.xlsx')
    >>> casing.add_trajectory(trajectory)

Running in hole
---------------

.. autofunction:: pwploads.Casing.running


Overpull
--------

.. autofunction:: pwploads.Casing.overpull

Green cement pressure test
--------------------------

.. autofunction:: pwploads.Casing.green_cement


Example
-------

.. code-block:: python

    >>> casing.running()                            # add load case: running in hole
    >>> casing.overpull()                           # add load case: overpull
    >>> casing.green_cement()                       # add load case: green cement pressure test
    >>> casing.plot(plot_type='pyplot').show()      # plot

|casing_with_loads|

.. |casing_with_loads| image:: /figures/casing_all_loads.png
                       :scale: 40%

.. _well_profile: https://pypi.org/project/well-profile/