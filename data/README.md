# HeritageGraph Knowledge Graph (Nepal)

A real, production-grade RDF knowledge graph of Nepal's cultural heritage,
populated from **trusted open data sources** and conformant to the
[HeritageGraph ontology](../ontology/HeritageGraph.ttl) and its
[SHACL shapes](../ontology/HeritageGraph.shacl.ttl).

No synthetic data is used. Every entity is derived from a public, verifiable
source and carries machine-readable provenance.

## Contents

| File | Triples | Description |
|------|--------:|-------------|
| `kg/wikidata.ttl`     | ~4,000   | Heritage entities from Wikidata (CC0) |
| `kg/osm.ttl`          | ~114,000 | Physical heritage features from OpenStreetMap (ODbL) |
| `kg/unesco.ttl`       | ~150     | UNESCO World Heritage cultural components |
| `kg/intangible.ttl`   | ~350     | Curated **intangible heritage** (festivals, Guthi, Kumari, deities, castes, rituals) |
| `kg/crosswalk.ttl` + `intangible_crosswalk.ttl` | ~19,700 | `owl:sameAs` / `skos:altLabel` / provenance back-links (not SHACL-validated) |
| `build_stats.json`    | —        | Entity counts per source and per class |

**~7,850 tangible heritage entities** plus a curated **intangible-heritage** layer, across Nepal.

### Intangible heritage (curated layer)

Intangible heritage is not available in bulk open datasets, so `intangible.ttl`
is hand-curated from authoritative, citable sources (Wikidata CC0; UNESCO; and
the scholarship of Slusser, Toffin, Gellner, Locke; NHDP) and cross-linked to
Wikidata QIDs. It covers: festivals & chariot festivals (Indra Jatra, Rato/Seto
Machhindranath, Bisket, Gai Jatra, Ghode Jatra), masked dances (Navadurga,
Lakhe), Guthi institutions (incl. Guthi Sansthan), caste ritual roles
(Vajracharya, Shakya, Jyapu, Gathu, Manandhar), deities and **syncretic
relationships** (Avalokiteshvara ≡ Matsyendranath; Taleju ↔ Kumari), periodic
rituals (Nitya Puja, Kumari daily puja), and the **Living-Goddess (Kumari)
lifecycle** modelled at institutional level (no named minors, for privacy).
Traditional/uncertain dates carry `date_precision = Circa/Century`.

### Entity classes (whole KG)

| Class | Count |
|-------|------:|
| `heritageGraph:ArchitecturalStructure` | 6,769 |
| `heritageGraph:BuddhistMonument`       | 798 |
| `heritageGraph:WaterStructure`         | 141 |
| `heritageGraph:DhungeDhara`            | 115 |
| `heritageGraph:Chaitya`                | 13 |
| `heritageGraph:Stupa`                  | 13 |
| `heritageGraph:Murti`                  | 1 |

Generic temples are typed `ArchitecturalStructure` (their super-class) rather
than `Temple`, because the `Temple` shape *requires* an architectural-style
value from a fixed enum (`Pagoda`/`Shikhara`/…) that is not reliably present in
the sources. Inventing a style would be fabrication, so the nearest fully
satisfiable class is used. `Stupa`→`StupaStyle` and `Chaitya`→`ChaityaStyle`
are definitional and therefore set.

## Sources & licensing (important for redistribution / AWS Open Data)

| Source | License | Implication |
|--------|---------|-------------|
| **Wikidata** | **CC0 1.0** | Public domain. The `wikidata.ttl` graph can be republished with no restriction. |
| **OpenStreetMap** | **ODbL 1.0** | Share-alike + attribution. The `osm.ttl` graph (and any database derived from it) must retain "© OpenStreetMap contributors" and the ODbL. |
| **UNESCO WHC** | Attribution | Factual inscriptions; cite the UNESCO World Heritage Centre. |

The sources are kept in **separate named graphs** so a pure-CC0 core (Wikidata +
the factual UNESCO layer) can be published independently of the ODbL OSM layer.

Named graph IRIs:

```
https://data.cair-nepal.org/heritagegraph/graph/wikidata
https://data.cair-nepal.org/heritagegraph/graph/openstreetmap
https://data.cair-nepal.org/heritagegraph/graph/unesco
https://data.cair-nepal.org/heritagegraph/graph/crosswalk
https://w3id.org/heritagegraph/ontology               (TBox)
```

## Namespaces

- **Schema / TBox** — `https://w3id.org/heritagegraph/` (unchanged, published).
- **Instances / ABox** — `https://data.cair-nepal.org/heritagegraph/id/`
  (entities), `…/place/…`, `…/assertion/…`, `…/source/…`.

## Provenance model

Each entity links to a `heritageGraph:DataSource` (one per source dataset) via
`prov:wasInfluencedBy`, and to a `crminf:I2_Belief` provenance assertion via
`heritageGraph:has_provenance_assertion`. The assertion records
`prov:wasDerivedFrom`, `prov:generatedAtTime`, `heritageGraph:confidence_score`
(Wikidata 0.9, UNESCO 0.95, OSM 0.6) and `heritageGraph:epistemic_stance`
(`Scholarly` / `State` / `Community`). Dated inceptions (Wikidata P571, UNESCO
inscription year) are recorded as `heritageGraph:asserted_value`.

The `owl:sameAs` links to Wikidata QIDs and `rdfs:seeAlso` to OSM elements live
in `crosswalk.ttl` for full verifiability.

## SHACL conformance

`scripts/kg/validate.py` validates the generated core (entities + places +
assertions + sources) against `HeritageGraph.shacl.ttl` and reports
**Conforms: True**.

The shapes are LinkML-generated and `sh:closed`; they are designed for
**exact-type validation** (each node checked against the shape of its declared
`rdf:type`, no subclass inference). Under `inference="rdfs"` the closed,
zero-property `crm:E1_CRM_Entity` shape becomes unsatisfiable for every
instance — the project's own demonstrator ABox yields 51 violations in that
mode. The `asserts_about_entity` back-pointer (whose `sh:class crm:E1_CRM_Entity`
is incompatible with that closed shape) is therefore kept in the unvalidated
`crosswalk.ttl`; the forward `has_provenance_assertion` link is retained in the
validated core.

## Rebuild from scratch

```bash
source venv/bin/activate
bash scripts/kg/build_kg.sh        # extract -> transform -> validate
bash scripts/kg/load_fuseki.sh     # deploy Fuseki (Docker) + load named graphs
python scripts/kg/run_cq.py        # run competency questions against the live KG
```

Requires: Python venv (`rdflib`, `pyshacl`), `curl`, Docker.
Raw extracts are cached under `data/raw/` so transforms can be re-run offline.
