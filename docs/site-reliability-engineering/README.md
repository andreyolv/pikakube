
graph TD
    subgraph Kubernetes
        direction TD
        subgraph Backup & Restore
            Velero[(Velero)]
        end

        subgraph Canary Deployment
            Flagger[(Flagger)]
        end

        subgraph Chaos Engineering
            Litmus[(Litmus)]
        end
    end
    