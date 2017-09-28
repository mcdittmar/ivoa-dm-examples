
{% capture filename %}/examples/{{page.model}}/{{page.flavor}}/instances/{{include.name}}.jovial{% endcapture %}

File: [{{ filename }} ]({{ filename }})

``` groovy
{% include_relative {{ filename }} %}
```
