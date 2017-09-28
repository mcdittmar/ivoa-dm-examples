
{% capture filename %}/examples/{{page.flavor}}/instances/{{include.name}}.jovial{% endcapture %}

File: [{{ filename }} ]({{ filename }})

``` groovy
{% include_relative {{ filename }} %}
```
