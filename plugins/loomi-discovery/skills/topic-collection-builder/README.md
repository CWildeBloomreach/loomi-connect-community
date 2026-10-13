# Topic collection builder

Builds one product collection for a topic or query you name, such as "pickleball", "camo" or "wedding guest", from two sources:

- **Data:** the wordings shoppers actually search for the topic, and the products those searches return, scored for how strongly each belongs (core, likely, needs review, off-topic).
- **Knowledge:** companion families that go with the topic but that shoppers search for separately. For pickleball that means court shoes, impact-resistant eyewear, knee supports and grip tape. Each family has a qualifier that makes a generic product fit (court shoes, not running shoes) and is checked against the catalog.

Each product and family is labelled with its evidence: data, knowledge, or both. The skill recommends a structure (a hub page of core and companion sections, one collection from a shared feed tag, or a core rule plus a manual kit list). It then writes rule-based dynamic categories and measures them against the products: its **precision** (how much of what it returns is on topic) and **core recall** (how many of the core products it catches), naming the products it wrongly includes and the ones it misses. When no attribute carries the topic, it gives a manual product list and the feed attribute to add. It never creates or changes anything.

To find *which* collections are worth building in the first place, use [collection-suggester](../../../loomi-platform/skills/collection-suggester/).

| | |
|---|---|
| **Products** | Discovery (Engagement optional, for a co-purchase check on companion families) |
| **Access** | Read-only |
| **Loomi Connect tools** | `list_discovery_accounts`, `list_discovery_sites`, `get_discovery_query_performance`, `get_autosuggest_results`, `list_synonyms_user`, `search_discovery_product_grid_insights`, `get_discovery_product_performance_table`, `search_dynamic_categories`, `list_categories`; optional: `list_cloud_organizations`, `list_projects`, `get_event_schema`, `estimate_eql_cost`, `execute_analytics_eql` |
| **Tested with** | Not yet run end to end against a live account. The tool behaviours it relies on (fq lists for AND, standard vs hybrid mode, title filtering, dynamic category conditions) were verified while building `collection-suggester` and are recorded in [docs/known-tool-behaviour.md](../../../../docs/known-tool-behaviour.md). `scripts/score_association.py` was tested on made-up grid responses. Not yet tested in an OpenAI client. |
| **Maintainer** | Bloomreach |

## Example prompts

- "Build a pickleball collection."
- "Which of our products belong in a camo edit?"
- "I want a landing page for wedding guest outfits. What rule should the dynamic category use?"
- "What products are associated with the search 'gym bag'?"
- "Build a pickleball kit page: everything a beginner needs."

## Scripts

Standard library only; no network access.

- `scripts/score_association.py`: reads saved product grid responses for the topic's wordings and scores each product's association (position across wordings, weighted by sessions, with a bonus for keyword-mode matches), assigns tiers using topic and neighbour terms in titles, folds in companion-family catalog probes (`--family`), labelling each product's evidence as data, knowledge or both, and compares candidate rules' product lists with the scored set (`--rule`). It never prints the debug URL, which contains an auth key.

## Notes and limitations

- **Companion families come from the assistant's knowledge.** They are labelled as such and checked against the catalog with an explicit qualifier, but a knowledge-only family has no data behind it yet. The optional Engagement co-purchase check, or a test as a page section, can confirm it.
- **Association comes from search ranking, not per-query clicks.** No Loomi Connect tool returns which products shoppers clicked or bought for a given query; product performance is site-wide. The score uses where the engine ranks each product across the topic's wordings, checked against keyword-mode results and titles. The assistant then reviews titles and moves products between tiers.
- **Hybrid search over-matches.** It returns semantically close products even when the catalog has nothing relevant, so keyword (standard) mode results carry more weight.
- **Rules need attribute data.** Titles can't be filtered. A topic that lives only in titles gets a manual list, labelled as not self-updating, and a recommended feed attribute.
- **No NOT condition** was seen in dynamic category conditions, so neighbour topics are kept out by choosing a narrower attribute, not by excluding.
- Only the first 48 results per wording are scored. Rule products outside that set are reported as unscored, with a sample of titles to judge.
