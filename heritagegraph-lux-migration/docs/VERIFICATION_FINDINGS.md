# Deep verification — what I found and fixed

**Date:** May 2026
**Scope:** Cross-checked every class and property mapping in `heritagegraph-lux-alignment.ttl`, `HeritageGraph_LUX_Mapping.xlsx`, and `lux_to_hg_migration.sparql` against the official Linked Art JSON-LD context (`https://linked.art/ns/v1/linked-art.json`) and CIDOC-CRM v7.x.

## Method

1. Fetched the canonical Linked Art JSON-LD context and parsed it programmatically. This file is the source of truth for which short names LUX exposes and which URI each one expands to.
2. Extracted every `la:Xxxx` reference from my TTL with regex; cross-checked each against the canonical mapping.
3. Compared CIDOC-CRM class numbers and property numbers against the official ontology (v7.1.3) for naming and inverse direction.
4. Re-verified TTL parses cleanly with rdflib.

## Critical findings — all fixed

### 1. The `la:` prefix was misused throughout

**Wrong assumption:** I had been writing `la:HumanMadeObject`, `la:Person`, `la:Activity`, etc. as if these were real URIs in Linked Art's namespace.

**Reality:** Linked Art's JSON-LD context maps short names DIRECTLY to `crm:` / `dig:` / `sci:` URIs. Only **seven** classes are genuinely under the `la:` namespace:

```
la:Set, la:Transfer, la:Payment, la:Addition,
la:Removal, la:RightAcquisition, la:DigitalService
```

Everything else expands to a CRM URI. A LUX record with `"type": "HumanMadeObject"` becomes `?obj a crm:E22_Human-Made_Object` — never `la:HumanMadeObject`.

**Fix:** Rewrote the TTL alignment so HG classes map to the actual `crm:Enn` URIs. Reserved `la:` only for `la:Set` (the genuine la: class HG uses). The XLSX column was renamed from "Linked Art (la:) Class" to "LUX alias (JSON-LD)" + "URI in LUX data" so the distinction is clear at a glance.

Affected: 40+ TTL triples, 65 XLSX class rows, 30+ XLSX property rows, 9 SPARQL queries.

### 2. `Encounter` was mapped to the wrong CRM class

**Was:** `la:Encounter → crm:E87_Curation_Activity`

**Should be:** LUX's "Encounter" alias expands to `sci:S19_Encounter_Event` (CRMsci extension), not `crm:E87`. The CRMsci namespace is separate from the core CIDOC-CRM and uses URI `http://www.ics.forth.gr/isl/CRMsci/`.

**Fix:** Added `@prefix sci:` to the TTL, changed `hg:Encounter rdfs:subClassOf sci:S19_Encounter_Event`. Added a separate `hg:CurationActivity rdfs:subClassOf crm:E87_Curation_Activity` for the (genuinely different) curation activity.

### 3. `DigitalObject` namespace prefix was wrong

**Was:** `crmdig:D1_Digital_Object`

**Should be:** `dig:D1_Digital_Object`. Linked Art uses the prefix `dig:` for `http://www.ics.forth.gr/isl/CRMdig/`, not `crmdig:`. Different prefix, same namespace, but the alignment file should match Linked Art's convention so federated queries don't silently miss instances.

**Fix:** Replaced `@prefix crmdig:` with `@prefix dig:` in the TTL and updated all references.

### 4. `LegalConcept` doesn't exist in Linked Art

**Was:** `hg:LegalConcept rdfs:subClassOf la:LegalConcept, crm:E89_Propositional_Object`

**Reality:** There is no `la:LegalConcept`. Linked Art has `la:LegalObject` which expands to `crm:E72_Legal_Object`.

**Fix:** Renamed `hg:LegalConcept` → `hg:LegalObject` and aligned to `crm:E72_Legal_Object`. Updated the migration coverage sheet and SPARQL query.

### 5. `ProvenanceActivity` is not a separate la: class

**Was:** Implied that `la:Provenance_Activity` was a real class.

**Reality:** Not in the JSON-LD context. LUX models provenance as `crm:E7_Activity classified_as` a "provenance" Type concept — there is no separate class.

**Fix:** Kept `hg:ProvenanceActivity` but rooted it as `rdfs:subClassOf crm:E7_Activity` with a comment explaining the Type-classified pattern LUX uses. Migration query #6 catches these via the same E7 union.

### 6. `Concept` is not a la: class

The agent had me writing `skos:closeMatch la:Concept` for `hg:Deity`. There is no `la:Concept` in the JSON-LD context. The closest thing is `crm:E28_Conceptual_Object` (already aligned) or `crm:E55_Type` for typed concepts.

**Fix:** Removed `skos:closeMatch la:Concept` lines.

## Findings I rejected (the verification agent was wrong)

### 1. `Name → crm:E33_E41_Linguistic_Appellation` is correct

The agent claimed `la:Name` doesn't exist and that E33_E41 is "non-standard". Both wrong. The Linked Art JSON-LD context explicitly maps `Name → crm:E33_E41_Linguistic_Appellation`. The Linked Art profile docs (https://linked.art/model/profile/class_analysis/) say:

> "we use only the `Name` mapping of `E33_E41_Linguistic_Appellation` that inherits both Appellation and Linguistic Object. This class should be used in place of E35 Title for consistency."

So my original mapping was correct. Kept as-is.

### 2. `crm:P59i_is_located_on_or_within` label is correct

The agent claimed the label should be `has_on_or_within_it`. Per CIDOC-CRM v7.1.3 RDFS, the official label of P59i is `is located on or within`. Kept as-is.

### 3. `Set → crm:E78` vs `Set → crm:E89`

The agent claimed `la:Set` should be `subClassOf crm:E89_Propositional_Object`. In reality, **`la:Set` is its own la: class with no canonical CRM equivalent** — Linked Art deliberately mints it distinct from both E78 (Curated Holding) and E89. The most defensible alignment is `skos:closeMatch crm:E78_Curated_Holding`.

**Fix:** Used `rdfs:subClassOf la:Set` (genuine la: class) plus `skos:closeMatch crm:E78_Curated_Holding`. Added a separate `hg:CuratedHolding rdfs:subClassOf crm:E78` for genuine curated holdings.

## New classes added during verification

While cross-checking, I identified four LUX classes I had previously missed:

| LUX alias | URI | Why HG needs it |
|---|---|---|
| `Inscription` | `crm:E34_Inscription` | Stone/metal/manuscript inscriptions on temples and artifacts. Highly relevant for HG. |
| `Title` | `crm:E35_Title` | Titled name of a work. |
| `MonetaryAmount` | `crm:E97_Monetary_Amount` | Goes with Currency in Acquisition/Payment activities. |
| `CuratedHolding` | `crm:E78_Curated_Holding` | Distinct from `la:Set`. Formally curated museum holdings. |

These bring the new-class count from 29 to **34** in the latest XLSX.

## Files updated

| File | Change |
|---|---|
| `heritagegraph-lux-alignment.ttl` | Rewrote: 40+ la: → crm: substitutions; added `dig:` and `sci:` prefixes; renamed `LegalConcept` → `LegalObject`; added `Inscription`, `Title`, `MonetaryAmount`, `CuratedHolding`. Now 273 triples, 33 owl:Class, 12 owl:equivalentClass, 88 rdfs:subClassOf, 18 owl:equivalentProperty, 45 rdfs:subPropertyOf. |
| `HeritageGraph_LUX_Mapping.xlsx` | Rebuilt all 5 sheets. Class Mapping (65), Property Mapping (69), HG New Classes (34), LUX → HG Coverage (46), Notes. |
| `lux_to_hg_migration.sparql` | All 9 CONSTRUCT queries now use the actual LUX URIs (crm:E22, crm:E21, sci:S19, dig:D1) instead of la: aliases that don't exist. Sanity-check query updated to scan all 4 LUX namespaces. |
| `build_mapping.py` | Source of truth for the XLSX, fully regenerated with verified data. |

## Self-consistency check (after fixes)

```
Triples in alignment.ttl:           273
owl:Class declarations:              33
owl:equivalentClass:                 12
rdfs:subClassOf:                     88
owl:equivalentProperty:              18
rdfs:subPropertyOf:                  45
Remaining la: URI inconsistencies:    0
TTL parses cleanly with rdflib:    YES
XLSX formula errors:                  0
LUX classes covered:                 46  (was 41)
HG new classes proposed:             34  (was 29)
```

Every `la:` reference in the TTL now resolves to a class that genuinely exists in the Linked Art namespace. Every `crm:` reference matches a real CIDOC-CRM v7.x class/property.
