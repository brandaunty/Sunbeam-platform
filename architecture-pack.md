# Sunbeam: Task 1 Architecture Pack

D = 0 | Tier = Small (200,000 meters, 500 feeders) | My feeders = Feeder 0 (urban) | Task 4 incident = Contractor login used to download part of the data lake

**Who and why.** The field revenue officer is a Sunbeam staff member on a phone, assigned to a set of feeders, reporting tampering, bypass and wrong mapping. Every workload below serves one of three decisions: **(A)** which feeders to visit this month, **(B)** is there an outage on a feeder now (within 15 minutes), **(C)** is this estimated bill justified and can this disconnection be reviewed.

## Table 1: Workload inventory

| # | Workload | Load pattern | Data sensitivity | Operated by | Service model | Reason (decision) |
|---|---|---|---|---|---|---|
| 1 | Readings ingest and quality pipeline | Nightly batch plus bursts after network outages | High (readings linked to accounts, pseudonymised) | Sunbeam code on provider platform | PaaS (container, runs on Dokku too) | Bursty, no platform engineer to run VMs (A, B) |
| 2 | Data lake (South Africa) | Steady growth, about 1.4M readings per 30 days in the lab | High, pseudonymised only | Provider | Managed object storage | Durability is not our core skill (A) |
| 3 | Query engine over the lake | Spiky, monthly heavy use | High | Provider | Managed PaaS | Pay per query, no cluster to patch (A, C) |
| 4 | **Re-identification key service** | Tiny, constant | Very high (re-identifies households) | **Sunbeam, Abeokuta** | **IaaS / own server** | Key never leaves our control (C) |
| 5 | Outage alert (loss-of-supply to alert in 15 min) | Event-driven, bursty | Medium (feeder level) | Sunbeam code, provider runtime | FaaS | Pay per event, fits the 15-minute target (B) |
| 6 | Field officer dashboard (phone) | Daytime, low concurrency | Medium to high (own feeders only) | Sunbeam | PaaS (Docker / Dokku) | Same code on two hosts, simple to run (A, C) |
| 7 | Feeder loss prediction model | Monthly batch | Medium (feeder aggregates) | Sunbeam | PaaS batch job | Serves the monthly visit decision (A) |
| 8 | Question-answering assistant | Occasional | Must receive **no** personal data | Provider model API | SaaS / API | Answers from policy and feeder aggregates only (C) |

## Table 2: Shared responsibility, readings pipeline

| Layer | Sunbeam keeps | Provider operates |
|---|---|---|
| Physical, network, hypervisor | n/a | Yes |
| Storage durability and platform patching | Chooses region and retention | Yes |
| Pipeline code and quality rules (units, duplicates, ordering, feeder mapping) | Yes | No |
| Pseudonymisation and the key | Yes (Abeokuta) | Never sees it |
| Identity and access (roles, least privilege, MFA, contractor accounts) | Yes | Provides the tooling |
| Encryption keys for the lake | Yes (customer-managed where offered) | Provides the service |
| Legal basis, NDPA duties, NDPC transfer terms | Yes | Provides contract terms and region information |
| Monitoring and alerting on our data and code | Yes | Platform health |

## Table 3: Responsible-use brief

| Who could be harmed | Where the system must refuse or escalate | First position |
|---|---|---|
| Households with no meter, billed by estimate, who cannot dispute what they cannot see | Never auto-issue or raise an estimated bill without a recorded justification and a NERC-compliant cap. Escalate any bill above the cap to a human. | Estimated billing: capped, justified, and reviewable by the customer. A wrong estimate is a real harm. |
| Poor or rural neighbourhoods if the model sends field teams only to "high-loss" feeders | Do not rank or target individual households. Targeting is at feeder level, with human review. Rural feeders with late or missing data are flagged "low confidence", not "high loss". | Fairness is tested across metered vs estimated customers and urban vs rural feeders (Task 4). |
| Any customer facing disconnection | **Refuse** to build automated disconnection. The system only recommends review. A named human decides and the customer can appeal. | Disconnection: human reviewer plus a documented appeal route. |

**What I refuse to build:** any step that disconnects, or sets a customer's bill, without a human in the loop.

## ADR summary (full text in `decisions.md`)

- **ADR-01:** Readings pipeline on managed PaaS. Quality rules stay in our code. Containerised for portability.
- **ADR-02:** The re-identification key service stays on a server we control in Abeokuta.
