# HeritageGraph Ontology
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Documentation](https://img.shields.io/badge/Documentation-Online-blue.svg)](https://cairnepal.github.io/heritagegraphontology/)

An event-centric OWL ontology for representing (Nepalese) cultural heritage, including tangible and intangible heritage assets, sacred places, rituals, festivals, institutions, communities, and the relationships that connect them.

---

## Overview

HeritageGraph provides a semantic framework for documenting, integrating, and publishing cultural heritage knowledge as Linked Open Data.
 
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


## Repository Structure

```text
.
├── docs/              # Documentation resources
├── evaluation/        # Ontology evaluation artifacts
├── provenance/        # Provenance metadata
├── resources/         # Supporting resources
├── webvowl/           # WebVOWL visualization
├── HeritageGraph.owl  # OWL ontology
├── HeritageGraph.ttl  # Turtle serialization
└── README.md
```

## Documentation

Complete ontology documentation is available at:

**https://cairnepal.github.io/heritagegraphontology/**

The documentation includes:

* Class hierarchy
* Object properties
* Data properties
* Ontology metadata
* Provenance information
* WebVOWL visualization
* Downloadable ontology serializations


## Downloads

The ontology is available in multiple RDF serializations:

* OWL
* Turtle (TTL)
* RDF/XML
* N-Triples
* JSON-LD 

## Example

```turtle
@prefix hg: <https://cairnepal.github.io/heritagegraphontology#> .

:IndraJatra
    a hg:Festival ;
    hg:locatedIn :Kathmandu ;
    hg:organizedBy :Guthi ;
    hg:hasCulturalSignificance "Major annual festival of Kathmandu Valley" .
```


## Citation

If you use HeritageGraph in research, publications, software, or datasets, please cite:

```text
Niraj Karki, Nabin Oli, Anu Sapkota, Semih Yumusak and Tek Raj Chhetri. (2026).
HeritageGraph Ontology (Version 1.0.0).
https://cairnepal.github.io/heritagegraphontology/
```
 
## Contributing

Contributions, bug reports, and enhancement proposals are welcome.

Please open an issue or submit a pull request through GitHub.
 
## License

© 2026 CAIR-Nepal

This ontology is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

You are free to use, share, adapt, and redistribute this ontology for any purpose, including commercial use, provided that appropriate attribution is given and any modifications are clearly indicated.

For full license terms, see the [LICENSE](LICENSE.md) file.


