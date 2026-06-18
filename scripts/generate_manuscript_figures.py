#!/usr/bin/env python3
"""Generate publication-quality figures for HeritageGraph manuscript."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# Nature-style palette
C = {
    "tangible": "#4C72B0",
    "event": "#DD8452",
    "prov": "#8172B2",
    "sync": "#C44E52",
    "inst": "#55A868",
    "neutral": "#4C4C4C",
    "light": "#F0F0F0",
}


def save(fig, name: str) -> None:
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Wrote {name}.pdf/.png")


def box(ax, xy, w, h, text, color, fs=9):
    p = FancyBboxPatch(
        xy, w, h, boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2, edgecolor=color, facecolor=color + "22", transform=ax.transAxes,
    )
    ax.add_patch(p)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha="center", va="center",
            fontsize=fs, transform=ax.transAxes, wrap=True)


def arrow(ax, start, end):
    ax.annotate("", xy=end, xytext=start,
                xycoords="axes fraction", textcoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", lw=1.4, color=C["neutral"]))


def fig_methodology():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    phases = [
        (0.05, 0.55, "Phase 1\nRequirements\n& CQs", C["neutral"]),
        (0.28, 0.55, "Phase 2\nConceptualisation\n& ODPs", C["event"]),
        (0.51, 0.55, "Phase 3\nReuse &\nCRM Alignment", C["tangible"]),
        (0.74, 0.55, "Phase 4\nLinkML → OWL\n& Validation", C["prov"]),
    ]
    for x, y, t, col in phases:
        box(ax, (x, y), 0.2, 0.28, t, col, fs=8)
    for i in range(3):
        arrow(ax, (phases[i][0] + 0.2, 0.69), (phases[i + 1][0], 0.69))
    box(ax, (0.2, 0.12), 0.6, 0.22,
        "Iterative refinement loop: CQ TBox ASK (32/32) · OWL-RL · HermiT · OOPS! · SHACL · ABox SPARQL",
        C["inst"], fs=8)
    for x in (0.15, 0.4, 0.65):
        arrow(ax, (x, 0.55), (x, 0.34))
    ax.set_title("HeritageGraph ontology engineering workflow (NeOn-informed)", fontsize=11, fontweight="bold", pad=12)
    save(fig, "fig01_methodology")


def fig_architecture():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    layers = [
        (0.05, 0.72, 0.9, 0.18, "Tangible layer\nArchitecturalStructure · IconographicObject · ArchitecturalElement\n(extends crm:E22, E25)", C["tangible"]),
        (0.05, 0.48, 0.9, 0.18, "Event layer\nProduction · RitualEvent · TransferOfCustody · Consecration · Enshrinement\n(extends crm:E7, E10, E12, E14)", C["event"]),
        (0.05, 0.24, 0.42, 0.18, "Provenance layer\nHeritageAssertion · DataSource · DocumentationActivity\n(crminf:I2_Belief + PROV-O)", C["prov"]),
        (0.53, 0.24, 0.42, 0.18, "Syncretic & religious\nSyncreticRelationship · Deity · ReligiousTradition\n(crm:E13, E28)", C["sync"]),
        (0.05, 0.02, 0.9, 0.16, "Institutional layer\nGuthi · CasteGroup · LivingGoddessTenure (crm:E4, E74)", C["inst"]),
    ]
    for x, y, w, h, t, col in layers:
        box(ax, (x, y), w, h, t, col, fs=7.5)
    ax.set_title("HeritageGraph modular architecture", fontsize=11, fontweight="bold")
    save(fig, "fig02_architecture")


def fig_cq_pipeline():
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    steps = ["Stakeholder\nelicitation", "32 CQs\n(4 dimensions)", "SPARQL\ntemplates", "TBox ASK\nschema tests", "ABox SELECT\ninstance demos"]
    xs = [0.02, 0.22, 0.42, 0.62, 0.82]
    for x, t in zip(xs, steps):
        box(ax, (x, 0.35), 0.16, 0.35, t, C["tangible"], fs=8)
    for i in range(4):
        arrow(ax, (xs[i] + 0.16, 0.52), (xs[i + 1], 0.52))
    ax.text(0.5, 0.12, "Traceability matrix links each CQ to required classes and properties",
            ha="center", fontsize=8, style="italic")
    ax.set_title("Competency-question validation pipeline", fontsize=11, fontweight="bold")
    save(fig, "fig03_cq_pipeline")


def fig_event_pattern():
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.5, 2.5), 2, 1.2, boxstyle="round", fc=C["tangible"] + "33", ec=C["tangible"], lw=1.5))
    ax.text(1.5, 3.1, "PhysicalHeritageThing\n(Temple, Murti, …)", ha="center", va="center", fontsize=9)
    events = [(4, 4.2, "Production"), (4, 2.8, "Consecration"), (4, 1.4, "ConditionAssessment")]
    for x, y, label in events:
        ax.add_patch(FancyBboxPatch((x, y), 2.2, 0.9, boxstyle="round", fc=C["event"] + "33", ec=C["event"], lw=1.5))
        ax.text(x + 1.1, y + 0.45, label, ha="center", va="center", fontsize=9)
        ax.annotate("", xy=(x, y + 0.45), xytext=(2.5, 3.1),
                    arrowprops=dict(arrowstyle="-|>", color=C["neutral"], lw=1.2))
    ax.text(7.5, 3.1, "Historically contingent\nproperties mediated\nby typed events", ha="center", fontsize=9,
            bbox=dict(boxstyle="round", fc=C["light"], ec=C["neutral"]))
    ax.set_title("Event-mediated tangible heritage pattern", fontsize=11, fontweight="bold")
    save(fig, "fig04_event_pattern")


def fig_kumari():
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    nodes = [(1, 2, "LivingGoddess\nSelection"), (4, 2, "LivingGoddess\nTenure\n(crm:E4)"), (7, 2, "LivingGoddess\nRetirement")]
    for x, y, t in nodes:
        ax.add_patch(FancyBboxPatch((x - 0.7, y - 0.5), 1.4, 1, boxstyle="round", fc=C["sync"] + "22", ec=C["sync"], lw=1.5))
        ax.text(x, y, t, ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(3.3, 2), xytext=(1.7, 2), arrowprops=dict(arrowstyle="-|>", lw=1.4))
    ax.annotate("", xy=(6.3, 2), xytext=(4.7, 2), arrowprops=dict(arrowstyle="-|>", lw=1.4))
    ax.text(4, 0.6, "Person ≠ Deity: tenure scopes embodied_deity, residence_structure, had_participant",
            ha="center", fontsize=8, style="italic")
    ax.set_title("Sacred embodiment model (Living Goddess lifecycle)", fontsize=11, fontweight="bold")
    save(fig, "fig05_kumari_lifecycle")


def fig_syncretic():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    for x, label in [(1.5, "Deity A"), (5, "SyncreticRelationship\ncrm:E13"), (8.5, "Deity B")]:
        ax.add_patch(FancyBboxPatch((x - 0.8, 1.5), 1.6, 1, boxstyle="round",
                    fc=C["sync"] + "22" if "Syncretic" not in label else C["prov"] + "22",
                    ec=C["sync"] if "Syncretic" not in label else C["prov"], lw=1.5))
        ax.text(x, 2, label, ha="center", va="center", fontsize=8)
    ax.annotate("", xy=(4.2, 2), xytext=(2.3, 2), arrowprops=dict(arrowstyle="-|>", lw=1.4))
    ax.annotate("", xy=(7.7, 2), xytext=(5.8, 2), arrowprops=dict(arrowstyle="-|>", lw=1.4))
    ax.text(5, 0.5, "No owl:sameAs — provenance via HeritageAssertion + DataSource", ha="center", fontsize=8, style="italic")
    ax.set_title("Uncertainty-preserving syncretic identity model", fontsize=11, fontweight="bold")
    save(fig, "fig06_syncretic")


def fig_provenance():
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")
    chain = ["DataSource", "HeritageAssertion\ncrminf:I2_Belief", "Entity / Event\n(asserts_about)"]
    for i, (x, t) in enumerate([(1, chain[0]), (4, chain[1]), (7.5, chain[2])]):
        ax.add_patch(FancyBboxPatch((x - 0.9, 1), 1.8, 1, boxstyle="round", fc=C["prov"] + "22", ec=C["prov"], lw=1.5))
        ax.text(x, 1.5, t, ha="center", va="center", fontsize=8)
        if i < 2:
            ax.annotate("", xy=(chain_x := [2.9, 5.9][i], 1.5), xytext=(x + 0.9, 1.5),
                        arrowprops=dict(arrowstyle="-|>", lw=1.4))
    ax.text(5, 0.3, "Multi-vocal claims: epistemic_stance · confidence_score · conflicts_with_assertion",
            ha="center", fontsize=8, style="italic")
    ax.set_title("Assertion-level provenance model", fontsize=11, fontweight="bold")
    save(fig, "fig07_provenance")


def fig_custodianship():
    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.8, 1.5), 2, 1.2, boxstyle="round", fc=C["inst"] + "22", ec=C["inst"], lw=1.5))
    ax.text(1.8, 2.1, "Guthi\ncrm:E74_Group", ha="center", va="center", fontsize=9)
    ax.add_patch(FancyBboxPatch((4, 2.2), 2, 0.9, boxstyle="round", fc=C["tangible"] + "22", ec=C["tangible"], lw=1.5))
    ax.text(5, 2.65, "Temple", ha="center", va="center", fontsize=9)
    ax.add_patch(FancyBboxPatch((4, 0.8), 2, 0.9, boxstyle="round", fc=C["event"] + "22", ec=C["event"], lw=1.5))
    ax.text(5, 1.25, "RitualEvent", ha="center", va="center", fontsize=9)
    ax.annotate("holds_custody_of", xy=(4, 2.65), xytext=(2.8, 2.1), fontsize=7,
                arrowprops=dict(arrowstyle="-|>", lw=1.2))
    ax.annotate("performs_ritual", xy=(4, 1.25), xytext=(2.8, 2.0), fontsize=7,
                arrowprops=dict(arrowstyle="-|>", lw=1.2))
    ax.set_title("Institutional custodianship model", fontsize=11, fontweight="bold")
    save(fig, "fig08_custodianship")


def fig_evaluation():
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    dims = [
        "A. Ontology quality\n(HermiT · OWL-RL · OOPS!)",
        "B. CQ coverage\n(32 TBox ASK + 9 ABox SELECT)",
        "C. Standards\n(CRM · SHACL · VoID · EDM)",
        "D. Structural metrics\n(70 classes · 170 props)",
        "E. Comparative\n(CRM · ArCo · EDM · Arches)",
        "F. Expert review\n(planned custodian workshop)",
    ]
    positions = [(0.05, 0.62), (0.37, 0.62), (0.69, 0.62), (0.05, 0.22), (0.37, 0.22), (0.69, 0.22)]
    for i, (t, (col, row)) in enumerate(zip(dims, positions)):
        box(ax, (col, row), 0.28, 0.3, t, list(C.values())[i % 6], fs=7)
    ax.set_title("Multi-dimensional evaluation framework", fontsize=11, fontweight="bold")
    save(fig, "fig09_evaluation")


def fig_cidoc_mapping():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    ax.text(2, 4.2, "HeritageGraph classes", fontsize=10, fontweight="bold", ha="center")
    ax.text(8, 4.2, "CIDOC-CRM / extensions", fontsize=10, fontweight="bold", ha="center")
    pairs = [("Temple", "E22/E24"), ("RitualEvent", "E7_Activity"), ("HeritageAssertion", "crminf:I2_Belief"),
             ("LivingGoddessTenure", "E4_Period"), ("Guthi", "E74_Group")]
    for i, (hg, crm) in enumerate(pairs):
        y = 3.2 - i * 0.55
        ax.add_patch(FancyBboxPatch((0.5, y - 0.18), 3, 0.36, boxstyle="round", fc=C["tangible"] + "18", ec=C["tangible"]))
        ax.text(2, y, hg, ha="center", va="center", fontsize=8)
        ax.add_patch(FancyBboxPatch((6.5, y - 0.18), 3, 0.36, boxstyle="round", fc=C["event"] + "18", ec=C["event"]))
        ax.text(8, y, crm, ha="center", va="center", fontsize=8)
        ax.annotate("", xy=(6.5, y), xytext=(3.5, y), arrowprops=dict(arrowstyle="-|>", lw=1.0))
    ax.set_title("CIDOC-CRM alignment architecture (31 subClassOf axioms)", fontsize=11, fontweight="bold")
    save(fig, "fig10_cidoc_mapping")


def main():
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 10})
    fig_methodology()
    fig_architecture()
    fig_cq_pipeline()
    fig_event_pattern()
    fig_kumari()
    fig_syncretic()
    fig_provenance()
    fig_custodianship()
    fig_evaluation()
    fig_cidoc_mapping()
    print(f"All figures written to {OUT}")


if __name__ == "__main__":
    main()
