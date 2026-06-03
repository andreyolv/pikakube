https://github.com/kubernetes/dashboard

Get Token:
https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md

kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d

merda pra local host https://github.com/kubernetes/dashboard/issues/8829