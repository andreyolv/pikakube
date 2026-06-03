kubectl run myapp --image=busybox:1.28 --restart=Never -- sleep 1d

kubectl debug myapp --container=myapp -it --image=ubuntu --share-processes --copy-to=myapp-debug