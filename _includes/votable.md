
{% capture filename %}/examples/{{page.model}}/{{page.flavor}}/instances/{{include.name}}.vot.xml{% endcapture %}

File: [{{ filename }} ]({{ filename }})

``` xml
{% include_relative {{ filename }} %}
```
