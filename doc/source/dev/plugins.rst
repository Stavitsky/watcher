..
      Except where otherwise noted, this document is licensed under Creative
      Commons Attribution 3.0 License.  You can view the license at:

          https://creativecommons.org/licenses/by/3.0/

===============
Watcher plugins
===============

Writing a Watcher Decision Engine plugin
========================================

Watcher has an external :ref:`strategy <strategy_definition>` plugin interface
which gives anyone the ability to integrate an external :ref:`strategy
<strategy_definition>` in order to make use of placement algorithms.

This section gives some guidelines on how to implement and integrate custom
Stategies with Watcher.

Pre-requisites
--------------

Before using any strategy, you should make sure you have your Telemetry service
configured so that it would provide you all the metrics you need to be able to
use your strategy.


Creating a new plugin
---------------------

First of all you have to:

- Extend the base ``BaseStrategy`` class
- Implement its ``execute`` method

Here is an example showing how you can write a plugin called ``DummyStrategy``:

.. code-block:: python

    # Filepath = third-party/third_party/dummy.py
    # Import path = third_party.dummy

    class DummyStrategy(BaseStrategy):

        DEFAULT_NAME = "dummy"
        DEFAULT_DESCRIPTION = "Dummy Strategy"

        def __init__(self, name=DEFAULT_NAME, description=DEFAULT_DESCRIPTION):
            super(DummyStrategy, self).__init__(name, description)

        def execute(self, model):
            self.solution.add_change_request(
                Migrate(vm=my_vm, src_hypervisor=src, dest_hypervisor=dest)
            )
            # Do some more stuff here ...
            return self.solution

As you can see in the above example, the ``execute()`` method returns a
solution as required.

Please note that your strategy class will be instantiated without any
parameter. Therefore, you should make sure not to make any of them required in
your ``__init__`` method.


Abstract Plugin Class
---------------------

Here below is the abstract ``BaseStrategy`` class that every single strategy
should implement:

.. automodule:: watcher.decision_engine.strategy.base
    :noindex:

.. autoclass:: BaseStrategy
    :members:


Add a new entry point
---------------------

In order for the Watcher Decision Engine to load your new strategy, the
strategy must be registered as a named entry point under the
``watcher_strategies`` entry point of your ``setup.py`` file. If you are using
pbr_, this entry point should be placed in your ``setup.cfg`` file.

The name you give to your entry point has to be unique.

Here below is how you would proceed to register ``DummyStrategy`` using pbr_:

.. code-block:: ini

    [entry_points]
    watcher_strategies =
        dummy = third_party.dummy:DummyStrategy


To get a better understanding on how to implement a more advanced strategy,
have a look at the :py:class:`BasicConsolidation` class.

.. _pbr: http://docs.openstack.org/developer/pbr/

Using strategy plugins
----------------------

The Watcher Decision Engine service will automatically discover any installed
plugins when it is run. If a Python package containing a custom plugin is
installed within the same environment as Watcher, Watcher will automatically
make that plugin available for use.

At this point, the way Watcher will use your new strategy if you reference it
in the ``goals`` under the ``[watcher_goals]`` section of your ``watcher.conf``
configuration file. For example, if you want to use a ``dummy`` strategy you
just installed, you would have to associate it to a goal like this:

.. code-block:: ini

    [watcher_goals]
    goals = BALANCE_LOAD:basic,MINIMIZE_ENERGY_CONSUMPTION:dummy


You should take care when installing strategy plugins. By their very nature,
there are no guarantees that utilizing them as is will be supported, as
they may require a set of metrics which is not yet available within the
Telemetry service. In such a case, please do make sure that you first
check/configure the latter so your new strategy can be fully functional.

Querying metrics
~~~~~~~~~~~~~~~~

The metrics available depend on the hypervisors that OpenStack manages on
the specific implementation. You can find the metrics available per hypervisor
and OpenStack release on the OpenStack site.

There are different possible ways to obtain usage metrics in Watcher, you can
use the default Ceilometer API or our Helper.
The Helper attempted to make the Ceilometer API more reusable and easy to use.

Read usage metrics using the Python binding
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can find the information about the Ceilometer Python binding on the
OpenStack `ceilometer client python API documentation
<http://docs.openstack.org/developer/python-ceilometerclient/api.html>`_

The first step is to authenticate against the Ceilometer service
(assuming that you already imported the Ceilometer client for Python)
with this call:

.. code-block:: py

 cclient = ceilometerclient.client.get_client(VERSION, os_username=USERNAME,
  os_password=PASSWORD, os_tenant_name=PROJECT_NAME, os_auth_url=AUTH_URL)

Using that you can now query the values for that specific metric:

.. code-block:: py

 value_cpu = cclient.samples.list(meter_name='cpu_util', limit=10, q=query)

Read usage metrics using the Watcher Cluster History Helper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here below is the abstract ``BaseClusterHistory`` class of the Helper.

.. automodule:: watcher.metrics_engine.cluster_history.api
    :noindex:

.. autoclass:: BaseClusterHistory
    :members:


The following snippet code shows how to create a Cluster History class:

.. code-block:: py

    query_history  = CeilometerClusterHistory()

Using that you can now query the values for that specific metric:

.. code-block:: py

    query_history.statistic_aggregation(resource_id=hypervisor.uuid,
                                  meter_name='compute.node.cpu.percent',
                                  period="7200",
                                  aggregate='avg'
                                  )

