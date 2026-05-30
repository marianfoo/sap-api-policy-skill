# MCP Server Setup — SAP API Policy Evidence Skill

The `sap-api-policy-evidence` skill gathers evidence from five SAP MCP servers. You don't need all
five — the skill degrades gracefully and says which sources were unavailable — but more servers =
higher-confidence assessments. **SAP Docs is the minimum useful baseline; SAP API Hub + SAP Notes
are what let assessments reach `high` confidence.**

This guide keeps setup short and links to each project's full docs. Verified against the published
packages on 2026-05-28.

## At a glance

| Server | Package / install | Auth | Role in the skill |
| --- | --- | --- | --- |
| **SAP Docs** | **hosted URL** (`mcp-sap-docs.marianzeis.de`) — or self-host (`mcp-sap-docs`, clone + build) | none | SAP Help, Architecture Center, released-object status, Discovery Center |
| **SAP API Hub** | `sap-api-hub-mcp` — **`npx -y`** | api.sap.com login (Playwright) | prove Published-API status / version / auth / specs |
| **SAP Roadmap** | `sap-roadmap-mcp` — **`npx -y`** | roadmaps.sap.com login (Playwright) | future replacement APIs / endorsed pathways (planning only) |
| **SAP Notes** | `sap-note-search-mcp` — **`node`** (in the `sap-mcp-servers` monorepo) | S-user / me.sap.com (Playwright) | explicit "not permitted" / deprecated / successor notes |
| **ARC-1** | `arc-1` — **`npx arc-1@latest`** | live SAP system via ADT | connected-system release state, custom-API dependencies, ATC |

> **The three authenticated servers share one repo.** SAP API Hub, SAP Roadmap, and SAP Notes — plus
> the shared `@marianfoo/sap-mcp-auth` login module — live in the
> **[`sap-mcp-servers`](https://github.com/marianfoo/sap-mcp-servers) monorepo** (npm workspaces).
> They're still published as separate npm packages, so the `npx -y` forms below keep working; or clone
> the monorepo once and run `npm install && npm run build` to get all three built locally.

## Prerequisites

- **Node.js 20+** and npm (`npx` ships with npm).
- **One SAP login for all three authenticated servers.** SAP API Hub, SAP Roadmap, and SAP Notes all
  sign in with the **same** SAP Universal ID / S-user — put the **identical** `SAP_USERNAME` (your SAP
  email / S-user) and `SAP_PASSWORD` in each of the three configs — or share a single SSO login across all three (see
  *Authenticate once for all three* under Auth, sessions & MFA). SAP Docs needs no login; ARC-1 uses
  separate SAP *system* credentials (`SAP_USER` / `SAP_PASSWORD` for your ABAP system, not the sap.com
  login).
- The three browser-auth servers (API Hub, Roadmap, Notes) use **Playwright Chromium**. On first run
  install it once: `npx playwright install chromium`.
- **Never commit credentials or token/cookie caches.** This repo's `.gitignore` already excludes
  `.env*`, `*token-cache*`, `*.tokens`, `*cookies*` — keep it that way (see *Security* below).

---

## 1. SAP Docs — hosted URL (simplest) or self-host

No SAP login needed. The **simplest** option is the public hosted endpoint — no clone, no build, no
Node:

| Variant | Endpoint |
| --- | --- |
| SAP Docs (use this) | `http://mcp-sap-docs.marianzeis.de/mcp` |
| ABAP-only | `https://mcp-abap.marianzeis.de/mcp` |

`.cursor/mcp.json` (remote — Cursor and other modern clients):
```json
"sap-docs": { "url": "http://mcp-sap-docs.marianzeis.de/mcp" }
```
For stdio-only clients, proxy it: `{ "command": "npx", "args": ["-y", "mcp-remote", "http://mcp-sap-docs.marianzeis.de/mcp"] }`.

**Self-host** instead (offline / air-gapped / data-residency). One codebase ships two variants via
`MCP_VARIANT`; use **`sap-docs`** (broad SAP/BTP/Architecture-Center docs), not the `abap`-only one:
```bash
git clone https://github.com/marianfoo/mcp-sap-docs && cd mcp-sap-docs
MCP_VARIANT=sap-docs npm run setup && MCP_VARIANT=sap-docs npm run build
```
```json
"sap-docs": {
  "command": "node",
  "args": ["/ABS/PATH/mcp-sap-docs/dist/src/server.js"],
  "env": { "MCP_VARIANT": "sap-docs" }
}
```

Full docs (incl. remote/self-host details — see the repo's `REMOTE_SETUP.md`): https://github.com/marianfoo/mcp-sap-docs

## 2. SAP API Hub — `sap-api-hub-mcp` (npx)

Published on npm — no clone needed. Logs in to api.sap.com to read the Business Accelerator Hub
catalog (read-only; caches a browser session locally). Uses the **same** `SAP_USERNAME` /
`SAP_PASSWORD` as the Roadmap and Notes servers.

```json
"sap-api-hub": {
  "command": "npx",
  "args": ["-y", "sap-api-hub-mcp"],
  "env": {
    "MCP_TRANSPORT": "stdio",
    "SAP_USERNAME": "your.email@company.com",
    "SAP_PASSWORD": "your_sap_password"
  }
}
```

First run / MFA: add `"HEADFUL": "true"` temporarily to complete the browser login once, then remove
it. The session is cached so later runs are headless.

Full docs: https://github.com/marianfoo/sap-mcp-servers/tree/main/packages/api-hub

## 3. SAP Roadmap — `sap-roadmap-mcp` (npx)

Published on npm. Logs in to roadmaps.sap.com with the **same** `SAP_USERNAME` / `SAP_PASSWORD` as
API Hub and Notes. **Roadmap is future-planning evidence only** — the skill never treats it as
current permission.

```json
"sap-roadmap": {
  "command": "npx",
  "args": ["-y", "sap-roadmap-mcp"],
  "env": {
    "MCP_TRANSPORT": "stdio",
    "SAP_USERNAME": "your.email@company.com",
    "SAP_PASSWORD": "your_sap_password",
    "ROADMAP_DEFAULT_RANGE": "CURRENT-LAST"
  }
}
```

MFA bootstrap: `npm run auth:login` in the repo, or add `"HEADFUL": "true"` once.

Full docs: https://github.com/marianfoo/sap-mcp-servers/tree/main/packages/roadmap

## 4. SAP Notes — `sap-note-search-mcp` (node, from the monorepo)

Published on npm as `sap-note-search-mcp`, but it exposes **no CLI `bin`**, so run it with `node`
after building (not `npx <name>`). It lives in the `sap-mcp-servers` monorepo under `packages/notes`. Authenticates to SAP Support Portal / me.sap.com with the **same**
`SAP_USERNAME` / `SAP_PASSWORD` as API Hub and Roadmap (or an SAP Passport certificate), and uses
Playwright to fetch note content.

```bash
git clone https://github.com/marianfoo/sap-mcp-servers && cd sap-mcp-servers
npm install && npm run build      # builds all three servers; Notes lands in packages/notes/dist
```

```json
"sap-notes": {
  "command": "node",
  "args": ["/ABS/PATH/sap-mcp-servers/packages/notes/dist/mcp-server.js"],
  "env": {
    "AUTH_METHOD": "auto",
    "SAP_USERNAME": "your.email@company.com",
    "SAP_PASSWORD": "your_sap_password"
  }
}
```

First run / MFA: add `"HEADFUL": "true"` once to complete login. Requires an S-user with SAP Support
Portal access. Note: in headless CI the full-text `fetch` can hit a sign-in wall — search metadata
still works; the skill handles that gap and caps confidence accordingly.

Full docs: https://github.com/marianfoo/sap-mcp-servers/tree/main/packages/notes

## 5. ARC-1 — `arc-1` (npx) — live SAP system, read-only by default

Published on npm (and as a Docker image). Connects to a **live** SAP system via the ADT REST API.
**ARC-1 is safe by default** — read-only, no writes, no table preview, no free SQL, no transport/Git
writes. So for policy work the minimal config is just the connection; you do **not** set any
`SAP_ALLOW_*` flags (they default to off), which keeps it inside the FAQ "endorsed development
tooling" envelope.

Minimal `.cursor/mcp.json`:
```json
"arc-1": {
  "command": "npx",
  "args": ["-y", "arc-1@latest"],
  "env": {
    "SAP_URL": "https://your-sap-host:44300",
    "SAP_USER": "YOUR_USER",
    "SAP_PASSWORD": "your_password"
  }
}
```

`SAP_CLIENT` / `SAP_LANGUAGE` are optional (sensible defaults). Only connect ARC-1 when accessing
that system is appropriate, and **leave `SAP_ALLOW_DATA_PREVIEW` and `SAP_ALLOW_FREE_SQL` off** —
those two sit outside the FAQ "endorsed development tooling" scope (business-data reads / backend SQL).

ARC-1 has the most complete external docs — start there rather than duplicating config here:
- Full documentation: https://marianfoo.github.io/arc-1/
- Quickstart (5-min npx + client setup): https://marianfoo.github.io/arc-1/quickstart/
- Tool reference: https://marianfoo.github.io/arc-1/tools/
- Repo: https://github.com/marianfoo/arc-1

## Auth, sessions & MFA (the three browser servers)

API Hub, Roadmap, and Notes all sign in with the **same SAP username/password** (your SAP Universal
ID / S-user) via a real browser (Playwright), and each **caches its own session locally** so
subsequent runs are headless:

1. First run: set `"HEADFUL": "true"` in that server's `env`, start it, complete login/MFA in the
   window that opens.
2. Remove `HEADFUL` (or set `false`). The cached session is reused until it expires.
3. If calls start failing with sign-in errors, the session expired — repeat step 1.

### Authenticate once for all three (shared SSO storage state)

By default each server logs in on its own. To log in **once** and have all three reuse the same SAP
SSO session, add these two keys to the `env` of **all three** servers (alongside the shared
`SAP_USERNAME` / `SAP_PASSWORD`), all pointing at the **same** file:

```json
"SAP_SSO_STORAGE_STATE": "/Users/you/.sap-mcp/sso-storage-state.json",
"SAP_LOGIN_URL": "https://me.sap.com/home"
```

Bootstrap the shared session **once** with a single HEADFUL login: the first server you start with
`"HEADFUL": "true"` and `SAP_SSO_STORAGE_STATE` set opens a browser — complete login + MFA, and it
writes that shared SSO file. The other two then reuse the `accounts.sap.com` SSO cookies from it and
silently mint their own app-specific cookies — no second or third login. (If you cloned the Roadmap
repo, `npm run auth:login` runs exactly this headful bootstrap.)

- Use an **absolute path** for the storage-state file (`npx` working directories vary).
- Each server still keeps its own small app-specific token cache — that's automatic, not another login.
- The shared SSO session expires (`MAX_COOKIE_AGE_H` / `MAX_JWT_AGE_H`, default ~12 h); when calls
  start returning sign-in errors, repeat the one-time HEADFUL bootstrap.
- Want zero interactive login (and Docker-friendly)? Use a SAP Passport certificate instead — the
  same `.pfx` in all three (`AUTH_METHOD=certificate`, `PFX_PATH`, `PFX_PASSPHRASE`); see each repo's README.

## Security

- Put credentials in the MCP client config `env` (or each repo's own `.env`), **never in committed
  files**. This repo's `.gitignore` blocks `.env*` and credential/cookie caches.
- The browser servers write a session/token cache (e.g. `api-hub-token-cache.json`). These are
  secrets — keep them ignored and never share them. Rotate your SAP session if one leaks.
- ARC-1 touches a live system: keep `SAP_ALLOW_WRITES` / `SAP_ALLOW_DATA_PREVIEW` /
  `SAP_ALLOW_FREE_SQL` set to `false` for policy-assessment work.

## Verify

After editing `.cursor/mcp.json`, restart Cursor (or your MCP client). The skill does a runtime
self-check and reports which servers it actually reached. A quick manual smoke test:

- SAP Docs: search for `MCP Gateway Integration Suite` → should return Architecture Center hits.
- SAP Notes: search `3255746` → should return *"Unpermitted usage of ODP Data Replication APIs"*.
- API Hub: search `API_SALES_ORDER_SRV` → should return the Sales Order (A2X) artifact.

The repo ships a portable **[`.cursor/mcp.json.example`](.cursor/mcp.json.example)** wiring all five
servers with the hosted SAP Docs URL and the `npx -y` forms. Copy it to `.cursor/mcp.json`, then fill
in your `SAP_USERNAME` / `SAP_PASSWORD`, set the `SAP_SSO_STORAGE_STATE` **absolute** path (same value
in all three authenticated servers = one login), and point the `sap-notes` `node` arg at your local
`sap-mcp-servers` clone. Your real `.cursor/mcp.json` is gitignored, so machine-specific paths and
credentials never get committed.

---

## Using the skill

The skill lives in `skills/sap-api-policy-evidence/` (`SKILL.md` + `references/` + `agents/openai.yaml`).
The lowest-friction, cross-agent install is the [`skills`](https://github.com/vercel-labs/skills) CLI
(Claude Code, Cursor, Codex, and others):

```bash
# adjust owner/repo to where it's published; add -g for a global (all-projects) install
npx skills add marianfoo/sap-api-policy-skill --skill sap-api-policy-evidence
```

Then ask in plain language — the skill runs its own self-check and uses whatever MCP servers are
reachable (it says which were unavailable and adjusts confidence).

### Manual install (no CLI)

- **Claude Code** — put the skill folder where Claude Code discovers skills:
  - Project-scoped: `<project>/.claude/skills/sap-api-policy-evidence/` (this repo already symlinks it
    to `skills/sap-api-policy-evidence/`).
  - Personal (all projects):
    ```bash
    ln -s "$PWD/skills/sap-api-policy-evidence" ~/.claude/skills/sap-api-policy-evidence
    ```
  Start a fresh session so skills load. Auto-triggers on matching questions; otherwise say
  `Use the sap-api-policy-evidence skill to assess: …`.
- **Cursor** — attach `skills/sap-api-policy-evidence/SKILL.md` to the chat (or tell the agent
  "follow SKILL.md"); it pulls in `references/` as needed.
- **Codex** — picks it up via `skills/sap-api-policy-evidence/agents/openai.yaml`.

### Example prompts
- *Decisive — exercises SAP Notes:* "Is it allowed under SAP's API policy to extract data from our
  BW/4HANA into Snowflake nightly via ODP-RFC through a third-party ETL tool?"
- *Should be aligned:* "We sync ~500 Shopify orders/day into S/4HANA Cloud via the standard Sales
  Order OData API using Boomi. Are we OK under the 2026 API policy?"
- *Scan mode — hand it a list:* "Which of these are OK to keep using under the API policy:
  API_SALES_ORDER_SRV, RFC_READ_TABLE, SD_SALESDOCUMENT_CREATE, ODP-RFC, I_SalesDocument?"

Every result is an evidence-based **technical** assessment with a fixed verdict label, a confidence
level, cited sources, and a non-legal disclaimer — it routes legal/commercial/roadmap questions to
SAP rather than answering them. More servers connected (especially API Hub + an authenticated SAP
Notes session) = the only way assessments reach `high` confidence.
