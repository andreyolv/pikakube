https://github.com/kubecost/cost-analyzer-helm-chart
https://github.com/kubecost/cost-prediction-action

curl http://kubecost.dev.xxxx.ai/model/allocation \
  -d window=3d \
  -d aggregate=namespace \
  -d accumulate=false \
  -d shareIdle=false \
  -d format=csv \
  -G

https://github.com/kubecost/cost-analyzer-helm-chart/issues/2392
