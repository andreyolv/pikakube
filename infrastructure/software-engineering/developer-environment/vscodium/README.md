[← Developer environment](../README.md)

# VSCodium

<https://github.com/VSCodium/vscodium>

---

## The problem it solves

VS Code is confusing in a specific way: **the source is MIT-licensed, the download is not.**
Microsoft builds that source with telemetry enabled and ships it under a proprietary licence with
its own branding.

VSCodium is the same source, built without the telemetry and without the branding, released under
the MIT licence. Same editor, same settings, same keybindings, same UI — a build with the
proprietary parts removed.

| Concern | VS Code | VSCodium |
|---|---|---|
| Licence of the binary | proprietary Microsoft licence | MIT |
| Telemetry | on by default | not compiled in |
| Default extension marketplace | Microsoft's | Open VSX |
| Branding and logos | Microsoft's | removed |

That third row is where the practical difference lives, and it is not a preference.

## When to use it

| Situation | Why |
|---|---|
| **Telemetry is disallowed by policy** | it is absent from the build, not switched off in a setting someone can flip back |
| **The distributed binary must be open source** | MIT, including the build |
| Redistributing an editor inside an image | the proprietary licence restricts what you may ship; MIT does not |
| An offline or air-gapped environment | no telemetry endpoints to block, and Open VSX can be mirrored |
| Building a workspace image for a team | the licence question is answered before anyone asks it |

## When not to use it

| Situation | Use instead |
|---|---|
| **Microsoft's proprietary extensions are needed** | VS Code — see below; this is the deciding factor in practice |
| Remote Development and Dev Containers extension packs | VS Code — Microsoft-branded builds only |
| A team that will not accept any friction | VS Code — the marketplace difference is a real cost |
| Settings Sync through a Microsoft account | VS Code, or a different sync mechanism |

## Notes

The original note is the repository link. What matters before adopting it:

**The extension marketplace is the whole story.** Microsoft's marketplace terms permit use only
from Microsoft's own products, so VSCodium ships with [Open VSX](https://open-vsx.org/) instead.
Most extensions are on both. The ones that are not are Microsoft's own, and the list is
inconvenient:

| Extension | Consequence |
|---|---|
| **Remote Development / Dev Containers** | the direct integration with [`devcontainer/`](../devcontainer/README.md) is unavailable |
| Pylance | the Python language server falls back to the open alternative |
| C/C++ (`ms-vscode.cpptools`) | licensed for Microsoft-branded builds only |
| Live Share | Microsoft account and service |

The first row is the one that lands hardest in this folder. If the plan is local devcontainers
driven from the editor, VSCodium is the harder path — and [DevPod](../devpod/README.md) is a way
around it, since it consumes the same `devcontainer.json` from a CLI rather than from a
Microsoft extension.

**It is a build, not a fork.** VSCodium tracks upstream releases and applies build patches; it is
not a divergent codebase with its own features. Upstream versions arrive shortly after Microsoft's.

**Migration is close to free.** Settings, keybindings and profiles are the same format and the
config directory differs only in name, so moving in either direction is a copy. That makes trying
it cheap — the only thing to check is whether the extensions in use exist on Open VSX.

Nothing here is deployed; this is a reference. Where it becomes concrete for this platform is the
day a workspace image is built for other people: at that point the licence of the editor being
redistributed is a question that has to have an answer.

---

[← Developer environment](../README.md)
