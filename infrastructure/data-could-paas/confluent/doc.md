azure limitation
https://docs.confluent.io/cloud/current/networking/peering/azure-peering.html

Transitive VNet peering is not supported. If you peer Network A to Network B, and peer Network B to Confluent Cloud, applications running in Network A will not be able to access Confluent Cloud.
