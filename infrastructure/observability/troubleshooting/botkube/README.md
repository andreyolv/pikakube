[← Troubleshooting](../README.md)

# Botkube

<https://github.com/kubeshop/botkube>

---

## The problem it solves

During an incident the first question in the channel is usually "can someone check the pods?"
— and the answer requires a terminal, a kubeconfig and the right context.

Botkube brings the cluster into chat: it posts notifications about cluster changes, and lets
approved commands be run from Slack, Teams, Discord or Mattermost with the output returned in
the thread.

The value is not saving keystrokes. It is that **triage happens where the conversation is**,
and everyone sees the same output instead of one person relaying it.

## When to use it

- the team coordinates incidents in chat
- read-only visibility for people who should not have cluster credentials
- keeping investigation output in the incident thread, where the post-mortem can use it

## When not to use it

- you want the **diagnosis**, not access to run commands — [k8sgpt](../k8sgpt/) or [HolmesGPT](../holmesgpt/)
- RBAC has not been thought through. See below

## The security consideration

Botkube runs with a ServiceAccount, and **whatever it can do, the channel can do**. A
permissive binding turns a chat room into cluster access, including for anyone who is later
added to it.

Start read-only. Grant mutating commands deliberately, scope them, and audit who is in the
channel — the membership list is now part of your access control.

---

[← Troubleshooting](../README.md)
