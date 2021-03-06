..
      Except where otherwise noted, this document is licensed under Creative
      Commons Attribution 3.0 License.  You can view the license at:

          https://creativecommons.org/licenses/by/3.0/

==========
 Glossary
==========

.. glossary::
   :sorted:

This page explains the different terms used in the Watcher system.

They are sorted in alphabetical order.

.. _action_definition:

Action
======

An :ref:`Action <action_definition>` is what enables Watcher to transform the
current state of a :ref:`Cluster <cluster_definition>` after an
:ref:`Audit <audit_definition>`.

An :ref:`Action <action_definition>` is an atomic task which changes the
current state of a target :ref:`Managed resource <managed_resource_definition>`
of the OpenStack :ref:`Cluster <cluster_definition>` such as:

-  Live migration of an instance from one compute node to another compute
   node with Nova
-  Changing the power level of a compute node (ACPI level, ...)
-  Changing the current state of an hypervisor (enable or disable) with Nova

In most cases, an :ref:`Action <action_definition>` triggers some concrete
commands on an existing OpenStack module (Nova, Neutron, Cinder, Ironic, etc.)
via a :ref:`Primitive <primitive_definition>`.

An :ref:`Action <action_definition>` has a life-cycle and its current state may
be one of the following:

-  **PENDING** : the :ref:`Action <action_definition>` has not been executed
   yet by the :ref:`Watcher Applier <watcher_applier_definition>`
-  **ONGOING** : the :ref:`Action <action_definition>` is currently being
   processed by the :ref:`Watcher Applier <watcher_applier_definition>`
-  **SUCCEEDED** : the :ref:`Action <action_definition>` has been executed
   successfully
-  **FAILED** : an error occured while trying to execute the
   :ref:`Action <action_definition>`
-  **DELETED** : the :ref:`Action <action_definition>` is still stored in the
   :ref:`Watcher database <watcher_database_definition>` but is not returned
   any more through the Watcher APIs.
-  **CANCELLED** : the :ref:`Action <action_definition>` was in **PENDING** or
   **ONGOING** state and was cancelled by the
   :ref:`Administrator <administrator_definition>`

.. _action_plan_definition:

Action Plan
===========

An :ref:`Action Plan <action_plan_definition>` is a flow of
:ref:`Actions <action_definition>` that should be executed in order to satisfy
a given :ref:`Goal <goal_definition>`.

An :ref:`Action Plan <action_plan_definition>` is generated by Watcher when an
:ref:`Audit <audit_definition>` is successful which implies that the
:ref:`Strategy <strategy_definition>`
which was used has found a :ref:`Solution <solution_definition>` to achieve the
:ref:`Goal <goal_definition>` of this :ref:`Audit <audit_definition>`.

In the default implementation of Watcher, an
:ref:`Action Plan <action_plan_definition>`
is only composed of successive :ref:`Actions <action_definition>`
(i.e., a Workflow of :ref:`Actions <action_definition>` belonging to a unique
branch).

However, Watcher provides abstract interfaces for many of its components,
allowing other implementations to generate and handle more complex
:ref:`Action Plan(s) <action_plan_definition>`
composed of two types of Action Item(s):

-  simple :ref:`Actions <action_definition>`: atomic tasks, which means it
   can not be split into smaller tasks or commands from an OpenStack point of
   view.
-  composite Actions: which are composed of several simple
   :ref:`Actions <action_definition>`
   ordered in sequential and/or parallel flows.

An :ref:`Action Plan <action_plan_definition>` may be described using
standard workflow model description formats such as
`Business Process Model and Notation 2.0 (BPMN 2.0) <http://www.omg.org/spec/BPMN/2.0/>`_
or `Unified Modeling Language (UML) <http://www.uml.org/>`_.

An :ref:`Action Plan <action_plan_definition>` has a life-cycle and its current
state may be one of the following:

-  **RECOMMENDED** : the :ref:`Action Plan <action_plan_definition>` is waiting
   for a validation from the :ref:`Administrator <administrator_definition>`
-  **ONGOING** : the :ref:`Action Plan <action_plan_definition>` is currently
   being processed by the :ref:`Watcher Applier <watcher_applier_definition>`
-  **SUCCEEDED** : the :ref:`Action Plan <action_plan_definition>` has been
   executed successfully (i.e. all :ref:`Actions <action_definition>` that it
   contains have been executed successfully)
-  **FAILED** : an error occured while executing the
   :ref:`Action Plan <action_plan_definition>`
-  **DELETED** : the :ref:`Action Plan <action_plan_definition>` is still
   stored in the :ref:`Watcher database <watcher_database_definition>` but is
   not returned any more through the Watcher APIs.
-  **CANCELLED** : the :ref:`Action Plan <action_plan_definition>` was in
   **PENDING** or **ONGOING** state and was cancelled by the
   :ref:`Administrator <administrator_definition>`

.. _administrator_definition:

Administrator
=============

The :ref:`Administrator <administrator_definition>` is any user who has admin
access on the OpenStack cluster. This user is allowed to create new projects
for tenants, create new users and assign roles to each user.

The :ref:`Administrator <administrator_definition>` usually has remote access
to any host of the cluster in order to change the configuration and restart any
OpenStack service, including Watcher.

In the context of Watcher, the :ref:`Administrator <administrator_definition>`
is a role for users which allows them to run any Watcher commands, such as:

-  Create/Delete an :ref:`Audit Template <audit_template_definition>`
-  Launch an :ref:`Audit <audit_definition>`
-  Get the :ref:`Action Plan <action_plan_definition>`
-  Launch a recommended :ref:`Action Plan <action_plan_definition>` manually
-  Archive previous :ref:`Audits <audit_definition>` and
   :ref:`Action Plans <action_plan_definition>`


The :ref:`Administrator <administrator_definition>` is also allowed to modify
any Watcher configuration files and to restart Watcher services.

.. _audit_definition:

Audit
=====

In the Watcher system, an :ref:`Audit <audit_definition>` is a request for
optimizing a :ref:`Cluster <cluster_definition>`.

The optimization is done in order to satisfy one :ref:`Goal <goal_definition>`
on a given :ref:`Cluster <cluster_definition>`.

For each :ref:`Audit <audit_definition>`, the Watcher system generates an
:ref:`Action Plan <action_plan_definition>`.

An :ref:`Audit <audit_definition>` has a life-cycle and its current state may
be one of the following:

-  **PENDING** : a request for an :ref:`Audit <audit_definition>` has been
   submitted (either manually by the
   :ref:`Administrator <administrator_definition>` or automatically via some
   event handling mechanism) and is in the queue for being processed by the
   :ref:`Watcher Decision Engine <watcher_decision_engine_definition>`
-  **ONGOING** : the :ref:`Audit <audit_definition>` is currently being
   processed by the
   :ref:`Watcher Decision Engine <watcher_decision_engine_definition>`
-  **SUCCEEDED** : the :ref:`Audit <audit_definition>` has been executed
   successfully (note that it may not necessarily produce a
   :ref:`Solution <solution_definition>`).
-  **FAILED** : an error occured while executing the
   :ref:`Audit <audit_definition>`
-  **DELETED** : the :ref:`Audit <audit_definition>` is still stored in the
   :ref:`Watcher database <watcher_database_definition>` but is not returned
   any more through the Watcher APIs.
-  **CANCELLED** : the :ref:`Audit <audit_definition>` was in **PENDING** or
   **ONGOING** state and was cancelled by the
   :ref:`Administrator <administrator_definition>`

.. _audit_template_definition:

Audit Template
==============

An :ref:`Audit <audit_definition>` may be launched several times with the same
settings (:ref:`Goal <goal_definition>`, thresholds, ...). Therefore it makes
sense to save those settings in some sort of Audit preset object, which is
known as an :ref:`Audit Template <audit_template_definition>`.

An :ref:`Audit Template <audit_template_definition>` contains at least the
:ref:`Goal <goal_definition>` of the :ref:`Audit <audit_definition>`.

It may also contain some error handling settings indicating whether:

-  :ref:`Watcher Applier <watcher_applier_definition>` stops the
   entire operation
-  :ref:`Watcher Applier <watcher_applier_definition>` performs a rollback

and how many retries should be attempted before failure occurs (also the latter
can be complex: for example the scenario in which there are many first-time
failures on ultimately successful :ref:`Actions <action_definition>`).

Moreover, an :ref:`Audit Template <audit_template_definition>` may contain some
settings related to the level of automation for the
:ref:`Action Plan <action_plan_definition>` that will be generated by the
:ref:`Audit <audit_definition>`.
A flag will indicate whether the :ref:`Action Plan <action_plan_definition>`
will be launched automatically or will need a manual confirmation from the
:ref:`Administrator <administrator_definition>`.

Last but not least, an :ref:`Audit Template <audit_template_definition>` may
contain a list of extra parameters related to the
:ref:`Strategy <strategy_definition>` configuration. These parameters can be
provided as a list of key-value pairs.

.. _availability_zone_definition:

Availability Zone
=================

Please, read `the official OpenStack definition of an Availability Zone <http://docs.openstack.org/developer/nova/aggregates.html#availability-zones-azs>`_.

.. _cluster_definition:

Cluster
=======

A :ref:`Cluster <cluster_definition>` is a set of physical machines which
provide compute, storage and networking resources and are managed by the same
OpenStack Controller node.
A :ref:`Cluster <cluster_definition>` represents a set of resources that a
cloud provider is able to offer to his/her
:ref:`customers <customer_definition>`.

A data center may contain several clusters.

The :ref:`Cluster <cluster_definition>` may be divided in one or several
:ref:`Availability Zone(s) <availability_zone_definition>`.

.. _cluster_data_model_definition:

Cluster Data Model
==================

A :ref:`Cluster Data Model <cluster_data_model_definition>` is a logical
representation of the current state and topology of the
:ref:`Cluster <cluster_definition>`
:ref:`Managed resources <managed_resource_definition>`.

It is represented as a set of
:ref:`Managed resources <managed_resource_definition>`
(which may be a simple tree or a flat list of key-value pairs)
which enables Watcher :ref:`Strategies <strategy_definition>` to know the
current relationships between the different
:ref:`resources <managed_resource_definition>`) of the
:ref:`Cluster <cluster_definition>` during an :ref:`Audit <audit_definition>`
and enables the :ref:`Strategy <strategy_definition>` to request information
such as:

-  What compute nodes are in a given
:ref:`Availability Zone <availability_zone_definition>`
   or a given :ref:`Host Aggregate <host_aggregates_definition>` ?
-  What :ref:`Instances <instance_definition>` are hosted on a given compute
   node ?
-  What is the current load of a compute node ?
-  What is the current free memory of a compute node ?
-  What is the network link between two compute nodes ?
-  What is the available bandwidth on a given network link ?
-  What is the current space available on a given virtual disk of a given
   :ref:`Instance <instance_definition>` ?
-  What is the current state of a given :ref:`Instance <instance_definition>`?
-  ...

In a word, this data model enables the :ref:`Strategy <strategy_definition>`
to know:

-  the current topology of the :ref:`Cluster <cluster_definition>`
-  the current capacity for each
   :ref:`Managed resource <managed_resource_definition>`
-  the current amount of used/free space for each
   :ref:`Managed resource <managed_resource_definition>`
-  the current state of each
   :ref:`Managed resources <managed_resource_definition>`

In the Watcher project, we aim at providing a generic and very basic
:ref:`Cluster Data Model <cluster_data_model_definition>` for each
:ref:`Goal <goal_definition>`, usable in the associated
:ref:`Strategies <strategy_definition>` through some helper classes in order
to:

-  simplify the development of a new
   :ref:`Strategy <strategy_definition>` for a given
   :ref:`Goal <goal_definition>` when there already are some existing
   :ref:`Strategies <strategy_definition>` associated to the same
   :ref:`Goal <goal_definition>`
-  avoid duplicating the same code in several
   :ref:`Strategies <strategy_definition>` associated to the same
   :ref:`Goal <goal_definition>`
-  have a better consistency between the different
   :ref:`Strategies <strategy_definition>` for a given
   :ref:`Goal <goal_definition>`
-  avoid any strong coupling with any external
   :ref:`Cluster Data Model <cluster_data_model_definition>`
   (the proposed data model acts as a pivot data model)

There may be various
:ref:`generic and basic Cluster Data Models <cluster_data_model_definition>`
proposed in Watcher helpers, each of them being adapted to achieving a given
:ref:`Goal <goal_definition>`:

-  For example, for a
   :ref:`Goal <goal_definition>` which aims at optimizing the network
   :ref:`resources <managed_resource_definition>` the
   :ref:`Strategy <strategy_definition>` may need to know which
   :ref:`resources <managed_resource_definition>` are communicating together.
-  Whereas for a :ref:`Goal <goal_definition>` which aims at optimizing thermal
   and power conditions, the :ref:`Strategy <strategy_definition>` may need to
   know the location of each compute node in the racks and the location of each
   rack in the room.

Note however that a developer can use his/her own
:ref:`Cluster Data Model <cluster_data_model_definition>` if the proposed data
model does not fit his/her needs as long as the
:ref:`Strategy <strategy_definition>` is able to produce a
:ref:`Solution <solution_definition>` for the requested
:ref:`Goal <goal_definition>`.
For example, a developer could rely on the Nova Data Model to optimize some
compute resources.

The :ref:`Cluster Data Model <cluster_data_model_definition>` may be persisted
in any appropriate storage system (SQL database, NoSQL database, JSON file,
XML File, In Memory Database, ...).

.. _cluster_history_definition:

Cluster History
===============

The :ref:`Cluster History <cluster_history_definition>` contains all the
previously collected timestamped data such as metrics and events associated
to any :ref:`managed resource <managed_resource_definition>` of the
:ref:`Cluster <cluster_definition>`.

Just like the :ref:`Cluster Data Model <cluster_data_model_definition>`, this
history may be used by any :ref:`Strategy <strategy_definition>` in order to
find the most optimal :ref:`Solution <solution_definition>` during an
:ref:`Audit <audit_definition>`.

In the Watcher project, a generic
:ref:`Cluster History <cluster_history_definition>`
API is proposed with some helper classes in order to :

-  share a common measurement (events or metrics) naming based on what is
   defined in Ceilometer.
   See `the full list of available measurements <http://docs.openstack.org/admin-guide-cloud/telemetry-measurements.html>`_
-  share common meter types (Cumulative, Delta, Gauge) based on what is
   defined in Ceilometer.
   See `the full list of meter types <http://docs.openstack.org/admin-guide-cloud/telemetry-measurements.html>`_
-  simplify the development of a new :ref:`Strategy <strategy_definition>`
-  avoid duplicating the same code in several
:ref:`Strategies <strategy_definition>`
-  have a better consistency between the different
:ref:`Strategies <strategy_definition>`
-  avoid any strong coupling with any external metrics/events storage system
   (the proposed API and measurement naming system acts as a pivot format)

Note however that a developer can use his/her own history management system if
the Ceilometer system does not fit his/her needs as long as the
:ref:`Strategy <strategy_definition>` is able to produce a
:ref:`Solution <solution_definition>` for the requested
:ref:`Goal <goal_definition>`.

The :ref:`Cluster History <cluster_history_definition>` data may be persisted
in any appropriate storage system (InfluxDB, OpenTSDB, MongoDB,...).

.. _controller_node_definition:

Controller Node
===============

A controller node is a machine that typically runs the following core OpenStack
services:

-  Keystone: for identity and service management
-  Cinder scheduler: for volumes management
-  Glance controller: for image management
-  Neutron controller: for network management
-  Nova controller: for global compute resources management with services
   such as nova-scheduler, nova-conductor and nova-network.

In many configurations, Watcher will reside on a controller node even if it
can potentially be hosted on a dedicated machine.

.. _compute_node_definition:

Compute node
============

Please, read `the official OpenStack definition of a Compute Node <http://docs.openstack.org/openstack-ops/content/compute_nodes.html>`_.

.. _customer_definition:

Customer
========

A :ref:`Customer <customer_definition>` is the person or company which
subscribes to the cloud provider offering. A customer may have several
:ref:`Project(s) <project_definition>`
hosted on the same :ref:`Cluster <cluster_definition>` or dispatched on
different clusters.

In the private cloud context, the :ref:`Customers <customer_definition>` are
different groups within the same organization (different departments, project
teams, branch offices and so on). Cloud infrastructure includes the ability to
precisely track each customer's service usage so that it can be charged back to
them, or at least reported to them.

.. _goal_definition:

Goal
====

A :ref:`Goal <goal_definition>` is a human readable, observable and measurable
end result having one objective to be achieved.

Here are some examples of :ref:`Goals <goal_definition>`:

-  minimize the energy consumption
-  minimize the number of compute nodes (consolidation)
-  balance the workload among compute nodes
-  minimize the license cost (some softwares have a licensing model which is
   based on the number of sockets or cores where the software is deployed)
-  find the most appropriate moment for a planned maintenance on a
   given group of host (which may be an entire availability zone):
   power supply replacement, cooling system replacement, hardware
   modification, ...


.. _host_aggregates_definition:

Host Aggregate
==============

Please, read `the official OpenStack definition of a Host Aggregate <http://docs.openstack.org/developer/nova/aggregates.html>`_.

.. _instance_definition:

Instance
========

A running virtual machine, or a virtual machine in a known state such as
suspended, that can be used like a hardware server.

.. _managed_resource_definition:

Managed resource
================

A :ref:`Managed resource <managed_resource_definition>` is one instance of
:ref:`Managed resource type <managed_resource_type_definition>` in a topology
with particular properties and dependencies on other
:ref:`Managed resources <managed_resource_definition>` (relationships).

For example, a :ref:`Managed resource <managed_resource_definition>` can be one
virtual machine (i.e., an :ref:`instance <instance_definition>`) hosted on a
:ref:`compute node <compute_node_definition>` and connected to another virtual
machine through a network link (represented also as a
:ref:`Managed resource <managed_resource_definition>` in the
:ref:`Cluster Data Model <cluster_data_model_definition>`).

.. _managed_resource_type_definition:

Managed resource type
=====================

A :ref:`Managed resource type <managed_resource_definition>` is a type of
hardware or software element of the :ref:`Cluster <cluster_definition>` that
the Watcher system can act on.

Here are some examples of
:ref:`Managed resource types <managed_resource_definition>`:

-  `Nova Host Aggregates <http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Nova::HostAggregate>`_
-  `Nova Servers <http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Nova::Server>`_
-  `Cinder Volumes <http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Cinder::Volume>`_
-  `Neutron Routers <http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Neutron::Router>`_
-  `Neutron Networks <http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Neutron::Net>`_
-  `Neutron load-balancers <http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Neutron::LoadBalancer>`_
-  `Sahara Hadoop Cluster <http://docs.openstack.org/developer/heat/template_guide/openstack.html#OS::Sahara::Cluster>`_
-  ...

It can be any of the `the official list of available resource types defined in OpenStack for HEAT <http://docs.openstack.org/developer/heat/template_guide/openstack.html>`_.

.. _efficiency_definition:

Optimization Efficiency
=======================

The :ref:`Optimization Efficiency <efficiency_definition>` is the objective
measure of how much of the :ref:`Goal <goal_definition>` has been achieved in
respect with constraints and :ref:`SLAs <sla_definition>` defined by the
:ref:`Customer <customer_definition>`.

The way efficiency is evaluated will depend on the
:ref:`Goal <goal_definition>` to achieve.

Of course, the efficiency will be relevant only as long as the
:ref:`Action Plan <action_plan_definition>` is relevant
(i.e., the current state of the :ref:`Cluster <cluster_definition>`
has not changed in a way that a new :ref:`Audit <audit_definition>` would need
to be launched).

For example, if the :ref:`Goal <goal_definition>` is to lower the energy
consumption, the :ref:`Efficiency <efficiency_definition>` will be computed
using several indicators (KPIs):

-  the percentage of energy gain (which must be the highest possible)
-  the number of :ref:`SLA violations <sla_violation_definition>`
   (which must be the lowest possible)
-  the number of virtual machine migrations (which must be the lowest possible)

All those indicators (KPIs) are computed within a given timeframe, which is the
time taken to execute the whole :ref:`Action Plan <action_plan_definition>`.

The efficiency also enables the :ref:`Administrator <administrator_definition>`
to objectively compare different :ref:`Strategies <strategy_definition>` for
the same goal and same workload of the :ref:`Cluster <cluster_definition>`.

.. _project_definition:

Project
=======

:ref:`Projects <project_definition>` represent the base unit of “ownership”
in OpenStack, in that all :ref:`resources <managed_resource_definition>` in
OpenStack should be owned by a specific :ref:`project <project_definition>`.
In OpenStack Identity, a :ref:`project <project_definition>` must be owned by a
specific domain.

Please, read `the official OpenStack definition of a Project <http://docs.openstack.org/glossary/content/glossary.html>`_.


.. _primitive_definition

Primitive
=========

A :ref:`Primitive <primitive_definition>` is the component that carries out a
certain type of atomic :ref:`Actions <action_definition>` on a given
:ref:`Managed resource <managed_resource_definition>` (nova, swift, neutron,
glance,..). A :ref:`Primitive <primitive_definition>` is a part of the
:ref:`Watcher Applier <watcher_applier_definition>` module.

For example, there can be a :ref:`Primitive <primitive_definition>` which is
responsible for creating a snapshot of a given instance on a Nova compute node.
This :ref:`Primitive <primitive_definition>` knows exactly how to send
the appropriate commands to Nova for this type of
:ref:`Actions <action_definition>`.

.. _sla_definition:

SLA
===

:ref:`SLA <sla_definition>` means Service Level Agreement.

The resources are negotiated between the :ref:`Customer <customer_definition>`
and the Cloud Provider in a contract.

Most of the time, this contract is composed of two documents:

-  :ref:`SLA <sla_definition>` : Service Level Agreement
-  :ref:`SLO <slo_definition>` : Service Level Objectives

Note that the :ref:`SLA <sla_definition>` is more general than the
:ref:`SLO <slo_definition>` in the sense that the former specifies what service
is to be provided, how it is supported, times, locations, costs, performance,
and responsibilities of the parties involved while the
:ref:`SLO <slo_definition>` focuses on more measurable characteristics such as
availability, throughput, frequency, response time or quality.

You can also read `the Wikipedia page for SLA <https://en.wikipedia.org/wiki/Service-level_agreement>`_
which provides a good definition.

.. _sla_violation_definition:

SLA violation
=============

A :ref:`SLA violation <sla_violation_definition>` happens when a
:ref:`SLA <sla_definition>` defined with a given
:ref:`Customer <customer_definition>` could not be respected by the
cloud provider within the timeframe defined by the official contract document.

.. _slo_definition:

SLO
===

A Service Level Objective (SLO) is a key element of a
:ref:`SLA <sla_definition>` between a service provider and a
:ref:`Customer <customer_definition>`. SLOs are agreed as a means of measuring
the performance of the Service Provider and are outlined as a way of avoiding
disputes between the two parties based on misunderstanding.

You can also read `the Wikipedia page for SLO <https://en.wikipedia.org/wiki/Service_level_objective>`_
which provides a good definition.

.. _solution_definition:

Solution
========

A :ref:`Solution <solution_definition>` is a set of
:ref:`Actions <action_definition>` generated by a
:ref:`Strategy <strategy_definition>` (i.e., an algorithm) in order to achieve
the :ref:`Goal <goal_definition>` of an :ref:`Audit <audit_definition>`.

A :ref:`Solution <solution_definition>` is different from an
:ref:`Action Plan <action_plan_definition>` because it contains the
non-scheduled list of :ref:`Actions <action_definition>` which is produced by a
:ref:`Strategy <strategy_definition>`. In other words, the list of Actions in
a :ref:`Solution <solution_definition>` has not yet been re-ordered by the
:ref:`Watcher Planner <watcher_planner_definition>`.

Note that some algorithms (i.e. :ref:`Strategies <strategy_definition>`) may
generate several :ref:`Solutions <solution_definition>`. This gives rise to the
problem of determining which :ref:`Solution <solution_definition>` should be
applied.

Two approaches to dealing with this can be envisaged:

-  **fully automated mode**: only the :ref:`Solution <solution_definition>`
 with the highest ranking (i.e., the highest
   :ref:`Optimization Efficiency <efficiency_definition>`)
   will be sent to the :ref:`Watcher Planner <watcher_planner_definition>` and
   translated into concrete :ref:`Actions <action_definition>`.
-  **manual mode**: several :ref:`Solutions <solution_definition>` are proposed
   to the :ref:`Administrator <administrator_definition>` with a detailed
   measurement of the estimated
   :ref:`Optimization Efficiency <efficiency_definition>` and he/she decides
   which one will be launched.

.. _strategy_definition:

Strategy
========

A :ref:`Strategy <strategy_definition>` is an algorithm implementation which is
able to find a :ref:`Solution <solution_definition>` for a given
:ref:`Goal <goal_definition>`.

There may be several potential strategies which are able to achieve the same
:ref:`Goal <goal_definition>`. This is why it is possible to configure which
specific :ref:`Strategy <strategy_definition>` should be used for each
:ref:`Goal <goal_definition>`.

Some strategies may provide better optimization results but may take more time
to find an optimal :ref:`Solution <solution_definition>`.

When a new :ref:`Goal <goal_definition>` is added to the Watcher configuration,
at least one default associated :ref:`Strategy <strategy_definition>` should be
provided as well.

.. _watcher_applier_definition:

Watcher Applier
===============

This component is in charge of executing the
:ref:`Action Plan <action_plan_definition>` built by the
:ref:`Watcher Decision Engine <watcher_decision_engine_definition>`.

See :doc:`architecture` for more details on this component.

.. _watcher_database_definition:

Watcher Database
================

This database stores all the Watcher domain objects which can be requested
by the Watcher API or the Watcher CLI:

-  Audit templates
-  Audits
-  Action plans
-  Actions
-  Goals

The Watcher domain being here "*optimization of some resources provided by an
OpenStack system*".

See :doc:`architecture` for more details on this component.

.. _watcher_decision_engine_definition:

Watcher Decision Engine
=======================

This component is responsible for computing a set of potential optimization
:ref:`Actions <action_definition>` in order to fulfill the
:ref:`Goal <goal_definition>` of an :ref:`Audit <audit_definition>`.

It first reads the parameters of the :ref:`Audit <audit_definition>` from the
associated :ref:`Audit Template <audit_template_definition>` and knows the
:ref:`Goal <goal_definition>` to achieve.

It then selects the most appropriate :ref:`Strategy <strategy_definition>`
depending on how Watcher was configured for this :ref:`Goal <goal_definition>`.

The :ref:`Strategy <strategy_definition>` is then executed and generates a set
of :ref:`Actions <action_definition>` which are scheduled in time by the
:ref:`Watcher Planner <watcher_planner_definition>` (i.e., it generates an
:ref:`Action Plan <action_plan_definition>`).

See :doc:`architecture` for more details on this component.

.. _watcher_planner_definition:

Watcher Planner
===============

The :ref:`Watcher Planner <watcher_planner_definition>` is part of the
:ref:`Watcher Decision Engine <watcher_decision_engine_definition>`.

This module takes the set of :ref:`Actions <action_definition>` generated by a
:ref:`Strategy <strategy_definition>` and builds the design of a workflow which
defines how-to schedule in time those different
:ref:`Actions <action_definition>` and for each
:ref:`Action <action_definition>` what are the prerequisite conditions.

It is important to schedule :ref:`Actions <action_definition>` in time in order
to prevent overload of the :ref:`Cluster <cluster_definition>` while applying
the :ref:`Action Plan <action_plan_definition>`. For example, it is important
not to migrate too many instances at the same time in order to avoid a network
congestion which may decrease the :ref:`SLA <sla_definition>` for
:ref:`Customers <customer_definition>`.

It is also important to schedule :ref:`Actions <action_definition>` in order to
avoid security issues such as denial of service on core OpenStack services.

See :doc:`architecture` for more details on this component.

