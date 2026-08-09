[← Certifications](../README.md)

# CKA

<https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/>
<https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/>
<https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/>
<https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/#normal-user>

---

## The problem it solves

Certified Kubernetes Administrator is a timed, hands-on exam: a terminal, a set of clusters, and
tasks to complete. Passing it requires being able to bootstrap, upgrade, back up, break and repair a
cluster without looking anything up.

The notes in this folder are the residue of doing that, and they are the closest thing in this
repository to an operational runbook for a self-managed cluster.

## When to use it

- You operate or intend to operate self-managed clusters
- The `kubeadm` upgrade order and etcd restore procedure need to be in muscle memory
- As a prerequisite for [CKS](../cks/README.md), which requires it
- To find out which parts of Kubernetes a managed control plane has been hiding

## When not to use it

- If the estate is entirely EKS/AKS/GKE and will stay that way — much of it never applies
- As a substitute for operating a real cluster; the exam certifies a snapshot
- Before being comfortable on Linux — [LFCS](../lfcs/README.md) is the layer underneath

## Notes

Eight files sit beside this one. What each contains and why it matters:

**`basic-commands`** — the speed toolkit. `alias k="kubectl"`, completion, `kubectl explain`, and
the generation idiom that replaces writing YAML:

```sh
kubectl apply -k <directory> --dry-run=client -o yaml > manifest.yaml
```

Plus context handling, which is the habit that prevents running a command against the wrong cluster:

```sh
kubectl config get-contexts
kubectl config use-context <name>
kubectl config set-context --current --namespace=<namespace>
kubectl config view --minify | grep namespace:      # verify it took
```

And the selectors that avoid grepping: `--selector type=user-space -A`, `--show-labels`,
`--field-selector status.phase=Running`, `-o wide --sort-by .spec.nodeName`. `--sort-by
.spec.nodeName` is the one worth stealing — it groups pods by node, which is how you see
distribution problems at a glance.

**`debug-problems`** — where to look when a node is wrong. `systemctl status/stop/start/enable
kubelet`, `journalctl -u kubelet`, and the log paths: `/var/log/kube-apiserver.log`,
`kube-scheduler.log`, `kube-controller-manager.log` on control-plane nodes; `kubelet.log`,
`kube-proxy.log` on workers. On a managed cluster none of these exist for you; on a self-managed one
they are the first place to go.

**`kubeadm-upgrade-nodes`** — the procedure that must be done in order:

```sh
# Control plane
kubectl drain control-plane --ignore-daemonsets
sudo apt-get install -y --allow-change-held-packages kubeadm=1.22.2-00
sudo kubeadm upgrade plan v1.22.2
sudo kubeadm upgrade apply v1.22.2
sudo apt-get install -y --allow-change-held-packages kubelet=1.22.2-00 kubectl=1.22.2-00
sudo systemctl daemon-reload && sudo systemctl restart kubelet
kubectl uncordon control-plane

# Workers
kubectl drain worker1 --ignore-daemonsets --force
sudo apt-get install -y --allow-change-held-packages kubeadm=1.22.2-00
sudo kubeadm upgrade node
sudo apt-get install -y --allow-change-held-packages kubelet=1.22.2-00 kubectl=1.22.2-00
sudo systemctl daemon-reload && sudo systemctl restart kubelet
kubectl uncordon worker1
```

Three things this encodes: `--allow-change-held-packages` is needed because the Kubernetes packages
are deliberately pinned with `apt-mark hold` so they never upgrade by accident; the control plane
goes first and workers second, because kubelets may lag the API server but never lead it; and
`kubeadm upgrade apply` on the control plane becomes `kubeadm upgrade node` on workers — different
commands for the same operation.

**`etcd-backup-restore`** and **`etcd-operations`** — short, with one practical note: on kind you
have to exec into the etcd container to reach `etcdctl`, because it is not on the host. The
operations themselves are `./etcd` to run it and `./etcdctl get`/`set` against it.

**`static-pod`** — `/etc/kubernetes/manifests`, and after dropping a manifest there,
`sudo systemctl restart kubelet`. This is how the control plane runs itself: the kubelet watches that
directory and starts whatever it finds, with no API server involved. It is also the recovery route
when the API server is the thing that is down.

**`users-auth`** — creating a real user, which Kubernetes has no object for. Generate a key and CSR,
sign it with the cluster CA in `/etc/kubernetes/pki/`, then build a kubeconfig:

```sh
openssl genrsa -out myuser.key 2048
openssl req -new -key myuser.key -out myuser.csr -subj "/CN=myuser"
sudo openssl x509 -req -in myuser.csr -CAcreateserial \
  -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key \
  -out myuser.crt -days 1000
```

Then `config set-cluster`, `set-credentials --embed-certs`, `set-context`, `use-context`, and finally
a Role and RoleBinding — the notes end with `kubectl create role databasemanager
--verb=get,list,create,delete --resource=pods --namespace databases` and a matching binding.

The point to carry away: **the `CN` of the certificate is the username** and its `O` is the group.
There is no user object; identity is whatever the CA signed. That is why a leaked cluster CA key is
total compromise, and why the file has `sudo` in front of the signing step.

(The file contains a typo — `ca.crs` where it should be `ca.crt`, and `rn` where `rm` was meant.
Preserved as written; both are obvious in practice.)

**`kubeadm-install-k8s`** — the two upstream installation guides, which is correctly all it needs to
be.

---

[← Certifications](../README.md)
