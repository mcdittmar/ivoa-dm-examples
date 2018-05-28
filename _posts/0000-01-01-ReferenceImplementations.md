---
title: Reference Implementations
about: |
    A high level description of the ongoing reference implementations for a number of standards in the Data Model
    working group.
layout: page
---

Table of Contents
-----------------
* TOC
{:toc}

Installation Instructions
-------------------------
This page refers to two software libraries. If you want to follow along, you can install the libraries on your system
or use a cloud service like [SciServer](https://alpha02.sciserver.org/compute/).

Jovial is a Groovy/JAVA library that implements the VODML and VODML Mapping to VOTable specifications for creating,
manipulating, and serializing data models and their instances, as well as to generate Python bindings for the models.
It runs on Windows, Linux, and macOS. It requires Java 8 to run.

Rama is an astropy-aware Python library that parses VOTables annotated according to the Mapping document. It currently
requires Python 3.6.

### Conda

The simplest way to install both libraries is to use `Anaconda`. If you have `Anaconda` installed, we suggest you
create a new environment, e.g.:

```
$ conda create -n vodml -c ivoa rama jovial
$ source activate vodml
```

This will install the libraries with all their dependencies, including appropriate versions of Python and Java.
If you want to test that the libraries are correctly installed:

```
$ jovial -h
```

Should display a usage help message.

```
$ conda install pytest
$ py.test --pyargs rama
```

Will run the full test suite for the Rama library.

### Build from git repository
Both libraries are available as git repositories, as is the repository that backs this website, which contains many
examples as well as runnable Jupyter notebooks:

```
$ git clone https://gitlab.com/olaurino/ivoa-dm-examples
$ git submodule init
$ git submodule update
$ cd ivoa-dm-examples
```

To build Jovial you need Maven:
```
$ cd jovial
$ mvn package -DskipTests=True
$ export jovial="java -jar $(pwd)/target/jovial-1.0-SNAPSHOT-jar-with-dependencies.jar"
$ jovial -h
```

To build Rama you need Python 3.6:
```
$ cd rama
$ python setup.py install
```

### Pip
If you have Python 3.6 you can also use `pip install rama`. Pip cannot be used to install JAVA packages.

### SciServer
If you are familiar with Jupyter notebooks and you have an account on
[SciServer](https://alpha02.sciserver.org/compute/), sign into your account and create a new Python container. Start the
container and then, using the *New* menu, start a new terminal.

In the terminal, type:

```
$ conda install -c ivoa rama jovial
```

To download the repository with the examples and the Jupyter notebooks, cd into a persistent volume and clone the git
repository:

```
$ git clone https://gitlab.com/olaurino/ivoa-dm-examples
```

Then from the Jupyter notebook navigate to the repository. The notebooks are located in the `notebooks` folder.

The Modeling Workflow
---------------------

As stated in the Data Model Working Group charter:

    The role of the Data Modeling group is to provide a framework for the description of metadata attached to observed or
    simulated data. The activity of the Data Model WG activity focuses on logical relationships between these metadata, 
    examines how an astronomer wants to retrieve, process and interpret astronomical data, and provides an architecture to
    handle them. What is defined in this WG can then be re-used in the protocols defined by the DAL WG or in VO aware
    applications.

A few standards in progress in the Working Group provide for such a framework. In a nutshell, the framework supports a
workflow sketched in the graph below.

{% mermaid %}
graph LR
    VODML[VODML XML Document] -- represents --> ConMod[Conceptual Model]
    Provider[Data Provider] -- produces --> VOT[Annotated VOTable file]
    VOT -- represents --> Instance[Instance]
    Instance -- of --> ConMod
    VOT[VOTable file] -- refers to --> VODML[VODML XML Document]
    Client[Client] -- parses --> VOT
    Client -- reconstructs --> Instance
{% endmermaid %}

A **Conceptual Model** *is represented by* a standard **VODML/XML document**. *Instances* of such models *are
represented by* **Annotated VOTables**. A **Data Provider** *annotates* the VOTables to *map* the VOTable
contents to the concepts in the model, so that a **Client**, by *parsing* the **VOTable annotations**, can *reconstruct*
the instances serialized by the Provider

Reference implementations
-------------------------

We present here a number of implementations that support the end-to-end process from modeling to parsing an annotated
file. The description will implement the following specific workflow:

### Generating the Model

{% mermaid %}
graph LR
    DSL[Model DSL] -- describes --> DM[Data Model]
    DM -- describes --> Domain[Astronomical Domain]
    Jovial[Java Library] -- parses --> DSL
    Jovial -- generates --> VODML[VODML XML]
    VODML -- represents --> DM
    Jovial -- generates --> Bindings[Python Bindings]
    Bindings -- represent --> DM
 {% endmermaid %}

The model must be represented as an XML document that validates against the VODML/XML schema.

While writing such document directly is always an option, the Data Model Working Group has been producing different
implementations of the standards to provide convenience tools. One tool allows modelers to employ UML graphical
applications for building the models with a point-and-click interface. Models are now exported in an
application-specific XMI format, which can then be translated to VODML/XML by a set of XSLT scripts.

The option described in this section takes a different approach. We use a library named Jovial, which defines an
*Internal Domain Specific Language*, i.e. a small ad-hoc language for representing data models in a computer-readable
format that is also more human-writable than XML. The *internal* qualifier denotes that the a DSL program is also
valid program in a complete programming language. Jovial is written in Groovy and it is 100% Java-compatible, so when
writing models using the DSL one can embed Java or Groovy constructs, use libraries and external packages, connect to
databses, etc. At the same time, Jovial can be seen as a JAVA API that implements the VODML standard. A model built
with the Jovial DSL has a Java-compatible representation and as such it can be used in JAVA programs. Conversely,
one can programatically create models in JAVA using Jovial as an API, and then serialize them in the formats supported
by Jovial.

A word of caution: Jovial has been instrumental in implementing the standards, but it is far from being
production-ready. In particular there is barely any error handling, so if something goes wrong only the full stack
trace will be printed out.

Let's start with a very simple model of an astronomical source. For the sake of simplicity, the model will be
self-contained. In actuality, a powerful feature of the VODML framwork is that you can import and reuse models. We will
present some examples of this in the following sections. We will import the IVOA model, a basic model that defines
some primitive types.

Here is its DSL representation:

```groovy
model("source") {
    include("ivoa", version: "1.0")
    dataType("Position") {
        attribute(name: "ra", dataType: "ivoa:real")
        attribute(name: "dec", dataType: "ivoa:real")
    }
    objectType("Source") {
        attribute(name: "name", dataType: "ivoa:real")
        attribute(name: "position", dataType: "source:Position")
    }
}
```

If we save this text to a file and we then run `jovial`:

```
$ jovial -m example.jovial > example.vot.xml
```

we'll get the following output:

```xml
<?xml version="1.0" encoding="UTF-8"?><vo-dml:model xmlns:vo-dml="http://www.ivoa.net/xml/VODML/v1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ivoa.net/xml/VODML/v1.0 http://volute.g-vo.org/svn/trunk/projects/dm/vo-dml
/xsd/vo-dml-v1.0.xsd">
  <name>source</name>
  <description/>
  <title>My Model</title>
  <version>1.0</version>
  <lastModified>2018-05-27T13:57:55.287Z</lastModified>
  <import>
    <name>ivoa</name>
    <version>1.0</version>
    <url/>
    <documentationURL/>
  </import>
  <dataType>
    <vodml-id>Position</vodml-id>
    <name>Position</name>
    <description/>
    <attribute>
      <vodml-id>Position.ra</vodml-id>
      <name>ra</name>
      <description/>
      <datatype>
        <vodml-ref>ivoa:real</vodml-ref>
      </datatype>
      <multiplicity>
        <minOccurs>1</minOccurs>
        <maxOccurs>1</maxOccurs>
      </multiplicity>
    </attribute>
    <attribute>
      <vodml-id>Position.dec</vodml-id>
      <name>dec</name>
      <description/>
      <datatype>
        <vodml-ref>ivoa:real</vodml-ref>
      </datatype>
      <multiplicity>
        <minOccurs>1</minOccurs>
        <maxOccurs>1</maxOccurs>
      </multiplicity>
    </attribute>
  </dataType>
  <objectType>
    <vodml-id>Source</vodml-id>
    <name>Source</name>
    <description/>
    <attribute>
      <vodml-id>Source.name</vodml-id>
      <name>name</name>
      <description/>
      <datatype>
        <vodml-ref>ivoa:real</vodml-ref>
      </datatype>
      <multiplicity>
        <minOccurs>1</minOccurs>
        <maxOccurs>1</maxOccurs>
      </multiplicity>
    </attribute>
    <attribute>
      <vodml-id>Source.position</vodml-id>
      <name>position</name>
      <description/>
      <datatype>
        <vodml-ref>source:Position</vodml-ref>
      </datatype>
      <multiplicity>
        <minOccurs>1</minOccurs>
        <maxOccurs>1</maxOccurs>
      </multiplicity>
    </attribute>
  </objectType>
</vo-dml:model>
```

As you can see the XML is much more complex than the DSL description, which is why working with a DSL, while not
necessarily a silver bullet, is appealing.

Given a VODML/XML representation of a model, Jovial can create the model's Python representation.
The specifics of the representation are defined by a Python library we'll use in the next sections. However,
since the Python library handles the details of the mapping specification, a Python model representation is rather
simple and straightforward.

Note that at this time you need to point Jovial to the VODML/XML file. Future versions will likely include support for
the DSL.

When called with `jovial -p example.vot.xml`, Jovial will print out:

```python
@VO('source:Position')
class Position(BaseType):
    ra = Attribute('source:Position.ra', min_occurs=1, max_occurs=1)
    dec = Attribute('source:Position.dec', min_occurs=1, max_occurs=1)


@VO('source:Source')
class Source(BaseType):
    name = Attribute('source:Source.name', min_occurs=1, max_occurs=1)
    position = Attribute('source:Source.position', min_occurs=1, max_occurs=1)

```

Jovial will do a lot of work for you, but not everything, at least not at the time of this writing. It might
provide the declaration of a supertype after the declaration of its sbtypes. In those cases you'll need to edit the
code accordingly. Also, Jovial does not know how you will organize the Python code, or where to import external models
from. Again, this is information that depends on your environment and decisions, and that you can simply add when you
paste the code in place (more on this in the client section that introduces Rama below).

### Serializing the Instance 
 {% mermaid %}
 graph LR
    IDSL[Instance DSL] -- describes --> Instance[Instance]
    Instance -- of --> DM
    Jovial[Java Library] -- generates --> VOT[Annotated VOTable]
    Jovial -- parses --> IDSL
    VOT -- represents --> Instance
{% endmermaid %}

In order to define instances of types defined in the data models, Jovial also allows you to use a specific DSL.

```groovy
def modelLocation = "file:example.vodml.xml"
def ivoaModelLocation = "https://volute.g-vo.org/svn/trunk/projects/dm/vo-dml/models/ivoa/vo-dml/IVOA-v1.0.vo-dml.xml"

dmInstance {
    model(vodmlURL: modelLocation)
    model(vodmlURL: ivoaModelLocation)
    instance(type: "source:Source") {
        instance(role: "name", value: "A Source")
        instance(role: "position") {
            instance(role: "ra", value: 122.02)
            instance(role: "dec", value: -12.44)
        }
    }
}
```

The command "jovial -i instance.jovial" will produce a VOTable representation of the instance accordin to the
Mappint document:

```xml
<?xml version="1.0" encoding="UTF-8"?><VOTABLE xmlns="http://www.ivoa.net/xml/VOTable/v1.4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <VODML>
    <MODEL>
      <NAME>source</NAME>
      <URL>file:example.vodml.xml</URL>
    </MODEL>
    <MODEL>
      <NAME>ivoa</NAME>
      <URL>https://volute.g-vo.org/svn/trunk/projects/dm/vo-dml/models/ivoa/vo-dml/IVOA-v1.0.vo-dml.xml</URL>
    </MODEL>
    <GLOBALS>
      <INSTANCE dmtype="source:Source">
        <ATTRIBUTE dmrole="source:Source.name">
          <LITERAL value="A Source" dmtype="ivoa:real"/>
        </ATTRIBUTE>
        <ATTRIBUTE dmrole="source:Source.position">
          <INSTANCE dmtype="source:Position">
            <ATTRIBUTE dmrole="source:Position.ra">
              <LITERAL value="122.02" dmtype="ivoa:real"/>
            </ATTRIBUTE>
            <ATTRIBUTE dmrole="source:Position.dec">
              <LITERAL value="-12.44" dmtype="ivoa:real"/>
            </ATTRIBUTE>
          </INSTANCE>
        </ATTRIBUTE>
      </INSTANCE>
    </GLOBALS>
  </VODML>
  <RESOURCE ID="EMPTY"/>
</VOTABLE>

```

Here is a slightly different version of the above example, generating a table of sources rather than a single source.

```groovy
def modelLocation = "file:example.vodml.xml"
def ivoaModelLocation = "https://volute.g-vo.org/svn/trunk/projects/dm/vo-dml/models/ivoa/vo-dml/IVOA-v1.0.vo-dml.xml"

def names = ["source_one", "source_two", "source_three"]
def ras = [122.02, 123.03, 124.02]
def decs = [-12.44, -11.13, -12.52]

dmInstance {
    model(vodmlURL: modelLocation)
    model(vodmlURL: ivoaModelLocation)
    table("_sources") {
        instance(type: "source:Source") {
            column(id: "_name", role: "name", data: names)
            instance(role: "position") {
                column(id: "_ra", role: "ra", data: ras)
                column(id: "_dec", role: "dec", data: decs)
            }
        }
    }
}
```

What's nice about internal DSLs is that we can use the underlying programming language support. It doesn't matter how
the arrays are generated. In the simple example above we generate it with a simple Groovy initialization, but they could
just as well come from a database connection, from parsing a FITS file, etc.

Here is the result:

```xml
<?xml version="1.0" encoding="UTF-8"?><VOTABLE xmlns="http://www.ivoa.net/xml/VOTable/v1.4" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <VODML>
    <MODEL>
      <NAME>source</NAME>
      <URL>file:example.vodml.xml</URL>
    </MODEL>
    <MODEL>
      <NAME>ivoa</NAME>
      <URL>https://volute.g-vo.org/svn/trunk/projects/dm/vo-dml/models/ivoa/vo-dml/IVOA-v1.0.vo-dml.xml</URL>
    </MODEL>
        <TEMPLATES tableref="_sources">
          <INSTANCE dmtype="source:Source">
            <ATTRIBUTE dmrole="source:Source.position">
              <INSTANCE dmtype="source:Position">
                <ATTRIBUTE dmrole="source:Position.ra">
                  <COLUMN dmtype="ivoa:real" ref="_ra"/>
                </ATTRIBUTE>
                <ATTRIBUTE dmrole="source:Position.dec">
                  <COLUMN dmtype="ivoa:real" ref="_dec"/>
                </ATTRIBUTE>
              </INSTANCE>
            </ATTRIBUTE>
            <ATTRIBUTE dmrole="source:Source.name">
              <COLUMN dmtype="ivoa:real" ref="_name"/>
            </ATTRIBUTE>
          </INSTANCE>
        </TEMPLATES>
      </VODML>
      <RESOURCE>
        <TABLE ID="_sources">
          <FIELD datatype="float" ID="_ra" name="_ra"/>
          <FIELD datatype="float" ID="_dec" name="_dec"/>
          <FIELD datatype="char" arraysize="10" ID="_name" name="_name"/>
          <DATA>
            <TABLEDATA>
              <TR>
                <TD>124.02</TD>
                <TD>-12.52</TD>
                <TD>source_three</TD>
              </TR>
              <TR>
                <TD>123.03</TD>
                <TD>-11.13</TD>
                <TD>source_two</TD>
              </TR>
              <TR>
                <TD>122.02</TD>
                <TD>-12.44</TD>
                <TD>source_one</TD>
              </TR>
            </TABLEDATA>
          </DATA>
        </TABLE>
      </RESOURCE>
</VOTABLE>

```

This DSL is specific for instances, but generic for all models. While this has been helpful so far, model-specific
DSLs could be developed in the future to further simplify the generation of valid annotations.

### Parsing the Instance
{% mermaid %}
graph LR
    Rama[Python Library] -- imports --> Bindings[Python Bindings]
    Bindings -- represent --> DM[Data Model]
    Rama -- parses --> VOT[Annotated VOTable]
    VOT -- represents --> Instance[Instance]
    Instance -- of --> DM
    Rama -- returns --> Obj[Python Objects]
{% endmermaid %}

Rama is a Python library that parses properly annotated VOTables and returns Python objects. The data itself is parsed
using Astropy, and STC types are mapped to Astropy's `SkyCoord` class (although at the time of this writing only
equatorial coordinates are properly handled).

You can find an example on how to use the library in a notebooks on this website:

  * [Hubble Space Catalog Demo]({{ site.baseurl }}{% link _posts/0000-01-03-HSC-Demo.md %})
  
The notebook explores interoperability with the HSC Mast services.

There is also an [old demo]({{ site.baseurl }}{% link _posts/0000-01-10-PythonParserDemo.md %}) that shows how to build
a parser from scratch, with examples parsing and displaying time series data.

Modeling Primer
---------------

### Modeling

End-to-End, a typical data modeling workflow would start with conceptual modeling of a specific domain, e.g.
spectral data sets, sources and detections, time series, space-time coordinates, and so on. The goal of the modeling
phase is to capture concepts in the domain under studies and the complex relationships among those concepts.

Note that a data model is *always an approximation* of the domain being modeled.

How can you describe data models? Depending on the reason for which you are modeling, there may be different answers.
In the IVOA context we model astronomical domains for achieving interoperability among data providers and data
consumers. Say a data provider implements a Cone Search service for sources, they may want to annotate the response
so that the values in the results (values in table cells, FITS carda, etc.) can be mapped to a specific context.

The VO Data Modeling Language and its related standards allow data providers to annotate their data products according
to a data model so that values in the data products can be understood by data consumers according to the same semantics.

This requires expressing Data Models themselves in an interoperable format. Some format exists, but their
interoperability is limited, so the IVOA decided to develop and adopt a simpler and stricter format, which we call
VODML/XML. Data Models in the IVOA are expressed as XML documents according to a specific XML schema. Such documents
can be validated to make sure that not only they are properly written as XML documents, but also that they comply with
the requirements dictated by the VODML standards in order to achieve interoperability.

The XML document describing a Data Model defines types, their attributes, and their relationships. When a data provider
annotates a table according to one or more data models, they want to *map* values to Data Model concepts. For instance
they might want to express that a `TABLE` element contains information about a `Source` and that some specific columns
(generally with arbitrary names) describe the `Position` and `Photometry` properties of the `Source`, with their
respective `Error`s.

In order to do so, the VODML XML format provides portable identifiers that univocally and globally identify a data model
concept, which is either a *type* or a *role* that a *type* plays in the definition of another *type*. These portable
identifiers are called `vodml-id`s.

A model may define a type `Source` with an identifier of `source:Source`, where the string on the left of the `:`
denotes a *prefix*, i.e. a specific namespace that makes the `vodml-id` unique to a model.

Another type may be `stc:Position`, and the two may be linked by a relationship named `position`. The relationship is
also given an ID, e.g. `source:Position.position`. The XML file describes, in a standardized machine readable format,
that the *type* `src:Position` has the role `source:Position.position` for the type `source:Source`.

### Mapping to VOTable ###
A specific source, say `M82`, can be described as an *instance* of the type `source:Source`, and its position is
analogously an *instance* of the `src:Position type`.

A data product served by a data provider thus contains *instances* of types defined in data models.

A data provider needs to annotate a response, e.g. a VOTable, so that the values therein can be interpreted semantically
by data consumers. The formal definition of a mapping scheme between VOTable contents and data models is the goal of 
*Mapping Data Model Instances to VOTable* ongoing standard. The document provides a way for data providers to
unambiguously annotate a VOTable so that the instances it contains can be properly interpreted by a client.

### Parsing a VOTable ###
If the annotation is properly carried out, clients can then interpres the contents of a file semantically, and
faithfully reconstruct the concepts the data provider encoded in the file. There is then interoperability between the
implementations
