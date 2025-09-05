https://github.com/controlplaneio-fluxcd/flux-operator
https://github.com/controlplaneio-fluxcd/charts

# Create Github App with Permissions
https://fluxcd.io/flux/installation/bootstrap/github/#github-organization

echo 'export PIKAKUBE_FLUX_OPERATOR_APP_ID=1633681' >> ~/.bashrc
echo 'export PIKAKUBE_FLUX_OPERATOR_INSTALLATION_ID=76665228' >> ~/.bashrc
source ~/.bashrc

kubectl get fluxreport/flux -n flux-system -o yaml

#https://github.com/fluxcd/flux2-monitoring-example/tree/main/monitoring/configs/dashboards
