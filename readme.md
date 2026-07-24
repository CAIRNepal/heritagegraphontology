# HeritageGraph Ontology

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Documentation](https://img.shields.io/badge/Documentation-Online-blue.svg)](https://cairnepal.github.io/heritagegraphontology/)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)

An **event-centric OWL 2 DL ontology for living-heritage systems**, demonstrated
through the cultural heritage of Nepal's Kathmandu Valley: tangible and
intangible heritage, sacred places, rituals and festivals, hereditary
institutions (Guthi), communities, the living-goddess (Kumari) tradition, and
the source-attributed knowledge claims that connect them.

This work is part of the [HeritageGraph](https://www.cair-nepal.org/research/projects/heritagegraph-illuminating-cultural-legacies-through-knowledge-graphs/)
project at CAIR-Nepal. Persistent base IRI: `https://w3id.org/heritagegraph/`.

---

## Overview

HeritageGraph provides a semantic framework for documenting, integrating, and
publishing cultural-heritage knowledge as Linked Open Data. It is generated from
a single [LinkML](https://linkml.io/) source of truth
(`ontology/HeritageGraph.yaml`), is logically consistent under the HermiT
reasoner, and reuses and aligns with CIDOC-CRM, CRMinf, PROV-O, SKOS, and the
Europeana Data Model (EDM).

**At a glance (v0.1.0):**

| | |
|---|---|
| Classes | **84** (66 newly minted + 18 reused from CIDOC-CRM, CRMinf, PROV-O, SKOS that carry local axioms) |
| Properties | **191** (149 object + 42 datatype) |
| Enumerations | **7** (published as SKOS ConceptSchemes / 51 concepts) |
| Reasoning | Consistent under HermiT; **0** unsatisfiable classes (standalone and merged with CRM/CRMinf/PROV-O) |
| Alignment | SKOS mappings to **12** external vocabularies + an EDM profile |
| Competency questions | **32/32** answered as SPARQL over the demonstrator ABox (expected-vs-actual) |

The ontology covers cultural-heritage sites and monuments, religious and sacred
places, festivals and rituals, cultural events, heritage objects and artefacts,
communities and institutions (Guthi and traditional organizations), historical
relationships, and provenance/documentation metadata.

---

## Modelling patterns

HeritageGraph contributes four reusable design patterns for *living* heritage —
significance that emerges through recurring practice, contested identities,
time-bounded sacred roles, and hereditary custodianship — rather than the static,
custodial framing of most heritage vocabularies:

1. **Event-mediated heritage change.** Contingent characteristics (condition,
   consecration, production) attach to typed CIDOC-CRM events rather than as
   static properties, so *who established a fact, when, and over what time-span*
   is queryable.
2. **Sacred-embodiment lifecycle.** The enduring person is separated from the
   time-bounded divine office (`KumariTenure`), bounded by typed selection,
   enthronement, and retirement events — avoiding the actor-role idiom's
   conflation of person and office.
3. **Provenance-qualified syncretism.** Theological equivalence
   (`SyncreticRelationship`) is modelled as an interpretive assertion with a
   source, *not* as semantic identity (`owl:sameAs`), so distinct traditions
   are not collapsed.
4. **Institutional custodianship.** The hereditary responsibilities of Guthi
   trusts — custody transfer, endowment, ritual obligation — are modelled
   explicitly.

A separate **epistemic layer** (aligned with PROV-O and CRMinf) records who
asserted each interpretation, on what evidence, and with what confidence, so
competing interpretations coexist and can be revised. A **multi-calendar** model
supports Bikram Sambat, Nepal Sambat, and Gregorian dates.

---

## Design principles

1. **Event-centric, not attribute-centric.** A structure is tied to the *events*
   that produced, used, documented, and (sometimes) destroyed it — following
   CIDOC-CRM — rather than carrying flat descriptive attributes.
2. **Emic terminology.** Where an established indigenous term exists it is the
   class name (`Stupa`, `Chaitya`, `DhungeDhara`, `Kumari`) rather than a generic
   English gloss.
3. **Living heritage.** Class names avoid authorized-heritage-discourse framing
   ("monument") that connotes static, past-tense heritage; the ontology treats
   these systems as ritually active.
4. **Contested knowledge is provenanced, not asserted.** Claims that different
   sources dispute are modelled as source-attributed assertions (CRMinf +
   PROV-O), never baked into class definitions.
5. **Direct PROV-O starting points.** Reusable LinkML mixins (`Entity`,
   `Activity`, `Agent`) carry the corresponding PROV-O class URIs; an individual
   may hold more than one category where appropriate.

---

## Vocabulary reuse and alignment

HeritageGraph reuses established vocabularies wherever possible rather than
minting its own terms:

| Prefix | Namespace | Used for |
|---|---|---|
| `crm:` | `http://www.cidoc-crm.org/cidoc-crm/` | Core event/object/actor backbone (E-classes, P-properties) |
| `crminf:` | `http://www.ics.forth.gr/isl/CRMinf/` | Assertion/belief backbone (I2 Belief, I4 Proposition Set) |
| `crmsci:` | `http://www.cidoc-crm.org/crmsci/` | Scientific observation (field survey) |
| `prov:` | `http://www.w3.org/ns/prov#` | Provenance: agents, activities, derivation, attribution, revision |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Enumerations, mappings, notes |
| `aat:` | `http://vocab.getty.edu/aat/` | Getty AAT concept/type mappings |
| `edm:` | `http://www.europeana.eu/schemas/edm/` | Europeana Data Model profile |
| `schema:` | `https://schema.org/` | Web-facing mappings |
| `wd:` | `http://www.wikidata.org/entity/` | Entity mappings / `owl:sameAs` anchors |

External mappings use `skos:exactMatch` / `closeMatch` / `broadMatch`,
`rdfs:subClassOf`, and `rdfs:subPropertyOf`. There is no normative
CIDOC-CRM↔PROV-O mapping, so PROV alignment is asserted at the project level on
HeritageGraph's own event classes, never as a global axiom on CRM classes.

---

## Enumerations

Published as SKOS ConceptSchemes (meaning-URIs used where declared, e.g.
`Pagoda` → `aat:300004829`; minted `scheme/<Enum>/<value>` IRIs otherwise).

- **ConditionType** — `Good`, `Damaged`, `Ruined`, `Restored`
- **ExistenceStatus** — `Extant`, `PartiallyExtant`, `Destroyed`, `Lost`, `Hypothetical`, `Unknown`
- **DatePrecision** — `Exact`, `Year`, `Decade`, `Century`, `Circa`
- **SyncreticType** — `Equivalence`, `Appropriation`, `Fusion`, `Historical`
- **ArchitecturalStyle** — `Pagoda`, `Shikhara`, `Dome`, `Chaitya`, `Stupa`
- **GuthiType** — `SiGuthi`, `JatraGuthi`, `PujaGuthi`, `TempleGuthi`, `NashaGuthi`, `SanaGuthi`, `SanGuthi`, `RajGuthi`
- **RitualType** — 19 values spanning worship frequency (`NityaPuja`,
  `NaimittikaPuja`, `KamyaPuja`), ritual form (`Homa`, `Yagna`, `Jatra`,
  `MaskedPerformance`, …), and lifecycle (`InstallationRitual`,
  `ReturningRitual`, …)

---

## Repository structure

```text
.
├── ontology/                        # Source ontology + generated release artefacts
│   ├── HeritageGraph.yaml           #   LinkML source of truth (edit here)
│   ├── HeritageGraph.ttl            #   OWL/Turtle release (generated)
│   ├── HeritageGraph.shacl.ttl      #   SHACL validation shapes (generated)
│   ├── HeritageGraph.schema.json    #   JSON Schema (generated)
│   ├── review.owl                   #   Reasoner review artefact
│   └── lux/                         #   Yale LUX / Linked Art bridge module
├── docs/                            # Generated documentation site (WIDOCO; do not edit)
│   └── webvowl/                     #   Interactive visualization
├── docs-src/sections/               # Authored HTML sections (survive WIDOCO rebuilds)
├── examples/                        # Sample instance data
│   ├── kathmandu-mini-abox.ttl      #   Demonstrator ABox (CQ witnesses; cited sources)
│   ├── kathmandu-conformant.ttl
│   ├── abox-conflicting-assertions.ttl
│   ├── lux-murti-merged.ttl
│   └── queries/cq-abox-32.rq        #   32 competency questions as SPARQL
├── evaluation/                      # Reproducible evaluation (see evaluation/README.md)
│   ├── run_abox_cq32.py             #   §7.3 CQ oracle (expected-vs-actual; --entailment mode)
│   ├── pattern_experiments.py       #   §7 pattern baselines/ablations (6 subcommands)
│   ├── mapping_audit.py             #   §7.6 external mapping audit + negative control
│   ├── reasoning_extras.py          #   §7.1 inconsistency injection + merged-vocab classification
│   ├── run_danam_scale_cq.py        #   §7 at-scale CQ run over independent data
│   └── results/                     #   Generated reports
├── data/                            # Independent-data bundle
│   ├── raw/                         #   DANAM source dumps
│   ├── reconciled/                  #   danam-heritagegraph.nq, wikidata-kv.nq (mapped to the ontology)
│   ├── reconcile_store.py           #   DANAM → HeritageGraph vocabulary reconciliation
│   └── enrich_wikidata.py           #   Wikidata enrichment (prov:wasDerivedFrom per statement)
├── deploy/fuseki/                   # Ready-to-deploy read-only public SPARQL endpoint (Fuseki + Caddy)
├── scripts/                         # Build and tooling
│   ├── build.sh                     #   Generate docs + WebVOWL (= make docs)
│   ├── regenerate_ontology_artifacts.py
│   └── run_release_quality.py
├── registry/                        # LOV registry submission metadata
├── release/                         # Release quality reports
├── w3id/                            # w3id.org redirect rules
├── CHANGELOG.md · CITATION.cff · LICENSE.md · requirements.txt
```

---

## Documentation

Complete, browsable documentation (class hierarchy, object/datatype properties,
metadata, WebVOWL visualization, and downloadable RDF serializations) is at:

**https://cairnepal.github.io/heritagegraphontology/**

---

## Building and reproducing

### Rebuild the documentation site

```bash
make docs        # runs scripts/build.sh → writes ./docs
make preview     # build into /tmp without touching docs/
make webvowl     # build, then serve http://localhost:8000/webvowl/
```

Requires Docker (WIDOCO runs inside the container — no local Java needed).

### Regenerate all RDF artefacts from the LinkML source

```bash
pip install -r requirements.txt linkml owlrl
python3 scripts/regenerate_ontology_artifacts.py   # YAML → TTL/SHACL/JSON Schema
python3 scripts/run_release_quality.py             # release quality report
```

### Run the evaluation

```bash
cd evaluation && pip install -r requirements.txt
make all                                   # consistency, OOPS!, CQs, alignment, metrics

python3 run_abox_cq32.py                   # 32 CQs, expected-vs-actual (32/32)
python3 run_abox_cq32.py --entailment      # CQ answers under OWL-RL closure + suite census
python3 pattern_experiments.py all         # the four modelling-pattern baselines/ablations
python3 mapping_audit.py audit             # external mapping audit
python3 reasoning_extras.py all            # inconsistency injection + merged-vocab HermiT
```

Results are written to `evaluation/results/`; see `evaluation/README.md` for the
full script-to-paper-section map.

---

## Example instance data

```turtle
@prefix hg:   <https://w3id.org/heritagegraph/> .
@prefix crm:  <http://www.cidoc-crm.org/cidoc-crm/> .

:IndraJatra
    a hg:Festival ;
    rdfs:label "Indra Jatra" ;
    hg:recurrencePattern "annual (lunar-tithi)" ;
    hg:performsRitual :Procession ;
    hg:hasCulturalSignificance "Major annual festival of the Kathmandu Valley" .
```

## Example queries

Prefixes: `hg: <https://w3id.org/heritagegraph/>`,
`prov: <http://www.w3.org/ns/prov#>`,
`crminf: <http://www.ics.forth.gr/isl/CRMinf/>`.

**Eligibility criteria to become a Kumari** (subclass query, no string parsing):

```sparql
SELECT ?criterion WHERE { ?criterion rdfs:subClassOf hg:SelectionCriterion . }
```

**Latest (non-superseded) assertion about an entity:**

```sparql
SELECT ?a WHERE {
  ?a a crminf:I2_Belief ;
     hg:assertsAbout ?entity .
  FILTER NOT EXISTS { ?newer prov:wasRevisionOf ?a . }
}
```

**Reconstruct a full Kumari lifecycle** (selection → enthronement → retirement):

```sparql
SELECT ?tenure ?selection ?enthronement ?retirement WHERE {
  ?tenure a hg:KumariTenure .
  OPTIONAL { ?tenure hg:selectedThrough  ?selection . }
  OPTIONAL { ?tenure hg:enthronedThrough ?enthronement . }
  OPTIONAL { ?tenure hg:retiredThrough   ?retirement . }
}
```

---

## Data and public SPARQL endpoint

An independent-data bundle accompanies the release so the ontology can be
exercised over real, third-party data mapped to the released vocabulary:

- `data/reconciled/danam-heritagegraph.nq` — ~130k quads reconciled from the
  DANAM / OpenStreetMap pipeline (tangible monuments + provenance);
- `data/reconciled/wikidata-kv.nq` — a Wikidata enrichment of Kathmandu Valley
  heritage, each statement carrying `prov:wasDerivedFrom` its source IRI
  (built by `data/enrich_wikidata.py`).

`deploy/fuseki/` contains a ready-to-deploy configuration (Apache Jena Fuseki
behind a Caddy HTTPS reverse proxy) that serves the graph as a **read-only**
public SPARQL endpoint. See `deploy/fuseki/README.md`.

---

## Citation

If you use HeritageGraph in research, publications, software, or datasets, please
cite:

```text
Niraj Karki, Nabin Oli, Anu Sapkota, Semih Yumusak, and Tek Raj Chhetri (2026).
HeritageGraph Ontology (Version 0.1.0).
https://cairnepal.github.io/heritagegraphontology/
```

A `CITATION.cff` file is included for automated citation tools (Zenodo, GitHub,
etc.).

---

## Contributing

Contributions, bug reports, and enhancement proposals are welcome. Please open an
issue or submit a pull request through GitHub. Edit the LinkML source
(`ontology/HeritageGraph.yaml`) and regenerate artefacts — never hand-edit the
generated `HeritageGraph.ttl`, SHACL, or `docs/`.

---

## License

© 2026 CAIR-Nepal

This ontology is licensed under the **Creative Commons Attribution 4.0
International (CC BY 4.0)**. You are free to use, share, adapt, and redistribute
it for any purpose, including commercial use, provided appropriate attribution is
given and modifications are clearly indicated.

For full license terms, see the [LICENSE](LICENSE.md) file.
