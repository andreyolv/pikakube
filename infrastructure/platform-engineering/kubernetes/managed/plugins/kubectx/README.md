[← Plugins](../README.md)

# kubectx

<https://github.com/ahmetb/kubectx>

---

## The problem it solves

Switching cluster with plain `kubectl` means:

```sh
kubectl config use-context arn:aws:eks:eu-west-1:123456789012:cluster/production
```

Typed, or found in shell history. With `kubectx` it is `kubectx production`, with tab completion, an
interactive picker if `fzf` is installed, and `kubectx -` to jump back to the previous context — the
same idea as `cd -`.

Its sibling `kubens` does the same for namespaces, replacing `kubectl config set-context --current
--namespace=x` and removing `-n` from every subsequent command.

## When to use it

- More than one cluster or more than one namespace — which is everyone
- Aliasing long cloud-generated context names to short readable ones
- Reducing the friction of switching, so that switching is done deliberately rather than avoided

## When not to use it

- In scripts; `kubectl --context=x` is explicit and does not depend on ambient state
- CI, where the context should be passed per command rather than set globally
- As the **only** defence against acting on the wrong cluster — see below

## Notes

Recorded as a link only.

**The important point is what `kubectx` does not solve.** It makes switching easy; it does not make
your current context visible. The wrong-cluster incident happens when someone has forgotten which
context they are on, and a tool that switches quickly does not help with that.

The three layers, in increasing order of effectiveness:

1. **Show the context in the shell prompt.** `kube-ps1`, or the equivalent in starship, powerlevel10k
   or oh-my-zsh. The single highest-value change on this page: it converts an invisible piece of state
   into something you cannot avoid seeing.
2. **`kubectx` / `kubens`** to make switching cheap and explicit.
3. **`direnv`** setting `KUBECONFIG` per project directory, from
   [`local/linux/shell/`](../../../local/linux/shell/README.md). This is the strongest because it
   removes the human step: the context follows the directory rather than the shell's history.

**Two practical notes:**

- **Context aliases are worth setting up.** `kubectx prod=arn:aws:eks:...` gives a short name, which
  matters because a readable prompt is one you actually read. A 60-character ARN in a prompt is
  scanned past.
- **`fzf` changes the experience.** With it installed, bare `kubectx` opens an interactive fuzzy
  picker instead of listing contexts. Worth having.

Maintained by Ahmet Alp Balkan; available through [krew](../krew/README.md) as `ctx` and `ns`, or as
standalone scripts.

---

[← Plugins](../README.md)
