[← Linux](../README.md)

# Shell

<https://github.com/ohmyzsh/ohmyzsh>
<https://github.com/nushell/nushell>
<https://github.com/direnv/direnv>
<https://github.com/withfig/autocomplete>

---

## The problem it solves

Everything in this repository is driven from a terminal. Four different itches get scratched here,
and they are not interchangeable:

| Tool | What it actually is |
|---|---|
| **Oh My Zsh** | a configuration framework for zsh — plugins, themes, completions |
| **Nushell** | a **different shell**, where commands pass structured data instead of text |
| **direnv** | per-directory environment variables, loaded on `cd` and unloaded on leaving |
| **Fig autocomplete** | inline completion UI for existing shells |

Of the four, `direnv` is the one that changes how you work rather than how the prompt looks. A
`.envrc` in a project directory sets `KUBECONFIG`, cloud credentials or a namespace automatically
when you enter it, and unsets them when you leave — which removes the single most common cause of
running a command against the wrong cluster.

## When to use it

- Oh My Zsh — you want kubectl/git completions and a readable prompt without configuring zsh by hand
- direnv — you switch between projects that need different `KUBECONFIG`s or credentials
- Nushell — you routinely parse command output and are tired of `awk` and `jq` glue
- Fig — you want completion hints for CLIs that ship none

## When not to use it

- Oh My Zsh on a server or in a container; it is a workstation convenience with a startup cost
- direnv without care: `.envrc` executes shell code, so allowing an untrusted one is a real risk
- Nushell as the shell in scripts — its syntax is not POSIX and portability disappears
- Fig — check its status before adopting; it was acquired and the product has moved

## Notes

The original note is four links with no commentary — a list of what is known, not what is chosen.
Two points worth adding since they are the ones that bite:

**direnv and `KUBECONFIG`.** The failure this prevents is severe and quiet: a shell left pointed at
a production context, then a `kubectl delete` intended for a local cluster. Per-directory
`KUBECONFIG` makes the context follow the directory instead of the shell's history. It pairs with
[`kubectx`/`kubens`](../../../managed/plugins/kubectx/README.md), which solve the same problem
interactively rather than declaratively.

**direnv's trust model.** `.envrc` is executed shell code, and direnv refuses to load one until you
run `direnv allow`. That prompt is a security boundary, not a nuisance — allowing an `.envrc` from
a cloned repository runs whatever is in it.

**Nushell's actual claim.** Commands return tables, so `ls | where size > 1mb` works without
parsing text. For anything that reads `kubectl -o json` and pipes it through `jq`, that is a
genuine simplification. The cost is that it is not bash: scripts written in it do not run anywhere
else.

---

[← Linux](../README.md)
