# Module 6: REST APIs, Clients, Painless Scripting

## 6.1 REST API Philosophy
Every interaction with Elasticsearch goes through HTTP REST verbs:
- `GET`: Retrieve documents or cluster states.
- `POST`: Create entirely new documents via automated IDs, or execute searches.
- `PUT`: Overwrite existing documents or create indices.
- `DELETE`: Remove indices or documents.

```mermaid
graph TD
    AppCode[Custom Application] --> |Language Native APIs| OfficialClient[Official ES Client]
    OfficialClient --> |HTTP REST Calls| ES[Elasticsearch Cluster Node]
```

## 6.2 Official Client Architecture
Official clients exist for Java, Python, Node.js, Go, and .NET. Instead of forcing you to format raw JSON or track endpoints natively, these libraries handle:
- Connection pooling
- Node retries on failure
- Serialization to native classes/objects

## 6.3 Painless Scripting Internals
**Painless** is a secure, sandboxed scripting language native to Elasticsearch. Built resembling Java, it lets you:
- Dynamically manipulate data inside Update APIs (e.g. `ctx._source.price += 10`).
- Implement custom scoring functions in search relevance loops.
- Avoid large overhead via compiled bytecode caching.

```mermaid
graph TD
    Query[Query JSON] --> Script[Painless Script Node]
    Script --> |Bytecode compilation| VM[Secure Sandbox VM]
    VM --> Result[Evaluated Result]
```




## Assignments
- [Proceed to Lab 14: Using Painless Scripts](lab14.md)
