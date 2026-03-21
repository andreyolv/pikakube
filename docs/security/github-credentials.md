# 🛡️ GitHub Credentials Policy: Authentication Standards & Governance

## 1. Overview and General Directive
This policy establishes the security standards for authenticating external tools (CI/CD, scripts, automations, and data platforms) with our organization's assets on GitHub.

**Core Directive:** No automation or systemic process shall operate under the identity of a personal user account. Programmatic identity must be strictly separated from biological (individual) identity.

---

## 2. The Gold Standard: GitHub App 🥇
The use of **GitHub Apps** is the highest priority and the mandatory standard for all new integrations.

### Why is the GitHub App the standard?

* **Principle of Least Privilege (Granularity):** Unlike a user token that accesses everything the person can see, an App is configured with surgical permissions (e.g., read-only access to *metadata* or write access to *pull requests* for specific repositories only).
* **Short-Lived Tokens:** The App utilizes installation tokens that automatically expire within **1 hour**. This drastically reduces the window of opportunity in the event of a credential leak.
* **Lifecycle Independence:** The App belongs to the organization, not an individual. If a developer or administrator leaves the company, automation **is not interrupted**.
* **Scalability and Rate Limits:** GitHub Apps have their own API quotas, independent of developer account limits, preventing bottlenecks in large-scale automations.
* **Superior Auditability:** All actions performed by the App are recorded in the organization's audit logs with the application's unique identity, making it easier to track changes.

---

## 3. Rejected Alternatives (Anti-patterns) 🚫

To prevent security gaps and technical debt, the following methods are discouraged or prohibited for production use:

### ❌ Personal Access Tokens (PATs)
* **Reason:** They are tied to an individual account. If the token owner is offboarded or changes teams, the pipeline breaks.
* **Risk:** They often have overprivileged permissions and do not offer efficient granular control per repository.

### ❌ Machine Users (Bot Accounts)
* **Reason:** "Ghost accounts" unnecessarily consume paid GitHub Enterprise licenses.
* **Risk:** They require complex management of passwords, MFA, and manual token rotation, increasing the attack surface for unauthorized manual logins.

### ❌ SSH Keys (Deploy Keys)
* **Reason:** While secure for Git operations, they are limited. They do not allow interaction with the GitHub API (e.g., commenting on PRs, approving deploys, checking security status).
* **Risk:** Managing private keys in plain text is generally less secure than the dynamic handshake of a GitHub App.

---

## 4. Decision Matrix

| Feature | GitHub App (STANDARD) | PAT (LEGACY) | Machine User (PROHIBITED) |
| :--- | :--- | :--- | :--- |
| **Identity Link** | Institutional (Org) | Individual (Person) | Separate Account |
| **Token Duration** | 60 minutes (Dynamic) | 30-90 days (Static) | Permanent |
| **Granularity** | High (Per API/Repo) | Low (By Scope) | Low |
| **License Cost** | Free | Free | Paid (1 Seat) |
| **Security Level** | Maximum | Medium/Low | Low |

---

## 5. Governance and Auditing
* **Monitoring:** The Security team performs periodic scans. PATs identified in production environments will be flagged for immediate migration.
* **Storage:** The GitHub App `Private Key` must never reside in the source code. It is mandatory to use an authorized **Secret Manager** (e.g., AWS Secrets Manager, HashiCorp Vault, or GitHub Actions Secrets).

---

> **Note:** This policy aims to ensure business continuity and the protection of our intellectual property. For technical questions regarding GitHub App implementation, consult the official documentation or the Architecture/DataOps team.
