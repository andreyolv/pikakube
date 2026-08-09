[← DAST](../README.md)

# Nuclei

<https://github.com/projectdiscovery/nuclei>

---

## The problem it solves

Nuclei is a fast, template-driven scanner. The engine itself is deliberately simple: send the
requests a template describes, match the responses against the conditions the template specifies,
report when they match.

```yaml
id: exposed-actuator-env
info:
  name: Spring Boot Actuator /env exposed
  severity: high
requests:
  - method: GET
    path:
      - "{{BaseURL}}/actuator/env"
    matchers:
      - type: word
        words: ["\"activeProfiles\""]
      - type: status
        status: [200]
```

That is the whole model, and it is why the tool is fast: no crawling, no browser, no state — just
targeted requests, massively parallel.

**The template library is the actual product.** Thousands of community-maintained templates
covering:

| Category | Examples |
|---|---|
| Known CVEs | a specific vulnerable version of a specific product, detected by its response |
| Exposed panels | admin interfaces, dashboards, management consoles reachable without authentication |
| Misconfigurations | directory listing, exposed `.git`, `/actuator`, debug endpoints, open metrics |
| Default credentials | vendor defaults still in place |
| Exposures | API keys and tokens in responses, verbose errors, stack traces |
| Takeovers | dangling DNS records pointing at unclaimed services |
| Technology detection | fingerprinting what is running |

New templates typically appear within hours of a CVE being published. Adopting Nuclei is best
understood as **subscribing to the community's detection knowledge**, not as installing a scanner.

Writing your own templates is genuinely easy — the YAML above is representative — which makes it a
good tool for encoding organisation-specific checks: "no host should ever expose this internal
path".

## When to use it

- **Sweeping a broad surface for known problems.** Many hosts, many services, checked fast. This
  is what it is best at and nothing else in this folder competes
- **Infrastructure and platform components**, which is the highest-value case for a repository
  like this one: Grafana, Airflow, Airbyte and every other exposed UI are well-known software with
  well-known exposures, and templates exist for all of them
- **Immediately after a headline CVE.** A template usually exists within hours; "are we exposed"
  becomes one command
- **Continuous external attack surface monitoring**, on a schedule against your own hostnames
- **Encoding your own rules** — a custom template for an internal path that must never be public
- **In CI, with a narrow template selection**, against a staging environment

## When not to use it

- **In place of a proper application scanner.** Nuclei checks for *known* problems. It will not
  find the SQL injection in the endpoint your team wrote last week — that needs
  [`../zaproxy/README.md`](../zaproxy/README.md) or SAST
- **With every template enabled.** Thousands of templates means thousands of requests: rate
  limiting, WAF bans, and noise. Select by tag, severity or technology
- **Against systems you do not own.** It is fast and aggressive enough that untargeted use looks
  exactly like an attack, because it is one
- **Against production without care.** Most templates are detection-only, but some are
  intrusive. Use severity and tag filters, and check what a template does before running it
  broadly
- **Without pinning the template version.** The library updates constantly, which is the point —
  and it also means a scheduled scan's results can change without your configuration changing.
  For a CI gate, pin; for monitoring, do not
- **As authenticated application testing.** It supports headers and cookies, but session-based,
  multi-step authenticated flows are ZAP's territory

## Notes

Original note recorded for this tool:

- <https://github.com/projectdiscovery/nuclei> — the engine, from ProjectDiscovery. The repository
  documents the template syntax (requests, matchers, extractors, `dsl` expressions, workflows for
  chaining templates), the filtering flags (`-tags`, `-severity`, `-exclude-tags`), rate limiting
  and concurrency controls, and the Go library interface for embedding it.

The companion repository the documentation assumes you know about is
**`projectdiscovery/nuclei-templates`** — the community template library. That is the one to watch
rather than the engine: it is where new detections land, and browsing the templates for the
software you actually run is the fastest way to decide which tags to enable.

Two practical notes:

- **`-tags` and `-severity` filtering is not optional** on a real target. The default is
  everything, and everything is a lot.
- ProjectDiscovery's other tools compose with it — `subfinder` for subdomain discovery, `httpx`
  for probing which of them respond, then Nuclei against the survivors. That pipeline is how the
  tool is used for external attack-surface monitoring, and it is worth knowing even if you only
  ever point it at a known list of hostnames.

---

[← DAST](../README.md)
