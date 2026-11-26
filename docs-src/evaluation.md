All figures on this page are produced by one command from a clean checkout of the repository, `make reproduce`, which regenerates every artefact from the LinkML source, checks that the regenerated files equal the released ones, runs every release check, and fails if a figure here or in the paper is stale. The checks are listed in the repository's `Makefile` (`check` target).

## The ontology

| | |
|---|---|
| OWL triples | 4606 |
| Classes (excluding enumerations) | 67 |
| Enumerations | 9 |
| Object / datatype properties | 85 / 28 |
| Classes stated subclasses of a CIDOC-CRM class | 21 |
| Deprecated terms (kept, never deleted) | 55 |
| SHACL shapes | 82 node shapes, 23958 triples |
| Mappings to other vocabularies (SSSOM) | 288 |
| CIDOC-CRM terms reused / HeritageGraph terms linked to CIDOC-CRM | 23 classes, 48 properties / 47 classes, 28 properties |

## Logic

- The ontology is in the OWL 2 DL profile and consistent under HermiT, with no unsatisfiable class.
- With CIDOC-CRM 7.1.3, CRMinf 1.0, CRMsci 2.0 and PROV-O loaded unmodified (each pinned by checksum), the merged graph is consistent, has no unsatisfiable class and no unintended class equivalence, with and without the optional CRM-PROV bridge.
- The core states no axiom about a term of another vocabulary unless that vocabulary states it itself, and gives no external class a HeritageGraph superclass (checked with a negative control).
- Every example data set is consistent with the ontology and with all aligned vocabularies.
- Inconsistency injection: the axioms bite (two embodied deities, a thing that is both a temple and a deity, a structure both destroyed and extant are each inconsistent; the controls are not).

## Competency questions

- **32 of 32** competency questions return exactly their expected answers over the demonstrator data, both as asserted and under OWL 2 RL entailment; a deliberately broken query is detected (negative control).
- By dimension: Institutional/Syncretic 7, Living Goddess 7, Ritual/Festival 12, Structural 6.
- **Inference questions**: 4 questions whose answers grow only with HeritageGraph's axioms: each returns fewer answers over the asserted data and over the external vocabularies alone (each frozen set checked) than with HeritageGraph:

  - IQ1 (6 answers, PASS): Which groups performed which rituals, as a CIDOC-CRM-only client sees them (crm:P14i)?
  - IQ2 (22 answers, PASS): Which PROV activities are recorded, as a PROV-O-only client sees them?
  - IQ3 (4 answers, PASS): Which assertions are recorded about each heritage subject, seen from the subject?
  - IQ4 (8 answers, PASS): Which physical heritage things are located where?

### How much the questions test (mutation analysis)

- 23 of 32 questions have a single expected answer in the demonstrator (one witness); their evidence is thin (see the limitations below).
- Swapping a term for a sibling HeritageGraph term changes the answer in 42 of 42 applicable cases.
- 4 questions depend on a TBox axiom (their answer changes when the axiom is deleted).

### Coverage of the vocabulary

| | terms | used in a question | used in the demonstrator |
|---|---|---|---|
| class | 67 | 15 | 31 |
| enumeration | 9 | 0 | 7 |
| property | 113 | 37 | 69 |

## Data validation (SHACL)

- 6 example data sets each have their expected validation outcome.
- **26 negative tests**, each a single injected error (a missing required value, a value of the wrong class or datatype, a value outside a controlled vocabulary, a time-span ending before it begins, two labels in one language, a misspelt property, a conflicting belief without a rival, ...), are all caught, each by the expected constraint (on the expected property, or on the node for the three node-level rules).
- The shapes are open, so data may use other vocabularies; three SHACL-SPARQL rules check what open shapes cannot (an undeclared or deprecated HeritageGraph property, a conflicting belief without a rival).

## Modelling experiments

- **Tenure** against the CIDOC-CRM role idiom (property of property P14.1) and the Wikidata P39 idiom: the same questions over the same facts, compared on answers and query size.
- **Custodianship and endowment**: an endowment held by a state heritage body that sustains a festival, a hereditary office held under that body's mandate, and a custody chain from a Guthi to the state body, with their questions.
- **Multiple calendars**: Bikram Sambat and Nepal Sambat dates converted to Gregorian bounds with full new-year windows, checked against positive and negative controls.
- **Reuse outside Nepal**: the generic Tenure pattern describes a church office and a museum custody period with no Nepal-specific term, and one query answers both.
- **PROV-O consumer**: queries that use only PROV-O terms traverse every recorded belief to its agent and source, over the data with the HeritageGraph TBox and the optional CRM-PROV bridge (which makes CRM-typed agents PROV agents).

## Known limitations

- The mappings are curated by the authors; independent rater verdicts are being collected (the rating sheet and the agreement script are in `evaluation/rater/`).
- The competency questions were written by the authors; a protocol for held-out questions from external experts is in `evaluation/expert_cq/`.
- The demonstrator is a small curated graph; a large populated graph (the DANAM data set) is built in a separate repository.
- The questions exercise 15 of 67 classes and 37 of 113 properties; most questions retrieve data, and 4 depend on a TBox axiom (the inference questions test the axioms).
- Lunar dates are recorded as text; structured lunar dating and recurring-practice modelling are future work.

