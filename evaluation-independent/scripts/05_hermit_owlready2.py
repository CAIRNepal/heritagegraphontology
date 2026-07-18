#!/usr/bin/env python3
"""05: Independent HermiT run via owlready2. Reports consistency and lists
unsatisfiable (inconsistent) classes, i.e. classes equivalent to owl:Nothing.
Run: venv/bin/python3 evaluation-independent/scripts/05_hermit_owlready2.py <java_exe>
"""
import sys, os
import owlready2
from owlready2 import get_ontology, sync_reasoner, default_world

owlready2.JAVA_EXE = sys.argv[1]
print(f"owlready2 {owlready2.VERSION}, JAVA_EXE={owlready2.JAVA_EXE}")

path = os.path.abspath("ontology/HeritageGraph.ttl")
onto = get_ontology(f"file://{path}").load()
print(f"Loaded: {onto.base_iri}")

try:
    with onto:
        sync_reasoner(debug=2)  # HermiT is owlready2's default reasoner
    print("CONSISTENT: True (HermiT completed without OwlReadyInconsistentOntologyError)")
except owlready2.base.OwlReadyInconsistentOntologyError:
    print("CONSISTENT: False (OwlReadyInconsistentOntologyError)")
    sys.exit(0)

unsat = list(default_world.inconsistent_classes())
print(f"UNSATISFIABLE_CLASS_COUNT: {len(unsat)}")
for c in unsat:
    print(f"  UNSAT: {c.iri}")
