https://github.com/prometheus-community/helm-charts
https://github.com/prometheus-operator/kube-prometheus
https://github.com/prometheus-operator/prometheus-operator
https://github.com/prometheus/OpenMetrics
https://github.com/prometheus/node_exporter
https://github.com/prometheus/prometheus
https://github.com/prometheus/pushgateway

libs go que enchem métricas no prometheus de linguiça
go_* process_* - https://github.com/prometheus/client_golang
rest_client_* - https://github.com/kubernetes/client-go
controller_runtime_* workqueue_* certwatcher_* - https://github.com/kubernetes-sigs/controller-runtime
apiserver_* - https://github.com/kubernetes/apiserver
disabled_metrics_total hidden_metrics_total registered_metrics_total cardinality_enforcement_unexpected_categorizations_total - https://github.com/kubernetes/component-base
aggregator_discovery_* leader_election_* - https://github.com/kubernetes/kubernetes

kube state metrics list
https://github.com/kubernetes/kube-state-metrics/tree/main/docs
k port-forward svc/kube-prometheus-stack-kube-state-metrics 8080

cadvidor metrics list
https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md

node exporter metrics list
não tem doc nessa merda pqp
k port-forward svc/kube-prometheus-stack-prometheus-node-exporter 9100

not Retention Time per Metric
https://github.com/prometheus/prometheus/issues/15350
https://github.com/prometheus/prometheus/issues/1381


https://github.com/prometheus-community/postgres_exporter/pull/911
https://github.com/prometheus/node_exporter/issues/2607

https://github.com/prometheus-operator/prometheus-operator/issues/1547
https://github.com/prometheus-operator/prometheus-operator/issues/2398
https://github.com/prometheus-operator/prometheus-operator/issues/5452
