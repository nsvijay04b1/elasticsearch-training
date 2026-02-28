# Module 4: Search DSL, ES|QL, EQL, SQL

## 4.1 Query Context vs Filter Context

![Architecture Diagram](images/architecture_diagram_1.png)
- **Query Context**: Used in `must` or `should`. Calculates a relevance score (BM25). Slower.
- **Filter Context**: Used in `filter`. Does not apply relevance scoring. Exact matches only. Faster because queries can be cached by Elasticsearch.

```mermaid
graph TD
    Query[Bool Query Structure]
    Query --> Must[Must: AND logic]
    Query --> Should[Should: OR logic]
    Query --> Filter[Filter: No scoring, Cacheable]
    Query --> MustNot[Must_Not: NOT logic]
```

## 4.2 Full-Text Search Internals
- **Tokenizers**: Chop text into individual words based on punctuation or whitespace.
- **Analyzers**: Includes the Tokenizer, but also applies Character Filters (e.g. removing HTML tags) and Token Filters (e.g. converting to lowercase, stemming words like "sneakers" to "shoe", or expanding synonyms).

## 4.3 BM25 Ranking
BM25 stands for Best Matching 25. It ranks search relevance based on 3 factors:
1. **Term Frequency (TF)**: How often the search term appears in the document field. (Higher = Better)
2. **Inverse Document Frequency (IDF)**: How rare the search term is across the entire corpus. (Rarer = Better)
3. **Field Length Normalization**: Short fields containing the term score higher than long fields.

## 4.4 Aggregations Framework

![Architecture Diagram](images/architecture_diagram_2.png)
Aggregations gather data into groups and perform calculations on those groups.
- **Bucket Aggregation**: Groups documents (e.g. `terms`, `date_histogram`). Similar to `GROUP BY` in SQL.
- **Metrics Aggregation**: Calculates math values (e.g. `avg`, `sum`, `max`).

```mermaid
graph TD
    Aggs[Aggregations]
    Aggs --> Buck[Bucket: e.g. Categories]
    Aggs --> Metr[Metrics: e.g. Average Price per Category bucket]
    Aggs --> Pipe[Pipeline: Operates on results of other aggregations]
```

## 4.5 ES|QL, EQL, and SQL
- **ES|QL**: A pipeline processing language designed specifically for real-time analytics. Combines filtering, sorting, joins, and time-series logic.
- **EQL**: Event Query Language. Built specifically for detecting behavioral sequences across events (common in security SIEMs).
- **SQL**: Standard relational querying. Allows you to bridge the gap with existing systems that only understand JDBC/SQL.

---


## Assignments
- [Proceed to Lab 9: Query vs. Filter Contexts](lab9.md)
- [Proceed to Lab 10: Aggregations Framework](lab10.md)
- [Proceed to Lab 10.2: Building Kibana Dashboards](lab10_2.md)
- [Proceed to Lab 11: Analyzing Search Performance](lab11.md)
- [Proceed to Lab 11.2: Querying with ES|QL, EQL, and SQL](lab11_2.md)

## 4.6 Search Applications

Search Applications provide a unified API layer for building search-powered UIs:
- Create search endpoints with pre-defined relevance rules.
- Apply query parameters, filters, and facets without exposing raw Elasticsearch DSL.
- Integrate with frontend frameworks via simple REST calls.

## 4.7 Machine Learning in Search

Elasticsearch integrates with ML tools to enhance search capabilities:
- **Semantic Search:** Understand user intent beyond exact keyword matching using vector embeddings.
- **Anomaly Detection:** Identify unusual patterns in time-series data automatically.
- **Query Expansion:** Suggest alternative or related queries based on user behavior.
- **Auto-Completion:** Predict and suggest search terms as users type, improving the search experience.
