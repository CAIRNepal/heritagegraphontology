# HeritageGraph Ontology
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Documentation](https://img.shields.io/badge/Documentation-Online-blue.svg)](https://cairnepal.github.io/heritagegraphontology/)

An event-centric OWL ontology for representing (Nepalese) cultural heritage, including tangible and intangible heritage assets, sacred places, rituals, festivals, institutions, communities, and the relationships that connect them.

This work is part of the [HeritageGraph](https://www.cair-nepal.org/research/projects/heritagegraph-illuminating-cultural-legacies-through-knowledge-graphs/) project at CAIR-Nepal.

---

## Overview

HeritageGraph provides a semantic framework for documenting, integrating, and publishing cultural heritage knowledge as Linked Open Data. It is generated from a [LinkML](https://linkml.io/) source of truth, is logically consistent (DL expressivity *ALCIQ(D)*), and is aligned with CIDOC-CRM 7.2.1, CRMinf, PROV-O, and the Europeana Data Model (EDM).

The ontology supports the representation of:

* Cultural heritage sites and monuments
* Religious and sacred places
* Festivals and rituals
* Cultural events and activities
* Heritage objects and artifacts
* Communities and institutions
* Guthi and traditional organizations
* Historical and cultural relationships
* Provenance and documentation metadata

---

## Repository Structure

```text
.
├── ontology/                        # Source ontology files
│   ├── HeritageGraph.yaml           #   LinkML source of truth
│   ├── HeritageGraph.ttl            #   OWL/Turtle release (core)
│   ├── HeritageGraph.shacl.ttl      #   SHACL validation shapes
│   ├── HeritageGraph-alignment.ttl  #   CIDOC-CRM / PROV-O / Wikidata alignment
│   ├── HeritageGraph-edm.ttl        #   Europeana EDM projection
│   ├── heritagegraph-metadata.ttl   #   VoID dataset description
│   └── lux/                         #   LUX / Linked Art bridge module
│       ├── heritagegraph-lux-alignment.ttl
│       └── HeritageGraph-lux.shacl.ttl
├── docs/                            # Generated documentation site (do not edit)
│   ├── index.html                   #   WIDOCO HTML documentation
│   ├── ontology.{owl,ttl,nt,jsonld} #   RDF serializations
│   ├── context.jsonld               #   JSON-LD @context
│   ├── sections/                    #   Generated HTML sections
│   ├── webvowl/                     #   Interactive visualization
│   └── provenance/                  #   Provenance metadata
├── docs-src/sections/               # Authored HTML sections (survive WIDOCO rebuilds)
│   ├── abstract-en.html
│   ├── introduction-en.html
│   ├── description-en.html
│   └── references-en.html
├── evaluation/                      # Evaluation scripts and results
│   ├── run_alignment.py
│   ├── run_consistency.py
│   ├── run_cq_validation.py
│   ├── run_metrics.py
│   ├── run_oops.py
│   ├── results/                     #   Generated evaluation reports
│   └── lux/                         #   LUX coverage evaluation
├── examples/                        # Sample instance data
│   ├── kathmandu-mini-abox.ttl
│   ├── kathmandu-conformant.ttl
│   ├── lux-murti-merged.ttl
│   └── queries/abox-cq-samples.rq
├── scripts/                         # Build and tooling scripts
│   ├── build.sh                     #   Generate docs + WebVOWL (= make docs)
│   ├── regenerate_ontology_artifacts.py
│   └── run_release_quality.py
├── release/                         # Release quality reports
│   └── evaluation/
├── registry/
│   └── lov-metadata.ttl             # LOV registry submission metadata
├── w3id/
│   └── heritagegraph/.htaccess      # w3id.org redirect rules
├── CHANGELOG.md
├── CITATION.cff
└── LICENSE.md
```

---

## Documentation

Complete ontology documentation is available at:

**https://cairnepal.github.io/heritagegraphontology/**

The documentation includes:

* Class hierarchy and object/datatype properties
* Ontology metadata and provenance
* WebVOWL interactive visualization
* Downloadable RDF serializations (OWL, Turtle, N-Triples, JSON-LD)

---

## Rebuilding the Documentation

After any change to the core ontology, regenerate the docs:

```bash
make docs        # runs scripts/build.sh → writes ./docs
make preview     # build into /tmp without touching docs/
make webvowl     # build, then serve http://localhost:8000/webvowl/
```

Requires Docker (WIDOCO runs inside the container — no local Java needed).

---

## Regenerate All Artifacts

```bash
pip install -r requirements.txt linkml owlrl
python3 scripts/regenerate_ontology_artifacts.py
python3 scripts/run_release_quality.py
```

---

## Evaluation

```bash
cd evaluation && pip install -r requirements.txt
make -C evaluation all   # or run individual run_*.py scripts
```

Results are written to `evaluation/results/`. A summary is in `release/QUALITY_REPORT.md`.

---

## Example

```turtle
@prefix hg: <https://w3id.org/heritagegraph/> .

:IndraJatra
    a hg:Festival ;
    hg:locatedIn :Kathmandu ;
    hg:organizedBy :Guthi ;
    hg:hasCulturalSignificance "Major annual festival of Kathmandu Valley" .
```

---

## Citation

If you use HeritageGraph in research, publications, software, or datasets, please cite:

```text
Niraj Karki, Nabin Oli, Anu Sapkota, Semih Yumusak and Tek Raj Chhetri. (2026).
HeritageGraph Ontology (Version 1.0.0).
https://cairnepal.github.io/heritagegraphontology/
```

A `CITATION.cff` file is included for automated citation tools (Zenodo, GitHub, etc.).

---

## Contributing

Contributions, bug reports, and enhancement proposals are welcome.

Please open an issue or submit a pull request through GitHub.

---

## License

© 2026 CAIR-Nepal

This ontology is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

You are free to use, share, adapt, and redistribute this ontology for any purpose, including commercial use, provided that appropriate attribution is given and any modifications are clearly indicated.

For full license terms, see the [LICENSE](LICENSE.md) file.
