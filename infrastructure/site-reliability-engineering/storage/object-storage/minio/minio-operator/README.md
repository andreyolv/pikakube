https://github.com/minio/operator

k get secret console-sa-secret -o jsonpath="{.data['token']}" | base64 --decode
