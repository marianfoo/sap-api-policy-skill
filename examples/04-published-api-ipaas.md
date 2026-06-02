> **Input prompt.** This report was produced by running the prompt below in Cursor against the [`sap-api-policy-evidence`](../skills/sap-api-policy-evidence/SKILL.md) skill, with the SAP MCP servers connected. The skill's output report follows.

```text
Follow the skill at skills/sap-api-policy-evidence/SKILL.md.

Assess this scenario: We sync about 500 sales orders per day from Salesforce into
S/4HANA Cloud (public edition) using Boomi as middleware, by calling the standard
Sales Order OData API (API_SALES_ORDER_SRV) with OAuth 2.0. Is this aligned with
the 2026 SAP API Policy?

Lean on the SAP API Hub for this one. Search the SAP Business Accelerator Hub for
the Sales Order API, fetch the artifact to confirm Published-API status, version,
direction (inbound A2X), and authentication, then pull its resources/operations and
the spec to check for documented rate limits, quotas, or deprecation. Use SAP Notes
and released-object data only to cross-check. Cite every API Hub artifact with its
URL, version, and retrieval date.

Write the full assessment report using the skill's report template, then save it as
a markdown file at examples/04-published-api-ipaas.md.
```

---

# SAP API Policy - Evidence Assessment

> **Not legal or final SAP advice.** This is an evidence-based *technical* assessment. Only SAP, the applicable contract, or SAP support/account/legal channels can give a binding answer for a specific customer landscape. SAP does not publish a binary compliant/not-compliant decision matrix (API Policy FAQ Q49); this report gets as close as the evidence allows and flags what to confirm with SAP.

**Assessment:** Likely aligned
**Confidence:** medium
**Date:** 2026-06-02
**Policy baseline:** SAP API Policy v.4.2026a and API Policy FAQ v1.2 (May 2026), plus the live sources listed below.

## Scenario facts

| Fact | Value | Status | Notes |
| --- | --- | --- | --- |
| SAP product | SAP S/4HANA Cloud Public Edition | Provided | API Hub evidence below verifies the public-edition artifact. |
| Release / tenant version | Not provided | Important, not blocker | API Hub package version retrieved as `2602.3`; the exact customer tenant release and communication arrangement still matter for productive setup and limits. |
| Source system | Salesforce | Provided | Salesforce is the external source of sales-order data. |
| Middleware | Boomi | Provided | A third-party iPaaS/middleware platform is not a policy red flag by itself; the SAP-facing API and usage pattern are decisive. |
| SAP interface | `API_SALES_ORDER_SRV` / Sales Order (A2X), OData V2 | Provided | API Hub search/fetch confirms the artifact. |
| Endpoint family | `/sap/opu/odata/sap/API_SALES_ORDER_SRV` | API Hub evidence | API Hub service URL is the S/4HANA Cloud sandbox endpoint; configuration also lists the tenant-host endpoint template. |
| Direction | External system/Boomi calls inbound into S/4HANA Cloud to create/read sales orders | Inferred from API Hub | API Hub metadata `Direction` returned `null`; the artifact title "Sales Order (A2X)", service endpoint, and create/read operation descriptions support inbound A2X use. |
| Operations | Create about 500 sales orders per day; likely read/lookup operations as needed | Provided / inferred | API Hub resources confirm `POST /A_SalesOrder`, `GET /A_SalesOrder`, `GET /A_SalesOrder('{SalesOrder}')`, and `$batch`. |
| Authentication | OAuth 2.0 | Provided and API Hub evidence | API Hub fetch returned `OAuth2Auth` labeled "OAuth 2.0" plus `BasicAuth`; search facet also listed `x509`. Use the tenant's documented communication arrangement rather than assuming sandbox security choices. |
| Volume | About 500 sales orders per day | Provided | This is a bounded operational integration volume, not large-scale extraction/replication on the facts supplied. Bursts, retry behavior, and payload complexity remain important. |
| AI / agentic flags | None stated | Provided by omission | This is deterministic middleware integration, not an autonomous/generative-AI agent scenario. |
| SAP written authorization / exception | None supplied | Not needed for first-pass result | Because the API is published and the use appears documented, a special authorization is not the basis for this assessment. |

## Runtime self-check

| Tool family | Runtime status | Evidence gathered | Gap handling |
| --- | --- | --- | --- |
| SAP API Hub MCP | Available and authenticated. `categories`, `search`, `fetch`, `resources`, `package`, and `spec` were callable on 2026-06-02. | Used API Hub as the primary source for `API_SALES_ORDER_SRV`: search result, artifact metadata, auth methods, resources/operations, package metadata, and JSON/YAML/EDMX spec endpoint status. | No material gap for Published API status. The MCP spec tool returned HTTP 200 and payload sizes, while the transcript did not expose the full million-byte spec text. Normalized artifact/resource metadata was therefore used for the detailed operation/control checks. |
| SAP Notes MCP | Available and authenticated. | Searched for `API_SALES_ORDER_SRV` deprecation, quota, rate-limit, and A2X sales-order notes; fetched SAP Note 3467023 as a representative cross-check note. | Notes returned correction/behavior evidence rather than a prohibition or deprecation signal. This is a cross-check only; API Hub is controlling for publication. |
| SAP Docs released-object tools | Available. | Looked up `I_SALESORDER` in public-cloud released-object data. | Supporting Clean Core signal only; released CDS status is not a substitute for API Hub publication of the OData service. |
| SAP Docs / Architecture Center | Not material for this scenario. | Not used beyond the local policy baseline and official policy/FAQ sources. | The user asked to lean on SAP Business Accelerator Hub; no architecture-center alternative was needed because the stated API path is positive. |
| SAP Roadmap MCP | Not material for this scenario. | Not used. | Roadmap evidence is future/planning only and is not needed for a current published API. |
| ARC-1 live SAP system MCP | Tool family may be available in the runtime, but was not used. | No live customer SAP system reads were performed. | The skill requires explicit confirmation before querying a live customer system, and this question can be answered from public SAP sources. |
| Raw unauthenticated spec fetch | Network available, but direct unauthenticated `curl` to the API Hub `$value` URL returned a small HTML shell, not the spec. | This contrasts with the API Hub MCP `spec` calls, which returned HTTP 200 for JSON, YAML, and EDMX. | Treated as a retrieval limitation of direct web access, not as a failure of the API Hub MCP evidence. |

## Interface inventory

| Capability | Interface (ID/type) | Endpoint/object | Provider | Publication evidence | Status | Controls | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Create sales orders in S/4HANA Cloud from Salesforce via Boomi | `API_SALES_ORDER_SRV` / Sales Order (A2X), OData V2 | `/sap/opu/odata/sap/API_SALES_ORDER_SRV`; `POST /A_SalesOrder` | SAP S/4HANA Cloud Public Edition | SAP Business Accelerator Hub artifact `API_SALES_ORDER_SRV`, version `1.0.0`, active, URL `https://api.sap.com/api/API_SALES_ORDER_SRV/overview`, retrieved 2026-06-02 | Published API for the documented sales-order integration operations | API Hub fetch returned OAuth 2.0 and Basic Auth; search facet listed x509. API Hub metadata returned `Deprecated: null`, `Successors: null`, and no documented quota/rate-limit field in the normalized output. Tenant communication arrangement, scopes, batching, retry, and throttling controls still apply. | None required for policy alignment. Evaluate newer/different Sales Order APIs only if the customer wants a functional modernization path. |
| Optional sales-order read/lookup support | `API_SALES_ORDER_SRV` / OData V2 read operations | `GET /A_SalesOrder`; `GET /A_SalesOrder('{SalesOrder}')`; navigation reads | SAP S/4HANA Cloud Public Edition | API Hub resources for version `1.0.0`, URL `https://api.sap.com/api/API_SALES_ORDER_SRV/overview`, retrieved 2026-06-02 | Published operations in the same API | Use filters, selects, expands, and pagination carefully; avoid broad unbounded reads and retry storms. | None required. |
| Supporting released-object signal | `I_SALESORDER` / DDLS | Released-object data for public cloud | SAP S/4HANA Cloud Public Edition | Released-object lookup returned state `released`, Clean Core level `A`, retrieved 2026-06-02 | Supporting positive signal only | Useful for extension/read model context, not the primary publication source for the OData service. | Not applicable. |

## Evidence

| Source | Type | Tool/query | Finding | Authority | Relevance | Retrieved |
| --- | --- | --- | --- | --- | --- | --- |
| [SAP API Policy v.4.2026a](https://help.sap.com/doc/sap-api-policy/latest/en-US/API_Policy_latest.pdf) | SAP Policy | Official SAP Help PDF, web search/open | Published APIs are those in SAP Business Accelerator Hub or product documentation; Specific API Controls include rate limits, quotas, deprecation, bulk preconditions, and security/technical requirements; General Controls still prohibit out-of-scope use, system-risk use, and bypassing controls. | official explicit | Policy baseline / Published API / Specific Controls / General Controls | 2026-06-02 |
| [API Policy FAQ v1.2, May 2026](https://www.sap.com/documents/2026/04/e2a0665e-4c7f-0010-bca6-c68f7e60039b.html) | SAP FAQ | Official SAP document page, web search/open | FAQ anchors in the local policy baseline say third-party middleware/iPaaS is assessed by the SAP-facing API surface and usage pattern, not by the tool brand; deterministic middleware use is distinct from autonomous AI-agent access; Q49 says SAP does not publish a binding decision matrix. | official explicit | Third-party middleware / non-finality / policy interpretation | 2026-06-02 |
| SAP Business Accelerator Hub categories | API Hub | `mcp__sap_api_hub.categories()` | API Hub catalog access was callable and returned live artifact categories including APIs, events, CDS views, BAdIs, and other content types. | official explicit | Runtime self-check | 2026-06-02 |
| [SAP Business Accelerator Hub - Sales Order (A2X)](https://api.sap.com/api/API_SALES_ORDER_SRV/overview) | API Hub artifact | `mcp__sap_api_hub.search(q="API_SALES_ORDER_SRV", categoryKey="API", artifactType="API", top=10)` | Search returned the public-edition artifact `API_SALES_ORDER_SRV`, title "Sales Order (A2X)", subtype OData, package `SAPS4HANACloud`, state `ACTIVE`, version `1.0.0`, service URL `https://sandbox.api.sap.com/s4hanacloud/sap/opu/odata/sap/API_SALES_ORDER_SRV`, short text "Create, read, update, and delete sales orders with this synchronous OData API." Search also returned a separate private-edition/on-premise sibling `OP_API_SALES_ORDER_SRV_0001`, version `1.1.0`, not used for this public-edition scenario. | official explicit | Published API search / artifact resolution / version / product scope | 2026-06-02 |
| [SAP Business Accelerator Hub - Sales Order (A2X)](https://api.sap.com/api/API_SALES_ORDER_SRV/overview) | API Hub artifact | `mcp__sap_api_hub.fetch(id="API_SALES_ORDER_SRV", kind="api", version="1.0.0")` | Fetch returned title "Sales Order (A2X)", status `ACTIVE`, type `OpenAPI`, version `1.0.0`, package `SAPS4HANACloud`, auth methods `OAuth2Auth` labeled "OAuth 2.0" and `BasicAuth`, endpoint template `https://{host}:{port}/sap/opu/odata/sap/API_SALES_ORDER_SRV`, `Deprecated: null`, `Successors: null`, `ModifiedAt: 2026-05-13T05:13:42.519Z`, and external business documentation URL for S/4HANA Cloud `2602.latest`. | official explicit | Published API / auth / endpoint / deprecation / successor / version | 2026-06-02 |
| [SAP Business Accelerator Hub - Sales Order resources](https://api.sap.com/api/API_SALES_ORDER_SRV/overview) | API Hub resources | `mcp__sap_api_hub.resources(id="API_SALES_ORDER_SRV", kind="api", version="1.0.0")` | Resources returned 101 paths and 158 operations. Relevant operations include `GET /A_SalesOrder` to read all sales order headers, `POST /A_SalesOrder` to create a sales order, `GET /A_SalesOrder('{SalesOrder}')`, `PATCH /A_SalesOrder('{SalesOrder}')`, `DELETE /A_SalesOrder('{SalesOrder}')`, related-entity create/read operations, and `POST /$batch`. | official explicit | Operation scope / inbound create-read capability | 2026-06-02 |
| SAP Business Accelerator Hub OpenAPI JSON spec | API Hub spec artifact | `mcp__sap_api_hub.spec(id="API_SALES_ORDER_SRV", kind="api", format="json", version="1.0.0")` | Spec endpoint returned HTTP `200`, content type `application/json`, URL `https://api.sap.com/odata/1.0/catalog.svc/APIContent.APIs('API_SALES_ORDER_SRV')/$value?type=json`, size `1003982` bytes. The tool did not expose the full content in the transcript. No rate-limit, quota, or deprecation control surfaced in the normalized API Hub fetch/resources output derived from the artifact. | official explicit for availability; tooling limitation for full-text inspection | Spec availability / controls check | 2026-06-02 |
| SAP Business Accelerator Hub YAML spec | API Hub spec artifact | `mcp__sap_api_hub.spec(id="API_SALES_ORDER_SRV", kind="api", format="yaml", version="1.0.0")` | Spec endpoint returned HTTP `200`, content type `text/yaml`, URL `https://api.sap.com/odata/1.0/catalog.svc/APIContent.APIs('API_SALES_ORDER_SRV')/$value?type=yaml`, size `618846` bytes. | official explicit for availability | Spec availability / controls check | 2026-06-02 |
| SAP Business Accelerator Hub EDMX spec | API Hub spec artifact | `mcp__sap_api_hub.spec(id="API_SALES_ORDER_SRV", kind="api", format="edmx", version="1.0.0")` | Spec endpoint returned HTTP `200`, content type `application/xml`, URL `https://api.sap.com/odata/1.0/catalog.svc/APIContent.APIs('API_SALES_ORDER_SRV')/$value?type=edmx`, size `275476` bytes. | official explicit for availability | Spec availability / OData metadata | 2026-06-02 |
| [SAP Business Accelerator Hub - SAP S/4HANA Cloud Public Edition package](https://api.sap.com/package/SAPS4HANACloud) | API Hub package | `mcp__sap_api_hub.package(id="SAPS4HANACloud", includeArtifacts=false)` | Package title is "SAP S/4HANA Cloud Public Edition", version `2602.3`, modified `2026-05-13T05:15:11.553Z`; description says the package provides ready-to-go APIs with supporting tools and documentation to build on top and integrate with partners. | official explicit | Product/package scope / API publication context | 2026-06-02 |
| Direct unauthenticated API Hub spec URL | API Hub retrieval attempt | `curl` to the JSON/EDMX `$value` URLs from shell | Direct unauthenticated `curl` returned small HTML documents, not the spec payloads. This did not match the authenticated API Hub MCP `spec` results, which returned HTTP 200 and payload sizes. | tooling signal / gap | Retrieval limitation statement | 2026-06-02 |
| SAP Notes targeted search | SAP Notes | `mcp__sap_notes.search(q="API_SALES_ORDER_SRV Sales Order A2X deprecation quota rate limit", lang="EN")` | Search returned correction/behavior notes for the Sales Order A2X API, including SAP Notes 3587611, 3605449, 3549362, 3311614, and others; no top result identified a policy prohibition, API deprecation, or published quota/rate-limit rule. | official cross-check | Notes cross-check for prohibition/deprecation/quota | 2026-06-02 |
| SAP Notes deprecation search | SAP Notes | `mcp__sap_notes.search(q="API_SALES_ORDER_SRV deprecated", lang="EN")` | Search returned zero results. | official cross-check | Deprecation cross-check | 2026-06-02 |
| [SAP Note 3467023 - Additional properties OData API Sales Order (A2X)](https://launchpad.support.sap.com/#/notes/3467023) | SAP Note | `mcp__sap_notes.fetch(id="3467023", lang="EN")` | Note is released to customer, version `2`, release date `29.05.2024`, component `SD-SLS-API`; it adds additional properties to `API_SALES_ORDER_SRV`/`A_SalesOrder`/`A_SalesOrderItem`. This is evidence of ongoing API maintenance, not a restriction. | official cross-check | API maintenance signal / no prohibition | 2026-06-02 |
| SAP released-object data | Released-object tool | `mcp__sap_docs.sap_get_object_details(object_type="DDLS", object_name="I_SALESORDER", system_type="public_cloud", target_clean_core_level="A")` | `I_SALESORDER` returned `found: true`, state `released`, Clean Core level `A`, source `released`, compliance `compliant`, component `SD-SLS-SO-2CL`, software component `SAPSCORE`. | official/tooling signal | Supporting released-object evidence | 2026-06-02 |

## Policy analysis

### Published API / Documented Use

The core SAP-facing interface is a positive finding. `API_SALES_ORDER_SRV` is listed in SAP Business Accelerator Hub for SAP S/4HANA Cloud Public Edition as an active OData API, version `1.0.0`, with the documented short text "Create, read, update, and delete sales orders with this synchronous OData API." API Hub resources confirm the exact create operation needed by the scenario: `POST /A_SalesOrder` creates a sales order. The same API also documents read operations, related-entity operations, and `$batch`.

Under the policy baseline, an API listed in SAP Business Accelerator Hub is a Published API for its documented use. Syncing Salesforce orders into S/4HANA Cloud by calling the standard Sales Order A2X API through Boomi is therefore directionally aligned, provided Boomi calls only the published API operations and the implementation follows the documented communication arrangement, authorizations, payload rules, and operational controls.

The use of Boomi does not make the scenario non-aligned. For third-party middleware and iPaaS, the policy analysis focuses on the SAP API surface and usage pattern, not the integration-platform brand. This is deterministic middleware integration, not agentic AI and not use of an internal/private SAP interface.

### Specific API Controls (rate/quota/deprecation/ingress-egress/bulk/security)

API Hub fetch returned positive security evidence for the scenario: `OAuth2Auth` labeled "OAuth 2.0" is documented in the artifact. It also returned `BasicAuth`, while the API Hub search facet listed `x509`; those are API Hub/communication-arrangement details to validate in the customer's tenant. Since the stated design uses OAuth 2.0 and the fetched artifact includes OAuth 2.0, the authentication fact is aligned at the API Hub level.

API Hub metadata returned `Deprecated: null` and `Successors: null` for `API_SALES_ORDER_SRV` version `1.0.0`. The API Hub JSON/YAML/EDMX spec endpoints were reachable through the MCP server with HTTP 200. The normalized artifact/resource/spec metadata exposed by the MCP tools did not surface documented rate limits, quotas, ingress/egress caps, or deprecation controls for this API. SAP Notes cross-checks likewise did not find a deprecation result or a top-result quota/rate-limit restriction for `API_SALES_ORDER_SRV`.

That absence is not permission to ignore productive controls. It means no API Hub artifact-level quota/deprecation red flag was found in this run. The customer should still confirm tenant-specific throttling, communication arrangement details, OAuth setup, user/role authorizations, `$batch` limits, payload size constraints, and retry/backoff behavior in their S/4HANA Cloud documentation and tenant operations. At about 500 sales orders per day, the stated volume appears modest for a business-object integration if smoothed and idempotent, but a badly designed burst or retry storm could still create system-risk issues.

### General Controls (competitive analysis / out-of-scope use / system risk)

No competitive-analysis use, control bypass, or private/internal endpoint was stated. No scraping, harvesting, or systematic large-scale extraction was stated. The integration writes operational business documents into S/4HANA Cloud through a published business API.

The main General-Control risks are implementation quality and production behavior: duplicate order creation, uncontrolled retries, broad reads, excessive `$expand`, large `$batch` payloads, missing idempotency/correlation IDs, insufficient OAuth/communication-user scoping, and weak monitoring. Those are normal integration-governance risks, not policy blockers on the facts supplied.

### Custom APIs / Clean Core

No custom SAP API or custom ABAP wrapper is part of the stated scenario. The released-object lookup for `I_SALESORDER` is a supporting Clean Core signal for the sales-order domain, but the stronger evidence is the API Hub publication of `API_SALES_ORDER_SRV` itself.

If the implementation adds custom middleware mappings or Boomi process logic, that customer-owned code is not a problem by itself. It should not call private SAP endpoints, generic table readers, RFC/BAPI backdoors, or custom wrappers around non-released SAP objects as fallback paths. Keep the SAP-facing integration boundary to the published OData API.

## Red flags

| Red flag | Present? | Evidence |
| --- | --- | --- |
| API not published on SAP Business Accelerator Hub | No | API Hub search/fetch returned active public-edition artifact `API_SALES_ORDER_SRV`, version `1.0.0`, retrieved 2026-06-02. |
| Use outside documented sales-order operations | Not on stated facts | API Hub documents create/read/update/delete operations; scenario creates about 500 sales orders/day from Salesforce. |
| Unsupported/internal/private interface | No | No RFC, table reader, private endpoint, or custom SAP wrapper was stated. |
| Agentic/generative AI plans API calls | No | Boomi middleware integration is deterministic on the facts supplied. |
| Large-scale extraction/replication | No | This is bounded inbound sales-order creation, not data harvesting or warehouse replication. |
| API deprecation signal | No evidence found | API Hub `Deprecated: null`, `Successors: null`; SAP Notes search for `API_SALES_ORDER_SRV deprecated` returned zero results. |
| Published quota/rate-limit violation | No evidence found | No API Hub artifact-level quota/rate-limit field surfaced; exact tenant throttles still need confirmation. |
| System-risk implementation pattern | Possible but not shown | Bursts, retry storms, oversized batches, or broad reads would be a design issue to control. |

## Missing information (and what would most improve confidence)

| Missing fact | Why it matters |
| --- | --- |
| Exact S/4HANA Cloud tenant release and communication arrangement | Confirms productive endpoint, OAuth/x509/basic availability, roles, scopes, and business catalogs. |
| Exact Boomi process behavior | Confirms whether it calls only `API_SALES_ORDER_SRV`, how it handles retries, idempotency, failures, and duplicate prevention. |
| Burst pattern and batch sizing | 500/day is modest, but 500 in a few seconds plus retries could be materially different from smoothed traffic. |
| Payload complexity | Deep inserts with many partners, pricing elements, texts, schedules, and related objects may create more load than the order count suggests. |
| Read pattern | Reads should be bounded with filters/selects and should avoid broad unbounded order scans. |
| Tenant-specific limits or SAP support guidance | API Hub did not surface a rate/quota value in this run; productive tenant guidance would improve confidence from medium to high. |
| Monitoring and audit controls | Needed for operational safety: correlation IDs, error handling, alerting, API response tracking, and order reconciliation. |

## Questions for SAP / internal governance

1. For this tenant/release, which communication arrangement and authentication method should be used for `API_SALES_ORDER_SRV` in S/4HANA Cloud Public Edition: OAuth 2.0, x509, basic, or a specific combination?
2. Are there tenant-specific API throttles, `$batch` limits, payload-size limits, or fair-use constraints for `API_SALES_ORDER_SRV` beyond what API Hub exposed?
3. Is the planned Boomi connector/process certified or documented to use only the standard Sales Order A2X OData API, with no fallback to RFC, table reads, or private endpoints?
4. What idempotency key, external reference, or duplicate-detection approach should be used so Salesforce retries do not create duplicate S/4HANA sales orders?
5. Which business roles, communication user scopes, and field-level controls are required for the exact sales-order document types and sales areas?
6. Are there customer-specific contract, Digital Access, or licensing questions for creating S/4HANA sales orders from Salesforce? Those are commercial/legal topics for SAP account/licensing channels, not this technical policy assessment.

## Recommended next steps

1. Proceed with `API_SALES_ORDER_SRV` as the SAP-facing interface, but keep the integration boundary strict: no RFC, table-reader, private endpoint, or custom wrapper fallback.
2. Configure the S/4HANA Cloud communication arrangement for OAuth 2.0 if that is the approved tenant pattern, and document the communication user/client, scopes, roles, and certificate/secret handling without storing secrets in design documents.
3. Shape the Boomi process for low system risk: bounded concurrency, exponential backoff, retry caps, duplicate prevention, correlation IDs, payload validation, and alerting.
4. Use `POST /A_SalesOrder` or documented deep insert only as needed; use `$batch` conservatively and only within documented OData/API constraints.
5. Keep read operations narrow with filters/selects and avoid broad polling of all sales orders unless separately documented and sized.
6. Ask SAP or tenant operations for any productive API quotas/throttles that were not visible in API Hub, then update the design runbook with those limits.
7. Reassess if the integration scope changes materially, for example to autonomous AI order creation, high-volume replication, large unbounded reads, or non-published fallback interfaces.

## Endorsed alternative (if a path is not aligned)

No replacement path is required for the stated design because the SAP-facing API is published and the usage pattern appears to match documented sales-order integration. If functional requirements outgrow OData V2 `API_SALES_ORDER_SRV`, evaluate SAP-published successor or adjacent Sales Order APIs in SAP Business Accelerator Hub for the specific tenant release, then reassess the new API/version and operations.

> **Reminder:** evidence-based technical assessment only - not legal/contractual advice and not a final SAP compliance decision. Confirm the specifics with SAP through the questions above.
