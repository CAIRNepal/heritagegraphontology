# HeritageGraph Ontology

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](CHANGELOG.md)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23435676.svg)](https://doi.org/10.5281/zenodo.23435676)
[![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://cairnepal.github.io/heritagegraphontology/)

HeritageGraph is an OWL 2 DL ontology for **living heritage**: heritage whose significance
lies in recurring ritual practice, contested religious identities, time-bounded sacred
roles, and the institutions that sustain them. It extends CIDOC-CRM, reuses PROV-O and
CRMinf for the provenance of claims, and is developed with the Kathmandu Valley, Nepal,
as its case study.

HeritageGraph is part of the [HeritageGraph project](https://www.cair-nepal.org/research/projects/heritagegraph-illuminating-cultural-legacies-through-knowledge-graphs/)
at the Center for Artificial Intelligence Research Nepal (CAIR-Nepal).

## Identifiers and downloads

| | |
|---|---|
| Namespace | `https://cair-nepal.org/heritagegraph/` (prefix `hg:`) |
| Ontology IRI | `https://cair-nepal.org/heritagegraph/ontology` |
| Version IRI | `https://cair-nepal.org/heritagegraph/ontology/1.0.1` |
| Ontology | [`ontology/HeritageGraph.ttl`](ontology/HeritageGraph.ttl) (Turtle; RDF/XML and JSON-LD in the [documentation](https://cairnepal.github.io/heritagegraphontology/)) |
| SHACL shapes | [`ontology/HeritageGraph.shacl.ttl`](ontology/HeritageGraph.shacl.ttl) |
| JSON Schema | [`ontology/HeritageGraph.schema.json`](ontology/HeritageGraph.schema.json) |
| LinkML source | [`ontology/HeritageGraph.yaml`](ontology/HeritageGraph.yaml) |
| Linked Art alignment | [`heritagegraph-lux-migration/`](heritagegraph-lux-migration/) |
| Archived releases | Zenodo, [doi:10.5281/zenodo.23435676](https://doi.org/10.5281/zenodo.23435676) (all versions) |

## At a glance (v1.0.1)

| | |
|---|---|
| Classes | 66 |
| Object / datatype properties | 102 / 32 |
| Controlled vocabularies | 7 enumerations, 51 values |
| Expressivity | OWL 2 DL, $\mathcal{ALCHOIN(D)}$; consistent under HermiT, no unsatisfiable classes |
| Validation | 75 SHACL node shapes |
| Alignment | 42 classes and 25 properties mapped to 11 external vocabularies |
| Competency questions | 32, each answered by a SPARQL query over the demonstrator data |

## Modelling patterns

HeritageGraph is organised around four design patterns and a shared provenance layer.

1. **Event-mediated tangible heritage.** Condition, custody, consecration and existence
   change through typed events (`crm:E12_Production`, `crm:E14_Condition_Assessment`,
   `hg:Consecration`, …) instead of being stored as fixed attributes of an object.
2. **Living Goddess lifecycle.** The Kumari's tenure is a node of its own
   (`hg:KumariTenure`), bounded by selection, enthronement and retirement events, so the
   girl and the deity she embodies remain distinct.
3. **Syncretic relationships.** A cross-tradition identification of deities is a typed,
   sourced `hg:SyncreticRelationship`, not an `owl:sameAs` link that would merge them.
4. **Institutional infrastructure.** Guthi trusts are typed custodial actors that keep
   structures, perform rituals and support sacred offices.

**Provenance layer.** Each contestable claim is a `crminf:I2_Belief` (a PROV-O entity)
with its subject, source, agent, confidence and revision history, so conflicting
claims coexist. Dates can be recorded in the Gregorian, Bikram Sambat and Nepal Sambat
calendars.

## Reused vocabularies

| Prefix | Namespace | Used for |
|---|---|---|
| `crm:` | `http://www.cidoc-crm.org/cidoc-crm/` | Events, objects, actors, places, time-spans (CIDOC-CRM 7.1.3) |
| `crminf:` | `http://www.cidoc-crm.org/extensions/crminf/` | Beliefs and propositions |
| `crmsci:` | `http://www.cidoc-crm.org/extensions/crmsci/` | Observation (field surveys) |
| `prov:` | `http://www.w3.org/ns/prov#` | Derivation, attribution, revision |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Enumerations and mappings |
| `time:` | `http://www.w3.org/2006/time#` | Temporal alignment |
| `geo:` | `http://www.opengis.net/ont/geosparql#` | Coordinates |
| `aat:` | `http://vocab.getty.edu/aat/` | Getty AAT mappings |
| `wd:` | `http://www.wikidata.org/entity/` | Identity links in example data |

Logical alignment uses `rdfs:subClassOf` and `rdfs:subPropertyOf` where inheritance is
intended, and SKOS mapping properties otherwise. HeritageGraph asserts no axioms that
change the meaning of the vocabularies it reuses; a release check enforces this.

## Controlled vocabularies

| Enumeration | Values |
|---|---|
| `ConditionType` | Good, Damaged, Ruined, Restored |
| `ExistenceStatus` | Extant, PartiallyExtant, Destroyed, Lost, Hypothetical, Unknown |
| `DatePrecision` | Exact, Year, Decade, Century, Circa |
| `SyncreticType` | Equivalence, Appropriation, Fusion, Historical |
| `ArchitecturalStyle` | Pagoda, Shikhara, Dome, Chaitya, Stupa |
| `GuthiType` | SiGuthi, JatraGuthi, PujaGuthi, TempleGuthi, NashaGuthi, SanaGuthi, SanGuthi, RajGuthi |
| `RitualType` | 19 values, e.g. NityaPuja, Homa, Jatra, ChariotProcession, InstallationRitual |

Each value has its own IRI, e.g.
`https://cair-nepal.org/heritagegraph/ConditionType#Damaged`.

## Example

A temple, its production, and a condition assessment after the 2015 earthquake:

```turtle
@prefix hg:  <https://cair-nepal.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix ex:  <https://cair-nepal.org/heritagegraph/example/> .

ex:Kasthamandap a hg:Temple ;
    hg:hasArchitecturalStyle <https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda> ;
    crm:P34i_was_assessed_by ex:CA_2015 .

ex:Prod_Kasthamandap a crm:E12_Production ;
    crm:P108_has_produced ex:Kasthamandap ;
    crm:P14_carried_out_by ex:LicchaviBuilders .

ex:CA_2015 a crm:E14_Condition_Assessment ;
    crm:P35_has_identified ex:CS_Damaged .

ex:CS_Damaged a crm:E3_Condition_State ;
    hg:hasConditionType <https://cair-nepal.org/heritagegraph/ConditionType#Damaged> .
```

Reconstructing a Kumari tenure from its lifecycle events:

```sparql
PREFIX hg: <https://cair-nepal.org/heritagegraph/>

SELECT ?tenure ?selection ?enthronement ?retirement WHERE {
  ?tenure a hg:KumariTenure .
  OPTIONAL { ?tenure hg:selectedThrough  ?selection . }
  OPTIONAL { ?tenure hg:enthronedThrough ?enthronement . }
  OPTIONAL { ?tenure hg:retiredThrough   ?retirement . }
}
```

All 32 competency queries are in [`examples/queries/cq-abox-32.rq`](examples/queries/cq-abox-32.rq),
and the demonstrator data in [`examples/kathmandu-mini-abox.ttl`](examples/kathmandu-mini-abox.ttl).

## Repository structure

```text
ontology/                     LinkML source and generated OWL, SHACL and JSON Schema
examples/                     Demonstrator data and the 32 competency queries
evaluation/                   Evaluation scripts and results (see evaluation/README.md)
heritagegraph-lux-migration/  Linked Art alignment module and Yale LUX migration tooling
docs/                         Generated documentation (WIDOCO, WebVOWL)
deploy/nginx/                 Content-negotiation configuration for cair-nepal.org
scripts/                      Build pipeline
```

## Building and evaluation

The LinkML file `ontology/HeritageGraph.yaml` is the single source; all other artefacts
are generated from it and should not be edited by hand.

```bash
pip install -r requirements.txt -r evaluation/requirements.txt
make artefacts   # regenerate OWL, SHACL and JSON Schema from the LinkML source
make check       # release checks: source/artefact sync, declared terms, OWL 2 DL and
                 # HermiT consistency with every example, no changes to reused vocabularies
make docs        # regenerate the documentation (requires Docker)
```

The evaluation reported in the accompanying paper (competency questions, SHACL tests,
pattern ablations, mapping audit, reasoning checks) is reproduced with:

```bash
cd evaluation && make all
```

## Citation

```bibtex
@software{heritagegraph_2026,
  author    = {Karki, Niraj and Oli, Nabin and Sapkota, Anu and Yumusak, Semih and Chhetri, Tek Raj},
  title     = {{HeritageGraph Ontology}},
  version   = {1.0.1},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23435676},
  url       = {https://doi.org/10.5281/zenodo.23435676}
}
```

## License

The ontology and its documentation are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); see [LICENSE.md](LICENSE.md).
The LUX migration tooling in `heritagegraph-lux-migration/` is licensed under Apache 2.0.
Contributions are welcome through issues and pull requests; please edit the LinkML source,
not the generated files.
