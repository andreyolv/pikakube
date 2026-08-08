

# pikakube

> Mi **homelab/monorepo** personal de **Ingeniería de Plataforma y Datos**, ejecutado en Kubernetes y con herramientas de código abierto: un laboratorio vivo para diseñar, probar y documentar plataformas de extremo a extremo.

`pikakube` es donde prototipo, valido y documento cómo construir una **Plataforma Interna de Desarrollo (Internal Developer Platform)** completa: desde el aprovisionamiento del clúster hasta GitOps, cubriendo observabilidad, seguridad, redes, datos, IA y FinOps. Cada componente incluye documentación técnica (`doc.md`), manifiestos declarativos y, cuando es útil, diagramas.

El objetivo no es solo "levantar un stack", sino **mapear el espacio de soluciones** de cada capacidad de la plataforma: comparando herramientas, registrando decisiones y manteniendo un catálogo reutilizable.

---

## 🎯 Propósito

- **Laboratorio de Ingeniería de Plataforma** — reproducir, en un entorno local/efímero, las capacidades de una plataforma de grado productivo.
- **Catálogo de herramientas** — para cada problema (CNI, ingress, secretos, CI/CD, lakehouse, servicio de LLM...), evaluar y documentar las principales opciones de código abierto.
- **Documentación como portafolio** — capturar decisiones de arquitectura, compensaciones (trade-offs) y patrones operativos (runbooks, ADRs, RFCs, recuperación ante desastres).
- **GitOps-first** — todo es declarativo y versionado; el repositorio es la fuente de verdad.

---

## 🧱 Cómo funciona

| Capa | Herramientas |
|---|---|
| **Clúster local/efímero** | [Kind](https://kind.sigs.k8s.io/) (configuraciones en [clusters/kind-configs/](clusters/kind-configs/)) |
| **GitOps / entrega continua** | [Flux CD](https://fluxcd.io/) (`HelmRelease` / `Kustomization`) y [Argo CD](https://argo-cd.readthedocs.io/) ([clusters/dev/](clusters/dev/)) |
| **Empaquetado** | Helm + Kustomize |
| **Entorno de desarrollo reproducible** | [Devbox](https://www.jetify.com/devbox) ([devbox.json](devbox.json)) — `kubectl`, `kind`, `helm`, `fluxcd`, `velero`, `trivy`, `uv`, etc. |
| **Seguridad base** | Registros de auditoría del API server, políticas, secretos externos |

> Flujo típico: `devbox shell` → levantar un clúster Kind desde [clusters/kind-configs/](clusters/kind-configs/) → Flux/Argo reconcilia los manifiestos en [infrastructure/](infrastructure/) → las capacidades quedan disponibles en el clúster.

---

## 🗂️ Estructura del repositorio

```
pikakube/
├── clusters/          # arranque del clúster (Kind) + apps GitOps (Flux/Argo)
├── infrastructure/    # catálogo de capacidades de plataforma (el núcleo del repo)
├── docs/              # documentación, estándares, hoja de ruta y diagramas (Mermaid)
├── portfolio/         # sitio del portafolio (MkDocs)
├── linkedin/ learning/# notas personales
└── devbox.json        # cadena de herramientas reproducible
```

La carpeta [infrastructure/](infrastructure/) está organizada por **disciplina** y, dentro de cada una, por **capacidad** (un único eje por nivel). Cada herramienta reside en su propia carpeta con un `doc.md` + manifiestos.

---

## 🛠️ Principales dominios y herramientas

### ☸️ Ingeniería de Plataforma

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Entrega declarativa de clústeres impulsada por Git | Flux, Argo CD |
| Aprovisionamiento de infraestructura desde Kubernetes | Crossplane, Terraform |
| Plataforma Interna de Desarrollo y autoservicio | Backstage, Headlamp |
| Multitenencia y arranque de clústeres | vCluster, Yunikorn, Kind/Kustomize |

### 🌐 Redes

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Red de pods y plano de datos eBPF | Cilium |
| Tráfico este-oeste / mTLS entre servicios | Service Mesh |
| Punto de entrada de API norte-sur | Kong, Envoy |
| Enrutamiento de tráfico externo hacia el clúster | NGINX Ingress, Gateway API |
| Exposición de servicios con IPs de LoadBalancer de hardware dedicado | MetalLB |
| Registros DNS automatizados | external-dns |
| Segmentación de red y visibilidad del tráfico | Network Policies, Retina |

### 👁️ Observabilidad

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Recolección de métricas y almacenamiento a largo plazo | Prometheus, Thanos |
| Paneles y visualización | Grafana |
| Agregación de registros | Fluent Bit |
| Trazabilidad distribuida | OpenTelemetry |
| Perfilado continuo | Pyroscope |
| Enrutamiento de alertas y turnos de guardia | Alertmanager |
| Gestión y respuesta a incidentes | runbooks / playbooks |

### 🔒 Seguridad

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Gobernanza de políticas y líneas base | políticas organizativas |
| Gestión de postura en la nube | Prowler |
| Seguridad de admisión del clúster y en tiempo de ejecución | Kyverno, Falco, Tetragon, Kubescape |
| Escaneo, firmado y SBOM de imágenes | Trivy, Cosign |
| Análisis estático/dinámico de código | SAST / DAST |
| Gestión de secretos | External Secrets, Vault, Sealed Secrets |

### 🔁 DevOps

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Pipelines de integración y entrega continua | CI/CD, scanners |
| Recarga automática de cargas de trabajo ante cambios de configuración | Reloader |
| Actualización automatizada de imágenes | Flux image update |
| Mantenimiento / reequilibrio del clúster | Descheduler |
| Estandarización de repositorios | versionado y plantillas |

### 🛡️ Ingeniería de Fiabilidad del Sitio (SRE)

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Copias de seguridad y restauración | Velero |
| Pruebas de resiliencia | Chaos Engineering |
| Lanzamientos seguros y graduales | Flagger |
| Definición y seguimiento de objetivos de fiabilidad | SLO / SLI |
| Gestión de almacenamiento y resiliencia de datos | Almacenamiento, Recuperación ante Desastres |
| Mantener la plataforma actualizada | actualizaciones de herramientas |

### 💰 FinOps

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Dimensionamiento adecuado y escalado elástico | Karpenter, KEDA, VPA, Spot |
| Asignación de costos y visibilidad | Kubecost |
| Reducción del gasto inactivo | apagado automático del clúster |

### 🤖 IA / MLOps

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Servidor de LLM autoalojado | Ollama, vLLM, Kaito |
| Acceso gobernado a modelos | Envoy AI Gateway |
| Orquestación de agentes y flujos de trabajo | Langflow, Langfuse, n8n, CrewAI, LangGraph |
| Integración de herramientas/contenedores para LLMs | MCP |
| Ciclo de vida de ML y seguimiento de experimentos | MLflow |
| Aplicaciones y UI de datos/ML | Streamlit |

### 📊 Ingeniería de Datos y Streaming

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Orquestación de flujos de trabajo | Airflow |
| Procesamiento distribuido | Spark on K8s |
| Consultas interactivas | Trino |
| Transmisión de eventos y CDC | Kafka, Flink, Debezium |
| Analítica en tiempo real | OLAP |

### 🔧 Ingeniería Analítica

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Integración e ingestión de datos | Airbyte, NiFi, SeaTunnel |
| Transformación y modelado | dbt, SQLMesh |
| Capa semántica / de métricas | Cube |
| Cuadernos interactivos | Jupyter, Zeppelin |
| Inteligencia de negocios y paneles | Metabase, Superset, Lightdash, Redash |

### 🏛️ Gobernanza de Datos

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Catálogo y descubrimiento de datos | OpenMetadata |
| Linaje, contratos y calidad | Linaje, Data Contracts, Data Quality |
| Formato de tabla abierto / lakehouse | Iceberg, Lakekeeper |
| Privacidad y anonimización | anonimización |

### 🗄️ Bases de Datos

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Relacional (PostgreSQL en K8s) | CloudNativePG |
| NoSQL y caché | MongoDB, Redis |
| Analítico / incrustado | DuckDB |
| Bases de datos distribuidas | motores distribuidos |
| Monitoreo y ajuste fino | PgHero, PMM, exporters |

### ☁️ Computación en la Nube

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Servicios gestionados de AWS | EKS, EMR on K8s, S3, IAM, Athena, Redshift |
| Servicios gestionados de Azure | AKS, Databricks, Key Vault, Event Hubs |
| Infraestructura como código | Terraform |
| Emulación de nube local | LocalStack |

### 💻 Ingeniería de Software

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Diseño y exposición de APIs | APIs |
| Mensajería asíncrona | RabbitMQ |
| Banderas de características y funciones sin servidor | feature flags, serverless |
| Aplicación de calidad de código | linters |
| Extracción web | herramientas de scraping |
| Empaquetado y entornos de Python | uv |

### 📚 Documentación

| Propósito / Problema que resuelve | Herramientas |
|---|---|
| Sitios de documentación estática | MkDocs, Docusaurus, Docsify, GitBook, Sphinx |
| Diagramas y documentación visual | Excalidraw, Mermaid |
| Documentación ejecutable / ejecutable | Runme |

---

## 🚀 Primeros pasos

```bash
# 1. Entrar al entorno reproducible (instala kubectl, kind, helm, flux, etc.)
devbox shell

# 2. Levantar un clúster Kind local
kind create cluster --config clusters/kind-configs/core.yaml

# 3. Inicializar GitOps y/o aplicar los manifiestos de infraestructura
#    (Flux reconcilia HelmReleases/Kustomizations desde este repositorio)
```

Cada carpeta en [infrastructure/](infrastructure/) contiene un `doc.md` con instrucciones específicas, enlaces de referencia y manifiestos listos para aplicar.

---

## 📖 Documentación

- [docs/](docs/) — estándares de escritura, hoja de ruta y notas por disciplina
- [docs/docs-standard.md](docs/docs-standard.md) — convenciones de documentación utilizadas en este repositorio
- `doc.md` en cada herramienta — referencia técnica focalizada
- [docs/mermaid/](docs/mermaid/) — diagramas de arquitectura

---

## 📄 Licencia

Ver [LICENSE](LICENSE).
