# pikakube

> My personal **Platform & Data Engineering** homelab/monorepo, running on Kubernetes and open-source tooling — a living lab to design, test, and document end-to-end platforms.

`pikakube` is where I prototype, validate, and document how to build a complete **Internal Developer Platform**: from cluster provisioning to GitOps, covering observability, security, networking, data, AI, and FinOps. Each component ships with technical docs (`doc.md`), declarative manifests, and — where it helps — diagrams.

The goal isn't just to "spin up a stack", but to **map the solution space** of every platform capability — comparing tools, recording decisions, and keeping a reusable catalog.

---

## 🎯 Purpose

- **Platform Engineering lab** — reproduce, in a local/ephemeral environment, the capabilities of a production-grade platform.
- **Tooling catalog** — for each problem (CNI, ingress, secrets, CI/CD, lakehouse, LLM serving...), evaluate and document the main open-source options.
- **Documentation as a portfolio** — capture architecture decisions, trade-offs, and operational patterns (runbooks, ADRs, RFCs, disaster recovery).
- **GitOps-first** — everything is declarative and versioned; the repository is the source of truth.

---

## 🧱 How it works

| Layer | Tooling |
|---|---|
| **Local/ephemeral cluster** | [Kind](https://kind.sigs.k8s.io/) (configs in [clusters/kind-configs/](clusters/kind-configs/)) |
| **GitOps / continuous delivery** | [Flux CD](https://fluxcd.io/) (`HelmRelease` / `Kustomization`) and [Argo CD](https://argo-cd.readthedocs.io/) ([clusters/dev/](clusters/dev/)) |
| **Packaging** | Helm + Kustomize |
| **Reproducible dev environment** | [Devbox](https://www.jetify.com/devbox) ([devbox.json](devbox.json)) — `kubectl`, `kind`, `helm`, `fluxcd`, `velero`, `trivy`, `uv`, etc. |
| **Baseline security** | API server audit logs, policies, external secrets |

> Typical flow: `devbox shell` → bring up a Kind cluster from [clusters/kind-configs/](clusters/kind-configs/) → Flux/Argo reconciles the manifests in [infrastructure/](infrastructure/) → the capabilities become available in the cluster.

---

## 🗂️ Repository structure

```
pikakube/
├── clusters/          # cluster bootstrap (Kind) + GitOps apps (Flux/Argo)
├── infrastructure/    # platform capability catalog (the core of the repo)
├── docs/              # documentation, standards, roadmap, and diagrams (Mermaid)
├── portfolio/         # portfolio site (MkDocs)
├── linkedin/ learning/# personal notes
└── devbox.json        # reproducible toolchain
```

The [infrastructure/](infrastructure/) folder is organized by **discipline** and, within each one, by **capability** (a single axis per level). Each tool lives in its own folder with a `doc.md` + manifests.

---

## 🛠️ Main domains and tools

### ☸️ Platform Engineering

| Purpose / Problem it solves | Tools |
|---|---|
| Declarative, Git-driven cluster delivery | Flux, Argo CD |
| Provisioning infrastructure from Kubernetes | Crossplane, Terraform |
| Internal Developer Platform & self-service | Backstage, Headlamp |
| Multi-tenancy & cluster bootstrap | vCluster, Yunikorn, Kind/Kustomize |

### 🌐 Network

| Purpose / Problem it solves | Tools |
|---|---|
| Pod networking & eBPF dataplane | Cilium |
| East-west traffic / mTLS between services | Service Mesh |
| North-south API entry point | Kong, Envoy |
| Routing external traffic into the cluster | NGINX Ingress, Gateway API |
| Exposing services with bare-metal LoadBalancer IPs | MetalLB |
| Automated DNS records | external-dns |
| Network segmentation & traffic visibility | Network Policies, Retina |

### 👁️ Observability

| Purpose / Problem it solves | Tools |
|---|---|
| Metrics collection & long-term storage | Prometheus, Thanos |
| Dashboards & visualization | Grafana |
| Log aggregation | Fluent Bit |
| Distributed tracing | OpenTelemetry |
| Continuous profiling | Pyroscope |
| Alert routing & on-call | Alertmanager |
| Incident management & response | runbooks / playbooks |

### 🔒 Security

| Purpose / Problem it solves | Tools |
|---|---|
| Policy governance & baselines | org policies |
| Cloud posture management | Prowler |
| Cluster admission & runtime security | Kyverno, Falco, Tetragon, Kubescape |
| Image scanning, signing & SBOM | Trivy, Cosign |
| Static/dynamic code analysis | SAST / DAST |
| Secrets management | External Secrets, Vault, Sealed Secrets |

### 🔁 DevOps

| Purpose / Problem it solves | Tools |
|---|---|
| Continuous integration & delivery pipelines | CI/CD, scanners |
| Auto-reloading workloads on config change | Reloader |
| Automated image updates | Flux image update |
| Cluster housekeeping / rebalancing | Descheduler |
| Repository standardization | versioning & templating |

### 🛡️ Site Reliability Engineering

| Purpose / Problem it solves | Tools |
|---|---|
| Backup & restore | Velero |
| Resilience testing | Chaos Engineering |
| Safe, gradual rollouts | Flagger |
| Defining & tracking reliability targets | SLO / SLI |
| Storage management & data resilience | Storage, Disaster Recovery |
| Keeping the platform up to date | tooling updates |

### 💰 FinOps

| Purpose / Problem it solves | Tools |
|---|---|
| Right-sizing & elastic scaling | Karpenter, KEDA, VPA, Spot |
| Cost allocation & visibility | Kubecost |
| Cutting idle spend | automatic cluster shutdown |

### 🤖 AI / MLOps

| Purpose / Problem it solves | Tools |
|---|---|
| Self-hosted LLM serving | Ollama, vLLM, Kaito |
| Governed access to models | Envoy AI Gateway |
| Agent & workflow orchestration | Langflow, Langfuse, n8n, CrewAI, LangGraph |
| Tool/context integration for LLMs | MCP |
| ML lifecycle & experiment tracking | MLflow |
| Data/ML apps & UIs | Streamlit |

### 📊 Data Engineering & Streaming

| Purpose / Problem it solves | Tools |
|---|---|
| Workflow orchestration | Airflow |
| Distributed processing | Spark on K8s |
| Interactive querying | Trino |
| Event streaming & CDC | Kafka, Flink, Debezium |
| Real-time analytics | OLAP |

### 🔧 Analytics Engineering

| Purpose / Problem it solves | Tools |
|---|---|
| Data integration & ingestion | Airbyte, NiFi, SeaTunnel |
| Transformation & modeling | dbt, SQLMesh |
| Semantic / metrics layer | Cube |
| Interactive notebooks | Jupyter, Zeppelin |
| Business Intelligence & dashboards | Metabase, Superset, Lightdash, Redash |

### 🏛️ Data Governance

| Purpose / Problem it solves | Tools |
|---|---|
| Data catalog & discovery | OpenMetadata |
| Lineage, contracts & quality | Lineage, Data Contracts, Data Quality |
| Open table format / lakehouse | Iceberg, Lakekeeper |
| Privacy & anonymization | anonymization |

### 🗄️ Databases

| Purpose / Problem it solves | Tools |
|---|---|
| Relational (PostgreSQL on K8s) | CloudNativePG |
| NoSQL & caching | MongoDB, Redis |
| Analytical / embedded | DuckDB |
| Distributed databases | distributed engines |
| Monitoring & tuning | PgHero, PMM, exporters |

### ☁️ Cloud Computing

| Purpose / Problem it solves | Tools |
|---|---|
| AWS managed services | EKS, EMR on K8s, S3, IAM, Athena, Redshift |
| Azure managed services | AKS, Databricks, Key Vault, Event Hubs |
| Infrastructure as Code | Terraform |
| Local cloud emulation | LocalStack |

### 💻 Software Engineering

| Purpose / Problem it solves | Tools |
|---|---|
| API design & exposure | APIs |
| Asynchronous messaging | RabbitMQ |
| Feature flags & serverless functions | feature flags, serverless |
| Code quality enforcement | linters |
| Web scraping | scraping tools |
| Python packaging & environments | uv |

### 📚 Docs

| Purpose / Problem it solves | Tools |
|---|---|
| Static documentation sites | MkDocs, Docusaurus, Docsify, GitBook, Sphinx |
| Diagrams & visual docs | Excalidraw, Mermaid |
| Executable / runnable docs | Runme |

---

## 🚀 Getting started

```bash
# 1. Enter the reproducible environment (installs kubectl, kind, helm, flux, etc.)
devbox shell

# 2. Bring up a local Kind cluster
kind create cluster --config clusters/kind-configs/core.yaml

# 3. Bootstrap GitOps and/or apply the infrastructure manifests
#    (Flux reconciles HelmReleases/Kustomizations from this repository)
```

Each folder in [infrastructure/](infrastructure/) contains a `doc.md` with specific instructions, reference links, and ready-to-apply manifests.

---

## 📖 Documentation

- [docs/](docs/) — writing standards, roadmap, and notes per discipline
- [docs/docs-standard.md](docs/docs-standard.md) — documentation conventions used in this repository
- `doc.md` in each tool — focused technical reference
- [docs/mermaid/](docs/mermaid/) — architecture diagrams

---

## 📄 License

See [LICENSE](LICENSE).
