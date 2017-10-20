#### DSL

{% capture filename %}/examples/{{page.model}}/{{page.flavor}}/instances/{{include.name}}.jovial{% endcapture %}

File: [/assets{{ filename }} ](/assets/{{ filename }})

``` groovy
{% include {{ filename }} %}
```

#### VOTable

{% capture filename %}/examples/{{page.model}}/{{page.flavor}}/instances/{{include.name}}.vot.xml{% endcapture %}

File: [/assets{{ filename }} ](/assets/{{ filename }})

``` xml
{% include {{ filename }} %}
```
