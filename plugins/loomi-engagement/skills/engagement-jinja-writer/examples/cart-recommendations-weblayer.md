# Example: cart items and recommendations in a weblayer (illustrative)

**This example is illustrative.** Every ID, aggregate, catalog and field name is a placeholder. No project was changed.

**Prompt:** "I need Jinja for a weblayer that shows the first three items in the customer's cart, then four recommendations. The marketer should be able to pick the engine."

---

**HTML**

```html
{% set recCount = "[[ { name: 'RecCount', category: 'Recommendations', isJsonParam: true } : number | 4 ]]" | int %}

{% set cart = aggregates['your_cart_aggregate_id'] if aggregates['your_cart_aggregate_id'] and aggregates['your_cart_aggregate_id'] != 'None' else [] %}
{% set ids = [] %}
{% for it in cart %}
  {% if it['product_id'] %}{% append it['product_id'] to ids %}{% endif %}
{% endfor %}
{% set cartItems = catalogs['your_catalog_name'].items_by_id(ids[:3]) if ids else [] %}

{% set recs = recommendations("[[ { name: 'RecEngine', category: 'Recommendations', isJsonParam: true } : recommendation ]]", size=recCount, fill_with_random=true) | list %}

<div class="cart-recs">
  {% if cartItems %}
    <h3>Still thinking about these?</h3>
    {% for item in cartItems %}
      <a href="{{ item['url'] }}">{{ item['title'] | default('Your item') }}</a>
    {% endfor %}
  {% endif %}

  {% if recs %}
    <h3>You might also like</h3>
    {% for item in recs %}
      <a href="{{ item['url'] }}">{{ item['title'] | default('') }}</a>
    {% endfor %}
  {% endif %}
</div>
```

**Assets used**

| Type | Name | ID | Source |
|---|---|---|---|
| Aggregate | Last cart | `your_cart_aggregate_id` | Placeholder: replace with the real aggregate ID |
| Catalog | Products | `your_catalog_name` | Placeholder: replace with the catalog name |
| Recommendation engine | Picked by the marketer | `RecEngine` parameter | Template parameter |

**How to test it:** preview the weblayer for a test customer with items in their cart, and for one with an empty cart. The cart block should disappear for the second, and the recommendations should still show.
