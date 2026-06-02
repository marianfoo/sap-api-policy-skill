# SAP API Policy - Evidence Assessment

> **Not legal or final SAP advice.** This is an evidence-based *technical* assessment. Only SAP, the applicable contract, or SAP support/account/legal channels can give a binding answer for a specific customer landscape. SAP does not publish a binary compliant/not-compliant decision matrix (API Policy FAQ Q49); this report gets as close as the evidence allows and flags what to confirm with SAP.

**Assessment:** Likely not aligned
**Confidence:** high
**Date:** 2026-06-02
**Policy baseline:** SAP API Policy v.4.2026a and API Policy FAQ v1.2 (May 2026), plus the live sources listed below.

## Scenario facts

| Fact | Value | Status | Notes |
| --- | --- | --- | --- |
| SAP product | SAP BW/4HANA | Provided | SAP Note 3255746 explicitly names SAP BW/4HANA in the affected component set. |
| Deployment | BW/4HANA on-premise or private cloud | Inferred assumption | The prompt did not state deployment. The controlling Note covers SAP ABAP applications containing PI_BASIS, SAP BW, or SAP BW/4HANA that run on-premise or in private-cloud setup. |
| Version / support package | Not provided | Important, not blocker | Version affects implementation of self-assessment/technical blocking Notes, not the policy direction for ODP-RFC. |
| Interface | ODP-RFC, i.e. RFC modules of the Operational Data Provisioning Data Replication API | Provided | This is the decisive interface. |
| Consumer/tool | Third-party ETL tool | Provided | The API Policy applies regardless of SAP Integration Suite, API Management, or third-party middleware (FAQ Q14/Q32). |
| Target | Snowflake | Provided | Current SAP Architecture Center guidance points to SAP Business Data Cloud / BDC Connect for Snowflake for governed Snowflake integration. |
| Data direction | External tool calls into SAP BW/4HANA and extracts data to Snowflake | Inferred assumption | ODP-RFC is an inbound access path to the SAP ABAP/BW system used for outbound data movement. |
| Usage pattern | Nightly extraction / replication | Provided | This is systematic recurring data extraction and likely bulk/large-scale replication. Exact volume is not needed because ODP-RFC is explicitly prohibited for this consumer class. |
| AI / agentic flags | None stated | Provided by omission | No agentic-AI controls beyond the bulk extraction controls are needed. |
| SAP written authorization / contract evidence | None supplied | Missing | A customer-specific SAP written authorization could change the answer; no such authorization was provided. |

## Runtime self-check

| Tool family | Runtime status | Evidence gathered | Gap handling |
| --- | --- | --- | --- |
| SAP Docs MCP | Available. Search, Discovery Center search, and released-object tools were callable. | Used SAP Docs search/Discovery Center and released-object lookup tools. Official SAP Help pages for ODP-OData were also verified through web search because the Help Portal page body renders as a JavaScript shell in raw fetch. | No material confidence reduction. ODP-OData is treated as an alternative to assess separately, not as permission for ODP-RFC. |
| SAP API Hub MCP | Available and authenticated. `categories` returned live Business Accelerator Hub metadata on 2026-06-02. | Exact API Hub searches for `ODP-RFC` and `RODPS_REPL` returned zero artifacts. | Negative API Hub result is not the sole basis; SAP Note 3255746 and FAQ Q23/Q24 are controlling. |
| SAP Notes MCP | Available and authenticated. | Search/fetch succeeded for SAP Notes 3255746, 3439624, 3578329, and 3475661. | No material gap. This is the highest-authority source for the decisive ODP-RFC prohibition. |
| SAP Roadmap MCP | Available and authenticated. | Search/fetch succeeded for SAP Business Data Cloud Connect for Snowflake. | Roadmap evidence is used only for alternative-path availability/planning, not for current permission. |
| ARC-1 live SAP system MCP | Tool family present. | Not used. | The skill requires explicit confirmation before querying a live customer SAP system. The scenario does not need customer-system reads because SAP Notes/FAQ/API Hub settle the interface question. |

## Interface inventory

| Capability | Interface (ID/type) | Endpoint/object | Provider | Publication evidence | Status | Controls | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Nightly BW/4HANA data extraction to Snowflake via third-party ETL | ODP-RFC / Operational Data Provisioning Data Replication API RFC modules | ODP-RFC / `RODPS_REPL*` family named by SAP Notes | SAP BW/4HANA / ABAP ODP framework | Not found as a published API in API Hub exact searches; SAP Note 3255746 explicitly restricts this interface | Not aligned for customer/third-party access to BW/4HANA on on-premise/private-cloud systems | SAP Note 3439624 provides self-assessment tooling and describes unpermitted-call detection/blocking behavior | SAP BDC / BDC Connect for Snowflake; ODP-OData where documented and technically suitable; SLT where licensed/documented; analytical CDS/OData V4 for narrower analytical access |
| Documented ODP extraction alternative | ODP OData API | Generated SAP Gateway OData service for ODP extraction | SAP BW/4HANA / SAP Gateway | SAP Note 3255746 names ODP OData as an alternative; SAP Help documents generating the OData service | Potentially aligned if the exact service, entities, volume, and controls match documentation | Must follow OData extraction/delta semantics, API Policy controls, and product documentation | Validate separately for the exact BW/4HANA release and extraction objects |
| Governed Snowflake data sharing alternative | SAP Business Data Cloud / BDC Connect for Snowflake | Data products / Delta Sharing | SAP Business Data Cloud and Snowflake | SAP Architecture Center and SAP Road Map Explorer document BDC Connect for Snowflake | Endorsed alternative for Snowflake data platform integration | Governed data products, catalog/discovery, Delta Sharing, zero-copy where applicable | Prefer this path for Snowflake rather than ODP-RFC |
| Replication alternative | SAP Landscape Transformation Replication Server (SLT) | SLT replication | SAP LT Replication Server | FAQ Q38 lists SLT as a supported replication path; SAP Note 3475661 documents SLT maintenance strategy | Potentially aligned if licensed and used within documented SLT scenarios | Existing SLT limits and maintenance constraints apply | Validate SLT version, target, license, and volume with SAP |

## Evidence

| Source | Type | Tool/query | Finding | Authority | Relevance | Retrieved |
| --- | --- | --- | --- | --- | --- | --- |
| [SAP API Policy v.4.2026a](https://help.sap.com/doc/sap-api-policy/latest/en-US/API_Policy_latest.pdf) | SAP Policy | Web open, official SAP Help PDF | Published APIs must be in API Hub or product documentation; non-published APIs must not be accessed unless documentation or SAP authorization permits it; bulk extraction/replication needs documented controls and endorsed paths. | official explicit | Published API / Documented Use / Specific Controls / General Controls / bulk | 2026-06-02 |
| [API Policy FAQ v1.2, May 2026](https://www.sap.com/docs/download/2026/04/e2a0665e-4c7f-0010-bca6-c68f7e60039b.pdf) | SAP FAQ | Web click/open from SAP FAQ page | Q14 says third-party middleware is in scope. Q22/Q23/Q24 identify ODP-RFC as not endorsed / prohibited for customer or partner use. Q38 lists BDC, SLT, analytical CDS/OData V4 as large-scale access paths. Q41 names ODP-OData and customer-choice target platforms. Q49 says no binding decision matrix. | official explicit | Third-party tools / unsupported interface / bulk / alternatives / non-finality | 2026-06-02 |
| [SAP Note 3255746 - Unpermitted usage of ODP Data Replication APIs](https://launchpad.support.sap.com/#/notes/3255746) | SAP Note | `mcp__sap_notes.search(q="3255746")`; `mcp__sap_notes.fetch(id="3255746")` | ODP-RFC is intended for SAP-to-SAP data transfer; customer or third-party access to ABAP applications containing PI_BASIS, SAP BW, or SAP BW/4HANA on on-premise/private-cloud setups is prohibited. The Note points customers to BDC and ODP OData alternatives and to SAP contact channels. | official explicit | ODP-RFC status / unsupported / successor | 2026-06-02 |
| [SAP Note 3439624 - Self-Assessment for data access to ODP Data Replication APIs](https://launchpad.support.sap.com/#/notes/3439624) | SAP Note | `mcp__sap_notes.fetch(id="3439624")` | Provides self-assessment tooling for existing ODP-RFC usage, status values for permitted/unpermitted/unclear calls, and delivery information for SAP BW and SAP BW/4HANA releases. | official explicit | ODP-RFC control / assessment / remediation | 2026-06-02 |
| [SAP Note 3578329 - Frameworks, Technologies and Development Patterns in Context of Clean Core Extensibility](https://launchpad.support.sap.com/#/notes/3578329) | SAP Note | `mcp__sap_notes.fetch(id="3578329")` | Classifies "ODP Framework RFC APIs" under integration-related technologies as Clean Core level D, not upgrade stable, not public-cloud ready, and points to SAP Note 3255746. | official explicit | Released/classification signal / Clean Core / unsupported | 2026-06-02 |
| [SAP Note 3475661 - SAP LT Replication Server - Maintenance Strategy](https://launchpad.support.sap.com/#/notes/3475661) | SAP Note | `mcp__sap_notes.fetch(id="3475661")` | Documents SLT maintenance dependencies and versions; useful only for the SLT alternative, not for permitting ODP-RFC. | official explicit | Alternative path / SLT maintenance | 2026-06-02 |
| SAP Business Accelerator Hub (API Hub) | API Hub | `mcp__sap_api_hub.categories()` | API Hub authenticated catalog access was available and returned live category metadata for APIs, events, CDS views, BAdIs, and other artifact categories. | official explicit | Runtime self-check / Published API catalog | 2026-06-02 |
| SAP Business Accelerator Hub exact search | API Hub | `mcp__sap_api_hub.search(q="ODP-RFC", top=10)` | Exact search for `ODP-RFC` returned zero artifacts. | official inferred | Published API evidence gap / ODP-RFC | 2026-06-02 |
| SAP Business Accelerator Hub exact search | API Hub | `mcp__sap_api_hub.search(q="RODPS_REPL", top=10)` | Exact search for `RODPS_REPL` returned zero artifacts. | official inferred | Published API evidence gap / ODP-RFC implementation family | 2026-06-02 |
| [Data Products in SAP Business Data Cloud](https://architecture.learning.sap.com/docs/ref-arch/f5b6b597a6/1) | SAP Architecture Center | Web open, official Architecture Center | Describes data products as a standardized way to expose datasets for consumption outside the producing application, optimized for analytics, and lists Delta Sharing as a supported access pattern with governance and zero-copy benefits. | official inferred | Endorsed data path / bulk analytics | 2026-06-02 |
| [Modernizing SAP BW with SAP Business Data Cloud](https://architecture.learning.sap.com/docs/ref-arch/f5b6b597a6/4) | SAP Architecture Center | Web open, official Architecture Center | Describes BW modernization through BW data products in SAP BDC, including SAP BW/4HANA data publication, delta-load support for selected InfoProviders, and sharing through data products. | official inferred | BW/4HANA alternative / large-scale analytics | 2026-06-02 |
| [Integration with Snowflake](https://architecture.learning.sap.com/docs/ref-arch/a07a316077/5) | SAP Architecture Center | Web open, official Architecture Center | Describes SAP Snowflake and BDC Connect for Snowflake for governed, bidirectional, zero-copy sharing of data products between SAP BDC and Snowflake; positions the integration as avoiding ETL pipelines and duplication. | official inferred | Snowflake alternative / endorsed architecture | 2026-06-02 |
| SAP Road Map Explorer - SAP Business Data Cloud Connect for Snowflake | SAP Roadmap | `mcp__sap_roadmap.search(q="BDC Connect Snowflake", range="CURRENT-LAST")`; `fetch_item(id="9198570EEC624C9D98DEBACCA56351E3")` | Roadmap item "SAP Business Data Cloud Connect for Snowflake" is marked delivered in Q2 2026 and describes bidirectional zero-copy sharing with no ETL/pipelines/customer-managed movement. | official inferred, planning/availability only | Alternative availability / roadmap | 2026-06-02 |
| SAP Help - Generate the Service for Extracting ODP Data via OData | SAP Help | Web search/open of `help.sap.com/docs/SAP_BW4HANA/.../49505ffb55fb46b991d4ab537318a4e5.html`; raw page checked with `curl` | SAP Help documents generating an OData service for extracting ODP data via SAP Gateway Service Builder. The page body rendered as a JavaScript shell in raw fetch, so the report uses the official URL and search extraction as documentation evidence. | official explicit, retrieval caveat | ODP-OData alternative | 2026-06-02 |
| SAP Help - Define Data Model for the Service | SAP Help | Web search/open of `help.sap.com/docs/SAP_BW4HANA/.../603db87a1eb34974a473da8f8de7cda3.html` | SAP Help documents defining the data model for an ODP OData service, including selecting ODP context and ODPs for extraction. The page body rendered dynamically in raw fetch. | official explicit, retrieval caveat | ODP-OData alternative / Documented Use | 2026-06-02 |
| SAP released-object data | Released-object tool | `sap_search_objects(query="RODPS_REPL", system_type="private_cloud/on_premise", clean_core_level="D")`; `sap_search_objects(app_component="BC-BW-ODP", ...)`; `sap_get_object_details(CLAS, CL_RODPS_REPLICATION, ...)` | Public release-state lookup found no matching released-object entries for the ODP-RFC implementation family or BC-BW-ODP component. A broader `ODP` search returned unrelated released objects but no publication signal for ODP-RFC. | tooling signal / gap | Released-object status | 2026-06-02 |
| SAP Discovery Center search | SAP Docs Discovery Center | `sap_discovery_center_search(query="SAP Business Data Cloud Connect Snowflake")`; `sap_discovery_center_search(query="SAP Business Data Cloud")` | Discovery Center did not return a BDC Connect for Snowflake service entry; broader BDC search surfaced related SAP Datasphere/HANA Cloud services. | tooling signal / gap | Alternative-path discovery | 2026-06-02 |

## Policy analysis

### Published API / Documented Use

The proposed mechanism is ODP-RFC, not ODP-OData, BDC Connect, SLT, analytical CDS/OData V4, or another documented bulk access path. The controlling evidence is SAP Note 3255746, which addresses ODP-RFC directly and names SAP BW/4HANA. The exact API Hub searches for `ODP-RFC` and `RODPS_REPL` returned no published artifact. Under SAP API Policy section 1.1/1.2 and FAQ Q23, an interface is not treated as Published merely because it exists technically or has been historically callable.

The third-party ETL tool does not make the access pattern better or worse by itself. FAQ Q14 and Q32 frame the relevant question as the SAP-facing API surface and usage pattern. A third-party tool consuming Published APIs within documented controls can be aligned; a third-party tool using ODP-RFC for BW/4HANA extraction is not aligned because SAP has separately classified that mechanism as unpermitted for customer/third-party access.

### Specific API Controls (rate/quota/deprecation/ingress-egress/bulk/security)

ODP-RFC has a specific control/prohibition, not just an unknown quota. SAP Note 3255746 states the interface is restricted to its intended SAP-to-SAP use and points customers to alternatives. SAP Note 3439624 adds an operational control layer: self-assessment reporting for ODP-RFC calls and technical validation/blocking of unpermitted calls. That means this is not merely a "no API Hub listing" uncertainty; it is an explicitly controlled interface.

If the customer migrates to ODP-OData, SLT, analytical CDS/OData V4, or BDC/Snowflake, the controls must be assessed on that new path: extraction objects, volumes, delta handling, quotas, licensing, identity, authorizations, and support-pack prerequisites.

### General Controls (competitive analysis / out-of-scope use / system risk)

No competitive-analysis use was stated. The main General-Control issue is systematic data extraction/replication through a path SAP has not endorsed for this consumer class. API Policy section 2.2.2 and FAQ Q38 distinguish bounded operational APIs from analytical/replication surfaces designed for bulk movement. Nightly extraction into Snowflake is a recurring replication pattern, so it belongs on a documented data-access pathway rather than on ODP-RFC.

SAP also prohibits bypassing controls through intermediary services or gateways. Using a third-party ETL tool to call ODP-RFC would not neutralize the ODP-RFC prohibition; it is exactly the kind of customer/third-party access that Note 3255746 covers.

### Large-scale data / replication

This scenario is large-scale or systematic extraction by design: BW/4HANA data is copied nightly into Snowflake. The policy does not say customers can never access their own data, and legal export/data-portability questions remain outside this technical assessment. But the mechanism still matters. FAQ Q38 points customers toward BDC/Delta Sharing, SLT, and analytical CDS/OData V4 for large-scale data access. FAQ Q41 also names BDC/Delta Sharing and ODP-OData as SAP-side data access mechanisms while preserving customer choice of target platform such as Snowflake.

For Snowflake specifically, the Architecture Center now documents SAP Snowflake and BDC Connect for Snowflake. The Road Map Explorer item for BDC Connect for Snowflake is marked delivered in Q2 2026 for AWS and describes the pattern as zero-copy/bidirectional and not customer-managed ETL. That does not retroactively permit ODP-RFC, but it gives a concrete migration direction.

## Red flags

| Red flag | Present? | Evidence |
| --- | --- | --- |
| SAP Note explicitly says the interface is unpermitted/prohibited | Yes | SAP Note 3255746; FAQ Q23/Q24. |
| Interface is not published on API Hub | Yes | Exact API Hub searches for `ODP-RFC` and `RODPS_REPL` returned zero artifacts. |
| Third-party tool uses the interface | Yes | Scenario facts; FAQ Q14 says policy applies regardless of third-party middleware. |
| Systematic/large-scale extraction or replication | Yes | Nightly extraction to Snowflake; API Policy section 2.2.2 and FAQ Q38 apply. |
| Attempt to bypass controls through intermediary tooling | Risk | A third-party ETL connector cannot be used to bypass an ODP-RFC restriction. |
| Customer-specific SAP authorization supplied | No | Missing; would need written SAP confirmation if claimed. |

## Missing information (and what would most improve confidence)

The assessment is high confidence for the stated ODP-RFC path because SAP Note 3255746 is direct and current as retrieved. The facts below would not likely change the ODP-RFC conclusion, but they would help scope remediation:

| Missing fact | Why it matters |
| --- | --- |
| Exact BW/4HANA release/support package | Determines which correction/self-assessment Notes and technical blocking behavior apply. |
| Exact ETL product and connector implementation | Confirms whether it truly uses ODP-RFC or already supports ODP-OData, BDC, SLT, or another documented path. |
| Volume, data domains, delta/full pattern, and retention | Needed to size alternatives and validate bulk controls. |
| Existing SAP support/account-team written authorization | Could override the generic technical assessment if SAP explicitly authorized this customer-specific architecture. |
| Current ODP-RFC usage assessment output from `RODPS_REPL_SUBSCRIBER_ASSESS` | Useful for migration inventory and risk triage; do not share raw business payloads. |

## Questions for SAP / internal governance

1. Does SAP confirm that this customer-specific BW/4HANA to Snowflake scenario must migrate away from ODP-RFC under SAP Note 3255746, and by what date relative to the June 2026 technical blocking update?
2. Which SAP-endorsed path does SAP recommend for this exact data scope: BDC Connect for Snowflake, BW data products via Data Product Generator, ODP-OData, SLT, analytical CDS/OData V4, or another documented interface?
3. If the ETL vendor claims certification or SAP approval, what exact certification scope, interface list, and renewal status apply to the ODP-RFC connector?
4. Are there contractual, legal-export, data-portability, or RISE-specific commitments that affect the migration path or timing? This is outside the technical assessment and should go to SAP account/legal channels.
5. What self-assessment results does SAP expect from SAP Note 3439624 before migration planning, and how should "Unclear" subscriber types be handled?

## Recommended next steps

1. Stop treating the ODP-RFC connector as a production-safe target architecture. If it is already productive, classify it as a migration/remediation item rather than an approved steady-state integration.
2. Implement or verify SAP Note 3439624 in the relevant BW/4HANA system and run `RODPS_REPL_SUBSCRIBER_ASSESS` on a regular basis to identify existing ODP-RFC usage patterns. Keep results aggregated/redacted for governance discussions.
3. Ask the ETL vendor for a written connector bill of materials: exact SAP interfaces used, whether ODP-RFC is used, whether ODP-OData/SLT/BDC are supported, and any SAP certification scope.
4. Engage SAP with the questions above, especially if the business relies on the nightly Snowflake feed.
5. Design a replacement path using one of the documented alternatives below, then assess that replacement separately against the exact data objects, volumes, controls, and licensing.

## Endorsed alternative

The strongest Snowflake-oriented replacement is SAP Business Data Cloud with BDC Connect for Snowflake, where available for the customer's hyperscaler/region. SAP Architecture Center describes this as governed, bidirectional, zero-copy sharing of SAP data products with Snowflake, and SAP Road Map Explorer marks the AWS-based BDC Connect for Snowflake deliverable as delivered in Q2 2026. For BW/4HANA specifically, the Architecture Center describes BW data products and the Data Product Generator path into SAP BDC/Datasphere, including support for selected InfoProvider types and delta loads.

If BDC is not available or not suitable for the scope, assess the alternatives named by SAP for the exact use case:

| Alternative | When to consider | Caveat |
| --- | --- | --- |
| ODP-OData | The business wants ODP-style extraction but through a documented OData service generated in SAP Gateway. | Must validate BW/4HANA release, generated service, ODP context, OData client delta semantics, and volume controls. |
| SLT | Continuous replication is required and the organization has the right SLT product/version/license. | SLT maintenance/version constraints apply; confirm target-system support and SAP Note 3475661 implications. |
| Analytical CDS / OData V4 analytical services | The need is analytical access below full replication, with filtering/aggregation. | Requires published views/services in API Hub/product docs and documented query limits. |
| BDC / BDC Connect for Snowflake | The target is Snowflake and the goal is governed large-scale analytics/AI-ready data. | Availability can depend on region/hyperscaler/product scope; confirm with SAP. |

> **Reminder:** evidence-based technical assessment only - not legal/contractual advice and not a final SAP compliance decision. Confirm the specifics with SAP through the questions above.
