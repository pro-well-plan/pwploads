.. _create_casing:


Creating a casing object
========================

.. autoclass:: pwploads.Casing

Example
-------

Let's create a casing with the following characteristics:

* od: 8 in
* id: 7.2 in
* length: 1500 m
* nominal weight: 100 kg/m
* yield_s: 80000 psi
* VME Design Factor: 1.25
* API Design Factors:
    - burst: 1.1
    - collapse: 1.1
    - tension: 1.3
    - compression: 1.3

.. code-block:: python

    >>> import pwploads as pld
    >>> casing = pld.Casing(8, 7.2, 1500, nominal_weight=100, yield_s=80000, df_burst=1.1, df_collapse=1.1, df_tension=1.3, df_compression=1.3, df_vme=1.25)
    >>> casing.plot(plot_type='pyplot').show()

|casing_created|

.. |casing_created| image:: /figures/casing_api_triaxial.png
                    :scale: 40%
