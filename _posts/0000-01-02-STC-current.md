---
title: Measurements and Coordinates
about: |
    The STC v1 model has been separated into three
    different, and simpler, components. The components have been given a version 2 to clarify that they are part of
    an overarching STC v2 framework.
layout: page
model: stc2
flavor: current
---

Table of Contents
-----------------
* TOC
{:toc}

Model Files
-----------

{% capture stc-coords %}/assets/examples/{{page.model}}/{{page.flavor}}/models/STC_coords-v2.0.html{% endcapture %}
{% capture stc-meas %}/assets/examples/{{page.model}}/{{page.flavor}}/models/STC_meas-v2.0.html{% endcapture %}
[Coordinates HTML documentation]({{ stc-coords | absolute_url }})

[Measurements HTML documentation]({{ stc-meas | absolute_url }})

Generalities
------------

As for the other examples we provide two representations for the instances. One is expressed in
a Domain Specific Language (DSL) that we are developing along with the VODML-related standards.

The DSL is independent of the serialization format, and allows to describe the instances
in a simpler language without much boilerplate.

We also provide the VOTable serializations of those instances, which is what providers and
clients will need to work with in practice.

Rationale
---------

Here is a list of requirements we took into account when trying to rework the STC v1 standard.

  * **simple and common things should be simple to provide and consume.** There is nothing in this model that
  provides more functionality when compared to the *current* proposal. However, we tried to simplify the most
  common scenarios for both data providers and data consumers.
  
  * **complex, custom things should be possible.** At the same time, the model should keep supporting more uncommon,
  complex, or in any way custom scenarios, which is something the *current* proposal does.
  
  * **COOSYS works in simple cases.** So the model provides structures that provide the same information, but in
  the VODML framework.
  
  * **Allow standardization of common instances.** The model should allow a standard library of commonly used
  instances that can be referenced through globally unique identifiers that client can rely on. This makes the
  serializations less verbose and makes it easier for clients to parse files in the most common cases.

Coordinate Frames
-----------------

A coordinate frame defines:
  * its origin in terms of another reference frame, possibly a standard one
  * its orientation or direction

It does not define its own axes.

Note that a library of common/standard reference frames could be built but it is probably not really useful, because
frame definitions are in this model rather lightweight, and suitable for being included along with the data in all
cases. The current model for `SpaceFrame` looks a lot like the `COOSYS` element, but expressed rigorously in the VODML
framework, allowing for more complex relationships to be created if need be.

Positions
---------

Positions can be expressed with a great deal of flexibility in this model. However, the price of such flexibility is
complexity, which is not ideal for simple, most common cases. For these reasons we modeled some *shortcut* types
that can be used in most cases. Such types make a lot of assumptions implicit, thus reducing the number 

### ICRS position

This is the simplest possible position, with just an RA and a DEC. The `SpaceFrame` instance plays the same role as
`COOSYS`, but it is more flexible, as in more complicated instances there may be more frames and sets of coordinates,
as well as custom frame, not necessarily spatial.

Using specific types like `SkyPosition` allows instances to be simpler in the most common cases.

Note that in principle the frame instance and reference could be omitted. Whether or not this is a valid instance it
depends on the final version of the model document. One could decide that omitting the frame information a client can
infer the coordinate frame is `ICRS` and the reference position `TOPOCENTER`, or simply assume the information is
unknown or irrelevant. These cases should be dictated by the STC standard(s).

{% include examples.md name='position-icrs' %}

### FK4 B1950 position

This is also a simple example, but in a different frame. You can compare these examples with the `ICRS` one above.

{% include examples.md name='position-fk4' %}

### ICRS Position with Ellipse Error

In this example the position also has an associated error, in particular an ellipse.

Note how the error, like the frame, is a property of the measurement, not the coordinate itself. A client with
knowledge of the `coords` model can only find out about the RA and DEC values, while a client of the `meas` model
will be able to understand a lot of information, e.g. information about the frame, so that in many cases coordinates
expressed in different frames can be reduced to the same one and e.g. plotted together. Also, `meas` clients can figure
out the error of a measurement and its shape.

{% include examples.md name='position-icrs-ellipse' %}

### ICRS Position with Symmetric Error

For comparison, here is a position in `ICRS` with a symmetric 2D error, i.e. a circle rather than an ellipse.

{% include examples.md name='position-icrs-symmetric' %}

Time measurements
-----------------

### TT ISO Time

{% include examples.md name='tt-iso-time' %}

### TT JD Time

{% include examples.md name='tt-jd-time' %}

### TT MJD Time

{% include examples.md name='tt-mjd-time' %}

### TT MET Time

{% include examples.md name='tt-met-time' %}

Other Measurements
------------------

### Magnitude with Symmetric Error

{% include examples.md name='magnitude-sym-error' %}

### Magnitude with Asymmetric Error

{% include examples.md name='magnitude-asym-error' %}

Notes
-----

### VODML Mapping

There is currently no mechanism for referencing an object by ID/URI. Should there be one or is
`REMOTEREFERENCE` enough?