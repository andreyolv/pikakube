https://github.com/parca-dev/parca
https://github.com/parca-dev/helm-charts

k port-forward svc/parca-server 7070

problema ao rodar agens no kind por causa do docker, erro:
level=error name=parca-agent ts=2024-04-20T16:33:31.364892571Z caller=main.go:375 msg="last stderr" last_stderr="level=warn name=parca-agent ts=2024-04-20T16:33:31.184887101Z caller=main.go:528 msg=\"failed to set GOMAXPROCS automatically\" err=\"path \\\"/docker/7e844a947116714d8576372366bde54cd4bb15a62d732437781b41a6fec56ccc/kubelet.slice/kubelet-kubepods.slice/kubelet-kubepods-besteffort.slice/kubelet-kubepods-besteffort-pod1c5d0bde_130b_4784_a547_f45e619f2514.slice/cri-containerd-bd6fe092f10330edc4ad6e283948c2ef1a455af0b5063b90b2b37d3d850d6690.scope\\\" is not a descendant of mount point root \\\"/docker/7e844a947116714d8576372366bde54cd4bb15a62d732437781b41a6fec56ccc/kubelet\\\" and cannot be exposed from \\\"/sys/fs/cgroup/cpuset/kubelet\\\"\"\nlevel=error name=parca-agent ts=2024-04-20T16:33:31.31811835Z caller=main.go:562 msg=\"the agent can't run in a container, run with privileges and in the host PID (`hostPID: true` in Kubernetes, `--pid host` in Docker)\"\n"