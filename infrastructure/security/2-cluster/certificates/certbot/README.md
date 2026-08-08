# certbot

<https://github.com/certbot/certbot>
<https://eff-certbot.readthedocs.io/>

The classic ACME client from the EFF. Talks to Let's Encrypt, solves the challenge,
installs the certificate and schedules renewal via a systemd timer or cron.

Where it sits against cert-manager and the cloud services: [../README.md](../README.md)

---

## Where it shines

A VM or bare-metal host running nginx or Apache, with a public domain, and no Kubernetes in
the picture. Renewal becomes a systemd timer you never think about again.

## Where not to use it

**Inside Kubernetes.** cert-manager does the same job declaratively, landing the certificate
as a `Secret` the Ingress consumes directly. Running certbot in a cluster means a pod
writing files to a volume that something else has to pick up — it fights the model.

## Common commands

```bash
# obtain and configure automatically for nginx
certbot --nginx -d example.com -d www.example.com

# obtain only, without touching the web server config
certbot certonly --webroot -w /var/www/html -d example.com

# DNS-01, required for wildcards and for hosts not reachable from the internet
certbot certonly --dns-route53 -d '*.example.com'

# verify renewal works, without hitting rate limits
certbot renew --dry-run

# what is currently managed on this host
certbot certificates
```

## Where things live

| Path | What |
|---|---|
| `/etc/letsencrypt/live/<domain>/` | the current certificate and key (symlinks) |
| `/etc/letsencrypt/renewal/<domain>.conf` | per-certificate renewal configuration |
| `/etc/letsencrypt/archive/` | every historical version |

Renewal runs twice daily through the packaged systemd timer and only acts when the
certificate is within 30 days of expiry.

## Rate limits

Let's Encrypt enforces production rate limits per registered domain. Use
`--dry-run`, or the staging endpoint, while iterating:

```bash
certbot certonly --staging -d example.com
```

Staging certificates chain to an untrusted root on purpose — they validate the flow, not
the trust.
