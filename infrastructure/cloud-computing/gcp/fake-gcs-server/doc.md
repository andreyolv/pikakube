https://github.com/fsouza/fake-gcs-server

An emulator for the **Cloud Storage API only**. BSD-2-Clause.

Three ways to run it, and the first is the differentiator:

- as a **Go library** (`fakestorage`), in-process inside a test — no container, no port, no
  lifecycle to manage
- as a standalone binary
- as a container: `fsouza/fake-gcs-server`

Limits worth knowing before wiring it into a test suite:

- signed URLs are not really validated — signature and expiry are accepted as-is
- clients must be pointed at the emulator; there is no interception of
  `storage.googleapis.com`, and signed-URL flows need `-public-host` set to match

When to prefer it over [floci-gcp](../floci/doc.md): the test only touches buckets and objects,
and an in-process fake is worth more than a second container in CI. When not: anything beyond
storage — Pub/Sub, BigQuery, Secret Manager — where floci-gcp covers the surface and this
does not.

Same role in this repo as [azurite](../../azure/azurite/doc.md) does for Azure Blob: the narrow,
storage-only emulator next to the broad one.
