# Kubeelasti

```
k port-forward svc/kubeelasti-operator-controller-service 8013
k port-forward svc/kubeelasti-resolver-service 8013
```

http://127.0.0.1:8013/metrics


```
sort_desc(
  count by (__name__) (
    {
      __name__ =~ "elasti_.*"
    }
  )
)
```
