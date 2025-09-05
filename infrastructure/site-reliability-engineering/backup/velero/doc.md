https://github.com/vmware-tanzu/velero
https://github.com/vmware-tanzu/helm-charts
https://github.com/vmware-tanzu/velero-plugin-for-csi
https://github.com/vmware-tanzu/velero-plugin-for-aws
https://github.com/vmware-tanzu/velero-plugin-for-microsoft-azure
https://github.com/seriohub/velero-ui
https://github.com/kopia/kopia

procsso pra restore do strimzi

podemos deletar um volume que é criado automaticamente pelo operator novamente
em caso de restore de um pvc é necessário pausar o operator pra ele não criar um pvc novo do zero
kubectl scale deploy/strimzi-cluster-operator --replicas=0

https://github.com/seriohub/velero-ui/blob/main/tmp/helm/seriohub-velero/values.yaml


DONE
- Integrar com MinIO (S3 Bucket da AWS).
- Integrar com Blob Storage da Azure.
- Backups, restores e schedules aplicados atráves dos yamls CRD's do Velero para sincronia com GitOps e manter histórico no Github.

TODO
- File System Backup com Kopia

https://github.com/vmware-tanzu/velero/tree/main/design/Implemented

https://github.com/vmware-tanzu/velero/discussions/7196
https://github.com/vmware-tanzu/velero/issues/6195
https://github.com/vmware-tanzu/velero/issues/4802
https://github.com/vmware-tanzu/velero/discussions/4786

https://github.com/vmware-tanzu/velero/discussions/8794
https://github.com/vmware-tanzu/velero/issues/3151
