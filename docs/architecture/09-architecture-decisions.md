# 09. Architecture Decisions

This document captures the key architectural decisions made for this project using the **Architecture Decision Record (ADR)** format.

---

## ADR-001: Use DynamoDB Single-Table Design

**Status:** Accepted

---

### Context

The Subscription Platform requires a database to store and manage:

* Merchants
* Products
* Orders
* Subscriptions

The system must support:

* Fast read and write operations
* Low operational cost
* Automatic scaling (serverless environment)
* High availability with minimal infrastructure management

Traditional relational databases introduce operational overhead (connection pooling, scaling, maintenance), which conflicts with the serverless architecture goals.

---

### Decision

We will use **Amazon DynamoDB** with a **single-table design**.

All entities (merchants, products, orders, subscriptions) will be stored in a single table using:

* **Partition Key (PK)**
* **Sort Key (SK)**

Access patterns will be modeled upfront to support efficient queries.

---

### Rationale

* **Serverless scaling**: On-demand capacity automatically scales with traffic
* **Cost efficiency**: Pay-per-request model (scales to zero)
* **Performance**: Single-digit millisecond latency
* **No connection management**: Uses HTTP API instead of persistent DB connections
* **Operational simplicity**: One table instead of multiple reduces complexity
* **Best fit for access-pattern-driven design**

---

### Consequences

#### ✅ Positive

* Highly scalable and resilient architecture
* Simplified infrastructure management
* Optimized for known access patterns
* Reduced operational overhead

#### ⚠️ Negative

* Requires **strict upfront data modeling**
* Queries are **less flexible than SQL**
* Harder to perform ad-hoc queries
* Team must learn **DynamoDB single-table design patterns**

---

### Notes

This decision aligns with a **serverless-first architecture** and prioritizes:

* scalability
* performance
* cost optimization

Future changes to access patterns may require **schema evolution** or additional indexes (GSIs).
