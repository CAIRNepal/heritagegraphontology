# Tool configuration

- `robot_report_profile.tsv`: the ROBOT `report` profile used for the documentation's quality page
  (`ontoreview.toml`, `robot_profile`). It is ROBOT 1.9.8's default profile with one change:
  `missing_definition` is reported as INFO instead of WARN. ROBOT's rule looks for the OBO
  definition property (IAO:0000115); every HeritageGraph term carries its definition as
  `skos:definition` instead, and reused CIDOC-CRM, PROV-O and DCMI terms carry their owners' own
  definitions (`rdfs:comment`, `prov:definition`). The rule's findings stay visible on the page.
