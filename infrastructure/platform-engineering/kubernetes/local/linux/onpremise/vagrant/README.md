[← On premise](../README.md)

# Vagrant

<https://github.com/hashicorp/vagrant>
<https://github.com/Karandash8/virtualbox_WSL2>

---

## The problem it solves

You need several Linux VMs with known IPs, known specs and a known base image, created identically
every time, so you can install Kubernetes on them by hand and destroy the result without regret.
A `Vagrantfile` describes that; `vagrant up` builds it.

This is the environment in which `kubeadm` is worth learning. A managed cluster hides the control
plane, and a kind cluster fakes the nodes; Vagrant gives you actual machines with actual kubelets,
which is the only way the bootstrap and upgrade procedures in
[`on-premise/provision/`](../../../../on-premise/provision/README.md) mean anything.

## When to use it

- Practising cluster bootstrap and upgrades on real, disposable multi-node VMs
- Reproducing a multi-machine networking scenario that containers cannot represent
- Certification practice — CKA and LFCS both assume a machine you can break
- Any test that needs a real kernel and a real systemd per node

## When not to use it

- The inner loop for application code — far too slow; use [`local/distributions/`](../../../distributions/README.md)
- Production provisioning; that is Cluster API, Kubespray or Kubean
- Cloud VMs — Terraform/OpenTofu is the right tool there
- Machines with little RAM; three VMs is three real memory allocations

## Notes

**The command set** recorded here is the whole working vocabulary:

```sh
vagrant -v
vagrant up
vagrant status
vagrant ssh <name>
vagrant reload
vagrant halt
vagrant destroy
```

`halt` stops the VMs and keeps them; `destroy` removes them. The distinction matters when a lab
takes twenty minutes to build.

**Debugging SSH**, which is where Vagrant most often goes wrong:

```sh
vagrant ssh -- -vvv
vagrant ssh -debug
vagrant ssh-config
```

`vagrant ssh -- -vvv` passes verbosity through to the underlying `ssh`, which is what tells you
whether the failure is Vagrant's or the network's. `vagrant ssh-config` prints the host, port and
key file — the details you need to connect with a plain `ssh` client or point an IDE at the VM.

**Running a command without an interactive session:**

```sh
vagrant ssh <master-name> -c "command"
```

This is how a multi-node setup gets scripted — `kubeadm init` on the master, `kubeadm join` on the
workers, without typing in three terminals.

The `hello-world` example in this folder serves a page at `localhost:8080/site.html`, which is the
minimum proof that port forwarding from the VM to the host is working before anything harder is
attempted.

### Vagrant under WSL

This is the awkward part, and it is recorded in detail because it is not discoverable. Vagrant
running inside WSL has to drive VirtualBox running on **Windows**, which means crossing the
boundary deliberately:

```sh
echo 'export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"' >> ~/.bashrc
echo 'export PATH="$PATH:/mnt/c/Program Files/Oracle/VirtualBox"' >> ~/.bashrc
echo 'export VAGRANT_WSL_WINDOWS_ACCESS_USER_HOME_PATH="/mnt/c/Users/andre/vagrant/hello-world"' >> ~/.bashrc
source ~/.bashrc
cat ~/.bashrc
```

What each one does, since none of them is guessable:

- `VAGRANT_WSL_ENABLE_WINDOWS_ACCESS` — permits the Linux-side Vagrant to touch the Windows
  filesystem at all. Off by default.
- The `PATH` addition points at the Windows VirtualBox binaries; without it Vagrant reports that no
  provider is available.
- `VAGRANT_WSL_WINDOWS_ACCESS_USER_HOME_PATH` tells Vagrant which Windows directory corresponds to
  its working directory. The project must live under `/mnt/c/...` — a `Vagrantfile` on the Linux
  filesystem is not reachable by the Windows-side VirtualBox.

Which is why the working directory is on the Windows side:

```sh
cd /mnt/c/Users/andre/vagrant
vagrant up
vagrant ssh
```

**Version matching is a hard requirement.** The recorded note is short and load-bearing: the
Vagrant version on Windows and the one in WSL must be the same. Mismatched versions produce state
files that one side cannot read.

**The plugin:**

```sh
vagrant plugin install virtualbox_WSL2
```

Reference: <https://github.com/Karandash8/virtualbox_WSL2>. Vagrant does not natively understand
this Linux-driving-Windows arrangement; the plugin is what makes the VirtualBox provider work from
inside WSL.

**Recorded upstream issue:** <https://github.com/joelhandwell/ubuntu_vagrant_boxes/issues/1> — a
problem with the Ubuntu box images themselves, which is the other place this setup fails and looks
like a Vagrant bug.

`ssh-keygen` appears at the end of the notes: the keys have to exist on the side that will connect,
and in the WSL arrangement it is easy to end up with a key Windows generated and Linux cannot read.

---

[← On premise](../README.md)
