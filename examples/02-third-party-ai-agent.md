> **Input prompt.** This report was produced by running the prompt below in Cursor against the [`sap-api-policy-evidence`](../skills/sap-api-policy-evidence/SKILL.md) skill, with the SAP MCP servers connected. The skill's output report follows.

```text
Follow the skill at skills/sap-api-policy-evidence/SKILL.md.

Assess this scenario: We want to connect a third-party AI agent to S/4HANA Cloud
through our own custom MCP gateway, so it can autonomously read and create sales
orders via the standard OData APIs based on a user chat. Is that aligned with the
2026 SAP API Policy?

Do a runtime self-check, gather live evidence and cite every source with its
retrieval date, then write the full assessment report and save it as a markdown
file at examples/02-third-party-ai-agent.md.
```

---

# SAP API Policy - Evidence Assessment

> **Not legal or final SAP advice.** This is an evidence-based *technical* assessment. Only SAP, the applicable contract, or SAP support/account/legal channels can give a binding answer for a specific customer landscape. SAP does not publish a binary compliant/not-compliant decision matrix (API Policy FAQ Q49); this report gets as close as the evidence allows and flags what to confirm with SAP.

**Assessment:** Likely not aligned
**Confidence:** high
**Date:** 2026-06-02
**Policy baseline:** SAP API Policy v.4.2026a and API Policy FAQ v1.2 (May 2026), plus the live sources listed below.

## Scenario facts

| Fact | Value | Status | Notes |
| --- | --- | --- | --- |
| SAP product | SAP S/4HANA Cloud | Provided | The prompt did not specify Public Edition vs Private Edition. API Hub evidence below verifies the Public Edition artifact `API_SALES_ORDER_SRV`; a private-edition/on-premise sibling artifact also exists. |
| Deployment | Treated as S/4HANA Cloud Public Edition for first-pass API evidence | Inferred assumption | If the actual landscape is S/4HANA Cloud Private Edition, the API ID/version may differ, but the agentic-AI control still applies to the usage pattern. |
| Version / release | Not provided | Important, not blocker | Exact release affects API version and communication arrangement details, not the policy direction for unendorsed autonomous AI access. |
| Interface | Standard Sales Order OData APIs, assumed `API_SALES_ORDER_SRV` ("Sales Order (A2X)") | Inferred assumption from "standard OData APIs" and "sales orders" | API Hub confirms the artifact is active and published for reading and creating sales orders. |
| Operations | Read and create sales orders | Provided | API Hub resources confirm `GET /A_SalesOrder` and `POST /A_SalesOrder`, plus related entity operations. |
| Consumer/tool | Third-party AI agent | Provided | This is not ordinary deterministic middleware; it is an AI agent. |
| Gateway | Customer-built custom MCP gateway | Provided | The prompt says "our own custom MCP gateway"; no SAP Integration Suite MCP Gateway, Joule, Agent Gateway, or written SAP authorization was provided. |
| Data direction | External agent/gateway calls inbound into S/4HANA Cloud | Inferred assumption | API Policy FAQ Q12 treats inbound external access to SAP-provided services as in scope. |
| Usage pattern | Agent autonomously reads and creates sales orders based on user chat | Provided | This squarely triggers the AI/agentic controls because the AI plans/selects/executes API calls. |
| Human approval gate | Not stated; treated as absent for the stated scenario | Inferred assumption | The word "autonomously" implies no mandatory human approval before write operations. If writes require human approval through an SAP-endorsed path, reassess. |
| SAP written authorization / contract evidence | None supplied | Missing | Customer-specific SAP authorization could change the answer, but no such evidence was provided. |

## Runtime self-check

| Tool family | Runtime status | Evidence gathered | Gap handling |
| --- | --- | --- | --- |
| SAP Docs MCP | Available. Search/fetch, Discovery Center, and released-object tools were callable. | Used Architecture Center search/fetch for A2A/MCP and pro-code agent guidance; used Discovery Center for SAP Integration Suite; used released-object lookup for Sales Order DDLS artifacts. | No material confidence reduction. |
| SAP API Hub MCP | Available and authenticated. `categories` returned live Business Accelerator Hub metadata on 2026-06-02. | Used `search`, `fetch`, `resources`, and `package` for `API_SALES_ORDER_SRV` and the S/4HANA Cloud package; searched `SAP_COM_1294` as a nuance. | No material gap. API publication status was verified. |
| SAP Notes MCP | Available and authenticated. | Searched for API Policy/MCP terms; fetched SAP Note 3747787 for current MCP-adjacent supply-chain/security risk context. | No direct controlling SAP Note for "custom MCP gateway to sales orders" was found in the top targeted searches. This does not lower confidence because the SAP API Policy, FAQ, API Hub, and Architecture Center sources are controlling. |
| SAP Roadmap MCP | Available and authenticated. | Searches for `MCP Gateway Integration Suite` and `Agent Gateway A2A Joule` returned zero current/last items through this tool. | Roadmap is future/planning evidence only. The zero-result finding is recorded as a non-material source gap. |
| ARC-1 live SAP system MCP | Tool families were discoverable in the runtime. | Not used. | The skill requires explicit confirmation before querying a live customer SAP system. The scenario does not require live tenant reads because public SAP sources settle the policy direction. |
| Official web sources | Available. | Used official SAP Help, SAP FAQ PDF, SAP Architecture Center, and SAP webpages as public live sources. | No material gap. |

## Interface inventory

| Capability | Interface (ID/type) | Endpoint/object | Provider | Publication evidence | Status | Controls | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Read/create sales orders from an external system | `API_SALES_ORDER_SRV` / OData V2 API | `GET /A_SalesOrder`, `POST /A_SalesOrder`, related sales-order entities | SAP S/4HANA Cloud Public Edition | SAP Business Accelerator Hub lists `API_SALES_ORDER_SRV` as active, title "Sales Order (A2X)", package `SAPS4HANACloud`, with read/create/update/delete capabilities | API itself is published for documented sales-order integration | API Hub metadata lists communication scenario `Sales Order Integration (SAP_COM_0109)`, x509 authentication, and other communication scenarios including `SAP_COM_1294`; productive tenant limits/scopes still must be checked | Continue using the published API only within documented controls and an SAP-endorsed agentic architecture |
| Proposed agentic access layer | Customer-built custom MCP gateway exposing the OData API as tools | Customer MCP server/gateway/tool manifest | Customer / third party | No SAP source retrieved that identifies a customer-operated custom MCP gateway as an endorsed pathway for external autonomous business-process access | Likely not aligned for autonomous read/create use | API Policy section 2.2.2(a), section 3, FAQ Q17/Q22/Q39, and Architecture Center A2A/MCP guidance apply | SAP Integration Suite MCP Gateway, or A2A/Joule/Agent Gateway where available and fit for purpose |
| SAP-endorsed MCP tool exposure | MCP Gateway in SAP Integration Suite | Governed MCP-compliant tool exposure for SAP and non-SAP APIs | SAP Integration Suite | Architecture Center and FAQ identify SAP Integration Suite MCP Gateway as the SAP-endorsed pattern for governed MCP tool access | Candidate aligned path if used within documented controls | OIDC authentication/authorization, rate limiting, payload protection, traffic management, monitoring, tracing, analytics, and lifecycle governance | Use this on the SAP side of the architecture before exposing Sales Order API operations to external agents |
| SAP-endorsed multi-agent interoperability | A2A through Joule / Agent Gateway | A2A protocol, Joule, Agent Gateway | SAP BTP / Joule | Architecture Center identifies A2A as SAP's preferred external interoperability approach; the same page says Agent Gateway was not yet GA and current architecture supports outbound only as of the retrieved page | Candidate path, subject to current availability and SAP confirmation | IAS App2App tokens, named user context, standardized A2A contract, SAP-managed gateway | Confirm GA status and supported direction with SAP before relying on this as current production permission |
| Supporting released Sales Order object signal | `I_SALESORDER` / DDLS | S/4HANA Cloud released-object data | SAP S/4HANA Cloud Public Edition | Released-object lookup returned `I_SALESORDER` as state `released`, Clean Core level A | Supporting signal only; API Hub is the stronger business API evidence | Clean Core level A/released API object | Useful for extension design, not a substitute for API Policy agentic controls |

## Evidence

| Source | Type | Tool/query | Finding | Authority | Relevance | Retrieved |
| --- | --- | --- | --- | --- | --- | --- |
| [SAP API Policy v.4.2026a](https://help.sap.com/doc/sap-api-policy/latest/en-US/API_Policy_latest.pdf) | SAP Policy | Web open, official SAP Help PDF | Published APIs are those in API Hub or product documentation; non-published APIs must not be accessed unless documentation or SAP authorization permits it. Section 2.2.2 prohibits API use for semi-autonomous/generative AI systems that plan, select, or execute API-call sequences except through SAP-endorsed architectures/pathways. Section 3 prohibits bypassing controls through intermediary services, custom code, proxies, gateways, or impersonation. | official explicit | Published API / General Controls / agentic AI / gateway bypass | 2026-06-02 |
| [API Policy FAQ v1.2, May 2026](https://www.sap.com/docs/download/2026/04/e2a0665e-4c7f-0010-bca6-c68f7e60039b.pdf) | SAP FAQ | Web click/open from SAP FAQ page | Q14/Q32 say the policy applies regardless of third-party middleware; the criterion is the SAP API surface and usage pattern. Q17 explains risks from ungoverned AI. Q22/Q39 say third-party AI platforms can connect through endorsed architectures such as A2A/Joule/Agent Gateway and SAP Integration Suite MCP Gateway. Q40 excludes deterministic RPA only when there is no autonomous reasoning/LLM planning. Q48-Q51 define documented use and SAP-endorsed reference architectures, and Q49 says there is no binding decision matrix. | official explicit | Third-party tools / AI agent / endorsed paths / non-finality | 2026-06-02 |
| [SAP Business Accelerator Hub - Sales Order (A2X)](https://api.sap.com/api/API_SALES_ORDER_SRV/overview) | API Hub | `mcp__sap_api_hub.search(q="API_SALES_ORDER_SRV", categoryKey="API", artifactType="API")`; `fetch(id="API_SALES_ORDER_SRV", kind="api")` | `API_SALES_ORDER_SRV` is active, vendor SAP, package `SAP S/4HANA Cloud Public Edition`, OData, version 1.0.0, short text "Create, read, update, and delete sales orders with this synchronous OData API." | official explicit | Published API / Documented Use | 2026-06-02 |
| [SAP Business Accelerator Hub - Sales Order resources](https://api.sap.com/api/API_SALES_ORDER_SRV/overview) | API Hub | `mcp__sap_api_hub.resources(id="API_SALES_ORDER_SRV", kind="api", version="1.0.0")` | Resources returned 101 paths and 158 operations, including `GET /A_SalesOrder` to read sales order headers and `POST /A_SalesOrder` to create a sales order. | official explicit | Exact operations / read-write scope | 2026-06-02 |
| [SAP Business Accelerator Hub - SAP S/4HANA Cloud Public Edition package](https://api.sap.com/package/SAPS4HANACloud) | API Hub | `mcp__sap_api_hub.package(id="SAPS4HANACloud", includeArtifacts=false)` | Package title is SAP S/4HANA Cloud Public Edition; description says it provides ready-to-go APIs with supporting tools/documentation to build on top and integrate with partners; package version returned as 2602.3. | official explicit | Product/package scope | 2026-06-02 |
| SAP Business Accelerator Hub search for `SAP_COM_1294` | API Hub | `mcp__sap_api_hub.search(q="SAP_COM_1294", categoryKey="API", artifactType="API")` | Search returned many S/4HANA Cloud API artifacts whose metadata includes `Agent and Tool Integration Layer for SAPSCORE Integration (SAP_COM_1294)`, including APIs in the same public-cloud package. This is a notable signal, but no retrieved SAP documentation showed that `SAP_COM_1294` authorizes a customer-operated custom MCP gateway for autonomous third-party business writes. | official explicit for metadata; official inferred for gap | Communication scenario nuance / SAP confirmation question | 2026-06-02 |
| [SAP Architecture Center - SAP's AI Golden Path](https://architecture.learning.sap.com/docs/ai-golden-path) | SAP Architecture Center | Web open, official Architecture Center | SAP's AI Golden Path is SAP's starting point for AI applications across the SAP ecosystem and covers agentic architectures, Joule, AI Core/generative AI hub, HANA Cloud, Business Data Cloud, and MCP/tooling concepts. | official inferred | Endorsed AI architecture context | 2026-06-02 |
| [SAP Architecture Center - A2A and MCP for Interoperability](https://architecture.learning.sap.com/docs/ref-arch/ca1d2a3e/1) | SAP Architecture Center / SAP Docs MCP | Web open; `mcp__codex_apps__sap_docs_mcp._search`; `_fetch("/architecture-center/RA0029/1-a2a-and-mcp/readme#mcp-gateway-in-integration-suite")` | Architecture Center recommends Agent Gateway using A2A and MCP Gateway in SAP Integration Suite for governed, production-grade agentic access. It says Integration Suite MCP Gateway exposes SAP and non-SAP APIs as governed MCP-compliant tools and provides authentication/authorization, rate limiting, payload protection, traffic management, monitoring, tracing, and analytics. It also states SAP uses A2A as the preferred external interoperability approach for vendors and third-party agents. | official explicit | Endorsed pathway / MCP / A2A / governance | 2026-06-02 |
| [SAP Architecture Center - Pro-Code AI Agents on SAP BTP](https://architecture.learning.sap.com/docs/ref-arch/ca1d2a3e/3) | SAP Architecture Center / SAP Docs MCP | `_fetch("/architecture-center/RA0029/3-pro-code-ai-agents/readme#agent-integration-layer")` | Pro-code agent guidance describes SAP BTP, SAP Cloud SDK for AI, Generative AI Hub, CAP, Destination Service, Connectivity Service, A2A exposure, and MCP tool consumption as part of SAP's reference architecture for custom agents. | official inferred | SAP-side agent architecture / alternative path | 2026-06-02 |
| [SAP Architecture Center - Integration, Security, Ethics & Governance](https://architecture.learning.sap.com/docs/ai-native-north-star-architecture/integration-security-ethics-governance) | SAP Architecture Center | Web open, official Architecture Center | SAP describes autonomous agents as needing enterprise-grade boundaries for governance, identity, interoperability, fine-grained tool policies, auditability, and human-in-the-loop routing for critical decisions. | official inferred | Agent governance / write-risk controls | 2026-06-02 |
| [SAP Architecture Center - Global Standards for Agentic AI](https://architecture.learning.sap.com/docs/global-standards-for-agentic-ai) | SAP Architecture Center | Web open, official Architecture Center | SAP states it is establishing clear frameworks for data and transactional access through MCP and A2A and participates in agentic AI standards. This supports the conclusion that protocol use alone is not enough; governed frameworks matter. | official inferred | Standards / MCP-A2A context | 2026-06-02 |
| [SAP Discovery Center - SAP Integration Suite](https://discovery-center.cloud.sap/serviceCatalog/f810c887-8d25-4942-9849-354837951066) | Discovery Center | `sap_discovery_center_search(query="SAP Integration Suite")`; `sap_discovery_center_service(serviceId="SAP Integration Suite", include_roadmap=false, include_pricing=false)` | Discovery Center describes SAP Integration Suite as an enterprise-grade integration platform-as-a-service with API Management, Cloud Integration, Open Connectors, Integration Assessment, business events, and API governance/protection capabilities. | official explicit | Endorsed-path service capability | 2026-06-02 |
| [SAP Note 3747787](https://launchpad.support.sap.com/#/notes/3747787) | SAP Note | `mcp__sap_notes.search(q="3747787 Mini Shai-Hulud MCP")`; `fetch(id="3747787")` | Note 3747787 is a current HotNews security note for malicious open-source packages in SAP CAP/MTA tooling, including credential exfiltration risk and references to MCP-related secrets among items to rotate if affected. It is contextual security evidence, not the policy source for this scenario. | official explicit | Security risk context / custom open-source gateway hygiene | 2026-06-02 |
| SAP Notes targeted searches | SAP Notes | `search(q="API Policy MCP Gateway AI agent")`; `search(q="customer operated MCP servers")` | Searches did not produce a direct top-result SAP Note that supersedes the policy/FAQ/Architecture Center guidance for custom MCP gateways. Top results were unrelated or product-specific. | tooling signal / gap | Source-gap statement | 2026-06-02 |
| SAP Road Map Explorer searches | SAP Roadmap | `search(q="MCP Gateway Integration Suite", range="CURRENT-LAST")`; `search(q="Agent Gateway A2A Joule", range="CURRENT-LAST")` | No current/last Road Map Explorer items were returned by this tool for those exact queries. Roadmap evidence is not used for current permission. | tooling signal / gap | Roadmap source gap / future only | 2026-06-02 |
| SAP released-object data | Released-object tool | `sap_search_objects(query="SalesOrder", system_type="public_cloud", clean_core_level="A", object_type="DDLS", app_component="SD-SLS")`; `sap_get_object_details(object_type="DDLS", object_name="I_SALESORDER", system_type="public_cloud", target_clean_core_level="A")` | Search returned multiple released public-cloud Sales Order DDLS objects; `I_SALESORDER` returned state `released`, Clean Core level A, compliance `compliant`. | tooling signal | Supporting released-object evidence | 2026-06-02 |

## Policy analysis

### Published API / Documented Use

The Sales Order OData API itself is a positive finding. SAP Business Accelerator Hub lists `API_SALES_ORDER_SRV` as an active S/4HANA Cloud Public Edition API, and API Hub resources confirm the exact read and create operations the scenario needs. On that narrow point, using the standard OData API is better than using a private endpoint, table read, RFC/BAPI wrapper, or undocumented service.

That does not make the whole scenario aligned. Documented Use is still bounded by the API Policy's Specific and General Controls. The sales-order API is documented for sales-order integration operations; the proposed architecture additionally exposes those operations to a third-party AI agent that autonomously plans/selects/executes calls through a customer custom MCP gateway. That second layer triggers API Policy section 2.2.2(a).

### Specific API Controls (rate/quota/deprecation/ingress-egress/bulk/security)

API Hub metadata identifies the API as active and shows communication scenario information, including `Sales Order Integration (SAP_COM_0109)` and an API Hub metadata signal for `Agent and Tool Integration Layer for SAPSCORE Integration (SAP_COM_1294)`. The API resource list confirms read and write paths, including `POST /A_SalesOrder`.

The retrieved API Hub metadata does not show productive tenant rate limits, exact communication arrangement setup, authorization scopes, or any rule saying a customer-operated MCP gateway may expose those write operations to an autonomous third-party agent. Those details should be checked in the tenant documentation, communication arrangement, and SAP support/account guidance before implementation. They are not the decisive gap here; the decisive control is the AI/agentic rule.

### General Controls (competitive analysis / out-of-scope use / system risk)

No competitive-analysis purpose was stated. The main General-Control issues are system risk and control bypass. API Policy section 2.2.1 prohibits use that creates risk to performance, stability, or security. The FAQ identifies ungoverned AI agents as risky because a prompt can trigger unpredictable API call volume, sensitive-data access, or incorrect write-back. This scenario includes autonomous creation of sales orders, so data integrity and authorization controls are central.

API Policy section 3 is also directly relevant. A custom gateway is not prohibited merely because it is custom code, but it cannot be used to bypass API Controls. A customer-built MCP gateway that lets a third-party AI agent autonomously issue read/write sales-order calls is materially different from a deterministic integration flow or a normal third-party iPaaS call using published APIs.

### AI / agentic / MCP / automation

This is the controlling branch. The policy prohibits API use for interaction or integration with semi-autonomous or generative AI systems that plan, select, or execute API-call sequences, except through SAP-endorsed architectures, data services, or service-specific pathways expressly intended for that purpose.

The scenario says the third-party AI agent can autonomously read and create sales orders based on a chat. That is not deterministic RPA under FAQ Q40; it is LLM/agentic decision-making with business-data reads and business-object writes. The use of MCP does not make it endorsed by itself. SAP's FAQ and Architecture Center distinguish governed SAP-side pathways from direct community-built or customer-operated MCP servers. For external business-process access, the named SAP-side paths are SAP Integration Suite MCP Gateway for governed MCP tool exposure and A2A/Joule/Agent Gateway where available and appropriate.

As stated, the architecture uses "our own custom MCP gateway," not the SAP Integration Suite MCP Gateway and not A2A through SAP-managed Joule/Agent Gateway. Without written SAP authorization or documentation proving that this exact custom gateway is an SAP-endorsed pathway, the proposed architecture is likely not aligned.

### Custom APIs / Clean Core

The custom MCP gateway is customer-owned integration code outside the S/4HANA system. Customer code and middleware are not per se prohibited. The issue is what the code enables. FAQ Q27/Q31 and API Policy section 3 are the relevant analogy: custom layers must not create a pathway for unendorsed agentic AI interactions or circumvent General/Specific API Controls.

If the gateway is retained, it should be redesigned as a governed policy-enforcement layer behind an SAP-endorsed path, not as a substitute for that path. It should expose only allowlisted published APIs, enforce least privilege, propagate named-user context where required, rate-limit and audit every tool call, validate payloads, and require human approval for write actions that can materially affect orders, pricing, credit, delivery, or financial downstream processes.

## Red flags

| Red flag | Present? | Evidence |
| --- | --- | --- |
| Autonomous/generative AI plans/selects/executes SAP API calls | Yes | Scenario facts; API Policy section 2.2.2(a); FAQ Q17/Q34-Q40. |
| External third-party AI agent can write business data | Yes | Scenario states autonomous sales order creation via chat. |
| Gateway is customer custom MCP, not an SAP-endorsed pathway | Yes, as stated | Prompt says "our own custom MCP gateway"; FAQ Q39 and Architecture Center point to SAP Integration Suite MCP Gateway rather than customer-operated/community MCP servers for enterprise business-process access. |
| Human approval before writes is absent or unproven | Risk | Prompt says "autonomously"; no human-in-the-loop control was supplied. |
| Published API status is positive but insufficient | Yes | API Hub confirms `API_SALES_ORDER_SRV` is active and published, but the AI/agentic usage pattern is separately controlled. |
| SAP_COM_1294 appears in API Hub metadata but is not explained by retrieved docs | Nuance / confirmation item | API Hub metadata lists `Agent and Tool Integration Layer for SAPSCORE Integration (SAP_COM_1294)`, but no retrieved source showed it authorizes a customer-operated custom MCP gateway. |
| Customer-specific SAP written authorization supplied | No | Missing. |

## Missing information (and what would most improve confidence)

The assessment is high confidence for the architecture as stated: a third-party AI agent autonomously writes sales orders through a customer-built custom MCP gateway. The facts below would mainly help design a compliant replacement or identify a customer-specific authorization:

| Missing fact | Why it matters |
| --- | --- |
| Actual deployment: S/4HANA Cloud Public Edition vs Private Edition | Determines exact API ID/version, communication arrangement setup, and tenant controls. |
| Exact OData API IDs and versions exposed as MCP tools | Confirms whether only published APIs are exposed and whether any internal/private endpoints are included. |
| Whether the gateway uses SAP Integration Suite MCP Gateway or only custom/community MCP code | This is the central architecture fact. The prompt indicates custom-only; if that is wrong, reassess. |
| Meaning and availability of `SAP_COM_1294` for this customer and this API | API Hub metadata makes it a valid SAP question, but it was not enough to override the FAQ's warning about customer-operated MCP servers. |
| Identity model | Need named-user context, technical user use, OAuth/x509 setup, IAS/App2App, principal propagation, and least-privilege authorizations. |
| Human approval gate and write controls | Critical for sales-order creation. Approval policy, validation, and audit logging can reduce business risk, but they do not by themselves create an SAP-endorsed pathway. |
| Rate limits, retry/backoff, and monitoring | Needed to avoid stability and fair-use issues. |
| SAP account/support written authorization or architecture approval | Could change the assessment if SAP explicitly authorizes this exact design. |

## Questions for SAP / internal governance

1. Does SAP consider a customer-built custom MCP gateway an "SAP-endorsed architecture" for an external third-party AI agent to autonomously create sales orders in S/4HANA Cloud, or must the SAP-side path be SAP Integration Suite MCP Gateway, A2A/Joule/Agent Gateway, or another documented service-specific path?
2. What exactly does `Agent and Tool Integration Layer for SAPSCORE Integration (SAP_COM_1294)` authorize for `API_SALES_ORDER_SRV`, and is it available for customer-operated third-party AI agents or only for SAP-managed agent/tool scenarios?
3. Is autonomous sales-order creation allowed under any endorsed path, or must create/update operations require human approval before the SAP API call?
4. Which identity pattern is required: named user, technical communication user, IAS App2App, x509, OAuth scopes, principal propagation, or a combination?
5. What tenant-specific rate limits, payload constraints, approval rules, and audit/retention controls apply to `API_SALES_ORDER_SRV` when exposed as an AI-agent tool?
6. If the organization already has written SAP approval, which document/ticket/contract clause names this exact architecture, API list, agent behavior, and gateway controls?

## Recommended next steps

1. Do not productionize the stated custom-only MCP gateway for autonomous sales-order create/read access as the target architecture.
2. Keep the Sales Order OData API in scope, but expose it only through an SAP-endorsed agentic pathway or with explicit written SAP authorization.
3. Redesign the flow so high-impact write operations such as `POST /A_SalesOrder` require a deterministic policy check and human approval before execution, at least until SAP confirms a fully autonomous write pattern for this process.
4. Build a tool registry that allowlists exact APIs, entities, methods, and fields. Avoid broad "sales order API access" tools that let the agent discover arbitrary operations.
5. Enforce named-user or approved delegated identity, least-privilege authorizations, rate limits, retry/backoff, payload validation, prompt-injection/tool-output safeguards, complete audit logs, and kill-switch controls.
6. Ask SAP the questions above, specifically about `SAP_COM_1294` and whether SAP Integration Suite MCP Gateway is required for this use case.
7. Reassess after the target architecture is changed; the assessment could move from `Likely not aligned` to `Needs SAP confirmation` or `Likely aligned` if the SAP-side endorsed path, controls, and exact API usage are documented.

## Endorsed alternative

The most direct SAP-side alternative is SAP Integration Suite MCP Gateway: expose `API_SALES_ORDER_SRV` as a governed MCP-compliant tool through Integration Suite rather than through a custom-only MCP gateway. Keep the third-party AI platform as the non-SAP-side orchestrator if desired, but put SAP-side tool exposure, authentication, authorization, rate limiting, traffic management, monitoring, tracing, and lifecycle governance in the SAP-endorsed layer.

For multi-agent interoperability, evaluate A2A through Joule and Agent Gateway. Treat this carefully: the Architecture Center page retrieved on 2026-06-02 says Agent Gateway is not yet generally available and the current architecture supports outbound communication only. Use it as a production path only when SAP confirms current availability and direction for the customer's tenant.

For custom pro-code agents, SAP's Architecture Center points to SAP BTP with SAP Cloud SDK for AI, Generative AI Hub, CAP, Destination Service, Connectivity Service, and A2A/MCP patterns. That is a better fit than a standalone custom gateway because it keeps the agent, model access, connectivity, and governance inside SAP's documented AI reference architecture.

The target pattern should look like this:

| Layer | Recommended control |
| --- | --- |
| User chat | Authenticate the user, capture business intent, and display proposed order action before write-back. |
| AI agent | Limit autonomy to bounded tool choices; use structured plans and deterministic validators. |
| SAP-side gateway | Use SAP Integration Suite MCP Gateway or another SAP-confirmed endorsed path, not a custom-only MCP server. |
| Tool manifest | Expose only `GET` and narrowly scoped `POST` operations needed for the use case; avoid broad CRUD by default. |
| Write execution | Require human approval and business-rule validation before `POST /A_SalesOrder` unless SAP confirms full autonomy is supported. |
| S/4HANA API | Use only published API Hub artifacts such as `API_SALES_ORDER_SRV`, within documented communication arrangements, quotas, and authorizations. |
| Governance | Log prompt, plan, tool call, payload summary, approver, SAP response, and correlation IDs without storing unnecessary sensitive data. |

> **Reminder:** evidence-based technical assessment only - not legal/contractual advice and not a final SAP compliance decision. Confirm the specifics with SAP through the questions above.
