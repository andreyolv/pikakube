https://github.com/argoproj/argo-events
https://github.com/argoproj/argo-helm

https://github.com/argoproj/argo-events/tree/master/examples


kubectl -n argo-events port-forward $(kubectl -n argo-events get pod -l eventsource-name=webhook -o name) 12000:12000 &
