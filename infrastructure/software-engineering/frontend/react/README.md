[← Frontend](../README.md)

# React

<https://github.com/facebook/react>

---

## The problem it solves

Keeping a complicated UI consistent with the state behind it. Before component frameworks, that
meant hand-written code that found elements and mutated them, and every new piece of state
multiplied the number of transitions someone had to get right.

React's answer is to make the UI a **function of state**: describe what the interface should look
like for a given state, and let the library work out the minimum set of DOM changes needed to get
there. Transitions stop being written at all.

The second thing it solves is reuse. A component bundles markup, behaviour and — in practice —
styling into one unit that can be composed, which is why design systems are built on it.

Worth being precise about what it is, because it decides the rest of the work: **React is a
library, not a framework.** It renders components. Routing, data fetching, forms, build tooling and
state management are all separate choices. The ecosystem is enormous and every part of it is
optional, which is simultaneously its main strength and the reason two React projects can look
nothing alike.

## When to use it

- **Rich, stateful client applications**: dashboards, editors, anything where the interface has
  meaningful internal state.
- When the hiring pool matters. It is the most widely known option, and that is a legitimate
  engineering argument rather than a fashionable one.
- When a component library is wanted off the shelf. The largest selection of mature ones is here.
- Built statically with Vite and served as files. For an internal tool or a dashboard behind a
  login, this is almost always the right shape — see [`../`](../README.md) on why a static build is
  not a workload.

## When not to use it

- For **mostly-static pages with a little interaction**. A template rendered by the backend plus a
  small library does the job without a build pipeline, a bundle or a dependency tree.
- When server-rendering is required and nobody wants to operate a Node process. SSR turns the
  frontend into a real cluster workload with probes, limits and an on-call story.
- For a team already productive in Vue, Svelte or Angular. The differences are not large enough to
  justify retraining.
- When bundle size is the binding constraint. Svelte and similar compile-time approaches ship less
  JavaScript for the same interface.
- To hold anything secret. Everything in the bundle is public — an API key in a React build is an
  API key that has been published.

## Notes

The original note for this folder records exactly one thing:

- <https://github.com/facebook/react>

No example application, no Dockerfile, no manifest, no recorded opinion. This is the thinnest
entry in [`software-engineering/`](../../README.md), and it is worth being explicit about that
rather than padding the page.

What that means for how to read this: everything above is the general case for React, not a
finding from using it here. There is nothing recorded about how it was, or would be, built and
served in this cluster.

The platform-side facts that would matter if it ever is:

| Concern | Detail |
|---|---|
| Build output | Vite produces a directory of static files — HTML, hashed JS and CSS |
| Serving it | an object store plus a CDN, or an nginx container and an Ingress if it must stay in-cluster |
| API endpoint | injected at runtime from a served config file, not baked in per environment, or the artifact differs between staging and production |
| Cache headers | hashed assets cached forever, `index.html` never — the reverse serves users a version whose files no longer exist |
| SSR | a different decision entirely: a Node `Deployment`, with everything that implies |

The backend half of any application built with this is `api/`, which is where this repository's
actual depth on the application layer sits.

---

[← Frontend](../README.md)
