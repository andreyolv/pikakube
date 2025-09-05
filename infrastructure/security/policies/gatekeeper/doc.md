https://github.com/open-policy-agent/gatekeeper
https://github.com/open-policy-agent/gatekeeper-library
https://github.com/open-policy-agent/opa

https://open-policy-agent.github.io/gatekeeper-library/website/
https://github.com/sigstore/cosign-gatekeeper-provider

https://opencredo.com/blogs/controlling-kafka-data-flows-using-open-policy-agent/

exceções politica de tags: flux, spot -> atualização de tags automática

podemos tentar pegar imagens inconformes do CRD, porém é limitado em 20 registros
kubectl get K8sAllowedRepos -o json | jq -r '["NAMESPACE", "NAME", "MESSAGE"], (.items[].status.violations[] | [.namespace, .name, .message]) | @tsv' | column -t -s $'\t' | tr '\t' '|' > images-dev.yaml

a melhor opção é pegar a lista dos logs do pod do gatekeeper, isso pra cada cluster
kubectl logs -l gatekeeper.sh/system=yes -n gatekeeper-system --tail 2000 | jq -c -R -r 'fromjson? | select(.resource_namespace != null and .resource_name != null and .msg != null) | "\(.resource_namespace)\t\(.resource_name)\t\(.msg)"' | grep "has an invalid image repo" | sort | uniq | column -t -s $'\t' | tr '\t' '|' > images-dev.yaml
kubectl logs -l gatekeeper.sh/system=yes -n gatekeeper-system --tail 2000 | jq -c -R -r 'fromjson? | select(.resource_namespace != null and .resource_name != null and .msg != null) | "\(.resource_namespace)\t\(.resource_name)\t\(.msg)"' | grep "didn't specify an image tag" | sort | uniq | column -t -s $'\t' | tr '\t' '|' > images-dev.yaml

agora junta arquivos de cada cluster num só sem duplicados
awk '{$1=$2=""; print $0}' images-*.yaml | sort | uniq | awk -F '<|>' '{print $4}' > all-images.txt

comandos para separar registries por origem
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*quay\.io.*$' > quay-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*gcr\.io.*$' > gcr-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*ghcr\.io.*$' > ghcr-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep '^.*registry\.k8s\.io.*$' > registry-k8s-io.txt
awk '{$1=$2=""; print $0}' images-*.yaml | awk -F '<|>' '{print $4}' | sort | uniq | grep -vE '^(quay\.io|gcr\.io|ghcr\.io|registry\.k8s\.io)' > dockerhub.txt