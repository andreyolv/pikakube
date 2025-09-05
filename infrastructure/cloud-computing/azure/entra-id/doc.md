az ad group member list --group XXXXXXXXXXXX --query [].mail

az ad group member list --group XXXXXXXXXXXX --query [].mail | grep -oP '[^" ]+@[^" ]+' | while read -r email; do
  username=$(echo $email | cut -d '@' -f 1 | tr '.' '-' | tr '[:upper:]' '[:lower:]')
  echo "- $username"
done