# HeritageGraph governance and maintenance

## Maintainers

- Niraj Karki (CAIR-Nepal): lead maintainer, releases.
- The HeritageGraph team at CAIR-Nepal reviews changes. The LUX alignment module
  (`heritagegraph-lux-migration/`) is maintained with its author, Semih Yumuşak.

## How the ontology changes

1. **Requests.** Anyone may request a new term, a change or a correction by opening a GitHub
   issue with the *Term request* template: the term, a definition, an example from a
   documented source, the competency question it serves, and any community or access
   considerations.
2. **Review.** A maintainer checks the request against the modelling rules (reuse CIDOC-CRM
   and PROV-O terms where they fit; no axioms on terms HeritageGraph does not own; a class
   is stated a subclass of a CRM class only when every instance is one) and, for knowledge a
   community holds, asks that community before it is modelled or published.
3. **Change.** Every change to the core is made in `ontology/HeritageGraph.yaml` (never in a
   generated file) and regenerated with `make artefacts`. The LUX alignment module is a
   hand-maintained Turtle file, edited directly. Every change must pass `make check`, which
   includes the LUX module's conservativity gate. A change to a
   modelling pattern also gets a SHACL negative test or a competency question.
4. **Independent review.** Each change is reviewed by someone who did not write it before it
   is merged.

## Versioning

Semantic versioning on the ontology (`versionIRI` …/ontology/X.Y.Z):

- **Patch**: corrected labels, definitions or mappings; no change to what data is valid.
- **Minor**: new terms, or constraints that only accept more data; existing valid data stays valid.
- **Major**: a change that makes some previously valid data invalid, or changes a term's meaning.

From 1.1.0 on, each release is tagged, archived with a version DOI, and listed in `CHANGELOG.md`
with its migration notes. (1.0.0 is tagged and archived; 1.0.1 was published without a tag.)

## Deprecation policy

- A published IRI is never deleted or reused. A term that is withdrawn stays in the release as
  `owl:deprecated true`, with `dcterms:isReplacedBy` its replacement where there is one, and an
  editorial note giving the version and the reason. Its label starts with "obsolete" (e.g.
  "obsolete Stupa style"), the ROBOT/OBO convention.
- A deprecated term is kept, in the OWL and (for classes and properties) the JSON-LD context,
  for at least one major version, so data can migrate. The SHACL shapes do not validate deprecated
  container terms. The 1.0.x JSON-LD prefix `heritageGraph:` is kept as an
  alias of `hg:` for the same reason.
- Enumeration values are deprecated the same way (e.g. the ArchitecturalStyle values Stupa and
  Chaitya, replaced by the classes Stupa and Chaitya).
- A change that breaks valid data is listed in `CHANGELOG.md` with a migration rule (for
  1.1.0, under [Unreleased] until it is released: the holder of a Kumari tenure moves from `hg:hadParticipant` to `hg:tenureHolder`;
  an endowment that sustained a tenure sustains the tenure's office).

## Community knowledge and access

Restricted knowledge (e.g. esoteric *agam* practice) and data about identifiable people,
especially children holding ritual office, are recorded only with the consent of the
community concerned, with `hg:accessProtocol` stating the access conditions, and are not
published where the protocol restricts them.
