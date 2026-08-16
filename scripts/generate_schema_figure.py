#!/usr/bin/env python3
"""HeritageGraph connected schema diagram: key classes as nodes, real object
properties as labelled edges, module-coloured. Renders SVG -> PDF/PNG."""
from pathlib import Path
import subprocess, html, math
ROOT=Path(__file__).resolve().parents[1]; FIG=ROOT/"tgdk-overleaf"/"figures"
OUT=FIG/"HeritageGraph-Schema"

COL={"tan":("#C5D8F0","#2F5F9A"),"evt":("#F5E6A8","#8A7020"),"act":("#C8E6C0","#2E7D33"),
 "syn":("#F0C8D8","#8A3A5A"),"prov":("#E8D5F0","#6B3A8A"),"per":("#DDF2E3","#4F9A6A"),
 "spt":("#C9E6E3","#2E7D77")}

# id: (cx, cy, module, label, subtitle)
NODES={
 "Assertion":(560,70,"prov","Assertion","crminf:I2_Belief"),
 "DataSource":(300,70,"prov","DataSource","crm:E73"),
 "DocumentationActivity":(70,70,"prov","DocumentationActivity","crm:E7"),
 "Proposition":(770,70,"prov","Proposition","crminf:I4"),
 "AssertionSubject":(1000,70,"prov","AssertionSubject","union · crm:E1"),
 "PhysicalHeritageThing":(170,340,"tan","PhysicalHeritageThing","owl:unionOf · crm:E22"),
 "ArchitecturalStructure":(90,470,"tan","ArchitecturalStructure",""),
 "IconographicObject":(300,470,"tan","IconographicObject",""),
 "Production":(470,250,"evt","Production","crm:E12"),
 "RitualEvent":(690,300,"evt","RitualEvent","broad crm:E7"),
 "TransferOfCustody":(470,410,"evt","TransferOfCustody","crm:E10"),
 "ConditionAssessment":(690,430,"evt","ConditionAssessment","crm:E14"),
 "Guthi":(1180,300,"act","Guthi","crm:E74"),
 "Person":(1180,430,"act","Person","crm:E21"),
 "CasteGroup":(1360,430,"act","CasteGroup","crm:E74"),
 "Deity":(1180,600,"syn","Deity","crm:E28"),
 "ReligiousTradition":(1380,600,"syn","ReligiousTradition",""),
 "SyncreticRelationship":(1180,730,"syn","SyncreticRelationship","crm:E13"),
 "Place":(560,620,"spt","Place","crm:E53"),
 "TimeSpan":(740,620,"spt","TimeSpan","crm:E52"),
 "CalendarSystem":(740,730,"spt","CalendarSystem","BS/NS/CE"),
 "KumariTenure":(940,610,"per","KumariTenure","crm:E4 Period"),
 "KumariSelectionEvent":(820,730,"evt","KumariSelectionEvent",""),
 "KumariRetirementEvent":(1030,730,"evt","KumariRetirementEvent",""),
}
# object-property edges: (from,to,label)
PROP=[
 ("Assertion","DataSource","was_derived_from"),
 ("Assertion","DocumentationActivity","was_generated_by"),
 ("Assertion","Proposition","asserts_proposition"),
 ("Assertion","AssertionSubject","asserts_about"),
 ("Production","PhysicalHeritageThing","produced_object"),
 ("ConditionAssessment","PhysicalHeritageThing","assessed_object"),
 ("PhysicalHeritageThing","RitualEvent","crm:P12i participates_in"),
 ("PhysicalHeritageThing","TransferOfCustody","transferred_object"),
 ("Guthi","RitualEvent","performs_ritual"),
 ("Guthi","Person","has_membership"),
 ("RitualEvent","Place","crm:P7 took_place_at"),
 ("RitualEvent","TimeSpan","crm:P4 has_time-span"),
 ("TimeSpan","CalendarSystem","calendar_system"),
 ("RitualEvent","Deity","invokes_deity"),
 ("Deity","ReligiousTradition","has_religious_tradition"),
 ("SyncreticRelationship","Deity","crm:P140/P141"),
 ("KumariSelectionEvent","KumariTenure","initiated_tenure"),
 ("KumariRetirementEvent","KumariTenure","ended_tenure_of"),
 ("KumariTenure","Deity","embodied_deity"),
 ("KumariTenure","Person","had_participant"),
 ("KumariTenure","Guthi","supported_by_institution"),
]
# subClassOf (hollow triangle) and union (dashed)
SUB=[("KumariSelectionEvent","RitualEvent"),("KumariRetirementEvent","RitualEvent")]
UNI=[("PhysicalHeritageThing","ArchitecturalStructure"),("PhysicalHeritageThing","IconographicObject")]

def wof(l): return max(92,int(len(l)*7.0)+24)
H=40
def esc(s): return html.escape(s,quote=False)
def ept(nid,tw):
    cx,cy,_,lab,_=NODES[nid]; w=wof(lab); dx,dy=tw[0]-cx,tw[1]-cy
    if dx==0 and dy==0: return (cx,cy)
    sx=w/2/abs(dx) if dx else 9e9; sy=(H/2)/abs(dy) if dy else 9e9; s=min(sx,sy)
    return (cx+dx*s,cy+dy*s)

P=['<?xml version="1.0" encoding="UTF-8"?>']
W,Hc=1520,860
P.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Hc}" viewBox="0 0 {W} {Hc}">')
P.append('<defs>'
 '<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7.5" markerHeight="7.5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#555"/></marker>'
 '<marker id="sub" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto"><path d="M0 0 L12 6 L0 12 z" fill="#fff" stroke="#888" stroke-width="1.3"/></marker>'
 '</defs>')
P.append('<rect width="100%" height="100%" fill="#fff"/>')
P.append('<text x="760" y="24" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="14" font-weight="700" fill="#222">HeritageGraph — core classes and properties</text>')

# edges first
for a,b,lab in PROP:
    p=ept(a,NODES[b][:2]); q=ept(b,NODES[a][:2])
    P.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="#555" stroke-width="1.2" marker-end="url(#arr)"/>')
    mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2; ww=len(lab)*4.9+6
    P.append(f'<rect x="{mx-ww/2:.0f}" y="{my-6:.0f}" width="{ww:.0f}" height="12" fill="#fff" fill-opacity="0.92" rx="2"/>')
    P.append(f'<text x="{mx:.0f}" y="{my+3:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="8.2" fill="#444">{esc(lab)}</text>')
for a,b in SUB:
    p=ept(a,NODES[b][:2]); q=ept(b,NODES[a][:2])
    P.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="#999" stroke-width="1" marker-end="url(#sub)"/>')
for a,b in UNI:
    p=ept(a,NODES[b][:2]); q=ept(b,NODES[a][:2])
    P.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="#2F5F9A" stroke-width="1.1" stroke-dasharray="4 3"/>')
# nodes
for nid,(cx,cy,mod,lab,sub) in NODES.items():
    f,s=COL[mod]; w=wof(lab); x=cx-w/2; y=cy-H/2
    emph=' stroke-width="2.2"' if nid in("PhysicalHeritageThing","RitualEvent","Assertion") else ' stroke-width="1.5"'
    P.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{H}" rx="9" fill="{f}" stroke="{s}"{emph}/>')
    if sub:
        P.append(f'<text x="{cx}" y="{cy-2:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="10.5" font-weight="700" fill="#111">{esc(lab)}</text>')
        P.append(f'<text x="{cx}" y="{cy+11:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="8" fill="{s}">{esc(sub)}</text>')
    else:
        P.append(f'<text x="{cx}" y="{cy+3:.0f}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="10.5" font-weight="700" fill="#111">{esc(lab)}</text>')
# legend
ly=Hc-40
items=[("Tangible","tan"),("Events","evt"),("Actors","act"),("Syncretic","syn"),("Spatiotemporal","spt"),("Provenance","prov"),("Period","per")]
P.append('<g font-family="Helvetica,Arial,sans-serif" font-size="10.5" fill="#333">')
for i,(t,m) in enumerate(items):
    ex=50+i*135; f,s=COL[m]
    P.append(f'<rect x="{ex}" y="{ly-9}" width="13" height="13" rx="3" fill="{f}" stroke="{s}"/><text x="{ex+18}" y="{ly+1}">{t}</text>')
P.append(f'<line x1="50" y1="{ly+24}" x2="78" y2="{ly+24}" stroke="#555" stroke-width="1.2" marker-end="url(#arr)"/><text x="84" y="{ly+28}">object property</text>')
P.append(f'<path d="M 250 {ly+30} L 264 {ly+24} L 264 {ly+36} z" fill="#fff" stroke="#888"/><text x="272" y="{ly+28}">rdfs:subClassOf</text>')
P.append(f'<line x1="430" y1="{ly+24}" x2="458" y2="{ly+24}" stroke="#2F5F9A" stroke-width="1.1" stroke-dasharray="4 3"/><text x="464" y="{ly+28}">owl:unionOf</text>')
P.append('</g></svg>')

svg=FIG/"HeritageGraph-Schema.svg"; svg.write_text("\n".join(P)); print("wrote",svg)
for fmt in("pdf","png"):
    subprocess.check_call(["rsvg-convert","-f",fmt,"-o",str(OUT.with_suffix("."+fmt)),str(svg)]); print("wrote",OUT.with_suffix("."+fmt))
