# Sunbeam Electricity Distribution: Architecture Decisions

Student number last digit D: **0**
Scale tier: **Small (200,000 meters, 500 feeders)**
My feeders: **Feeder 0 (Urban)**
Task 4 incident: **Remainder 0: a contractor's login was used to download part of the data lake**

---

## ADR-01: Service model for the readings pipeline

**Status:** Accepted

**Context.** Meters report every 15 minutes. A nightly job copies readings to a data lake in South Africa, runs quality checks (unit conversion, de-duplication, late arrivals, wrong-feeder mapping), and feeds the monthly loss map. The team is three engineers, one of them a data engineer, and no one runs platforms. Load is spiky: a nightly batch plus bursts after mobile network outages. Readings tied to an account are personal data under the NDPA.

**Options considered.**
1. IaaS: VMs we install and patch ourselves (Spark, scheduler, database).
2. PaaS / managed services: provider-run storage, query engine and scheduler; Sunbeam owns the pipeline code and data rules.
3. FaaS only: event-driven functions for every step.
4. SaaS: an off-the-shelf meter-data-management product.

**Decision.** Option 2, PaaS with managed storage and a managed query engine. Pipeline code is containerised so it also runs on Dokku (same code, two hosts).

**Reasons.**
- Nobody on the team can be the platform operator, so patching, scaling and storage durability go to the provider.
- Batch plus bursty load suits pay-per-use managed services.
- Quality rules (units, duplicates, mapping) are Sunbeam's business logic and must stay in our code, which SaaS would hide.
- FaaS suits the outage alert (Task 3), but a 1.4M-row nightly job exceeds function time and memory limits.

**Consequences.**
- Some provider lock-in. Mitigation: open formats (Parquet) and containerised code.
- Dollar billing against naira revenue. The year-2 30% naira fall raises cost by about 43% (1/0.7). This is modelled in Task 2.
- Data leaves Nigeria, so we need NDPC-compliant transfer terms and pseudonymised data only.

---

## ADR-02: The workload kept on infrastructure we control

**Status:** Accepted

**Context.** Customer identities are replaced by codes before upload. The key that maps codes back to customers is the one asset that turns pseudonymous data back into personal data.

**Decision.** The re-identification key service stays on a server in Abeokuta that Sunbeam controls (a VirtualBox VM in the lab estate, a hardened on-premises host in production). It is not moved to any cloud region.

**Reasons.**
- Whoever holds the key can re-identify every household and infer when it is occupied (consumption patterns are sensitive).
- Keeping it local means a lake breach or a provider incident does not expose identities.
- It keeps the NDPA / NDPC cross-border question narrow: only pseudonymised data crosses the border.
- It is small and low-load, so running it ourselves is cheap and does not need a platform engineer.

**Consequences.**
- Sunbeam owns availability, backups and access control for it. Mitigation: two encrypted backups in separate locations, access limited to named roles, every lookup logged.
- Field officers receive only the customers for their own feeders, resolved through this service on demand.
- Single-site risk (power, connectivity in Abeokuta). Mitigation: documented restore runbook, tested in Task 4.
