#### DSL

{% capture filename %}/examples/{{page.model}}/{{page.flavor}}/instances/{{include.name}}.jovial{% endcapture %}

{% capture url %}/assets{{ filename }}{% endcapture %}

File: [{{ filename }} ]({{ url | absolute_url }})

``` groovy
{% include {{ filename }} %}
```

#### VOTable

{% capture filename %}/examples/{{page.model}}/{{page.flavor}}/instances/{{include.name}}.vot.xml{% endcapture %}

{% capture url %}/assets{{ filename }}{% endcapture %}

File: [{{ filename }} ]({{ url | absolute_url }})

``` xml
{% include {{ filename }} %}
```
