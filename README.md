# SAP API Policy Evidence Skill

An [agent skill](https://github.com/vercel-labs/skills) that assesses whether a given **SAP API
usage scenario aligns with the SAP API Policy** (v.4.2026a + FAQ) and returns an **evidence-based,
sourced technical assessment** with a confidence level — by gathering live evidence from official SAP
sources (SAP Help, Business Accelerator Hub, SAP Notes, Architecture Center, released-object data)
via MCP servers.

> **Not legal advice, not a final SAP compliance decision.** Only SAP, your contract, or SAP
> support/account/legal can give a binding answer. This skill gets as close as the evidence allows,
> labels its confidence, and routes legal/commercial/roadmap questions to SAP rather than answering
> them.

## Install

Cross-agent via the [`skills`](https://github.com/vercel-labs/skills) CLI (works with Claude Code,
Cursor, Codex, and others):

```bash
# install just this skill (use your own owner/repo if you fork it)
npx skills add marianfoo/sap-api-policy-skill --skill sap-api-policy-evidence

# or install everything in the repo
npx skills add marianfoo/sap-api-policy-skill

# globally, across all projects
npx skills add -g marianfoo/sap-api-policy-skill --skill sap-api-policy-evidence
```

Manual install (no CLI): copy `skills/sap-api-policy-evidence/` into your agent's skills directory
(e.g. `~/.claude/skills/` for Claude Code) — see **[MCP_SETUP.md](MCP_SETUP.md) → "Using the skill"**.

## Prerequisite: the SAP MCP servers

The skill gathers evidence through SAP MCP servers — set them up once (most are `npx`-installable, SAP
Docs has a hosted URL):

| Server | Install | Role |
| --- | --- | --- |
| SAP Docs | hosted URL or `mcp-sap-docs` | SAP Help, Architecture Center, released-object status |
| SAP API Hub | `npx -y sap-api-hub-mcp` | prove Published-API status / version / specs |
| SAP Notes | `sap-note-search-mcp` (node) | "not permitted" / deprecated / successor notes |
| SAP Roadmap | `npx -y sap-roadmap-mcp` | future replacement APIs (planning only) |
| ARC-1 | `npx -y arc-1@latest` | live-system release state / custom-API checks |

The three authenticated servers (API Hub, Roadmap, Notes) and their shared SAP login module live in
one repo — [`sap-mcp-servers`](https://github.com/marianfoo/sap-mcp-servers) (npm workspaces) — but
each is still published to npm individually, so the `npx -y` forms above work as-is.

Full setup (auth, MFA, portable config, per-client usage): **[MCP_SETUP.md](MCP_SETUP.md)**. The skill
degrades gracefully if some are missing and says which were unavailable; **SAP API Hub + an
authenticated SAP Notes session are what let assessments reach `high` confidence.**

## What it covers

Published-API vs internal/private status · "Documented Use" · third-party tools / iPaaS / RPA ·
agentic & generative-AI / MCP access · bulk extraction & replication · custom Z/Y OData & RFC/BAPI
wrappers & Clean Core · ADT developer-tooling boundaries (FAQ Q33) · ODP-RFC and other "not
permitted" interfaces · partner Integration Certification · RISE remediation · an **inventory/scan
mode** ("which of these APIs are allowed?").

## Example prompts

- *Decisive:* "Is it allowed under SAP's API policy to extract data from our BW/4HANA into Snowflake
  nightly via ODP-RFC through a third-party ETL tool?"
- *Should be aligned:* "We sync ~500 Shopify orders/day into S/4HANA Cloud via the standard Sales
  Order OData API using Boomi — OK under the 2026 API policy?"
- *Scan a list:* "Which of these are OK to keep using: API_SALES_ORDER_SRV, RFC_READ_TABLE,
  SD_SALESDOCUMENT_CREATE, ODP-RFC, I_SalesDocument?"

## Repo layout

```
skills/sap-api-policy-evidence/   the skill — SKILL.md + references/ + agents/openai.yaml
evals/evals.json                  22 scenario evals (the test suite)
tests/skill_static_checks.py      contract checks (fixed labels, required refs, URLs)
MCP_SETUP.md                      MCP server setup + how to consume the skill
CLAUDE.md                         contributor/maintainer guide (how to edit + validate the skill)
.cursor/mcp.json.example          portable MCP client config — copy to .cursor/mcp.json and fill in
```

## Validation

The skill was hardened over 6 eval iterations across 22 scenarios spanning every policy branch plus
adversarial over/under-flag, legal-wall, and scan-mode probes. It returns a fixed verdict label
(`Likely aligned` / `Likely not aligned` / `Needs SAP confirmation` / `Not assessable from provided
facts`), a single confidence level, cited sources, and the non-legal disclaimer.

## License

MIT — see [LICENSE](LICENSE).
