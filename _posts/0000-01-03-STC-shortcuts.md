---
title: STC model
about: |
    This is the current Space Time Coordinates model proposal
layout: page
model: stc2
flavor: shortcuts
---

Table of Contents
-----------------
* TOC
{:toc}

Generalities
------------

As for the other examples we provide two representations for the instances. One is expressed in
a Domain Specific Language (DSL) that we are developing along with the VODML-related standards.

The DSL is independent of the serialization format, and allows to describe the instances
in a simpler language without much boilerplate.

We also provide the VOTable serializations of those instances, which is what providers and
clients will need to work with in practice.

Coordinate Frames
-----------------

A coordinate frame defines:
  * its origin in terms of another reference frame, possibly a standard one
  * its orientation or direction

It does not define its own axes.

Note that a library of common/standard reference frames can be built in a single VOTable. Intances in other files can
refer to such frames when declaring their positions. The following example represents such a library of frames.

### DSL Instance

{% include jovial.md name='standard-frames' %}

### VOTable serialization

{% include votable.md name='standard-frames' %}

Positions
---------

Positions can be expressed in terms of the coordinate axes defined as part of the coordinate frames, even remotely
as shown in the examples below, where positions refer to axes defined in the `standard-frames.vot.xml` file.

Below are two examples of the same 2D position in the sky in two different reference frames.

### ICRS position, DSL

{% include jovial.md name='position-icrs' %}

### ICRS position, VOTable

{% include votable.md name='position-icrs' %}

### FK4 B1950 position, DSL

{% include jovial.md name='position-fk4' %}

### FK4 B1950 position, VOTable

{% include votable.md name='position-icrs' %}

### ICRS Position with Ellipse Error, DSL

{% include jovial.md name='position-icrs-ellipse' %}

### ICRS position with Ellipse Error, VOTable

{% include votable.md name='position-icrs-ellipse' %}

### ICRS Position with Symmetric Error, DSL

{% include jovial.md name='position-icrs-symmetric' %}

### ICRS position with Symmetric Error, VOTable

{% include votable.md name='position-icrs-symmetric' %}

Time measurements
-----------------

{% comment %}

Still need to figure it out

### TT ISO Time, DSL

{% include jovial.md name='tt-iso-time' %}

### TT ISO Time, VOTable

{% include votable.md name='tt-iso-time' %}

### TT JD Time, DSL

{% include jovial.md name='tt-jd-time' %}

### TT JD Time, VOTable

{% include votable.md name='tt-jd-time' %}

### TT MJD Time, DSL

{% include jovial.md name='tt-mjd-time' %}

### TT MJD Time, VOTable

{% include votable.md name='tt-mjd-time' %}

Custom Frames
-------------

The following example shows how to define a custom time frame in terms of standard ones.

### TT MET Time, DSL

{% include jovial.md name='tt-met-time' %}

### TT MET Time, VOTable

{% include votable.md name='tt-met-time' %}

{% endcomment %}


Other Measurements
------------------

### Magnitude with Symmetric Error, DSL

{% include jovial.md name='magnitude-sym-error' %}

### Magnitude with Symmetric Error, VOTable

{% include votable.md name='magnitude-sym-error' %}

### Magnitude with Asymmetric Error, DSL

{% include jovial.md name='magnitude-asym-error' %}

### Magnitude with Asymmetric Error, VOTable

{% include votable.md name='magnitude-asym-error' %}

Notes
-----

### VODML Mapping

There is currently no mechanism for referencing an object by ID/URI. Should there be one or is
`REMOTEREFERENCE` enough?