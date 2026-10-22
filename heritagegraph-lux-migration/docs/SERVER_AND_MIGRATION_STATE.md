# HeritageGraph ↔ LUX — Server, Migration, and Alignment State

*Bu dosya, `heritagegraph-lux-migration` projesinin sunucu, migration pipeline ve
alignment ontolojisi ile ilgili her şeyi tek bir yerde tutar. Başka bir Claude
oturumuna context olarak yapıştırıldığında hızlı katılım sağlar.*

Son güncelleme: 2026-07-26 (alpha5 core-ontology sync — bkz. §6.1)

---

## 1. Proje özeti

- **Amaç:** Yale LUX (~16M kayıt, Linked Art / CIDOC-CRM tabanlı) → CAIR Nepal
  HeritageGraph ontolojisine lossless migration.
- **HeritageGraph ana ontolojisi:** `github.com/CAIRNepal/heritagegraphontology`,
  namespace `https://w3id.org/heritagegraph/`, CC-BY 4.0.
  **ÖNEMLİ (2026-07-26 keşfi):** `main` branch Şubat 2026'dan beri
  değişmiyor — bu artık aktif geliştirme branch'i DEĞİL. Asıl aktif
  geliştirme `HeritageGraph` branch'inde sürüyor (son commit 2026-07-24).
  `server-bootstrap.sh` bu oturumda düzeltildi (bkz. Bölüm 6 "Alpha5
  core-ontology sync") — artık doğru branch/yoldan fetch ediyor. Ontoloji
  artık
  `ontology/HeritageGraph.{yaml,ttl,shacl.ttl}` altında (eskiden repo
  kökünde); ayrıca CAIR ekibi bizim alignment dosyamızın bir kopyasını da
  o branch'e `ontology/lux/heritagegraph-lux-alignment.ttl` olarak
  eklemiş (Niraj Karki, v1.0.0, 2026-06-18) — bkz. Bölüm 6.
- **Bu repo (LUX bridge):**
  `github.com/CAIRNepal/heritagegraph-lux-migration`, Apache 2.0.
- **Local path:** `/Users/semih/Documents/GitHub/heritagegraph-lux-migration`
- **Author of migration bridge:** Semih Yumuşak, Mayıs 2026.

## 2. Repo yapısı

```
heritagegraph-lux-migration/
├── README.md
├── LICENSE                     # Apache 2.0
├── CONTRIBUTING.md
├── CHANGELOG.md
├── Makefile                    # 25+ target: up/down/logs/deploy/ssh-*/reload-alignment
├── deploy.sh                   # rsync + remote docker compose up -d --build
├── .gitignore
├── .github/workflows/ci.yml    # 5 parallel job: TTL parse, ruff, sparql, hadolint, shellcheck
├── alignment/
│   ├── heritagegraph-lux-alignment.ttl   # 631 triple, 5 section (§5: July 2026 gap audit)
│   └── HeritageGraph.ttl                 # fetched at install, gitignored
├── mapping/
│   ├── build_mapping.py                  # canonical Python data → XLSX (script-relative output)
│   └── HeritageGraph_LUX_Mapping.xlsx    # 5 sheet: Class, Property, HG New, Coverage, Notes
├── queries/
│   ├── lux_to_hg_migration.sparql        # 10 CONSTRUCT template + sanity (# === tN === headers)
│   └── validation_queries.sparql         # 8 query, V1+V2 hard gate
├── scripts/
│   ├── migrate_lux_to_hg.py              # 4 mode: crawl / transform / validate / delta
│   ├── discover_lux_endpoints.sh         # LUX REST/ActivityStream probe
│   └── server-bootstrap.sh               # one-shot host prep
├── docker/
│   ├── docker-compose.yml                # 3 service: oxigraph + migrator + delta-syncer
│   ├── .env / .env.example
│   └── migrator/
│       ├── Dockerfile                    # Python 3.12 + raptor + supercronic (kalıyor ama kullanılmıyor)
│       ├── entrypoint.sh                 # 7-phase orchestrator (fetch → load → transform → validate → snapshot → master)
│       └── delta_loop.sh                 # pure-bash weekly scheduler (supercronic replaced)
└── docs/
    ├── MIGRATION_PLAN.md
    ├── DEPLOY_SERVER.md
    ├── LUX_DATA_DOWNLOAD.md              # 5 gerçek LUX data acquisition yolu
    ├── VERIFICATION_FINDINGS.md          # canonical Linked Art JSON-LD context'e karşı verification
    ├── GITHUB_SETUP.md
    ├── PILOT_RUN.md
    ├── SERVER_AND_MIGRATION_STATE.md     # bu dosya
    └── heritagegraph-alignment-graph.html  # interactive D3 viz (orphan-fix demo)
```

## 3. Sunucu

| Alan | Değer |
|---|---|
| SSH | `ssh root@server42.dnsbilisim.net` |
| Repo path | `/root/github/heritagegraph-lux-migration/` |
| Deploy komutu | `docker compose up -d --build` |
| Provider constraint | Hetzner IPv4 → Yale CloudFront 403; migrator `network_mode: host` kullanır |

### Deploy akışı

```bash
# Lokalden (Mac terminal):
make deploy               # rsync + remote docker compose up -d --build
make deploy-no-build      # sadece rsync + recreate
make deploy-migrator      # sadece migrator servisi
make ssh-status           # remote docker compose ps + triple counts
make ssh-logs             # remote log tail (all services)
make ssh-logs-migrator    # sadece migrator log
make ssh-shell            # remote migrator container'da bash
make ssh-reload-alignment # remote alignment graph reload
```

## 4. Docker stack

3 servis, tek bir `docker/docker-compose.yml` içinde:

| Servis | Rol | Restart | Network |
|---|---|---|---|
| `hg-oxigraph` | SPARQL 1.1 triplestore | `unless-stopped` | default bridge, 7878 expose |
| `hg-migrator` | One-shot 7-phase pipeline | `no` | `host` (Yale IPv4 sorunu için) |
| `hg-delta-syncer` | Haftalık delta pull | `unless-stopped` | default bridge |

### Named volumes
- `oxigraph_data` — RocksDB store
- `lux_data` — indirilen LUX dump/crawl outputları
- `migration_logs` — 7-phase run logları
- `migration_state` — pP1..P7 state flag'leri

### Build context özelliği
`context: ..` (repo root) → Dockerfile canonical dosyaları direkt `scripts/`,
`alignment/`, `queries/` altından COPY eder. Duplikasyon yok.

## 5. Oxigraph içinde canlı graph durumu

`make ssh-status` çıktısı (production):

```
https://lux.collections.yale.edu/                           3,467,368  raw LUX (import edilmiş .nq)
https://w3id.org/heritagegraph/imported/lux                    98,131  transformed HG (SPARQL CONSTRUCT sonrası)
https://w3id.org/heritagegraph/alignment/lux                      438  alignment ontolojisi
```

Union-default-graph aktif (`--union-default-graph`). Migration query'leri
GRAPH clause olmadan da tüm named graph'lerin birleşimini görür.

## 6. Alignment ontolojisi (`alignment/heritagegraph-lux-alignment.ttl`)

### 6 bölüm

| Bölüm | İçerik | Triple |
|---|---|---|
| §1 Class-level alignment | crm/prov ile class-level bağlar (Temmuz 2026'da 13 tautoloji satırı §6'da temizlendi) | ~85 |
| §2 Property-level alignment | 18 `owl:equivalentProperty`, 45 `rdfs:subPropertyOf` | ~63 |
| §3 New HG classes for LUX coverage | 33 yeni class (Birth, Death, Inscription, VisualItem, Dimension, Currency, MonetaryAmount, Language, PropositionalObject, …) | ~110 |
| §4 Internal HG hierarchy + object properties | 26 HG-internal `rdfs:subClassOf` + 29 HG-internal object property (orphan fix) | ~165 |
| §5 Coverage & taxonomy completion (Temmuz 2026 gap audit) | 26 yeni class (6 eksik `la:` class + Purchase/Joining/Leaving/BiologicalObject/Mark/Site/… + hg:Activity, hg:Concept, hg:Appellation, hg:Creation üst sınıfları), ~35 HG-internal re-parenting edge, 5 yeni object property | ~193 |
| §6 Alpha5 core-ontology sync (Temmuz 2026, bu güncelleme) | 12 class'ın `heritageGraph:` wrapper'ı retired edildi, doğrudan crm: URI kullanımına geçildi; dokümantasyon notu | 0 net (13 tautoloji silindi) |
| **Toplam** | | **617** |

### Alpha5 core-ontology sync (2026-07-26)

CAIR ekibinden gelen "ontoloji güncellendi, alignment'ı eşleştir" talebi
üzerine yapılan inceleme:

- **Asıl aktif branch `HeritageGraph`** (main değil — main Şubat 2026'dan
  beri donuk). `ontology/HeritageGraph.yaml` "alpha5" olarak
  2026-07-22'de yeniden üretilmiş (commit zinciri: ff1a1ac6 "Fixed the
  ontology and verified using Hermit and OOPS", 2026-07-16 → 2286a6e,
  2026-07-22 generate).
- **Mimari değişiklik:** 12 HG class'ı (`HumanMadeObject`, `Person`,
  `Actor`, `Place`, `TimeSpan`, `Material`, `Production`,
  `DestructionEvent`, `TransferOfCustody`, `ConditionAssessment`,
  `ConditionState`, `Technique`) artık ayrı bir `heritageGraph:` URI'si
  almıyor — YAML'deki `class_uri` doğrudan ilgili `crm:` URI'sine
  işaret ediyor. Yani `crm:E21_Person` artık HG class'ının KENDİSİ,
  `heritageGraph:Person` diye bir kaynak yok.
- **Etki:** Bizim ve Niraj'ın (CAIR, `ontology/lux/
  heritagegraph-lux-alignment.ttl`, v1.0.0, 2026-06-18) alignment
  kopyalarının ikisi de hâlâ `heritageGraph:Person owl:equivalentClass
  crm:E21_Person` gibi artık anlamsız (tautolojik) aksiyomlar
  içeriyordu; daha vahimi, migration pipeline'ı LUX kayıtlarını tam bu
  12 class için `heritageGraph:Person`, `heritageGraph:HumanMadeObject`
  tipinde üretiyordu — yani üretilen veri güncel ontolojiyle
  uyuşmuyordu.
- **Yapılan düzeltme (bu commit):**
  - `alignment/heritagegraph-lux-alignment.ttl`: 13 tautolojik satır
    silindi, 12 class'a referans veren tüm `rdfs:domain`/`rdfs:range`/
    `rdfs:subClassOf` doğrudan `crm:` URI'sine güncellendi, yeni §6
    eklendi, `crminf:E1_Entity` → `crm:E1_CRM_Entity` düzeltmesi
    (Niraj'ın Haziran fix'i) uygulandı.
  - `queries/lux_to_hg_migration.sparql` (t1/t2/t4/t5/t6/t10) ve
    `scripts/migrate_lux_to_hg.py` (`TRANSFORM_TEMPLATES`): bu 12
    class için `a heritageGraph:X` → `a crm:E..` .
  - `queries/validation_queries.sparql` **V1 hard gate**: doğrudan URI
    yeniden kullanımını (bu 12 class) da "eşlenmiş" sayacak ikinci bir
    `FILTER NOT EXISTS` dalı eklendi — yoksa her migration çalışması bu
    12 class'ın TÜM örneklerini "unmapped" diye V1'de fail ederdi.
  - `mapping/build_mapping.py`: ilgili 17 satır "IDENTITY (direct URI
    reuse)" olarak işaretlendi, XLSX yeniden üretildi.
  - Tüm SPARQL blokları (19/19) ve TRANSFORM_TEMPLATES (10/10) CI'ın
    kullandığı `prepareQuery`/`prepareUpdate` mantığıyla doğrulandı;
    `make ci-local` geçti.
- **Kapsam dışı bırakılan:** alpha5'te CAIR ayrıca ~25 Nepal-özel domain
  class'ı eklemiş (KumariHouse, ChariotFestival, Guthi seçim kriterleri,
  …). Bunların LUX karşılığı olmadığı için bu alignment dosyasına
  eklenmedi — bilinçli bir kapsam kararı.
- **TODO:** `server-bootstrap.sh` hâlâ `main` branch'ini fetch ediyor;
  `HeritageGraph` branch'ine geçirilmeli (ayrı bir görev — bu commit'in
  kapsamı değil, çünkü fetch script'i canlı sunucu bootstrap akışını
  etkiliyor ve ayrı test gerektiriyor).

### Prefix disipliini

**`la:` — 7 gerçek Linked Art class'ının ARTIK YEDİSİ DE map'li (§5):**
`la:Set` (§3'ten beri), `la:Transfer`, `la:Payment`, `la:Addition`,
`la:Removal`, `la:RightAcquisition`, `la:DigitalService` (§5, Temmuz 2026 —
öncesinde yalnız `la:Set` map'liydi; `la:DigitalService` her LUX digital
kaydında IIIF servisi olarak geçtiği için full-scale V1 için kritikti).

Diğer LUX JSON-LD alias'ları (Person, HumanMadeObject, Production, Encounter,
Inscription, Currency, …) tümü `crm:`, `dig:` veya `sci:` URI'lerine expand
olur. Alignment TTL bunu yansıtır.

### §5 Taksonomi tamamlama (Temmuz 2026 gap audit)

Niraj'ın orphan fix'i (§4) yetimliği "herhangi bir kenar" (object property
domain/range dahil) kriteriyle çözmüştü; taksonomik görünümde §3'ün 33
class'ından 20'si hâlâ HG-internal `subClassOf` parent'sızdı. §5 bunları
CRM-tutarlı iç kenarlarla bağlar:

- `Group ⊏ Actor` (E74⊏E39), `VisualItem ⊏ InformationObject` (E36⊏E73),
  `Name ⊏ LinguisticObject ∧ Appellation` (E33_E41), `Identifier ⊏ Appellation`
  (E42⊏E41), `Measurement ⊏ AttributeAssignment` (E16⊏E13),
  `MonetaryAmount ⊏ Dimension` (E97⊏E54), `Right ⊏ PropositionalObject`
  (E30⊏E89), `CuratedHolding ⊏ PhysicalHeritageThing` (E78⊏E24, pragmatik),
  `Inscription ⊏ Mark` (E34⊏E37), `HistoricalEvent ⊏ Period` (E5⊏E4).
- Yeni `hg:Activity ≡ E7` üst sınıfı: RitualEvent, DocumentationActivity,
  CurationActivity, ProvenanceActivity, AttributeAssignment, Encounter,
  Joining, Leaving, Creation hepsi altında.
- Yeni `hg:Concept ≡ E55` üst sınıfı: Language, Currency, MeasurementUnit,
  ProductType, ReligiousTradition + 6 enum altında.
- Ana ontoloji yetimleri de bağlandı: `Consecration/Enshrinement ⊏ RitualEvent`,
  `ArchitecturalElement ⊏ PhysicalFeature` (E25⊏E26),
  `Technique ⊏ PropositionalObject` (E29⊏E89).
- **Belgeli bilinçli root'lar (yetim DEĞİL):** `Period`, `Concept`,
  `Dimension`, `LegalObject`.
- **İki-rater incelemesine işaretli:** `hg:Presence ⊏ hg:Period` pragmatik
  (CRM'de E93 ⊏ E92 Spacetime Volume).
- Abstract CRM üstleri (E1, E2, E18, E19, E24, E70, E71, E77, E90, E92)
  bilinçli olarak map'lenmedi — LUX bunları instance @type olarak kullanmaz.

### 6 material hata (verification aşamasında yakalandı, düzeltildi)

| Hata | Düzeltme |
|---|---|
| `la:HumanMadeObject`, `la:Person`, … (yanlış namespace) | `crm:E22_Human-Made_Object`, `crm:E21_Person`, … |
| `la:Encounter` → `crm:E87_Curation_Activity` yanlış | Düzeltildi: `sci:S19_Encounter_Event` (CRMsci extension) + ayrı `hg:CurationActivity` for E87 |
| `crmdig:` prefix'i | Linked Art convention: `dig:` |
| `la:LegalConcept` yok | `hg:LegalObject` → `crm:E72_Legal_Object` |
| `la:Provenance_Activity` yok | `hg:ProvenanceActivity` → `crm:E7_Activity classified_as` provenance Type |
| `skos:closeMatch la:Concept` (böyle class yok) | Kaldırıldı |

Verification metodolojisi: `docs/VERIFICATION_FINDINGS.md`, kaynak canonical
Linked Art JSON-LD context (`https://linked.art/ns/v1/linked-art.json`).

### Orphan-node fix (§4, Haziran 2026, Niraj geri bildirimi)

**Problem:** §3'teki 33 yeni class sadece dış `crm:E...` URI'lerine subClassOf
ile bağlıydı. HG namespace'i tek başına gösterildiğinde (dashboard viz'lerinde)
36 node yetim görünüyordu.

**Çözüm §4:**

- **26 HG-internal `rdfs:subClassOf` edge:**
  - `Birth / Formation / Production ⊏ BeginningOfExistence`
  - `Death / Dissolution / DestructionEvent ⊏ EndOfExistence`
  - `TransferOfCustody / ConditionAssessment / Modification ⊏ CurationActivity`
  - `Acquisition / Move ⊏ ProvenanceActivity`
  - `Title ⊏ Name`, `Inscription ⊏ LinguisticObject`
  - `DigitalObject / LinguisticObject / PropositionalObject / Metadata / Container ⊏ InformationObject`
  - `Set ⊏ CuratedHolding`
  - `DataCustodian ⊏ Actor`
  - `HeritageAssertion / Verification / SyncreticRelationship ⊏ AttributeAssignment`
  - `LivingGoddessTenure ⊏ Period`

- **29 HG-internal object property** (domain → range hepsi HG namespace):
  `carries_inscription`, `has_dimension`, `has_visual_item`,
  `has_digital_representation`, `has_right`, `subject_to_legal_object`,
  `identified_by_identifier`, `identified_by_name`, `identified_by_title`,
  `was_born_by`, `died_in_event`, `was_formed_by`, `dissolved_by`,
  `was_modified_by`, `was_moved_by`, `was_acquired_through`,
  `was_encountered_in`, `was_measured_by`, `measurement_observes`,
  `dimension_has_unit`, `amount_in_currency`, `acquisition_amount`,
  `has_language`, `member_of_set`, `holds_item`, `occurs_during_period`,
  `about_proposition`, `has_metadata`, `has_data_custodian`.

Sonuç: 273 → 438 triple, 36 → 0 yetim.

Görsel: `docs/heritagegraph-alignment-graph.html` (interactive D3 force-directed).

## 7. Migration pipeline

### Template mimarisi (Temmuz 2026'da düzeltilen önemli ayrıntı)

**Runtime template'leri `scripts/migrate_lux_to_hg.py` içindeki
`TRANSFORM_TEMPLATES` dict'idir** (INSERT WHERE + pagination).
`queries/lux_to_hg_migration.sparql` aynı mantığın insan-okunur CONSTRUCT
referansıdır ve artık CI'ın ayrı ayrı parse edebilmesi için
`# === tN_label ===` başlıkları taşır. İkisi senkron tutulmalı.
(Temmuz öncesi: .sparql 9 template gösteriyordu, runtime'da yalnız 7 vardı —
concept ve identifier/name template'leri hiç çalışmıyordu.)

### 10 runtime template (`TRANSFORM_TEMPLATES`)

1. `object` — E22 → hg:HumanMadeObject (+ carries_inscription, has_dimension, has_visual_item)
2. `person` — E21 → hg:Person (+ was_born_by / died_in_event)
3. `group` — E74 → hg:Group (+ was_formed_by / dissolved_by)
4. `place` — E53 → hg:Place
5. `activity` — 30+ arm: Production, Modification, Move, TransferOfCustody,
   Purchase, Acquisition, Birth, Death, Formation, Dissolution, Joining,
   Leaving, Destruction, Transformation, PartAddition, PartRemoval,
   Encounter (sci:S19), CurationActivity, Measurement, ConditionAssessment,
   IdentifierAssignment, TypeAssignment, Creation, BeginningOfExistence,
   EndOfExistence, **la:Payment, la:Transfer, la:Addition→SetAddition,
   la:Removal→SetRemoval, la:RightAcquisition** + guard'lı fallback'ler:
   generic E13→AttributeAssignment, E7→Activity (ProvenanceActivity
   wrapper'ları artık düşmüyor), E5→HistoricalEvent, E4→Period
6. `work` — E33 (E34 hariç), E34→Inscription, E35→Title, E36 (E37 hariç),
   E37→Mark, E89, E32→AuthorityDocument, E31→DataSource, dig:D1
7. `set` — la:Set + E78
8. `concept` — E55→Concept (özelleşmişler hariç), E56/E57/E58/E97/E98/E72/E99
9. `identifier_name` — E42, E33_E41, generic E41→Appellation
10. `embedded` — E52 TimeSpan, E54 Dimension, E30 Right, la:DigitalService,
    E20 BiologicalObject, E26/E27/E25, E93 Presence, E3 ConditionState
    (3.47M → 98k düşük dönüşüm oranının ana nedeni bu embedded düğümlerin
    hiç transform edilmemesiydi)

### `queries/validation_queries.sparql`

8 query, ilk 2'si **hard gate** (0 satır dönmezse migration fail):

- **V1** — Unmapped LUX class detection
- **V2** — sameAs consistency check
- V3–V8 — coverage %, count parity, orphan detection, dangling ref, etc.

### `scripts/migrate_lux_to_hg.py`

~590 satır, 4 mode:

```bash
--mode crawl      # LUX REST API'den çek (RING_MODE=crawl için)
--mode transform  # Loaded LUX data üzerinde 9 template çalıştır
--mode validate   # 8 query çalıştır, exit 1 if V1/V2 fail
--mode delta      # Yale diff feed'den delta çek + transform + validate
```

Ortak: SPARQL INSERT WHERE + LIMIT/OFFSET pagination, resume-friendly state
file (`/work/state/migration.state.json`).

### 7-phase orchestrator (`docker/migrator/entrypoint.sh`)

State flag'li idempotent (her phase için `/work/state/pN.done`):

```
P1: fetch_dump      - LUX dump veya crawl
P2: load_lux        - .nq → oxigraph named graph
P3: load_hg         - HeritageGraph.ttl + alignment.ttl
P4: transform       - 9 template çalıştır
P5: validate        - V1+V2 hard gate
P6: snapshot        - oxigraph_data backup (opsiyonel)
P7: master.done     - final marker
```

## 8. Delta sync (haftalık)

### Konfigürasyon

Yale diff endpoint: `https://linked-art.lux.collections.yale.edu/data/diffs/latest.nq.gz`
(Change Discovery / ActivityStreams pattern).

Schedule variables (`docker/.env`):

```bash
# Klasik cron (backward-compat):
DELTA_CRON=0 4 * * MON

# Yeni pure-bash scheduler için split variables (opsiyonel):
DELTA_DAY=1        # 1=Mon..7=Sun
DELTA_HOUR=04
DELTA_MIN=00

# Test için:
DELTA_RUN_ON_START=1   # container start'ında bir kez tetikle
```

### Pure-bash scheduler (`docker/migrator/delta_loop.sh`)

Supercronic v0.2.34 fork-exec fail nedeniyle değiştirildi
(bkz. Bölüm 10, Bug 1). Şimdi ~120 satır pure bash:

- 30 saniyelik polling: `date +%u/%H/%M` karşılaştırması
- `trap TERM INT` graceful shutdown
- `LAST_FIRE_KEY` double-fire koruması (aynı dakika içinde tekrar çalışmasın)
- 90s "after-fire" cooldown
- Hem `DELTA_CRON` hem yeni split env vars'ı parse eder

## 9. Makefile target'ları

### Local stack
- `make up` / `down` / `logs` / `status`
- `make migrate` / `validate` / `snapshot` / `restore`
- `make reset` / `reset-everything`
- `make shell` / `sparql Q="..."` / `delta-now`

### Alignment reload
- `make reload-alignment` — CLEAR GRAPH + POST alignment TTL
- `make ssh-reload-alignment` — remote versiyonu

### CI-style local kontrol
- `make ttl-check` — rdflib ile TTL parse
- `make sparql-check` — SPARQL syntax
- `make py-check` — py_compile
- `make ci-local` — hepsini çalıştır

### Deploy
- `make deploy` — rsync + build + up
- `make deploy-no-build` — sadece rsync + recreate
- `make deploy-dry-run`
- `make deploy-bootstrap` — bir kereye mahsus server prep

### Remote (SSH)
- `make ssh` / `ssh-logs` / `ssh-status` / `ssh-shell`
- `make ssh-backup-pull` — remote snapshot + local'e çek
- `make ssh-tunnel` — 7878'i localhost'a forward

## 10. Deploy sürecinde çözülen bug'lar

### Bug 1 — Delta-syncer crashloop (supercronic)

- **Symptom:** container her 60 saniyede restart, log:
  ```
  time="..." level=info msg="reaping dead processes"
  time="..." level=fatal msg="Failed to fork exec: no such file or directory"
  ```
- **Root cause:** supercronic v0.2.34'ün cron-line parser'ı `0 4 * * MON`
  içindeki `MON`'u command olarak yorumlayıp fork-exec deniyordu.
- **Fix:** supercronic tamamen çıkarıldı; `delta_loop.sh` pure-bash polling
  loop'a çevrildi.
- **Commit:** `659abd2 Replace supercronic with pure-bash scheduler in
  delta-syncer`

### Bug 2 — Oxigraph "unhealthy" etiketi

- **Symptom:** `docker compose ps` → `hg-oxigraph  Up 9 days (unhealthy)`
- **Root cause:** Docker Compose healthcheck `wget` kullanıyor ama oxigraph
  0.4.x `gcr.io/distroless/cc-debian12:nonroot` üzerine build edilmiş — shell,
  wget, curl yok. Test her seferinde exit 1 dönüyor.
- **Fix:** healthcheck tamamen kaldırıldı. Bağımlı servisler zaten
  `condition: service_started` kullanıyordu, yani bu cosmetic bir sorundu.

### Bug 3 — `make status` Python syntax error

- **Symptom:**
  ```
  File "<string>", line 2
      import json,sys; \
  ...
  SyntaxError: invalid syntax
  ```
- **Root cause:** `python3 -c '...'` içindeki `\` continuation Python
  tarafından anlaşılmıyor (heredoc değil, tek string).
- **Fix:** multi-line yerine tek satırlık list comprehension:
  ```python
  python3 -c "import json,sys; [print('  %-60s %s' % (r['g']['value'], r['n']['value'])) for r in json.load(sys.stdin)['results']['bindings']]"
  ```

### Bug 4 — `make reload-alignment` curl URL parse fail

- **Symptom:** `curl: (3) URL using bad/illegal format or missing URL`
- **Root cause:** Single quote içinde `${OXIGRAPH_PORT:-7878}` bash tarafından
  expand edilmedi; curl literal `${OXIGRAPH_PORT:-7878}` gördü.
- **Fix:** Single quote → double quote (`?` glob'u zaten URL context'te
  problem değil).

### Bug 5 — Yetim class nodları (Niraj feedback)

- **Symptom:** HG dashboard viz'inde 36 class node kenarı olmadan boşta
  duruyordu.
- **Root cause:** §3'teki yeni class'lar sadece dış (`crm:E...`) URI'lere
  subClassOf ile bağlıydı; HG-only view dış edge'leri saklıyordu.
- **Fix:** Section 4 eklendi — 26 HG-internal subClassOf + 29 HG-internal
  object property.
- **Commit:** `d51214b Wire orphan classes into HG graph (Niraj feedback)`

### Bug 6 — CI sparql-syntax job'ı hiç doğru çalışmıyordu (Temmuz 2026)

- **Symptom:** Lokal simülasyonda migration dosyası "tek blok" olarak parse
  edilip patlıyor; validation dosyasında V6 "Unknown namespace prefix hg"
  veriyordu.
- **Root cause (2 ayrı hata):** (1) Split regex'i `# ====...` banner
  satırlarını label sanıyor, preamble'daki PREFIX'leri yutuyordu.
  (2) `is_update` tespiti `\bMove\b` gibi kelimeleri `hg:Move` URI'sinde
  yakalayıp CONSTRUCT'ı update olarak parse ettiriyordu.
- **Fix:** Regex script'teki katı biçime eşitlendi
  (`# *={3,}[ \t]+(\S+)`); keyword tespiti satır başına sabitlendi
  (`(?mi)^\s*(WITH|INSERT|...)`). Migration dosyasına `# === tN ===`
  başlıkları eklendi.

### Bug 7 — `build_mapping.py` stale mutlak path

- **Symptom:** CI'ın "regenerate XLSX and diff" adımı runner'da
  `FileNotFoundError` ile düşer (eski bir Claude sandbox path'i
  `/sessions/fervent-gallant-heisenberg/...` hard-code'luydu).
- **Fix:** `OUT_XLSX` script konumuna göre relative yapıldı
  (`mapping/HeritageGraph_LUX_Mapping.xlsx`).

### Bug 8 — Bootstrap'taki HeritageGraph.ttl URL'i 404

- **Symptom:** `server-bootstrap.sh` fetch adımı 404 (upstream repo
  `HeritageGraph` branch'ini kaldırmış; ontoloji `main`'de).
- **Fix:** `main` branch önce denenir, eski branch fallback olarak kaldı.
- **Not:** Upstream repo'da `HeritageGraphh.ttl` (çift h) typo dosyası da
  duruyor — CAIR ekibine bildirilebilir.

## 11. Environment variables (`docker/.env.example`)

```bash
# ---- Ring (scope) ------------------------------------------------------------
RING_MODE=crawl                # pilot / domain / full / dump / crawl
LIMIT_PER_QUERY=10000          # 0 = unlimited
BATCH_SIZE=50000               # SPARQL INSERT WHERE pagination

# ---- LUX source --------------------------------------------------------------
LUX_DUMP_URL=                  # Yale ITS'den bulk dump URL (opsiyonel)
# LUX_DUMP_PATH=/work/lux/lux.nq   # locally mounted alternative
LUX_FILTER=religious heritage  # crawl mode için search q= param
CRAWL_RPS=10                   # polite rate limit

# ---- Delta -------------------------------------------------------------------
# DELTA_URL=                   # override; default `linked-art.lux.collections.yale.edu/data/diffs/latest.nq.gz`
DELTA_CRON=0 4 * * MON         # legacy cron; parsed by pure-bash scheduler
# DELTA_DAY=1                  # yeni ayrık env vars (opsiyonel)
# DELTA_HOUR=04
# DELTA_MIN=00
# DELTA_RUN_ON_START=1         # test için: start'ta bir kez tetikle

# ---- Validation --------------------------------------------------------------
VALIDATION_MODE=strict         # strict = V1/V2 fail → migration fail; lenient = warn+continue

# ---- Networking --------------------------------------------------------------
OXIGRAPH_PORT=7878

# ---- Resource limits ---------------------------------------------------------
OXIGRAPH_MEM_LIMIT=64g
MIGRATOR_MEM_LIMIT=8g
```

## 12. CI (GitHub Actions, `.github/workflows/ci.yml`)

5 parallel job, `push`/`pull_request` on `main`:

| Job | Ne yapar | Regresyon assertion'ı |
|---|---|---|
| `ttl-parse` | Her `alignment/*.ttl`'i rdflib parse | `≥10 equivalentClass, ≥30 subPropertyOf` |
| `python-lint` | ruff + py_compile + XLSX row-count drift | XLSX regenerate → row count değişmedi mi |
| `sparql-syntax` | Her labeled SPARQL block'u `prepareQuery/Update` | 0 error |
| `docker-lint` | `docker compose config -q` + hadolint | failure-threshold: warning |
| `shell-syntax` | `bash -n` + shellcheck | 0 syntax error |

## 13. Sık kullanılan komutlar (cheat sheet)

```bash
# Lokal geliştirme
make up                     # docker stack başlat
make logs                   # tail
make migrate                # bir kez daha migrator çalıştır
make ci-local               # TTL/py sanity check
make reload-alignment       # alignment TTL değişti → oxigraph'a yeniden yükle

# Server ops
make ssh-status             # docker ps + triple count
make ssh-reload-alignment   # remote alignment reload
make deploy                 # rsync + recreate
make deploy-no-build        # sadece kod (Dockerfile değişmediyse)
ssh root@server42.dnsbilisim.net 'docker logs --tail=50 hg-delta-syncer'

# Ad-hoc SPARQL
make sparql Q="SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }"

# Direkt curl ile alignment reload (Makefile'sız):
ssh root@server42.dnsbilisim.net '
  curl -sSf -X POST "http://localhost:7878/update" \
    --data-urlencode "update=CLEAR GRAPH <https://w3id.org/heritagegraph/alignment/lux>" \
    -H "Content-Type: application/x-www-form-urlencoded"
  curl -sSf -X POST "http://localhost:7878/store?graph=https://w3id.org/heritagegraph/alignment/lux" \
    -H "Content-Type: text/turtle" \
    --data-binary @/root/github/heritagegraph-lux-migration/alignment/heritagegraph-lux-alignment.ttl
'
```

## 14. Commit tarihçesi (referans)

```
7b47c14  Initial release: HeritageGraph ↔ LUX migration v0.1.0
2c89eb1  Fix end-to-end migration: 7 issues found during first production run
d51214b  Wire orphan classes into HG graph (Niraj feedback)         ← §4 orphan fix
659abd2  Replace supercronic with pure-bash scheduler in delta-syncer  ← Bug 1
```

## 15. Bilinen kısıtlar ve TODO

- **Yale IPv4 blok:** Hetzner IPv4 range'i CloudFront tarafından 403 alıyor.
  Migrator `network_mode: host` + IPv6 üzerinden erişiyor. Delta-syncer
  bridge network'te ama gerekirse aynı workaround uygulanabilir.
- **Bulk dump URL yok:** Yale public bir `.nq.gz` yayınlamıyor.
  `docs/LUX_DATA_DOWNLOAD.md` beş gerçek acquisition yolu belgeler (A: Yale
  ITS email, B: ActivityStreams, C: REST crawl, D: LuxY, E: subset).
- **`HeritageGraph.ttl` gitignored:** Kurulum sırasında
  `raw.githubusercontent.com/CAIRNepal/heritagegraphontology/main/HeritageGraph.ttl`
  adresinden fetch edilir (bkz. `server-bootstrap.sh`; eski `HeritageGraph`
  branch URL'i 404 — Bug 8).
- **Two-rater alignment audit:** Şu an tek-rater; paper'ın future work'ünde.
  §5 pragmatik parent'ları (özellikle `hg:Presence ⊏ hg:Period`,
  `hg:BiologicalObject ⊏ hg:PhysicalHeritageThing`,
  `hg:CuratedHolding ⊏ hg:PhysicalHeritageThing`) inceleme listesinin başına.
- **DEPLOY GEREKLİ (Temmuz 2026 gap audit sonrası):** §5 + yeni template'ler
  henüz sunucuda değil. Sıra: `make deploy` → `make ssh-reload-alignment` →
  transform state'ini sıfırlayıp (`migration.state.json` içindeki yeni
  template label'ları zaten yok, dokunmaya gerek yok — `concept`,
  `identifier_name`, `embedded` ve genişletilmiş arm'lar ilk çalıştırmada
  işler) `--mode transform` re-run → `--mode validate`. `imported/lux`
  triple sayısında belirgin artış beklenir (embedded düğümler dahil).
- **V3 count parity:** Yeni class'lar geldikten sonra ±5 % eşiği ilk run'da
  gürültülü olabilir; V1/V2 hard gate esas.
- **DEPLOY GEREKLİ (§6 alpha5 sync sonrası, 2026-07-26):** yukarıdaki gibi
  §5 deploy'u da henüz yapılmamışken §6 üzerine geldi — ikisi birlikte
  deploy edilmeli. Ayrıca `--mode transform` daha önce çalıştıysa,
  `imported/lux` grafiğinde artık stale `heritageGraph:Person` /
  `heritageGraph:HumanMadeObject` / … tipli düğümler olabilir (12 class);
  bunlar yeni `crm:` tipli düğümlerle ÇAKIŞMAZ ama aynı kaydın iki farklı
  tipte iki kopyası olarak kalır. Re-deploy sonrası `--mode transform`
  öncesi `imported/lux` graph'ının temizlenmesi (`CLEAR GRAPH`) veya bir
  `--mode delta`/full re-run önerilir — kısmi re-run yeterli olmayabilir.
- **`server-bootstrap.sh` düzeltildi (2026-07-26):** artık önce
  `HeritageGraph` branch'inin `ontology/HeritageGraph.ttl` yolunu dener
  (alpha5 layout), sonra o branch'in eski kök yolunu, en son `main`'i
  (bilinen stale, son çare). Henüz sunucuda test edilmedi — bir sonraki
  `make deploy-bootstrap`'ta doğrulanmalı.

---

## Ekstra: TGDK paper entegrasyonu için özet

CAIR Nepal ekibi (Karki, Oli, Sapkota, Chhetri) HeritageGraph'ı TGDK'ya
gönderiyor (Special Issue: Semantic Digital Humanities). Bu bridge çalışması
paper'daki üç zayıflığı doğrudan güçlendiriyor:

1. **§5.8 "population at scale is future work"** → mevcut prototype:
   3.47M raw LUX triple'dan 98,131 HG-conformant triple materialise edildi.
2. **§5.6 tek-rater alignment audit** → LUX JSON-LD context'e karşı
   independent verification (6 material hata yakalanıp düzeltildi).
3. **§6 "federation with major aggregators" future work** → Linked Art
   ekosistemi ile working federation prototipi zaten canlıda.

Paper LaTeX patches için: bu repo'da `docs/PAPER_PATCH_v2.md` (eğer
oluşturulduysa) veya doğrudan Chhetri ile koordinasyon.
