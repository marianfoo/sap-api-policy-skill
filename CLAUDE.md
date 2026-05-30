# CLAUDE.md — sap-api-policy-skill

Guidance for Claude Code (and any agent) working **in this repo**. End users don't need this — they
just install the skill (see [README.md](README.md)).

## What this repo is

This repo packages the **`sap-api-policy-evidence`** agent skill, distributed via the
[`npx skills`](https://github.com/vercel-labs/skills) CLI. The skill assesses whether an SAP API
usage scenario aligns with the **SAP API Policy v.4.2026a** (+ FAQ v1.2) and returns an
evidence-based, sourced, confidence-rated **technical** assessment — gathering live evidence from SAP
MCP servers.

It is the skill + its test harness + setup docs. It is **not** the MCP servers themselves — those
live in the separate [`sap-mcp-servers`](https://github.com/marianfoo/sap-mcp-servers) monorepo (see
[MCP_SETUP.md](MCP_SETUP.md)).

## The one invariant — never break this

The skill's output is **never legal advice, contractual advice, or a final/definitive SAP compliance
decision** — only an evidence-based technical assessment with a confidence level and SAP-escalation
questions. SAP itself declines to publish a binary "compliant / not compliant" decision matrix (FAQ
Q49), so a confident yes/no would misrepresent what is knowable. Every report carries the non-legal
disclaimer at **top and bottom**, and legal / commercial / roadmap questions are **routed to SAP**,
not answered. Any change that lets the skill emit an unconditional verdict, drop the disclaimer, or
opine on legal/commercial matters is wrong.

## Layout

```
skills/sap-api-policy-evidence/
  SKILL.md                     entry point — loaded into context on trigger. KEEP IT LEAN.
  references/                  progressive-disclosure detail, read on demand per workflow step:
    policy-baseline.md         5 policy clauses, definitions, red flags, scenario rules, endorsed
                               pathways, SAP-Note examples, FAQ (Q##) anchors
    evidence-model.md          intake triage, source hierarchy, confidence rubric, ledger fields
    tool-playbooks.md          per-MCP-server tool calls, runtime self-check, auth-failure handling
    report-template.md         required report structure + fixed-label rules
    inventory-scan-mode.md     batch "which of these APIs are allowed?" workflow
  agents/openai.yaml           Codex integration
evals/evals.json               22 scenario evals (behavioral test suite)
tests/skill_static_checks.py   the machine-checkable contract (run this before committing)
MCP_SETUP.md                   how users wire up the SAP MCP servers + install the skill
README.md                      public front page
```

## Editing rules

- **Keep `SKILL.md` lean.** It's always in context once triggered; detail belongs in `references/`,
  pulled in at the relevant workflow step. Don't inline reference content into SKILL.md.
- **Output invariants (the static check enforces these):**
  - `**Assessment:**` is exactly one of — `Likely aligned` · `Likely not aligned` ·
    `Needs SAP confirmation` · `Not assessable from provided facts` — verbatim and **alone**, with no
    trailing words, parentheticals, or qualifiers.
  - `**Confidence:**` is exactly one of `high` · `medium` · `low` — alone, no hybrids (`medium-to-high`)
    or ranges.
  - All nuance goes in the analysis / `Why`, never in the label. (Two real drift classes — label
    qualifiers and hybrid confidence — were caught during hardening; the static check guards both.)
- **Ground policy claims** in `policy-baseline.md` and the actual policy/FAQ; cite `Q##` when a FAQ
  answer supports a finding. Don't invent policy text.
- The skill must **never request or accept** secrets (passwords, tokens, S-user creds, private keys,
  raw business data); ARC-1 stays read-only. Ask for aggregate counts / redacted summaries instead.

## Validate every change

Run the contract check — it must print `skill-static-checks-ok`:

```bash
python3 tests/skill_static_checks.py
```

It verifies: the skill structure (SKILL.md names + links all **five** references; `agents/openai.yaml`
exists), the fixed Assessment/Confidence label rules (no hybrids, no qualifiers), the live AI Golden
Path URL in `tool-playbooks.md` + `policy-baseline.md`, and that the 7 anchor evals are present with
their label expectations. **If you rename/move a reference or change a label, update
`tests/skill_static_checks.py` to match.**

The behavioral evals in `evals/evals.json` are run through the skill-creator eval loop in a local,
gitignored workspace — they are not wired into CI in this repo.

## MCP servers

The skill calls SAP MCP servers (SAP Docs, API Hub, Roadmap, Notes, ARC-1). Setup, auth/MFA, and the
shared-SSO single-login flow are in **[MCP_SETUP.md](MCP_SETUP.md)**; the three authenticated servers
live in the `sap-mcp-servers` monorepo. The skill does a runtime self-check, degrades gracefully when
a server is missing, and self-caps confidence (only API Hub + an authenticated SAP Notes session let
it reach `high`).

## Publishing

Distributed via `npx skills add marianfoo/sap-api-policy-skill --skill sap-api-policy-evidence` (see
README + MCP_SETUP.md → "Using the skill"). Canonical layout is `skills/<name>/SKILL.md` where
`<name>` matches the parent directory. Never commit `.env`, token/cookie caches, certificates, or
storage-state files — `.gitignore` already blocks them; keep it that way.
