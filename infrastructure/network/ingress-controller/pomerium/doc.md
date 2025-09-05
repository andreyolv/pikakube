https://github.com/pomerium/pomerium
https://github.com/pomerium/ingress-controller

kubectl apply -k github.com/pomerium/ingress-controller/config/default?ref=v0.28.0 --dry-run=client -o yaml > input.yaml

yq eval '.items[] | "---\n" + to_yaml' input.yaml | kubectl-slice -f - -o ./output

      allow:
        and:
          - claim/groups: 'xxxxxxxxxxxx'

#   #  ingress.pomerium.io/policy: |
#   #    allow:
#   #      and:
#   #      - user:
#   #          is: xxxxxxxxx
#   #    deny:
#   #      and:
#   #      - user:
#   #          is: xxxxxxxxxxxxx