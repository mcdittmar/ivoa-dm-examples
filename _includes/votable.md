
{% capture filename %}/examples/{{page.flavor}}/instances/{{include.name}}.vot.xml{% endcapture %}

File: [{{ filename }} ]({{ filename }})

``` xml
{% include_relative {{ filename }} %}
```
