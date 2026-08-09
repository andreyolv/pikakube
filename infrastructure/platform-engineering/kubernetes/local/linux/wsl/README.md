[← Linux](../README.md)

# WSL

<https://github.com/microsoft/WSL>
<https://github.com/sakai135/wsl-vpnkit>

---

## The problem it solves

Running the Linux toolchain — `kubectl`, `docker`, `flux`, shell scripts — on a Windows laptop
without dual-booting or running a full desktop VM. WSL2 is a real Linux kernel in a lightweight VM,
integrated well enough that it feels like a terminal.

The gap between "feels like a terminal" and "is a VM with its own disk, memory budget and network
stack" is where all the trouble lives, and every note below is a consequence of it.

## When to use it

- The workstation is Windows and the work is Linux
- You want Docker Desktop's Linux containers with a usable shell underneath
- Corporate policy makes dual-boot or a hypervisor impractical

## When not to use it

- Workloads that need real hardware access or precise I/O behaviour
- Anything where filesystem performance across `/mnt/c` dominates — keep the work inside the Linux filesystem
- As a stand-in for a Linux server; the VM's lifecycle is tied to Windows
- If the corporate VPN cannot be worked around; see the note below

## Notes

**Install** — from PowerShell:

```sh
wsl --install
```

Reference: <https://learn.microsoft.com/en-us/windows/wsl/install#install-wsl-command>

To find out which Ubuntu version you ended up with:

```sh
lsb_release -a
```

**Auto-starting Docker via `wsl.conf` does not work.** The recorded verdict, translated from the
original note, is blunt: *"in theory this would be beautiful, but in practice it does not work and
throws an error — do not use this rubbish."* The configuration in question:

```sh
sudo vi /etc/wsl.conf
```

```
[boot]
command = service docker start
```

Worth preserving exactly because it is the obvious thing to try, it is widely suggested online, and
it fails. Start the daemon from the shell profile or use Docker Desktop's WSL integration instead.

**The virtual disk.** WSL creates a VHD with a **1 TB default maximum size**, stored under
`C:\Users\<user>\AppData\Local\wsl`. Two consequences: the disk grows as you use it and **does not
shrink when you delete files**, and the C: drive is where that growth lands. Shrinking it is a
manual operation — <https://stephenreescarter.net/how-to-shrink-a-wsl2-virtual-disk/>.

**CPU and memory limits** are set on the Windows side, not inside Linux, in
`C:\Users\<user>\.wslconfig` —
<https://learn.microsoft.com/en-us/windows/wsl/wsl-config#example-wslconfig-file>. Without it, WSL
will take a large share of host memory and the symptom is a Windows machine that swaps while Linux
looks idle.

**Corporate VPNs break WSL networking.** This is common and has a known workaround —
<https://github.com/sakai135/wsl-vpnkit>. Enabling it:

```sh
wsl.exe -d wsl-vpnkit --cd /app sed -i -- "s/enabled=false/enabled=true/" /etc/wsl.conf
wsl.exe -d wsl-vpnkit --cd /app wsl-vpnkit
```

It runs as a separate WSL distribution that proxies traffic, which is why the commands target
`-d wsl-vpnkit` rather than your normal distro. Symptom it fixes: DNS and outbound connections work
on Windows and fail inside WSL the moment the VPN connects.

---

[← Linux](../README.md)
