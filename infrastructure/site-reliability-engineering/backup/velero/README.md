velero version

velero get backup, schedule, restore, backup-location

velero backup describe <BACKUP> --details > backup.yaml

kubectl -n velero edit backup <backupName>

---
efs
node agent
kubectl -n YOUR_POD_NAMESPACE annotate pod/YOUR_POD_NAME backup.velero.io/backup-volumes=YOUR_VOLUME_NAME_1,YOUR_VOLUME_NAME_2,...

---
migração entre cluster só funciona pra mesma região, caso contrário tem q usar backup filesystem
pra migrar é só apontar ambos veleros de cada cluster pro mesmo volumesnapshotlocation, super simples
