# Held-out competency questions from external experts (B3)

The 32 competency questions in `examples/queries/cq-abox-32.rq` were written by the ontology's
authors. This folder holds questions and gold answers elicited from experts who did not build the
ontology, so the evaluation is not only against the authors' own questions.

## Protocol

1. **Experts.** Two domain experts (e.g. a Newar ritual specialist or historian, and a heritage
   documentation professional), not authors of HeritageGraph. Record each as `E1`, `E2` in
   `experts.csv` (role, institution, expertise, date, consent to be named: yes/no).
2. **Elicitation.** Each expert reads a one-page scenario (the Kathmandu demonstrator's scope:
   temples and other structures, Guthi endowments and custody, Kumari tenure, rituals and
   calendars, contested claims) and writes the questions they would ask of such a knowledge
   graph, in their own words, before seeing the ontology.
3. **Gold answers.** For each question the expert gives the expected answer, with its source
   (publication, archive record, DANAM entry or their own fieldwork), independently of the
   demonstrator data.
4. **Held out.** The authors may not change the ontology after seeing the questions until each
   question is classified: (a) answerable with the current terms, (b) answerable with data that
   is missing, (c) not expressible. The paper reports the three counts and every (c).
5. Record each question in `held_out_cqs.csv` with its elicitation provenance.

## Files

- `experts.csv`: `expert_id, role, institution, expertise, date, consent_named`
- `held_out_cqs.csv`: one row per question (columns below)

| column | content |
|---|---|
| `cq_id` | `HCQ1`, `HCQ2`, ... |
| `expert_id` | who asked it |
| `question` | verbatim, in the expert's words |
| `language` | language it was asked in (with a translation if not English) |
| `elicited_on` | date |
| `method` | written, interview, workshop |
| `gold_answer` | the expected answer, in words |
| `gold_source` | where the answer comes from |
| `classification` | answerable / missing data / not expressible (filled in afterwards) |
| `sparql_file` | the query written afterwards, if answerable |
| `notes` | |

Restricted knowledge: a question or answer that the expert marks as restricted (e.g. agam
practice) is recorded only as "restricted", not in content, in line with GOVERNANCE.md.
