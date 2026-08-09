[← boto3](../README.md)

# Sample data

---

## What this is

Ten JSON files, `output_0.json` through `output_9.json`, used as the payload by every notebook in
this folder. Nothing here is documentation of a tool — it is the data the examples upload,
download, tag, lock and expire.

Each file holds one object with a `clientes` array of synthetic credit applications:

```json
{"clientes": [
  {"id": "caa20ad43184d21a512aa2f4f02c1b9e", "name": "KAYLAH", "idade": 48,
   "credito_solicitado": 221760, "data_solicitacao": "01/03/2022 17:50"}
]}
```

| Field | Content |
|---|---|
| `id` | a 32-character hex hash |
| `name` | a generated name, upper-case, with accented characters |
| `idade` | age |
| `credito_solicitado` | requested credit amount |
| `data_solicitacao` | request timestamp, `MM/DD/YYYY HH:MM` |

The data is **synthetic** — generated names and amounts, not extracted from anything.

## Why ten files rather than one

The count is the useful property. Several notebooks iterate a directory and upload everything in
it:

```python
lista_arquivos = sorted([f for f in os.listdir(PATH_ROOT) if f.endswith('.json')])
for arquivo in lista_arquivos:
    s3.upload_file(PATH_ROOT + arquivo, BUCKET, arquivo)
```

Ten distinct keys is enough to exercise listing, prefix filtering, per-object tagging and
per-object retention without any of it being a single-object special case — and small enough to run
in seconds.

The notebooks reference these under `/home/jovyan/jsons/`, the Jupyter container's home directory,
which is where they were run.

## Notes

Two things about the shape of this data are worth noticing, because they are exactly what a
lakehouse is for.

**It is nested JSON, and each file wraps its rows in a single top-level object.** Reading it means
parsing the whole file and unwrapping `clientes` — you cannot stream rows, and you cannot push a
predicate down. That is the everyday form raw ingestion arrives in, and the reason a landing zone
and a curated layer are different things. See [`table-formats/`](../../../../table-formats/README.md)
for what converting it to a columnar table buys.

**The fields look like personal data.** They are synthetic, but the *shape* — an identifier, a name,
an age, a financial amount — is precisely what triggers a retention obligation and a right to
erasure. That the notebooks exercise object lock, retention and lifecycle rules against exactly
this shape of record is a reasonable accident: those are the controls the shape demands. See
[`anonymization/`](../../../../../anonymization/README.md) for the other half of that problem.

The field names are in Portuguese, matching the original notes these examples came from.

---

[← boto3](../README.md)
