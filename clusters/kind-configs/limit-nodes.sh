#!/bin/bash

CPU_LIMIT="2"
MEMORY_LIMIT="8g"
MEMORY_SWAP_LIMIT="8g"  # Swap total = RAM (sem swap adicional)

# Aplica os limites em todos os nós do Kind
for node in $(docker ps --format '{{.Names}}' --filter name=pikakube | sort); do
  echo "🔧 Aplicando limites em $node..."
  docker update --cpus="$CPU_LIMIT" --memory="$MEMORY_LIMIT" --memory-swap="$MEMORY_SWAP_LIMIT" "$node"

  echo "🔁 Reiniciando $node..."
  docker restart "$node"

  echo "✅ Limites aplicados em $node:"
  echo -n "   CPUs:   "
  docker inspect "$node" --format='{{.HostConfig.NanoCpus}}' | awk '{ printf "%.2f\n", $1 / 1000000000 }'
  echo -n "   Memory: "
  docker inspect "$node" --format='{{.HostConfig.Memory}}' | awk '{ printf "%.2f GiB\n", $1 / 1024 / 1024 / 1024 }'
done

echo "🏁 Todos os nós foram atualizados com sucesso."
docker stats --no-stream

# kubectl describe nodes | grep -A6 "Capacity"
# https://github.com/kubernetes-sigs/kind/issues/877
# não atualiza o valor de CPU e memória no node
