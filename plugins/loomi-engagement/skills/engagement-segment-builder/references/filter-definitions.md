# Customer filter definitions

Engagement stores an audience as a **customer filter**: a list of condition atoms plus a boolean `formula` over them. The same structure appears in saved customer filters (`search_customer_filters`), in each segment of a segmentation (`search_segmentations`), and in scenario condition nodes.

```json
{
  "filters": [ <atom F0>, <atom F1>, ... ],
  "formula": "F0&!F1"
}
```

- Atoms are numbered from zero: `F0`, `F1`, ...
- Operators: `&` (and), `|` (or), `!` (not), with parentheses for grouping.
- An empty `filters` list with an empty `formula` means "all customers".

## Atom shapes

**Seen** means the shape was observed in live data. **Inferred** means it follows the same pattern but hasn't been confirmed. Before a write, always copy a real atom of the same kind from the project, as the next section explains.

### Segment membership (seen)

```json
{"type": "attribute",
 "attribute": {"type": "segmentation", "id": "<segmentation_id>"},
 "constraint": {"type": "string", "operator": "equals",
                "operands": [{"type": "constant", "value": "<segment name>"}]}}
```

With `"operator": "has value"` and an empty-string operand, it means "in any segment of that segmentation". This is the best way to **reuse** an existing segmentation.

### Event history (seen, with no date window)

```json
{"type": "funnel_steps",
 "steps": [{"type": "<event step type>", "name": "<event name>",
            "filter": [{"attribute": {"type": "property", "property": "<event property>"},
                        "constraint": {"type": "string", "operator": "equals",
                                       "operands": [{"type": "constant", "value": "..."}]}}]}],
 "date_filter": {"enabled": false, "type": "static", "absolute": false,
                 "duration": {"count": 30, "units": "days"}, "from_date": null, "to_date": null, "offset": null},
 "duration_filter": {"enabled": false, "duration": {"count": 30, "units": "days"}},
 "independent_if_reused": true}
```

- Use `!F<n>` in the formula for "has **not** done it".
- **The shape of an enabled, relative date window ("in the last 90 days") hasn't been confirmed.** Copy it from an existing filter that has one. If none exists in the project, don't offer the write: give the UI steps instead.
- Step `type` and `name` were both the event name in the one example seen. Confirm against an existing filter.

### Customer property (inferred)

```json
{"type": "attribute",
 "attribute": {"type": "property", "property": "<customer property>"},
 "constraint": {"type": "<string|number|boolean|date>", "operator": "<operator>",
                "operands": [{"type": "constant", "value": "..."}]}}
```

Operators seen in live data: `equals`, `has value`. Others shown in the Engagement UI include `does not equal`, `contains`, `has no value`, `greater than`, `less than`, `in the last`. Check the exact spelling against an existing filter.

### Consent

The consent condition's atom shape wasn't seen in testing. In EQL, use `has consent <category_id>`. For a write, copy the atom from an existing filter or segmentation that checks consent. If there's none, leave consent out of the write and tell the user to add it in the UI.

## Getting a reliable template

The create tools' own advice is to copy atoms from existing objects. Do this:

1. List `search_customer_filters` and `search_segmentations`, and pick ones whose names suggest similar conditions (purchase recency, consent, country).
2. Fetch one or two with their ID. Read their `filters` and `formula` (for a segmentation, each segment's `customer_filter`).
3. Copy the atom that matches each kind of condition you need, and change only the event, property, values and window.
4. If no template exists for a kind of condition, that condition can't be written reliably. Use the UI steps for the whole audience.

## Write payloads (only after explicit confirmation)

`create_customer_filter`: one reusable audience.

```json
{"project_id": "<project>", "name": "<name>", "filters": [ ... ], "formula": "F0&!F1", "tags": ["created-by-assistant"]}
```

`create_segmentation`: named buckets. At least one segment is required.

```json
{"project_id": "<project>", "name": "<name>",
 "segments": [{"name": "<segment name>", "customer_filter": {"filters": [ ... ], "formula": "F0&!F1"}}],
 "customer_filter": {"filters": [], "formula": ""}}
```

Both return `{"success": true, "id": "<new id>"}`, or `success: false` with an `error`. Report the error as it is; don't retry with guessed changes.
