https://github.com/Azure/acr

az account list --output table
az account set --subscription 
az login --service-principal --allow-no-subscriptions \
-u XXXXXXXXXXXXXX \
-p XXXXXXXXXXXXXX \
-t XXXXXXXXXXXXXX

PURGE_CMD="acr purge --filter 'kafka-strimzi/gac:.*' --ago 5d --keep 10 --dry-run" 
PURGE_CMD="acr purge --filter 'plot/.*:.*' --ago 120d --keep 30 --dry-run"

az acr run --cmd "$PURGE_CMD" --registry xxxxxxxxxx /dev/null

az login --use-device-code
az acr login --name <name>
docker pull <name>.azurecr.io/nomedasuaimagem:tag

az acr repository show --name xxxxxx --repository prefect-base
az acr repository show --name xxxxxx --image prefect-base:0.0

https://github.com/Azure/acr/issues/169

---------
repo_list="plot/plot-backend:.* plot/plot-frontend:.*"

for repo in $repo_list; do
    echo "Cleaning repository $repo ..."
    PURGE_CMD="acr purge --filter $repo --ago $DAYS_RETAIN --keep $IMAGES_RETAIN --dry-run"
    az acr run --cmd "$PURGE_CMD" --registry $ACR_NAME /dev/null
    echo "Repository $repo has been cleaned!"
done

-------------
arr_reglist="
ws-tunnel-client
ws-tunnel-server
zeus-api-ingest-data
"

for myReg in ${arr_reglist[@]}; do
  az acr repository show-manifests -n xxxxxxxx --repository $myReg --only-show-errors --detail --query '[].{Size: imageSize, Tags: tags[0],Created: createdTime}' -o tsv | awk -v myReg="$myReg" '{ byte =$1 /1024/1024; print myReg " " byte " " $2, $3}' >> "repos.yaml"
done

-----------
Show tags
az acr repository show-tags --name xxxxxxxxxx --repository kubecost-extraction-airflow-worker --output table
az acr manifest list-metadata --registry xxxxxxxxxx  --name kubecost-extraction-airflow-worker --query '[].{Tag:tags[0],Size:size}' --output table

az acr repository show-tags --name xxxxxxxxxx --repository kubecost-extraction-airflow-worker --detail --output json

az acr repository show-manifests -n xxxxxxxxxx --repository kubecost-extraction-airflow-worker --detail --query '[].{Size: imageSize, Tags: tags[0]}'

az acr repository show-manifests -n xxxxxxxxxx --repository kubecost-extraction-airflow-worker --only-show-errors --detail --query '[].{Size: imageSize, Tags: tags[0],Created: createdTime}' -o tsv | awk -v myReg="kubecost-extraction-airflow-worker" '{ byte =$1 /1024/1024; print myReg " " byte " " $2, $3}' >> "repos.yaml"
az acr repository show-manifests -n xxxxxxxxxx --repository analytics_hub_backend --only-show-errors --detail --query 'sort_by([].{Size: imageSize, Tags: tags[0], Created: createdTime}, &Created) | reverse(@)' -o tsv | awk -v myReg="analytics_hub_backend" '{ byte =$1 /1024/1024; print myReg " " $2 " " byte "MB " $3 }'


PURGE_CMD="acr purge --filter 'plot/plot-frontend:.*' --ago 30d --keep 10 --dry-run"
PURGE_CMD="acr purge --filter 'prog-backend:.*' --ago 30d --keep 10"

az acr run --cmd "$PURGE_CMD" --registry xxxxxxxxxx /dev/null

horrible limitations azure container registry
https://github.com/Azure/acr/issues/654
https://github.com/Azure/acr/issues/548
https://github.com/Azure/acr/issues/824
