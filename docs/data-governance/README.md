

graph TD
    subgraph Governance
        Catalog
        Lineage
        Quality
    end

    subgraph Policies
        Owner
        Lifecycle
        Column_Level_Security[Column Level Security]
    end

    subgraph Storage[Storage]
        direction TB
        Lakekeeper --> Iceberg
    end

