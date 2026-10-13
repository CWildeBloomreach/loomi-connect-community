# Mapping a topic into product families

Read this in step 2. The search data shows what shoppers already connect with the topic. It misses what they need but search for separately: someone taking up pickleball also needs court shoes and eye protection, but they won't type "pickleball sunglasses". Use what you know about the topic to propose those **companion families**, then check each one against the catalog and, where possible, against the data.

## 1. Work through the roles

Ask what someone doing, wearing, giving or celebrating the topic needs. Not every role applies; skip the ones that don't.

| Role | Question | Pickleball | Wedding guest | Camo (a print) |
|---|---|---|---|---|
| **Core** | What is the topic itself? | Paddles, balls, nets | Occasion dresses, suits | Camo-print clothing |
| **Use** | What do they use with it? | Ball hopper, portable court lines | — | — |
| **Wear** | What do they wear for it? | Court shoes, skirts and shorts, visors | Heels, ties, fascinators | Plain tees and boots that pair with it |
| **Protect** | What keeps them safe or comfortable? | Impact-resistant eyewear, knee and elbow supports | Shapewear, blister plasters | — |
| **Maintain** | What keeps the gear working? | Grip tape, edge guard tape | — | — |
| **Carry** | What do they carry it in? | Paddle bags, backpacks | Clutch bags | — |
| **Learn and gift** | What do beginners or gift-buyers want? | Starter sets, rule books, gift cards | Gift wrap, cards | — |

Aim for 4–8 families. More than that dilutes the collection.

## 2. Give each family a qualifier

The intelligence is in the **qualifier**: the property that makes a generic product fit the topic. Without one, "sunglasses" brings in fashion sunglasses and "shoes" brings in running shoes.

| Family | Qualifier | How to check it |
|---|---|---|
| Court shoes | Court or non-marking sole, lateral support. Not running shoes, which roll on lateral moves | Attribute (`sport`, `surface`, `activity`) if the catalog has one; else title words "court", "non-marking", "indoor court" |
| Eye protection | Impact-resistant (polycarbonate or rated) lenses, wraparound fit | Attribute (`lens_material`); else title words "polycarbonate", "impact", "sport", "protective" |
| Knee supports | Sports support, not medical post-surgery braces | Category plus title |
| Balls | The topic's ball: perforated plastic, indoor or outdoor. Not tennis balls | Title "pickleball"; this one is usually core |

Write the qualifier down before you search, so the check is honest.

## 3. Rate each family's specificity

| Specificity | Meaning | Example | Use |
|---|---|---|---|
| **Specific** | Only makes sense with the topic | Pickleball paddle bag, edge guard tape | Include |
| **Adapted** | A generic product with a topic qualifier | Court shoes, impact-resistant sunglasses | Include the qualifying products only |
| **Generic** | Fits any sport or occasion | Water bottles, towels, socks | Leave out unless the user wants a broad "kit" page; mention as an option |

## 4. Find the family in the catalog

Catalogs use their own wording, not the topic's. For each family, list 2–3 **catalog terms** (what a product title would say: "court shoe", "non-marking trainer", "sports sunglasses"), and search with those, not with "pickleball shoes".

- Use `search_mode="standard"` first: if it returns nothing, the catalog probably doesn't stock the family, and hybrid results will be loose.
- Check the response's facets for an attribute that carries the qualifier. If one exists, the family can be a rule.
- Read the titles against the qualifier. Count the products that pass, not `numFound`.

## 5. Label the evidence

Every family and product gets a source:

| Source | Meaning | Confidence |
|---|---|---|
| **Both** | You proposed it, and the topic's own searches return it too | Highest |
| **Data** | The topic's searches return it; you hadn't thought of it | High; check it isn't an off-topic match |
| **Knowledge, with demand** | You proposed it; nothing links it to the topic in search results, but a wording like "pickleball shoes" has sessions | Good |
| **Knowledge only** | You proposed it, and the catalog has it, but there's no data link yet | Suggested; say so, and suggest testing it as a section on the page |

Optional, if the user has Bloomreach Engagement and wants it: an aggregate co-purchase check ("of customers who bought a core product, how many also bought from this family's category") turns a knowledge-only family into a data-backed one. Resolve the project with `list_cloud_organizations` and `list_projects` (ask if there's more than one), check `get_event_schema` for a purchase line-item event with categories or product IDs, call `estimate_eql_cost` first and tell the user the cost level, and run aggregate counts only, at least 3 seconds apart. Never read individual customers.

## 6. Don't overreach

- Don't propose families the user's scope rules out ("equipment only" drops Wear).
- Don't invent qualifiers you aren't sure of. If you don't know what makes a product right for the topic, say so and ask the user.
- A family the catalog doesn't stock is an **assortment gap**, not a section. Report it with any demand behind it.
