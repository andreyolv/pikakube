https://github.com/floci-io/floci-az

The Azure counterpart to [floci](../../aws/floci/doc.md) (AWS). Same idea, same MIT licence,
same shape: one container, one port, no account and no auth token.

- 30+ services: Blob / Queue / Table, Cosmos DB (SQL, Mongo, PostgreSQL, Cassandra, Gremlin,
  Table APIs), Azure SQL, PostgreSQL flexible, Functions, Event Hubs, Service Bus, Event Grid,
  Key Vault, App Configuration, Managed Identity, API Management, VNets, ACR, ACI, AKS (k3s),
  Monitor / Log Analytics
- everything on port **4577**
- `docker compose up` — mount the Docker socket, because Functions, PostgreSQL and AKS run as
  real containers rather than in-process fakes

Why it matters here: [azurite](../azurite/doc.md) only emulates Blob, Queue and Table. Anything
past storage — Service Bus, Event Hubs, Key Vault, Cosmos — had no local answer in this repo.

Console for it: [floci-ui](../../aws/floci/doc.md) speaks to AWS, Azure and GCP runtimes at once.
