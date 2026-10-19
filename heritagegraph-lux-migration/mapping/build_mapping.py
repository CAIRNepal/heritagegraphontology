"""
Build HeritageGraph <-> LUX (Linked Art / CIDOC-CRM) mapping XLSX.
Output: HeritageGraph_LUX_Mapping.xlsx

Verified against the official Linked Art JSON-LD context
(https://linked.art/ns/v1/linked-art.json) on May 2026.

Important convention (from JSON-LD context):
  - LUX records use SHORT NAMES like "HumanMadeObject", "Person", "Activity"
    in their @type fields. Those short names expand to crm:Enn_* URIs after
    JSON-LD parsing — NOT to la:Xxx URIs.
  - Only seven classes are genuinely under the la: namespace:
        Set, Transfer, Payment, Addition, Removal,
        RightAcquisition, DigitalService.
  - Therefore the alignment binds HG classes to crm:Enn (with dig:/sci: where
    appropriate) and reserves la: for those seven classes.
"""

import os

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Always write next to this script so `python mapping/build_mapping.py`
# regenerates mapping/HeritageGraph_LUX_Mapping.xlsx regardless of CWD
# (the previous hard-coded sandbox path broke CI's regenerate-and-diff job).
OUT_XLSX = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "HeritageGraph_LUX_Mapping.xlsx")

# ---------------- Class mapping ----------------
# Cols: HG_Class | HG_Parent | LUX alias (JSON-LD) | URI in LUX data | Mapping_Type | Notes
CLASS_ROWS = [
    # ---- Top entities that map exactly ----
    ("HumanMadeObject",            "(none)",                       "HumanMadeObject",   "crm:E22_Human-Made_Object",       "identity (direct URI reuse)", "alpha5 (July 2026): hg:HumanMadeObject retired, crm:E22 is now the class itself — no wrapper."),
    ("Person",                     "(none)",                       "Person",            "crm:E21_Person",                  "identity (direct URI reuse)", "alpha5 (July 2026): hg:Person retired, crm:E21 is now the class itself — no wrapper."),
    ("Actor",                      "(none)",                       "Actor",             "crm:E39_Actor",                   "identity (direct URI reuse)", "Generic actor (Person OR Group). alpha5 (July 2026): hg:Actor retired, crm:E39 is now the class itself."),
    ("Place",                      "(none)",                       "Place",             "crm:E53_Place",                   "identity (direct URI reuse)", "alpha5 (July 2026): hg:Place retired, crm:E53 is now the class itself."),
    ("TimeSpan",                   "(none)",                       "TimeSpan",          "crm:E52_Time-Span",               "identity (direct URI reuse)", "alpha5 (July 2026): hg:TimeSpan retired, crm:E52 is now the class itself."),
    ("Material",                   "(none)",                       "Material",          "crm:E57_Material",                "identity (direct URI reuse)", "alpha5 (July 2026): hg:Material retired, crm:E57 is now the class itself."),
    ("Production",                 "(none)",                       "Production",        "crm:E12_Production",              "identity (direct URI reuse)", "alpha5 (July 2026): hg:Production retired, crm:E12 is now the class itself."),
    ("DestructionEvent",           "HistoricalEvent",              "Destruction",       "crm:E6_Destruction",              "identity (direct URI reuse)", "alpha5 (July 2026): hg:DestructionEvent retired, crm:E6 is now the class itself (still subClassOf hg:EndOfExistence in alignment §5)."),
    ("TransferOfCustody",          "(none)",                       "TransferOfCustody", "crm:E10_Transfer_of_Custody",     "identity (direct URI reuse)", "alpha5 (July 2026): hg:TransferOfCustody retired, crm:E10 is now the class itself."),
    ("HistoricalEvent",            "(none)",                       "Event",             "crm:E5_Event",                    "equivalentClass", ""),
    ("ConditionState",             "(none)",                       "ConditionState",    "crm:E3_Condition_State",          "identity (direct URI reuse)", "alpha5 (July 2026): hg:ConditionState retired, crm:E3 is now the class itself."),
    ("Deity",                      "(none)",                       "ConceptualObject",  "crm:E28_Conceptual_Object",       "equivalentClass", "Already exactMatch crm:E28 in HG."),
    ("ConditionAssessment",        "(none)",                       "ConditionAssessment","crm:E14_Condition_Assessment",   "identity (direct URI reuse)", "alpha5 (July 2026): hg:ConditionAssessment retired, crm:E14 is now the class itself (still subClassOf hg:CurationActivity in alignment §5)."),

    # ---- Architectural / object hierarchy (LUX uses HumanMadeObject + classified_as Type) ----
    ("ArchitecturalStructure",     "HumanMadeObject",              "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "In LUX a building is HumanMadeObject classified_as <aat:300004792> 'building'."),
    ("ArchitecturalElement",       "PhysicalFeature",              "HumanMadeFeature",  "crm:E25_Human-Made_Feature",      "subClassOf",      "LUX exposes 'HumanMadeFeature' for embedded architectural elements. E25 ⊏ E26 → internal parent hg:PhysicalFeature (§5)."),
    ("Temple",                     "ArchitecturalStructure",       "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "Use classified_as <aat:300007595> 'temple' to mirror LUX style."),
    ("Stupa",                      "BuddhistMonument",             "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "classified_as <aat:300007576> 'stupas'."),
    ("Chaitya",                    "BuddhistMonument",             "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "classified_as <aat:300007562> 'chaitya'."),
    ("BuddhistMonument",           "ArchitecturalStructure",       "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "Modeled with type assignment in LUX."),
    ("Pati",                       "RestHouse",                    "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "Newari open-air pavilion; type-classified."),
    ("Sattal",                     "RestHouse",                    "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "Multi-story rest house; type-classified."),
    ("Dharmashala",                "RestHouse",                    "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "Pilgrim lodge."),
    ("RestHouse",                  "ArchitecturalStructure",       "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      ""),
    ("DhungeDhara",                "WaterStructure",               "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "Stone water spout; novel HG class."),
    ("Pokhari",                    "WaterStructure",               "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "Sacred pond; novel."),
    ("WaterStructure",             "ArchitecturalStructure",       "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      ""),

    # ---- Iconographic / sacred objects ----
    ("IconographicObject",         "HumanMadeObject",              "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "The PHYSICAL object. Depicted content is VisualItem (E36)."),
    ("Murti",                      "IconographicObject",           "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "classified_as <aat:300047090> 'sculpture'. Consecration adds 'sacred' aspect."),
    ("Paubha",                     "IconographicObject",           "HumanMadeObject",   "crm:E22_Human-Made_Object",       "subClassOf",      "classified_as <aat:300033666> 'thangka'."),

    # ---- Person / group / actor ----
    ("Guthi",                      "Group",                        "Group",             "crm:E74_Group",                   "subClassOf",      "Nepal-specific endowed trust. Semantically a Group."),
    ("CasteGroup",                 "Group",                        "Group",             "crm:E74_Group",                   "subClassOf",      ""),
    ("DataCustodian",              "Actor",                        "Actor",             "crm:E39_Actor",                   "subClassOf",      "Could be Person or Group; LUX models as Actor."),

    # ---- Activities / events ----
    ("RitualEvent",                "Activity",                     "Activity",          "crm:E7_Activity",                 "subClassOf",      "Re-parented under hg:Activity (alignment §5, July 2026)."),
    ("Festival",                   "RitualEvent",                  "Activity",          "crm:E7_Activity",                 "subClassOf",      "Festival = Period-spanning Activity in LUX."),
    ("ChariotFestival",            "Festival",                     "Activity",          "crm:E7_Activity",                 "subClassOf",      ""),
    ("MaskedDance",                "Festival",                     "Activity",          "crm:E7_Activity",                 "subClassOf",      ""),
    ("Consecration",               "RitualEvent",                  "Activity",          "crm:E7_Activity",                 "subClassOf",      "Custom HG event; LUX has no specific class. Re-parented under RitualEvent (§5)."),
    ("Enshrinement",               "RitualEvent",                  "Activity",          "crm:E7_Activity",                 "subClassOf",      "Novel HG event. Re-parented under RitualEvent (§5)."),
    ("LivingGoddessSelection",     "RitualEvent",                  "Activity",          "crm:E7_Activity",                 "subClassOf",      "Novel HG event."),
    ("LivingGoddessRetirement",    "RitualEvent",                  "Activity",          "crm:E7_Activity",                 "subClassOf",      "Novel HG event."),
    ("LivingGoddessTenure",        "(none)",                       "Period",            "crm:E4_Period",                   "subClassOf",      ""),

    # ---- Documentation / source ----
    ("DocumentationActivity",      "Activity",                     "Activity",          "crm:E7_Activity",                 "subClassOf",      "Aligned via prov:Activity already in HG. Re-parented under hg:Activity (§5)."),
    ("FieldSurveyActivity",        "DocumentationActivity",        "(no LUX alias)",    "sci:S4_Observation",              "subClassOf",      "CRMsci preferred at deep level. LUX itself uses 'Activity' (E7)."),
    ("OralHistoryInterview",       "DocumentationActivity",        "Creation",          "crm:E65_Creation",                "subClassOf",      ""),
    ("Verification",               "DocumentationActivity",        "AttributeAssignment","crm:E13_Attribute_Assignment",   "subClassOf",      ""),
    ("DataSource",                 "(none)",                       "InformationObject", "crm:E73_Information_Object",      "subClassOf",      "Treat as information carrier (text or digital)."),
    ("InformationObject",          "DataSource",                   "InformationObject", "crm:E73_Information_Object",      "subClassOf",      ""),
    ("FieldSurveyDataset",         "DataSource",                   "Document",          "crm:E31_Document",                "subClassOf",      "If purely digital, use 'DigitalObject' (dig:D1)."),
    ("OralHistoryRecording",       "DataSource",                   "LinguisticObject",  "crm:E33_Linguistic_Object",       "subClassOf",      ""),
    ("ArchivalRecord",             "DataSource",                   "Document",          "crm:E31_Document",                "subClassOf",      "Aligned with rico:Record in HG."),

    # ---- Provenance / assertion ----
    ("HeritageAssertion",          "(none)",                       "AttributeAssignment","crm:E13_Attribute_Assignment",   "subClassOf",      "LUX uses E13 inside provenance/identification."),
    ("SyncreticRelationship",      "(none)",                       "AttributeAssignment","crm:E13_Attribute_Assignment",   "subClassOf",      "Already exactMatch crm:E13 in HG."),
    ("AssertableEntity",           "(none)",                       "(no direct match)", "crminf:E1_Entity",                "broadMatch",      "Abstract; LUX has no equivalent. Keep CRMinf alignment."),

    # ---- Concepts / types ----
    ("ReligiousTradition",         "(none)",                       "Type",              "crm:E55_Type",                    "subClassOf",      "Tradition modeled as a typed Concept (skos:Concept) in LUX."),
    ("Technique",                  "PropositionalObject",          "DesignOrProcedure", "crm:E29_Design_or_Procedure",     "identity (direct URI reuse)", "alpha5 (July 2026): hg:Technique retired, crm:E29 is now the class itself (still subClassOf hg:PropositionalObject in alignment §5)."),
    ("CalendarSystem",             "(none)",                       "(no LUX alias)",    "crm:E29_Designated_Reference_System", "broadMatch",  "time:Calendar exact match retained."),

    # ---- Containers / metadata ----
    ("Container",                  "(none)",                       "(no direct match)", "(none)",                          "no_direct_match", "LinkML container; LUX has no analogue."),
    ("Metadata",                   "(none)",                       "InformationObject", "crm:E73_Information_Object",      "subClassOf",      "Map at instance level via Identifier / Name."),
    ("PhysicalHeritageThing",      "(none)",                       "HumanMadeObject",   "crm:E22_Human-Made_Object",       "closeMatch",      "Union class — LUX equivalent is HumanMadeObject (closeMatch)."),

    # ---- Enums (treated as concept schemes / Type instances in LUX) ----
    ("DatePrecisionEnum",          "(none)",                       "Type",              "crm:E55_Type",                    "subClassOf",      "Enum -> SKOS ConceptScheme of Type instances."),
    ("ConditionTypeEnum",          "(none)",                       "Type",              "crm:E55_Type",                    "subClassOf",      ""),
    ("ExistenceStatusEnum",        "(none)",                       "Type",              "crm:E55_Type",                    "subClassOf",      ""),
    ("GuthiTypeEnum",              "(none)",                       "Type",              "crm:E55_Type",                    "subClassOf",      ""),
    ("RitualTypeEnum",             "(none)",                       "Type",              "crm:E55_Type",                    "subClassOf",      ""),
    ("SyncreticTypeEnum",          "(none)",                       "Type",              "crm:E55_Type",                    "subClassOf",      ""),
]

# ---------------- Property mapping ----------------
PROP_ROWS = [
    # HG property | Range | LUX alias (JSON-LD) | URI in LUX data | Mapping
    ("commissioned_by",          "Actor",                "(commissioning Activity → carried_out_by)", "crm:P14_carried_out_by", "subPropertyOf",   "LUX models as separate 'Activity' carried_out_by Actor."),
    ("carried_out_by",           "Actor",                "carried_out_by",             "crm:P14_carried_out_by",          "equivalentProperty", ""),
    ("carried_out_activity",     "RitualEvent",          "carried_out",                "crm:P14i_performed",              "equivalentProperty", ""),
    ("performed_by_group",       "Guthi/CasteGroup",     "carried_out_by",             "crm:P14_carried_out_by",          "subPropertyOf",      "Group-restricted variant."),
    ("performs_ritual",          "RitualEvent",          "carried_out",                "crm:P14i_performed",              "subPropertyOf",      ""),
    ("had_participant",          "Actor",                "participant",                "crm:P11_had_participant",         "equivalentProperty", ""),
    ("invokes_deity",            "Deity",                "(participant on Activity)",  "crm:P12_occurred_in_the_presence_of", "subPropertyOf", "Already broadMatch P12 in HG."),
    ("is_invoked_in_ritual",     "RitualEvent",          "(inverse: present_at)",      "crm:P12i_was_present_at",         "subPropertyOf",   ""),
    ("took_place_at",            "Place",                "took_place_at",              "crm:P7_took_place_at",            "equivalentProperty", ""),
    ("has_timespan",             "TimeSpan",             "timespan",                   "crm:P4_has_time-span",            "equivalentProperty", ""),
    ("has_current_location",     "Place",                "current_location",           "crm:P55_has_current_location",    "equivalentProperty", ""),
    ("hypothesized_location",    "Place",                "(current_location + assertion)","crm:P55",                      "subPropertyOf",   "Provenance assertion needed for hypothetical."),
    ("has_component",            "ArchitecturalElement", "part",                       "crm:P46_is_composed_of",          "subPropertyOf",   "P46 for physical (P106 for visual/linguistic)."),
    ("is_component_of",          "ArchitecturalStructure","part_of",                   "crm:P46i_forms_part_of",          "subPropertyOf",   ""),
    ("contains_structure",       "ArchitecturalStructure","(no LUX alias)",            "crm:P59i_is_located_on_or_within","subPropertyOf",   ""),
    ("used_materials",           "Material",             "made_of",                    "crm:P45_consists_of",             "subPropertyOf",   ""),
    ("used_technique",           "Technique",            "technique",                  "crm:P32_used_general_technique",  "subPropertyOf",   ""),
    ("has_architectural_style",  "crm:E55_Type",         "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("has_condition_type",       "ConditionTypeEnum",    "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("has_religious_tradition",  "ReligiousTradition",   "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("guthi_type",               "GuthiTypeEnum",        "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("ritual_type",              "RitualTypeEnum",       "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("place_type",               "xsd:string",           "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   "Make Place classified_as a Type Concept rather than string."),
    ("custodian_type",           "xsd:string",           "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("syncretic_type",           "SyncreticTypeEnum",    "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("date_precision",           "DatePrecisionEnum",    "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("source_type",              "xsd:string",           "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),
    ("existence_status",         "ExistenceStatusEnum",  "classified_as",              "crm:P2_has_type",                 "subPropertyOf",   ""),

    ("was_produced_by_event",    "Production",           "produced_by",                "crm:P108i_was_produced_by",       "equivalentProperty", ""),
    ("produced_object",          "PhysicalHeritageThing","produced",                   "crm:P108_has_produced",           "equivalentProperty", ""),
    ("destruction_event",        "DestructionEvent",     "destroyed_by",               "crm:P13i_was_destroyed_by",       "equivalentProperty", ""),
    ("transferred_to_actor",     "Actor",                "transferred_custody_to",     "crm:P29_custody_received_by",     "equivalentProperty", ""),
    ("transferred_from_actor",   "Actor",                "transferred_custody_from",   "crm:P28_custody_surrendered_by",  "equivalentProperty", ""),
    ("transferred_to_guthi",     "Guthi",                "transferred_custody_to",     "crm:P29_custody_received_by",     "subPropertyOf",      ""),
    ("transferred_object",       "PhysicalHeritageThing","transferred_custody_of",     "crm:P30_transferred_custody_of",  "equivalentProperty", ""),
    ("holds_custody_of",         "ArchitecturalStructure","(inverse of current_keeper)","crm:P49i_is_former_or_current_keeper_of", "subPropertyOf", ""),

    ("has_membership",           "Person",               "current_or_former_member",   "crm:P107_has_current_or_former_member",   "equivalentProperty", ""),
    ("member_of_group",          "Guthi",                "member_of",                  "crm:P107i_is_current_or_former_member_of","equivalentProperty", ""),
    ("managed_by_guthi",         "Guthi",                "current_keeper / current_owner","crm:P49_has_former_or_current_keeper", "subPropertyOf", ""),

    ("birth_timespan",           "TimeSpan",             "born → timespan",            "crm:E67_Birth via P4_has_time-span","subPropertyOf",      "Better modeled via 'born' Activity (P98i_was_born) with timespan."),
    ("death_timespan",           "TimeSpan",             "died → timespan",            "crm:E69_Death via P4_has_time-span","subPropertyOf",      ""),
    ("publication_timespan",     "TimeSpan",             "created → timespan",         "crm:E65_Creation via P4_has_time-span","subPropertyOf",   ""),

    ("documented_in_source",     "DataSource",           "referred_to_by",             "crm:P67i_is_referred_to_by",      "equivalentProperty", ""),
    ("was_documented_by",        "DocumentationActivity","(provenance)",               "crm:P94i_was_created_by",         "subPropertyOf",      ""),
    ("produced_information_object","InformationObject",  "created",                    "crm:P94_has_created",             "subPropertyOf",      ""),
    ("created_by_documentation", "DocumentationActivity","created_by",                 "crm:P94i_was_created_by",         "equivalentProperty", ""),

    ("is_about_entity",          "ArchitecturalStructure","about",                     "crm:P129_is_about",               "equivalentProperty", ""),
    ("is_about_event",           "RitualEvent",          "about",                      "crm:P129_is_about",               "equivalentProperty", ""),
    ("subject_entity",           "PhysicalHeritageThing","(attribute_assigned_to)",    "crm:P140_assigned_attribute_to",  "subPropertyOf",      ""),
    ("subject_event",            "RitualEvent",          "(assigned)",                 "crm:P141_assigned",               "subPropertyOf",      ""),

    ("is_part_of_festival",      "Festival",             "part_of",                    "crm:P9i_forms_part_of",           "subPropertyOf",      ""),
    ("includes_ritual_event",    "RitualEvent",          "part",                       "crm:P9_consists_of",              "subPropertyOf",      ""),
    ("occurred_after",           "RitualEvent",          "(no LUX alias)",             "crm:P183i_starts_after_the_end_of", "subPropertyOf",    ""),
    ("occurs_before",            "RitualEvent",          "(no LUX alias)",             "crm:P183_ends_before_the_start_of", "subPropertyOf",    ""),

    ("depicts_deity",            "Deity",                "represents (on VisualItem)", "crm:P138_represents",             "subPropertyOf",      "Object → VisualItem → represents → Deity."),
    ("is_about_deity",           "Deity",                "represents",                 "crm:P138_represents",             "subPropertyOf",      ""),
    ("is_depicted_in",           "IconographicObject",   "representation",             "crm:P138i_has_representation",    "subPropertyOf",      ""),

    ("name",                     "xsd:string",           "identified_by → Name",       "crm:P1_is_identified_by",         "subPropertyOf",      "LUX uses Name + content."),
    ("id",                       "xsd:anyURI",           "id",                         "crm:P1_is_identified_by",         "subPropertyOf",      ""),
    ("note",                     "xsd:string",           "referred_to_by → LinguisticObject", "crm:P3_has_note",          "subPropertyOf",      ""),
    ("source_citation",          "xsd:string",           "referred_to_by",             "crm:P67i_is_referred_to_by",      "subPropertyOf",      ""),
    ("source_url",               "xsd:string",           "digitally_carried_by",       "la:digitally_carried_by",         "subPropertyOf",      "One of the genuine la: properties (no CRM equivalent)."),
    ("place_coordinates",        "geo:wktLiteral",       "defined_by",                 "crm:P168_place_is_defined_by",    "equivalentProperty", ""),

    ("assertion_author",         "Actor",                "(carried_out_by on AttributeAssignment)", "crm:P14_carried_out_by", "subPropertyOf", ""),
    ("was_attributed_to_agent",  "Person",               "carried_out_by",             "crm:P14_carried_out_by",          "subPropertyOf",      ""),
    ("asserted_property",        "xsd:string",           "assigned_property",          "crm:P177_assigned_property_of_type", "subPropertyOf",   ""),
    ("asserted_value",           "xsd:string",           "assigned",                   "crm:P141_assigned",               "subPropertyOf",      ""),
    ("generated_at_time",        "xsd:dateTime",         "(AttributeAssignment.timespan)","crm:P4_has_time-span",          "subPropertyOf",      ""),
    ("confidence_score",         "xsd:float",            "(no LUX equivalent)",        "(none)",                          "no_direct_match",    "LUX/Linked Art has no built-in confidence score. Keep as HG-specific."),
]

# ---------------- Missing classes (proposed additions for full LUX -> HG migration) ----------------
MISSING_ROWS = [
    # Suggested HG class | LUX alias | URI in LUX data | Why we need it
    # ---- Actor branch ----
    ("hg:Group",              "Group",                "crm:E74_Group",                "Generic group above Guthi/CasteGroup; LUX exposes Group as top-level."),
    # ---- Object branch ----
    ("hg:DigitalObject",      "DigitalObject",        "dig:D1_Digital_Object",        "LUX top-level type at /data/digital/. Note: dig: (CRMdig), NOT crmdig:."),
    # ---- Information / work branch ----
    ("hg:VisualItem",         "VisualItem",           "crm:E36_Visual_Item",          "Depicted *content* (scene/deity) separate from the physical Murti/Paubha."),
    ("hg:LinguisticObject",   "LinguisticObject",     "crm:E33_Linguistic_Object",    "Inscriptions, manuscripts, transcribed oral history."),
    ("hg:PropositionalObject","PropositionalObject",  "crm:E89_Propositional_Object", "Abstract works, beliefs, doctrines."),
    ("hg:InformationObject",  "InformationObject",    "crm:E73_Information_Object",   "Generic super of LinguisticObject/VisualItem/DigitalObject."),
    ("hg:Set",                "Set",                  "la:Set (closeMatch crm:E78)",  "GENUINE la: class — Linked Art mints la:Set distinct from crm:E78_Curated_Holding."),
    ("hg:CuratedHolding",     "CuratedHolding",       "crm:E78_Curated_Holding",      "Formally curated holding (museum collection, library set)."),
    ("hg:Inscription",        "Inscription",          "crm:E34_Inscription",          "Stone/metal/manuscript inscriptions."),
    ("hg:Title",              "Title",                "crm:E35_Title",                "Titled name of a work or object."),
    # ---- Time / period ----
    ("hg:Period",             "Period",               "crm:E4_Period",                "Generic period (Lichhavi, Malla, Shah, Rana). LivingGoddessTenure becomes its subclass."),
    # ---- Event / activity branch ----
    ("hg:Birth",              "Birth",                "crm:E67_Birth",                "First-class person life event — LUX exposes 'born' for Person records."),
    ("hg:Death",              "Death",                "crm:E69_Death",                "Mirror of Birth — 'died' on Person records."),
    ("hg:Formation",          "Formation",            "crm:E66_Formation",            "Founding event of a Guthi/Group; LUX uses 'formed_by' on Group records."),
    ("hg:Dissolution",        "Dissolution",          "crm:E68_Dissolution",          "Termination event of a Group; LUX uses 'dissolved_by'."),
    ("hg:BeginningOfExistence","BeginningOfExistence","crm:E63_Beginning_of_Existence","Generic existence-start fallback when no Production/Birth/Formation applies."),
    ("hg:EndOfExistence",     "EndOfExistence",       "crm:E64_End_of_Existence",     "Generic existence-end fallback (mirror)."),
    ("hg:Modification",       "Modification",         "crm:E11_Modification",         "Restoration / alteration events on a Murti or Temple."),
    ("hg:Move",               "Move",                 "crm:E9_Move",                  "Physical relocation of an object — distinct from custody change."),
    ("hg:Acquisition",        "Acquisition",          "crm:E8_Acquisition",           "Title transfer (vs. custody only)."),
    ("hg:Encounter",          "Encounter",            "sci:S19_Encounter_Event",      "CRMsci extension. LUX uses 'Encounter' which expands to sci:S19 — NOT crm:E87."),
    ("hg:CurationActivity",   "CurationActivity",     "crm:E87_Curation_Activity",    "Conservation/inventory/accession activities by a museum or Guthi."),
    ("hg:Measurement",        "Measurement",          "crm:E16_Measurement",          "Act of measuring an object's dimension."),
    ("hg:ProvenanceActivity", "(Activity classified_as Provenance)","crm:E7_Activity","NOT a separate la: class. LUX uses crm:E7_Activity classified_as a 'provenance' Type."),
    # ---- Information sub-classes ----
    ("hg:AttributeAssignment","AttributeAssignment",  "crm:E13_Attribute_Assignment", "Super of HeritageAssertion / Verification / SyncreticRelationship."),
    # ---- Concept / type branch ----
    ("hg:Language",           "Language",             "crm:E56_Language",             "Devanagari / Nepali / Newari / Sanskrit / English language tags."),
    ("hg:Currency",           "Currency",             "crm:E98_Currency",             "Used in provenance Acquisition/Payment records."),
    ("hg:MonetaryAmount",     "MonetaryAmount",       "crm:E97_Monetary_Amount",      "Monetary values referenced in Acquisition/Payment."),
    ("hg:LegalObject",        "LegalObject",          "crm:E72_Legal_Object",         "Things subject to legal frameworks (e.g. 'Ancient Monument' under Nepal heritage law). NOTE: HG previously called this 'LegalConcept' which is not a Linked Art class."),
    # ---- Identifier / name ----
    ("hg:Identifier",         "Identifier",           "crm:E42_Identifier",           "Catalogue numbers, DANAM IDs, DOIs as first-class entities."),
    ("hg:Name",               "Name",                 "crm:E33_E41_Linguistic_Appellation","Multilingual names. Linked Art's 'Name' alias expands to the multi-instantiated E33_E41 class."),
    # ---- Dimension / measurement / right ----
    ("hg:MeasurementUnit",    "MeasurementUnit",      "crm:E58_Measurement_Unit",     "For dimensions of structures and objects."),
    ("hg:Dimension",          "Dimension",            "crm:E54_Dimension",            "Height / width / depth / weight values."),
    ("hg:Right",              "Right",                "crm:E30_Right",                "Access / IP rights on photographs and datasets."),

    # ---- July 2026 gap audit (alignment §5) --------------------------------
    # Structural supers:
    ("hg:Activity",           "Activity",             "crm:E7_Activity",              "Generic activity top + landing class for E7-typed LUX records (provenance wrappers). Internal parent of RitualEvent/DocumentationActivity/CurationActivity/ProvenanceActivity/AttributeAssignment."),
    ("hg:Concept",            "Type",                 "crm:E55_Type",                 "Conceptual top; landing class for /data/concept/ records. Internal parent of Language/Currency/MeasurementUnit/ProductType/ReligiousTradition/enums."),
    ("hg:Appellation",        "Appellation",          "crm:E41_Appellation",          "Super of Identifier and Name; closes unmapped E41."),
    ("hg:Creation",           "Creation",             "crm:E65_Creation",             "Generic creation of information objects (E65 ⊏ E7 ∧ E63)."),
    # The six missing genuine la: classes (only la:Set was mapped before):
    ("hg:Payment",            "Payment",              "la:Payment",                   "GENUINE la: class. Payments inside provenance activities; carries paid_amount."),
    ("hg:Transfer",           "Transfer",             "la:Transfer",                  "GENUINE la: class. Object transfer without title/custody assertion."),
    ("hg:SetAddition",        "Addition",             "la:Addition",                  "GENUINE la: class. Accession of a member into a la:Set. Named SetAddition to avoid clash with crm:E79."),
    ("hg:SetRemoval",         "Removal",              "la:Removal",                   "GENUINE la: class. Deaccession from a la:Set."),
    ("hg:RightAcquisition",   "RightAcquisition",     "la:RightAcquisition",          "GENUINE la: class. Acquisition of a Right over a thing."),
    ("hg:DigitalService",     "DigitalService",       "la:DigitalService",            "GENUINE la: class. IIIF image/presentation services on virtually every digital record."),
    # crm/sci classes observed in LUX data at full scale:
    ("hg:Purchase",           "Purchase",             "crm:E96_Purchase",             "Acquisition with sales price (E96 ⊏ E8)."),
    ("hg:Joining",            "Joining",              "crm:E85_Joining",              "Group-membership join events on person/group records."),
    ("hg:Leaving",            "Leaving",              "crm:E86_Leaving",              "Mirror of Joining."),
    ("hg:TypeCreation",       "TypeCreation",         "crm:E83_Type_Creation",        "Taxonomy-minting events (E83 ⊏ E65)."),
    ("hg:IdentifierAssignment","IdentifierAssignment","crm:E15_Identifier_Assignment","Identifier assignment activities (E15 ⊏ E13)."),
    ("hg:TypeAssignment",     "TypeAssignment",       "crm:E17_Type_Assignment",      "Type assignment activities (E17 ⊏ E13)."),
    ("hg:PartAddition",       "PartAddition",         "crm:E79_Part_Addition",        "Physical part added (E79 ⊏ E11)."),
    ("hg:PartRemoval",        "PartRemoval",          "crm:E80_Part_Removal",         "Physical part removed (E80 ⊏ E11)."),
    ("hg:Transformation",     "Transformation",       "crm:E81_Transformation",       "End of one thing, start of another (E81 ⊏ E63 ∧ E64)."),
    ("hg:BiologicalObject",   "BiologicalObject",     "crm:E20_Biological_Object",    "Natural-history specimens — LUX includes Yale Peabody Museum."),
    ("hg:PhysicalFeature",    "PhysicalFeature",      "crm:E26_Physical_Feature",     "Physical features; internal parent of ArchitecturalElement (E25 ⊏ E26) and Site."),
    ("hg:Site",               "Site",                 "crm:E27_Site",                 "Delimited sites (E27 ⊏ E26). NOTE: a physical thing, not an E53 Place."),
    ("hg:Mark",               "Mark",                 "crm:E37_Mark",                 "Hallmarks / maker's marks (E37 ⊏ E36); internal parent of Inscription (E34 ⊏ E37)."),
    ("hg:AuthorityDocument",  "AuthorityDocument",    "crm:E32_Authority_Document",   "Vocabulary source documents on concept records (E32 ⊏ E31)."),
    ("hg:ProductType",        "ProductType",          "crm:E99_Product_Type",         "Industrial product types (E99 ⊏ E55)."),
    ("hg:Presence",           "Presence",             "crm:E93_Presence",             "Spacetime slice used in provenance/exhibition modeling. Internal parent hg:Period is PRAGMATIC (E93 ⊏ E92); flagged for two-rater review."),
]

# ---------------- LUX -> HG Migration Coverage ----------------
LUX_COVERAGE = [
    # ---- Object branch -----------------------------------------------------------------
    ("HumanMadeObject",      "crm:E22_Human-Made_Object",   "/data/object/  (top-level)",
        "crm:E22_Human-Made_Object",                           "IDENTITY",
        "alpha5 (July 2026): hg:HumanMadeObject retired; the imported node is typed crm:E22 directly."),
    ("DigitalObject",        "dig:D1_Digital_Object",       "/data/digital/ (top-level)",
        "hg:DigitalObject",                                    "NEW",
        "IIIF images, 3D scans, audio. Note CRMdig prefix is 'dig:' in LUX."),

    # ---- Actor branch ------------------------------------------------------------------
    ("Person",               "crm:E21_Person",              "/data/person/  (top-level)",
        "crm:E21_Person",                                      "IDENTITY", "alpha5 (July 2026): hg:Person retired; typed crm:E21 directly."),
    ("Group",                "crm:E74_Group",               "/data/group/   (top-level)",
        "hg:Group",                                            "NEW",
        "New super-class above Guthi and CasteGroup."),
    ("Actor",                "crm:E39_Actor",               "(union; not its own endpoint)",
        "crm:E39_Actor",                                       "IDENTITY", "Generic actor — Person OR Group. alpha5 (July 2026): hg:Actor retired; typed crm:E39 directly."),

    # ---- Place branch ------------------------------------------------------------------
    ("Place",                "crm:E53_Place",               "/data/place/   (top-level)",
        "crm:E53_Place",                                       "IDENTITY", "alpha5 (July 2026): hg:Place retired; typed crm:E53 directly."),

    # ---- Concept branch -----------------------------------------------------------------
    ("Type",                 "crm:E55_Type",                "/data/concept/ (top-level)",
        "hg:* (enum classes) ⊑ E55", "EXISTING",
        "All HG enum classes become subclasses of crm:E55_Type."),
    ("Material",             "crm:E57_Material",            "embedded (rare top-level)",
        "crm:E57_Material",                                    "IDENTITY", "alpha5 (July 2026): hg:Material retired; typed crm:E57 directly."),
    ("Language",             "crm:E56_Language",            "embedded",
        "hg:Language",                                         "NEW",
        "LUX tags every Name/text with a Language."),
    ("Currency",             "crm:E98_Currency",            "embedded (in Acquisition/Payment)",
        "hg:Currency",                                         "NEW",
        "Even if HG rarely uses currency, LUX provenance records carry purchase prices."),
    ("MonetaryAmount",       "crm:E97_Monetary_Amount",     "embedded (in Acquisition/Payment)",
        "hg:MonetaryAmount",                                   "NEW",     "Goes hand-in-hand with Currency."),
    ("MeasurementUnit",      "crm:E58_Measurement_Unit",    "embedded (in Dimension)",
        "hg:MeasurementUnit",                                  "NEW",     "Required by every Dimension."),
    ("LegalObject",          "crm:E72_Legal_Object",        "embedded (in Right)",
        "hg:LegalObject",                                      "NEW",
        "Replaces the original (incorrect) hg:LegalConcept proposal — LegalObject is the actual Linked Art class name."),

    # ---- Time / Period -----------------------------------------------------------------
    ("TimeSpan",             "crm:E52_Time-Span",           "embedded",
        "crm:E52_Time-Span",                                   "IDENTITY", "alpha5 (July 2026): hg:TimeSpan retired; typed crm:E52 directly."),
    ("Period",               "crm:E4_Period",               "/data/event/ (subset)",
        "hg:Period",                                           "NEW",
        "Generic historical period. hg:LivingGoddessTenure becomes its subclass."),

    # ---- Event / Activity branch -------------------------------------------------------
    ("Event",                "crm:E5_Event",                "/data/event/   (top-level)",
        "hg:HistoricalEvent",                                  "EXISTING", "Generic event."),
    ("Activity",             "crm:E7_Activity",             "/data/event/   (top-level)",
        "hg:Activity (fallback) + subclasses",                 "NEW",
        "Was PARENT-ONLY. §5 adds hg:Activity ≡ E7 so generic/provenance E7 records now migrate (guarded fallback in template t6)."),

    ("Production",           "crm:E12_Production",          "embedded (in Object)",
        "crm:E12_Production",                                  "IDENTITY", "alpha5 (July 2026): hg:Production retired; typed crm:E12 directly."),
    ("Modification",         "crm:E11_Modification",        "embedded",
        "hg:Modification",                                     "NEW",
        "Restoration / alteration events on a Murti or Temple."),
    ("Move",                 "crm:E9_Move",                 "embedded (in ProvenanceActivity)",
        "hg:Move",                                             "NEW",
        "Physical relocation of an object — distinct from custody change."),
    ("TransferOfCustody",    "crm:E10_Transfer_of_Custody", "embedded",
        "crm:E10_Transfer_of_Custody",                         "IDENTITY", "alpha5 (July 2026): hg:TransferOfCustody retired; typed crm:E10 directly."),
    ("Acquisition",          "crm:E8_Acquisition",          "embedded (in ProvenanceActivity)",
        "hg:Acquisition",                                      "NEW",     "Title transfer (vs. custody only)."),
    ("Birth",                "crm:E67_Birth",               "embedded (on Person)",
        "hg:Birth",                                            "NEW",     "First-class person life event."),
    ("Death",                "crm:E69_Death",               "embedded (on Person)",
        "hg:Death",                                            "NEW",     "Mirror of Birth."),
    ("Formation",            "crm:E66_Formation",           "embedded (on Group)",
        "hg:Formation",                                        "NEW",     "Founding event of a Guthi/Group."),
    ("Dissolution",          "crm:E68_Dissolution",         "embedded (on Group)",
        "hg:Dissolution",                                      "NEW",     "Termination event of a Group."),
    ("BeginningOfExistence", "crm:E63_Beginning_of_Existence","embedded",
        "hg:BeginningOfExistence",                             "NEW",
        "Generic existence-start fallback."),
    ("EndOfExistence",       "crm:E64_End_of_Existence",    "embedded",
        "hg:EndOfExistence",                                   "NEW",     "Generic existence-end fallback."),
    ("Destruction",          "crm:E6_Destruction",          "embedded",
        "crm:E6_Destruction",                                  "IDENTITY", "alpha5 (July 2026): hg:DestructionEvent retired; typed crm:E6 directly."),
    ("Encounter",            "sci:S19_Encounter_Event",     "embedded",
        "hg:Encounter",                                        "NEW",
        "CRITICAL: LUX 'Encounter' expands to CRMsci sci:S19, NOT crm:E87."),
    ("CurationActivity",     "crm:E87_Curation_Activity",   "embedded",
        "hg:CurationActivity",                                 "NEW",
        "Distinct from Encounter — this is the museum/Guthi conservation/inventory activity."),
    ("Measurement",          "crm:E16_Measurement",         "embedded (in Dimension)",
        "hg:Measurement",                                      "NEW",
        "Act of measuring; carries the Dimension."),
    ("ProvenanceActivity",   "crm:E7_Activity (classified_as 'Provenance')",  "/data/event/ (subset)",
        "hg:ProvenanceActivity",                               "NEW",
        "NOT a separate la: class. LUX models as crm:E7_Activity classified_as 'provenance' Type."),
    ("AttributeAssignment",  "crm:E13_Attribute_Assignment","embedded",
        "hg:AttributeAssignment",                              "NEW",
        "Super of HeritageAssertion / Verification / SyncreticRelationship."),

    # ---- Information / Work branch -----------------------------------------------------
    ("LinguisticObject",     "crm:E33_Linguistic_Object",   "/data/work/    (top-level)",
        "hg:LinguisticObject",                                 "NEW",     "Inscriptions, manuscripts, transcribed oral history."),
    ("VisualItem",           "crm:E36_Visual_Item",         "/data/work/    (top-level)",
        "hg:VisualItem",                                       "NEW",
        "Depicted *content* — separated from the physical Murti/Paubha."),
    ("PropositionalObject",  "crm:E89_Propositional_Object","/data/work/    (top-level)",
        "hg:PropositionalObject",                              "NEW",     "Abstract works, doctrines, beliefs."),
    ("InformationObject",    "crm:E73_Information_Object",  "embedded super-class",
        "hg:InformationObject",                                "EXISTING (re-rooted)",
        "HG already has hg:InformationObject; we re-parent under crm:E73."),
    ("Set",                  "la:Set  (genuine la: class)", "/data/set/     (top-level)",
        "hg:Set",                                              "NEW",
        "ONE OF SEVEN GENUINE la: CLASSES. la:Set is distinct from crm:E78 (Curated Holding) — Linked Art deliberately mints la:Set as a more general grouping."),
    ("CuratedHolding",       "crm:E78_Curated_Holding",     "embedded / occasional top-level",
        "hg:CuratedHolding",                                   "NEW",
        "Distinct from Set (E78 is formal curated holding)."),
    ("Inscription",          "crm:E34_Inscription",         "embedded (on Object)",
        "hg:Inscription",                                      "NEW",
        "Stone/metal/manuscript inscriptions on temples and artifacts."),
    ("Title",                "crm:E35_Title",               "embedded (on every record)",
        "hg:Title",                                            "NEW",     "Titled name of a work."),

    # ---- Identifier / Name -------------------------------------------------------------
    ("Identifier",           "crm:E42_Identifier",          "embedded (on every record)",
        "hg:Identifier",                                       "NEW",     "Catalogue numbers, DANAM IDs, DOIs."),
    ("Name",                 "crm:E33_E41_Linguistic_Appellation","embedded (on every record)",
        "hg:Name",                                             "NEW",
        "Multilingual names. Linked Art's 'Name' alias points to the multi-instantiated E33_E41 class."),

    # ---- Dimension / Right -------------------------------------------------------------
    ("Dimension",            "crm:E54_Dimension",           "embedded (on Object)",
        "hg:Dimension",                                        "NEW",     "Height / width / depth / weight values."),
    ("Right",                "crm:E30_Right",               "embedded",
        "hg:Right",                                            "NEW",     "Access / IP rights on photographs and datasets."),

    # ---- July 2026 gap audit — previously UNMAPPED (V1 risk at full scale) --------------
    ("Payment",              "la:Payment (genuine la:)",    "embedded (in provenance)",
        "hg:Payment",                                          "NEW",
        "One of the six missing genuine la: classes; carries paid_amount/paid_from/paid_to."),
    ("Transfer",             "la:Transfer (genuine la:)",   "embedded (in provenance)",
        "hg:Transfer",                                         "NEW",     "Transfer without title/custody assertion."),
    ("Addition",             "la:Addition (genuine la:)",   "embedded (on Set)",
        "hg:SetAddition",                                      "NEW",     "Accession into a la:Set."),
    ("Removal",              "la:Removal (genuine la:)",    "embedded (on Set)",
        "hg:SetRemoval",                                       "NEW",     "Deaccession from a la:Set."),
    ("RightAcquisition",     "la:RightAcquisition (genuine la:)", "embedded (in provenance)",
        "hg:RightAcquisition",                                 "NEW",     "Acquisition of a Right."),
    ("DigitalService",       "la:DigitalService (genuine la:)", "embedded (on DigitalObject)",
        "hg:DigitalService",                                   "NEW",
        "IIIF services — present on virtually every LUX digital record; highest-volume former gap."),
    ("Purchase",             "crm:E96_Purchase",            "embedded (in provenance)",
        "hg:Purchase",                                         "NEW",     "E96 ⊏ E8; museum purchases."),
    ("Joining",              "crm:E85_Joining",             "embedded (on Group/Person)",
        "hg:Joining",                                          "NEW",     "Group membership joins."),
    ("Leaving",              "crm:E86_Leaving",             "embedded (on Group/Person)",
        "hg:Leaving",                                          "NEW",     "Group membership departures."),
    ("TypeCreation",         "crm:E83_Type_Creation",       "embedded (on Concept)",
        "hg:TypeCreation",                                     "NEW",     "E83 ⊏ E65."),
    ("IdentifierAssignment", "crm:E15_Identifier_Assignment","embedded",
        "hg:IdentifierAssignment",                             "NEW",     "E15 ⊏ E13."),
    ("TypeAssignment",       "crm:E17_Type_Assignment",     "embedded",
        "hg:TypeAssignment",                                   "NEW",     "E17 ⊏ E13."),
    ("PartAddition",         "crm:E79_Part_Addition",       "embedded (on Object)",
        "hg:PartAddition",                                     "NEW",     "E79 ⊏ E11."),
    ("PartRemoval",          "crm:E80_Part_Removal",        "embedded (on Object)",
        "hg:PartRemoval",                                      "NEW",     "E80 ⊏ E11."),
    ("Transformation",       "crm:E81_Transformation",      "embedded",
        "hg:Transformation",                                   "NEW",     "E81 ⊏ E63 ∧ E64."),
    ("Creation",             "crm:E65_Creation",            "embedded (on Work)",
        "hg:Creation",                                         "NEW",
        "Generic creation events now land on hg:Creation (OralHistoryInterview stays the HG-native subclass)."),
    ("BiologicalObject",     "crm:E20_Biological_Object",   "/data/object/ (Peabody subset)",
        "hg:BiologicalObject",                                 "NEW",     "Yale Peabody natural-history specimens."),
    ("PhysicalFeature",      "crm:E26_Physical_Feature",    "embedded",
        "hg:PhysicalFeature",                                  "NEW",     "Internal parent of ArchitecturalElement and Site."),
    ("Site",                 "crm:E27_Site",                "embedded",
        "hg:Site",                                             "NEW",     "E27 ⊏ E26; physical thing, not Place."),
    ("Mark",                 "crm:E37_Mark",                "embedded (on Object)",
        "hg:Mark",                                             "NEW",     "E37 ⊏ E36; hallmarks/stamps."),
    ("AuthorityDocument",    "crm:E32_Authority_Document",  "embedded (on Concept)",
        "hg:AuthorityDocument",                                "NEW",     "E32 ⊏ E31; vocabulary sources."),
    ("ProductType",          "crm:E99_Product_Type",        "embedded (rare)",
        "hg:ProductType",                                      "NEW",     "E99 ⊏ E55."),
    ("Presence",             "crm:E93_Presence",            "embedded (rare)",
        "hg:Presence",                                         "NEW",     "Pragmatic parent hg:Period; flagged for review."),
    ("Appellation",          "crm:E41_Appellation",         "embedded (on every record)",
        "hg:Appellation",                                      "NEW",     "Super of Identifier and Name; generic E41 instances land here."),
]

NOTES = [
    "Context",
    "  This workbook fills the column requested by Tek Raj on 8.04.2026 ('which of our class maps to the one from LUX?')",
    "  AND closes the broader requirement: every LUX class must have a HeritageGraph migration target so that",
    "  the LUX dataset can be ingested losslessly. LUX is the master data source; HG is the receiver.",
    "",
    "Critical convention (verified May 2026 against linked.art/ns/v1/linked-art.json)",
    "  LUX records use SHORT NAMES like 'HumanMadeObject' / 'Person' / 'Activity' in their @type fields.",
    "  Those short names expand to crm: / dig: / sci: URIs after JSON-LD parsing — NOT to la: URIs.",
    "  Only seven classes are genuinely under the la: namespace:",
    "      Set, Transfer, Payment, Addition, Removal, RightAcquisition, DigitalService.",
    "  The 'URI in LUX data' column shows the ACTUAL URI that appears in LUX data after parsing.",
    "",
    "Mapping_Type values",
    "  equivalentClass / equivalentProperty -> identical semantics; safe to use owl:equivalentClass / owl:equivalentProperty.",
    "  subClassOf / subPropertyOf            -> HG class is more specific; rdfs:subClassOf to the CRM class.",
    "  closeMatch                            -> not strictly equivalent but semantically close; use skos:closeMatch.",
    "  broadMatch                            -> HG class is BROADER than the CRM target; use skos:broadMatch.",
    "  no_direct_match                       -> no usable LUX/CRM class; keep HG-only, document rationale.",
    "",
    "Special-case mappings",
    "  Encounter        -> sci:S19_Encounter_Event  (CRMsci, NOT crm:E87 Curation Activity)",
    "  CurationActivity -> crm:E87_Curation_Activity",
    "  DigitalObject    -> dig:D1_Digital_Object   (CRMdig prefix is 'dig:', NOT 'crmdig:')",
    "  Set              -> la:Set                  (one of the seven genuine la: classes; closeMatch crm:E78)",
    "  Name             -> crm:E33_E41_Linguistic_Appellation  (multi-instantiated CRM class)",
    "  LegalObject      -> crm:E72_Legal_Object    (HG previously called this LegalConcept which is not a LA class)",
    "  ProvenanceActivity -> crm:E7_Activity classified_as 'Provenance'  (NOT a separate la: class)",
    "",
    "What's already in HeritageGraph.ttl",
    "  HG already aligns to crm: via skos:exactMatch / skos:broadMatch for ~30 classes (HumanMadeObject, Person,",
    "  Place, TimeSpan, Production, DestructionEvent, TransferOfCustody, ConditionState, etc.).",
    "  This workbook upgrades those skos:* alignments to owl:equivalentClass / rdfs:subClassOf where appropriate,",
    "  and adds 30 new HG classes for full LUX migration coverage.",
    "",
    "How to apply the alignment",
    "  1) Append heritagegraph-lux-alignment.ttl to HeritageGraph.ttl (or owl:imports).",
    "  2) Validate with rapper or rdflib: rapper -i turtle HeritageGraph.ttl alignment.ttl",
    "  3) Run the CONSTRUCT queries in lux_to_hg_migration.sparql.",
    "  4) Run the sanity-check query — should return zero rows if every LUX class has a HG target.",
    "",
    "July 2026 gap audit (alignment §5)",
    "  Closed two gap families found after the pilot run:",
    "  (a) Unmapped LUX classes — six genuine la: classes (Payment, Transfer, Addition, Removal,",
    "      RightAcquisition, DigitalService) plus E96/E85/E86/E20/E37/E26/E27/E32/E15/E17/E79/E80/E81/E93/E99/E41.",
    "  (b) Taxonomy orphans — 20 Section-3 classes had object-property edges but no HG-internal",
    "      subClassOf parent; re-parented with CRM-consistent internal edges (see alignment §5.4).",
    "  Deliberate documented HG roots: Period, Concept, Dimension, LegalObject.",
    "  Abstract CRM supers (E1, E2, E18, E19, E24, E70, E71, E77, E90, E92) remain deliberately",
    "  unmapped — LUX never uses them as @type on instances.",
]


def add_table(ws, header, rows, col_widths):
    bold = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    head_fill = PatternFill("solid", start_color="305496")
    body = Font(name="Arial", size=10)
    thin = Side(style="thin", color="BFBFBF")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    align_wrap = Alignment(vertical="top", wrap_text=True)

    ws.append(header)
    for c in range(1, len(header) + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = bold
        cell.fill = head_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = border

    for row in rows:
        ws.append(row)

    last_row = ws.max_row
    for r in range(2, last_row + 1):
        for c in range(1, len(header) + 1):
            cell = ws.cell(row=r, column=c)
            cell.font = body
            cell.alignment = align_wrap
            cell.border = border
            if r % 2 == 0:
                cell.fill = PatternFill("solid", start_color="F2F2F2")

    for i, w in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 32


def main():
    wb = Workbook()

    ws1 = wb.active
    ws1.title = "Class Mapping"
    add_table(
        ws1,
        ["HeritageGraph Class", "HG Parent", "LUX alias (JSON-LD)", "URI in LUX data", "Mapping Type", "Notes"],
        CLASS_ROWS,
        col_widths=[28, 24, 24, 38, 18, 60],
    )

    ws2 = wb.create_sheet("Property Mapping")
    add_table(
        ws2,
        ["HeritageGraph Property", "HG Range", "LUX alias (JSON-LD)", "URI in LUX data", "Mapping Type", "Notes"],
        PROP_ROWS,
        col_widths=[28, 22, 30, 40, 18, 60],
    )

    ws3 = wb.create_sheet("HG New Classes")
    add_table(
        ws3,
        ["Suggested HG Class", "LUX alias", "URI in LUX data", "Why HG should add it (migration rationale)"],
        MISSING_ROWS,
        col_widths=[26, 26, 40, 75],
    )

    ws4 = wb.create_sheet("LUX → HG Coverage")
    add_table(
        ws4,
        ["LUX alias", "URI in LUX data", "LUX endpoint", "HG target", "HG status", "Migration notes"],
        LUX_COVERAGE,
        col_widths=[24, 38, 32, 30, 18, 60],
    )
    status_col = 5
    fills = {
        "EXISTING":             PatternFill("solid", start_color="C6EFCE"),
        "EXISTING (re-rooted)": PatternFill("solid", start_color="C6EFCE"),
        "NEW":                  PatternFill("solid", start_color="FFEB9C"),
        "PARENT-ONLY":          PatternFill("solid", start_color="FCD5B4"),
    }
    for r in range(2, ws4.max_row + 1):
        v = ws4.cell(row=r, column=status_col).value
        if v in fills:
            ws4.cell(row=r, column=status_col).fill = fills[v]

    ws_n = wb.create_sheet("Notes")
    ws_n.column_dimensions["A"].width = 110
    body = Font(name="Arial", size=11)
    bold = Font(name="Arial", size=12, bold=True)
    for i, line in enumerate(NOTES, start=1):
        c = ws_n.cell(row=i, column=1, value=line)
        is_heading = (line and not line.startswith(" ") and not line.endswith("."))
        c.font = bold if is_heading else body
        c.alignment = Alignment(wrap_text=True, vertical="top")

    wb.save(OUT_XLSX)
    print(f"Wrote {OUT_XLSX}")
    print(f"Sheets: Class Mapping ({len(CLASS_ROWS)}) | Property Mapping ({len(PROP_ROWS)}) | "
          f"HG New Classes ({len(MISSING_ROWS)}) | LUX → HG Coverage ({len(LUX_COVERAGE)}) | Notes")


if __name__ == "__main__":
    main()
