# Independent evaluation vs. the paper's existing evaluation

My evaluation was written from scratch (`independent-eval/eval_hg.py`), run on
`HeritageGraph.ttl` + `HeritageGraph.shacl.ttl`, with no reference to the repo's
`evaluation/run_*.py` or the manuscript's numbers. Below, "Mine" = my run;
"Paper" = the existing Evaluation section in `main.tex`.

## 1. Where we AGREE exactly (independent confirmation)

| Measure | Mine | Paper | |
|---|---|---|---|
| Asserted triples | 5,049 | 5,049 | ✅ |
| Named classes | 70 | 70 | ✅ |
| Object properties | 123 | 123 | ✅ |
| Datatype properties | 47 | 47 | ✅ |
| Named individuals (enum values) | 64 | 64 | ✅ |
| Enumerations | 9 | 9 | ✅ |
| Named union classes | 3 | 3 | ✅ |
| Max hierarchy depth | 4 | 4 | ✅ |
| Inverse assertions / pairs | 18 / 9 | 18 / 9 | ✅ |
| `owl:disjointWith` axioms | 0 | 0 | ✅ |
| Min/max cardinality restrictions | 273 / 176 | 273 / 176 | ✅ |
| External subClassOf axioms | 31 | 31 | ✅ |
| Classes with label / definition | 70/70, 70/70 | 70/70, 70/70 | ✅ |
| Obj-prop range / dat-prop range | 100/123, 41/47 | 100/123, 41/47 | ✅ |
| OWL-RL closure / inferred | 25,353 / 20,304 | 25,353 / 20,304 | ✅ |
| Unsatisfiable classes | 0 | 0 | ✅ |
| SHACL NodeShapes | 61 | 61 | ✅ |

**Takeaway:** an independent toolchain reproduces every core number. The paper's
structural, reasoning, documentation, disjointness, and SHACL figures are accurate.

## 2. Where we DIFFER (methodology, not error)

### 2a. Alignment / interoperability
| | Classes | Properties | Vocabularies |
|---|---|---|---|
| **Mine** (axiom-based, distinct) | 42 | 73 | 13 |
| **Paper** (YAML `class_uri`/`slot_uri` + TTL, per-namespace) | 68 | 59 | 14 |

The gap is entirely methodological:
- **Classes 42 vs 68.** Mine counts *distinct* HeritageGraph classes that carry an
  alignment. The paper's 68 is the *sum of per-namespace* counts, so a class mapped
  to both CRM and AAT is counted twice. My per-namespace sum is 73; deduplicated, 42.
- **Properties 73 vs 59.** I count `rdfs:subPropertyOf` chains to CRM, which yields
  **62** CRM-aligned properties; the paper's "42 CRM properties" comes only from
  LinkML `slot_uri` mappings and undercounts the subproperty grounding.
- **Vocabularies 13 vs 14.** My axiom-based scan catches **Schema.org** (5 classes)
  that the paper omits, but misses **GeoSPARQL** and **DataCite**, which HeritageGraph
  *reuses directly* (e.g. `geo:asWKT`, `datacite:identifier`) rather than mapping an
  HG term onto them — so they don't appear as alignment axioms on HG terms.

**Recommendation:** state the counting method explicitly in the paper and report
*distinct* counts (42 classes / 73 properties) alongside "14 vocabularies (10 via
alignment axioms, plus GeoSPARQL/DataCite/OWL-Time via direct reuse)". This removes
the only thing a careful reviewer could trip on.

### 2b. Modelling-quality scan
| | Mine | Paper (OOPS!) |
|---|---|---|
| Missing domain | 152 props | P11 = 134 (domain *or* range, combined) |
| Missing range | 29 props | (folded into P11) |
| Sibling groups w/o disjointness | 11 | P10 = 12 |

Same phenomena, different counting granularity (I separate domain from range; OOPS
lumps them; my sibling-grouping differs by one). Both agree these are intentional
(polymorphic relations + SHACL-enforced disjointness), not defects.

### 2c. Functional coverage
| | Mine | Paper |
|---|---|---|
| Competency questions | 15 (my own set), 15/15 schema-level | 32 (4 dims), 32/32 TBox ASK |
| Instance-level demo | **synthetic ABox built in-script; real SPARQL returns a 2-row conflicting-assertion result** | 9-query "mini Kathmandu ABox" — **but the ABox + query files are missing from the repo** |
| SHACL | counts 61 shapes **and runs pySHACL** (constraints confirmed active) | reports 61 shapes; no validation run shown |

**Key advantage of the independent approach:** it has *no missing-file dependency*.
The paper's ABox evaluation cites `examples/kathmandu-mini-abox.ttl`, which is not in
the repo, git history, or the zip — so that result is currently irreproducible. My
script builds its own minimal ABox at runtime and still demonstrates the headline
multi-vocal/conflicting-provenance capability with real query output.

## 3. Net assessment

- The paper's evaluation is **numerically sound** on everything I could recompute.
- The **alignment numbers need a methodology note** (distinct vs per-namespace; axiom
  vs direct reuse) — this is the single substantive fix.
- The paper should either **restore the ABox files** or **adopt the in-script
  synthetic-ABox demonstration** so the instance-level claim is reproducible.
