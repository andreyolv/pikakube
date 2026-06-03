yq eval '.items[] | "---\n" + to_yaml' input.yaml | kubectl-slice -f - -o ./output
