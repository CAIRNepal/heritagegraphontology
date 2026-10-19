# Changelog

All notable changes to this project will be documented in this file. Format inspired by [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed — synced to HeritageGraph v1.0.0 (October 2026)
- Namespace `https://w3id.org/heritagegraph/` → `https://cair-nepal.org/heritagegraph/` (terms, named graphs, minted instance IRIs); the ontology is fetched from `ontology/HeritageGraph.ttl` on the HeritageGraph branch.
- Every HeritageGraph term in the alignment, queries, migrator templates and mapping workbook resolved to its v1.0.0 IRI: LinkML class → `class_uri`, slot → `slot_uri`, new LUX classes/properties → camelCase. Renames: `LivingGoddessTenure/Selection/Retirement` → `KumariTenure/KumariSelectionEvent/KumariRetirementEvent`, `*Enum` → enumeration names, `AssertableEntity` → `AssertionSubject`, `HeritageAssertion` → `Assertion` (`crminf:I2_Belief`).
- Mappings whose HG property is now the CRM property itself (e.g. `carried_out_by` = `crm:P14_carried_out_by`) are identity, not `owl:equivalentProperty`; no axioms are asserted on external CRM/PROV terms; `Activity`, `Concept`, `HistoricalEvent` are `rdfs:subClassOf` (not `≡`) their CRM class; `Deity ≡ crm:E28`, `CalendarSystem → crm:E29_Designated_Reference_System` (not a CRM class) and enumeration ⊑ `Concept` dropped; `hadParticipant ≡ crm:P11` → `skos:closeMatch`; datatype shortcuts `placeType`, `custodianType`, `sourceCitation` use `rdfs:seeAlso`; `dissolvedBy ⊑ crm:P99i_was_dissolved_by` (the Linked Art IRI).
- Object materials migrate to `crm:P45_consists_of` (LA `made_of`); the reference CONSTRUCTs link imported nodes with `owl:sameAs`, as the production templates do.
- Alignment: 677 triples, 0 `owl:equivalentClass`, 178 `rdfs:subClassOf`, 2 `owl:equivalentProperty`, 52 `rdfs:subPropertyOf`; core + alignment is OWL 2 DL and HermiT-consistent.

### Added
- **`alignment/heritagegraph-lux-alignment.ttl` Section 4** — internal HG hierarchy and 29 new object properties wiring every new class from Section 3 into the existing HG graph. Closes the "orphan nodes" feedback (Niraj, June 2026): before this change the 33 new classes (Birth, Death, Inscription, VisualItem, …) sat only under external CRM/Linked-Art URIs and appeared disconnected in HG-only visualisations. Now each has at least one HG-internal `rdfs:subClassOf` and / or appears in the domain or range of an HG object property.
  * Existence-event hierarchy: `Birth/Formation/Production ⊏ BeginningOfExistence`; `Death/Dissolution/DestructionEvent ⊏ EndOfExistence`.
  * Curation hierarchy: `TransferOfCustody/ConditionAssessment/Modification ⊏ CurationActivity`; `Acquisition/Move ⊏ ProvenanceActivity`.
  * Identification: `Title ⊏ Name`, `Inscription ⊏ LinguisticObject`.
  * Information objects: `DigitalObject/LinguisticObject/PropositionalObject/Metadata/Container ⊏ InformationObject`.
  * 29 new object properties with HG domain → HG range — e.g. `carries_inscription`, `has_dimension`, `has_visual_item`, `has_digital_representation`, `was_born_by`, `died_in_event`, `was_formed_by`, `dissolved_by`, `was_modified_by`, `was_moved_by`, `was_acquired_through`, `was_encountered_in`, `was_measured_by`, `amount_in_currency`, `dimension_has_unit`, `has_language`, `identified_by_identifier/name/title`, `member_of_set`, `holds_item`.
- Total alignment triples: **273 → 438** (+165). HG-internal `subClassOf`: 26 new. HG-internal object properties: 29 new.
- Top-level `README.md`, `LICENSE` (Apache 2.0), `CONTRIBUTING.md`, `CHANGELOG.md`, `.gitignore`.
- GitHub Actions workflows in `.github/workflows/` (TTL parse, Python syntax check, SPARQL syntax check, Docker compose lint).
- Reorganized repo into `alignment/`, `mapping/`, `queries/`, `scripts/`, `docker/`, `docs/`.
- `deploy.sh` lives at repo root and rsyncs the whole repo to `server42`.
- `docker-compose.yml` uses `context: ..` so the Dockerfile reads canonical files from `scripts/`, `alignment/`, `queries/` — no duplication.

## [0.1.0] — 2026-05

Initial pilot release covering the CAIR Nepal request from 8 April 2026.

### Added
- **Alignment** (`alignment/heritagegraph-lux-alignment.ttl`) — 273 OWL triples, 33 new HG class declarations, 12 `owl:equivalentClass`, 88 `rdfs:subClassOf`, 18 `owl:equivalentProperty`, 45 `rdfs:subPropertyOf`. Verified against the official Linked Art JSON-LD context.
- **Mapping** (`mapping/HeritageGraph_LUX_Mapping.xlsx`) — 5 sheets: Class Mapping (65), Property Mapping (69), HG New Classes (34), LUX → HG Coverage (46), Notes.
- **SPARQL** — 9 CONSTRUCT-as-INSERT transformations in `queries/lux_to_hg_migration.sparql`; 8 validation queries in `queries/validation_queries.sparql` (V1/V2 hard gates).
- **Orchestrator** — `scripts/migrate_lux_to_hg.py` with 4 modes (crawl, transform, validate, delta).
- **Docker stack** — `docker/docker-compose.yml` with oxigraph + migrator + delta-syncer; `docker/migrator/Dockerfile` Python 3.12 + supercronic + raptor.
- **Deployment** — `deploy.sh` for rsync-push to `server42`; `scripts/server-bootstrap.sh` for one-time host prep; systemd unit for reboot resilience; logrotate config.
- **Documentation** — `docs/MIGRATION_PLAN.md` (7-phase plan), `docs/DEPLOY_SERVER.md` (server playbook), `docs/LUX_DATA_DOWNLOAD.md` (honest assessment of LUX data acquisition options), `docs/VERIFICATION_FINDINGS.md` (deep verification report).

### Fixed (during verification pass)
- `la:` prefix misuse — Linked Art short names map to `crm:` URIs in JSON-LD; only seven classes are genuinely under `la:` (Set, Transfer, Payment, Addition, Removal, RightAcquisition, DigitalService). All other usages corrected.
- `la:Encounter` → `sci:S19_Encounter_Event` (CRMsci, not `crm:E87_Curation_Activity`).
- `DigitalObject` namespace `dig:` (Linked Art convention), not `crmdig:`.
- `la:LegalConcept` does not exist → renamed `hg:LegalConcept` to `hg:LegalObject` aligned to `crm:E72_Legal_Object`.
- `la:Provenance_Activity` does not exist as a class → modelled as `crm:E7_Activity` classified_as a Provenance Type.
- Removed `skos:closeMatch la:Concept` references (no such class).

### Known issues
- LUX bulk dump URL is not public; default `RING_MODE=crawl` falls back to the REST API. See `docs/LUX_DATA_DOWNLOAD.md` for the five real acquisition paths.
- `HeritageGraph.ttl` is not committed; it is fetched from CAIRNepal upstream by `scripts/server-bootstrap.sh` or manually before `make up`.
