#!/usr/bin/env python3
"""Generate the HeritageGraph architecture-overview figure (class hierarchy +
union types + key CIDOC-CRM alignments) as an SVG, corrected to the current
ontology. Renders to PDF/PNG via rsvg-convert.

  python3 scripts/generate_overview_figure.py
"""
from pathlib import Path
import subprocess, sys, html

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "tgdk-overleaf" / "figures"
OUT = FIG / "HeritageGraph-Overview"

# ---- module palette (matches the caption colour bands) ----
COL = {
    "tan": ("#C5D8F0", "#2F5F9A"),   # tangible heritage (blue)
    "evt": ("#F5E6A8", "#8A7020"),   # events / rituals (yellow)
    "act": ("#C8E6C0", "#2E7D33"),   # actors / institutions (green)
    "syn": ("#F0C8D8", "#8A3A5A"),   # syncretic / religious (red)
    "prov":("#E8D5F0", "#6B3A8A"),   # provenance (purple)
    "per": ("#DDF2E3", "#4F9A6A"),   # period (pale green)
}

# ---- node metadata: id -> (label, subtitle, module) ----
N = {
 # tangible
 "PhysicalHeritageThing": ("PhysicalHeritageThing", "owl:unionOf", "tan"),
 "HumanMadeObject": ("HumanMadeObject", "crm:E22", "tan"),
 "ArchitecturalStructure": ("ArchitecturalStructure", "", "tan"),
 "ReligiousStructure": ("ReligiousStructure", "", "tan"),
 "RestHouse": ("RestHouse", "", "tan"),
 "WaterStructure": ("WaterStructure", "", "tan"),
 "IconographicObject": ("IconographicObject", "", "tan"),
 "ArchitecturalElement": ("ArchitecturalElement", "crm:E25", "tan"),
 "Temple": ("Temple", "", "tan"), "Stupa": ("Stupa", "", "tan"),
 "Chaitya": ("Chaitya", "", "tan"), "KumariHouse": ("KumariHouse", "", "tan"),
 "Pati": ("Pati", "", "tan"), "Sattal": ("Sattal", "", "tan"),
 "Dharmashala": ("Dharmashala", "", "tan"),
 "DhungeDhara": ("DhungeDhara", "", "tan"), "Pokhari": ("Pokhari", "", "tan"),
 "Murti": ("Murti", "", "tan"), "Paubha": ("Paubha", "", "tan"),
 # events
 "RitualEvent": ("RitualEvent", "broad crm:E7", "evt"),
 "Festival": ("Festival", "", "evt"),
 "ChariotFestival": ("ChariotFestival", "", "evt"),
 "MaskedDance": ("MaskedDance", "", "evt"),
 "RitualAssessment": ("RitualAssessment", "", "evt"),
 "FearlessnessAssessment": ("FearlessnessAssessment", "", "evt"),
 "KumariLifecycleEvent": ("KumariLifecycleEvent", "", "evt"),
 "KumariSelectionEvent": ("KumariSelectionEvent", "", "evt"),
 "KumariEnthronementEvent": ("KumariEnthronementEvent", "", "evt"),
 "KumariRetirementEvent": ("KumariRetirementEvent", "", "evt"),
 "Production": ("Production", "crm:E12", "evt"),
 "Consecration": ("Consecration", "", "evt"),
 "TransferOfCustody": ("TransferOfCustody", "crm:E10", "evt"),
 "ConditionAssessment": ("ConditionAssessment", "crm:E14", "evt"),
 "HistoricalEvent": ("HistoricalEvent", "", "evt"),
 "DestructionEvent": ("DestructionEvent", "", "evt"),
 # actors
 "Actor": ("Actor", "crm:E39", "act"),
 "Guthi": ("Guthi", "crm:E74", "act"), "Person": ("Person", "crm:E21", "act"),
 "CasteGroup": ("CasteGroup", "crm:E74", "act"),
 "DataCustodian": ("DataCustodian", "", "act"),
 # syncretic / religious
 "Deity": ("Deity", "crm:E28", "syn"),
 "ReligiousTradition": ("ReligiousTradition", "", "syn"),
 "SyncreticRelationship": ("SyncreticRelationship", "crm:E13", "syn"),
 # provenance
 "Assertion": ("Assertion", "crminf:I2_Belief", "prov"),
 "AssertionSubject": ("AssertionSubject", "union · crm:E1", "prov"),
 "Proposition": ("Proposition", "crminf:I4", "prov"),
 "DataSource": ("DataSource", "crm:E73", "prov"),
 "FieldSurveyDataset": ("FieldSurveyDataset", "", "prov"),
 "OralHistoryRecording": ("OralHistoryRecording", "", "prov"),
 "ArchivalRecord": ("ArchivalRecord", "", "prov"),
 "InformationObject": ("InformationObject", "", "prov"),
 "DocumentationActivity": ("DocumentationActivity", "crm:E7", "prov"),
 "FieldSurveyActivity": ("FieldSurveyActivity", "", "prov"),
 "OralHistoryInterview": ("OralHistoryInterview", "", "prov"),
 "Verification": ("Verification", "", "prov"),
 # period
 "KumariTenure": ("KumariTenure", "crm:E4 Period", "per"),
}

# ---- subClassOf edges: child -> parent ----
SUB = [
 ("ArchitecturalStructure","HumanMadeObject"),("IconographicObject","HumanMadeObject"),
 ("ReligiousStructure","ArchitecturalStructure"),("RestHouse","ArchitecturalStructure"),
 ("WaterStructure","ArchitecturalStructure"),
 ("Temple","ReligiousStructure"),("Stupa","ReligiousStructure"),
 ("Chaitya","ReligiousStructure"),("KumariHouse","ReligiousStructure"),
 ("Pati","RestHouse"),("Sattal","RestHouse"),("Dharmashala","RestHouse"),
 ("DhungeDhara","WaterStructure"),("Pokhari","WaterStructure"),
 ("Murti","IconographicObject"),("Paubha","IconographicObject"),
 ("Festival","RitualEvent"),("RitualAssessment","RitualEvent"),
 ("KumariLifecycleEvent","RitualEvent"),
 ("ChariotFestival","Festival"),("MaskedDance","Festival"),
 ("FearlessnessAssessment","RitualAssessment"),
 ("KumariSelectionEvent","KumariLifecycleEvent"),
 ("KumariEnthronementEvent","KumariLifecycleEvent"),
 ("KumariRetirementEvent","KumariLifecycleEvent"),
 ("DestructionEvent","HistoricalEvent"),
 ("Guthi","Actor"),("Person","Actor"),("CasteGroup","Actor"),("DataCustodian","Actor"),
 ("FieldSurveyDataset","DataSource"),("OralHistoryRecording","DataSource"),
 ("ArchivalRecord","DataSource"),("InformationObject","DataSource"),
 ("FieldSurveyActivity","DocumentationActivity"),
 ("OralHistoryInterview","DocumentationActivity"),("Verification","DocumentationActivity"),
]

# ---- union edges (dashed): union -> member ----
UNI = [("PhysicalHeritageThing","ArchitecturalStructure"),
       ("PhysicalHeritageThing","IconographicObject"),
       ("PhysicalHeritageThing","ArchitecturalElement")]

# ---- key property edges: LOCAL only (within/between adjacent clusters).
# Long cross-diagram relations are shown in the dedicated pattern figures.
PROP = [
 ("Assertion","DocumentationActivity","prov:wasGeneratedBy"),
 ("Assertion","DataSource","prov:wasDerivedFrom"),
 ("Assertion","AssertionSubject","asserts_about"),
 ("Assertion","Proposition","crminf:J4_that"),
 ("KumariSelectionEvent","KumariTenure","initiated_tenure"),
 ("KumariRetirementEvent","KumariTenure","ended_tenure_of"),
 ("KumariTenure","Deity","embodied_deity"),
 ("SyncreticRelationship","Deity","crm:P140/P141"),
 ("Deity","ReligiousTradition","has_religious_tradition"),
]

# ---------- tidy-tree layout ----------
def tidy(root, children, xgap, ygap):
    pos, leaf = {}, [0]
    def dfs(n, d):
        ch = children.get(n, [])
        if not ch:
            x = leaf[0]*xgap; leaf[0]+=1
        else:
            xs=[dfs(c,d+1) for c in ch]; x=(xs[0]+xs[-1])/2
        pos[n]=[x, d*ygap]; return x
    dfs(root,0); return pos

def child_map(pairs):
    m={}
    for c,p in pairs: m.setdefault(p,[]).append(c)
    return m

CM = child_map(SUB)

def cluster(root, xgap, ygap, ox, oy):
    p = tidy(root, CM, xgap, ygap)
    return {k:[v[0]+ox, v[1]+oy] for k,v in p.items()}

POS = {}
# --- Band 4: tangible tree (bottom, wide) ---
POS.update(cluster("HumanMadeObject", 118, 95, 60, 780))
# --- Band 1: RitualEvent subtree (top-right) ---
POS.update(cluster("RitualEvent", 185, 90, 860, 100))
# --- Band 3: actors tree (center) ---
POS.update(cluster("Actor", 120, 90, 650, 600))
# --- Band 1: provenance (top-left): DataSource + DocumentationActivity trees ---
POS.update(cluster("DataSource", 140, 90, 120, 120))
POS.update(cluster("DocumentationActivity", 150, 90, 120, 290))

# manual placements (singletons / unions / standalone-event row / syncretic / period)
POS.update({
 "Assertion":[220,55], "AssertionSubject":[430,55], "Proposition":[600,55],
 "PhysicalHeritageThing":[320,600], "ArchitecturalElement":[480,600],
 # standalone events row (Band 2)
 "Production":[700,470],"Consecration":[830,470],"TransferOfCustody":[975,470],
 "ConditionAssessment":[1135,470],"HistoricalEvent":[1285,470],"DestructionEvent":[1285,555],
 # period
 "KumariTenure":[1660,470],
 # syncretic / religious (Band 3, right)
 "Deity":[1380,600],"ReligiousTradition":[1600,600],"SyncreticRelationship":[1380,690],
})

# ---------- SVG emission ----------
def wof(label):  # width from label
    return max(96, int(len(label)*7.2)+26)

def esc(s): return html.escape(s, quote=False)

parts=['<?xml version="1.0" encoding="UTF-8"?>']
W,H = 1960, 1180
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
parts.append('<defs>'
 '<marker id="sub" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto"><path d="M0 0 L12 6 L0 12 z" fill="#fff" stroke="#777" stroke-width="1.3"/></marker>'
 '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#555"/></marker>'
 '</defs>')
parts.append(f'<rect width="100%" height="100%" fill="#fff"/>')

Hh = 38
def box(nid):
    cx,cy = POS[nid]; label,sub,mod = N[nid]; fill,stroke = COL[mod]
    w = wof(label); x=cx-w/2; y=cy-Hh/2
    emph = ' stroke-width="2.2"' if nid in ("PhysicalHeritageThing","AssertionSubject") else ' stroke-width="1.4"'
    s=f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{Hh}" rx="9" fill="{fill}" stroke="{stroke}"{emph}/>'
    if sub:
        s+=f'<text x="{cx:.0f}" y="{cy-2:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="10.5" font-weight="700" fill="#111">{esc(label)}</text>'
        s+=f'<text x="{cx:.0f}" y="{cy+10:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="8" fill="{stroke}">{esc(sub)}</text>'
    else:
        s+=f'<text x="{cx:.0f}" y="{cy+3:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="10.5" font-weight="700" fill="#111">{esc(label)}</text>'
    return s

def edge_pt(nid, toward):  # nearest point on box border toward a target point
    cx,cy=POS[nid]; w=wof(N[nid][0]); import math
    dx,dy=toward[0]-cx, toward[1]-cy
    if dx==0 and dy==0: return (cx,cy)
    sx = w/2/abs(dx) if dx else 9e9; sy=(Hh/2)/abs(dy) if dy else 9e9
    s=min(sx,sy); return (cx+dx*s, cy+dy*s)

# subClassOf edges (child bottom -> parent, hollow triangle)
for c,p in SUB:
    if c not in POS or p not in POS: continue
    a=edge_pt(c,POS[p]); b=edge_pt(p,POS[c])
    parts.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#888" stroke-width="1" marker-end="url(#sub)"/>')
# union edges (dashed)
for u,m in UNI:
    if u not in POS or m not in POS: continue
    a=edge_pt(u,POS[m]); b=edge_pt(m,POS[u])
    parts.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#2F5F9A" stroke-width="1.1" stroke-dasharray="4 3"/>')
# property edges (labelled, filled arrow)
for f,t,lab in PROP:
    if f not in POS or t not in POS: continue
    a=edge_pt(f,POS[t]); b=edge_pt(t,POS[f])
    mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    parts.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#555" stroke-width="1" marker-end="url(#arr)"/>')
    ww=len(lab)*4.6+6
    parts.append(f'<rect x="{mx-ww/2:.0f}" y="{my-6:.0f}" width="{ww:.0f}" height="11" fill="#fff" fill-opacity="0.9" rx="2"/>')
    parts.append(f'<text x="{mx:.0f}" y="{my+2:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="7.6" fill="#555">{esc(lab)}</text>')
# nodes on top
for nid in N:
    if nid in POS: parts.append(box(nid))

# legend
lx,ly=40,H-70
items=[("Tangible (CIDOC-aligned)","tan"),("Events / rituals","evt"),("Actors / institutions","act"),
       ("Syncretic / religious","syn"),("Provenance","prov"),("Period","per")]
parts.append(f'<g font-family="Helvetica,Arial,sans-serif" font-size="10.5" fill="#333">')
for i,(t,m) in enumerate(items):
    ex=lx+(i%3)*230; ey=ly+(i//3)*22; f,s=COL[m]
    parts.append(f'<rect x="{ex}" y="{ey-9}" width="13" height="13" rx="3" fill="{f}" stroke="{s}"/><text x="{ex+19}" y="{ey+1}">{t}</text>')
parts.append(f'<line x1="{lx+700}" y1="{ly-4}" x2="{lx+726}" y2="{ly-4}" stroke="#888" stroke-width="1" marker-end="url(#sub)"/><text x="{lx+732}" y="{ly}">rdfs:subClassOf</text>')
parts.append(f'<line x1="{lx+700}" y1="{ly+18}" x2="{lx+726}" y2="{ly+18}" stroke="#2F5F9A" stroke-width="1.1" stroke-dasharray="4 3"/><text x="{lx+732}" y="{ly+22}">owl:unionOf</text>')
parts.append(f'<line x1="{lx+900}" y1="{ly-4}" x2="{lx+926}" y2="{ly-4}" stroke="#555" stroke-width="1" marker-end="url(#arr)"/><text x="{lx+932}" y="{ly}">object property / CRM alignment</text>')
parts.append('</g>')
parts.append('</svg>')

svg = FIG / "HeritageGraph-Overview.svg"
svg.write_text("\n".join(parts))
print("wrote", svg)
for fmt in ("pdf","png"):
    subprocess.check_call(["rsvg-convert","-f",fmt,"-o",str(OUT.with_suffix("."+fmt)),str(svg)])
    print("wrote", OUT.with_suffix("."+fmt))
