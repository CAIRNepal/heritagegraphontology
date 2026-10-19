# LUX verilerini nasıl indireceğiz?

**Status (May 2026):** Yale, LUX için tek-tıkla bir bulk N-Quads / Turtle dump'ı *kamuya açık olarak yayınlamıyor.* Önceki `MIGRATION_PLAN.md` ve docker stack'inde `https://linked-art.lux.collections.yale.edu/data/dump/latest.nq.gz` URL'i benim varsayımımdı, gerçek bir endpoint değil. Bu belge gerçek alternatifleri sıralar.

## TL;DR — Tavsiye edilen yol

> **Birinci tercih:** Yale ITS'e bir e-posta atın (Robert Sanderson / LUX team, [lux@yale.edu](mailto:lux@yale.edu)). CAIR Nepal'ın akademik amaçlı kullanım için bulk dump talebi büyük olasılıkla onaylanır. Bu beklerken paralelde alttaki **(C) REST crawl + IIIF Change Discovery** yolunu başlatın.
>
> **Pilot (10K kayıt, ~30 dk):** Hemen başlayın — `migrate_lux_to_hg.py --mode crawl` LUX'un public Search API'sini kullanır.
>
> **Tam migration (16M kayıt):** Yale dump'ını alana kadar, **IIIF Change Discovery / ActivityStreams** üzerinden incremental harvest yapın (3-4 gün sürer ama Yale'in resmi olarak desteklediği yöntem budur).

---

## Mevcut beş gerçek seçenek

### A) Yale ITS'den bulk dump talep et — **EN İYİ**

**Nasıl:** Robert Sanderson (LUX yöneticisi, Yale ITS) veya `lux@yale.edu` adresine kısa bir akademik kullanım talebi yazın. LUX takımı 2023'ten beri araştırma projelerine destek veriyor; Linked Art topluluğunun da bir parçasısınız (LUX'un kendisi Linked Art uygulamasıdır).

**E-posta şablonu:**

```
Subject: Bulk LUX data export request — CAIR Nepal HeritageGraph project

Dear LUX team,

We are building HeritageGraph (https://github.com/CAIRNepal/heritagegraphontology),
a Linked Art–aligned ontology and triplestore for Nepali cultural heritage.
For a forthcoming Nature-portfolio paper we want to enrich HeritageGraph with
relevant LUX records via ontology alignment (paper draft attached).

Would Yale be able to share a bulk JSON-LD / N-Quads export of the LUX dataset,
or guide us to the most appropriate harvest endpoint for ~16M records?

We will cite Yale appropriately and preserve provenance via owl:sameAs links
back to the original LUX URIs.

Thank you,
[Tek Raj Chhetri], CAIR Nepal
```

**Süre:** 1-2 hafta (insan response time).
**Sonuç:** Muhtemelen onaylanır; Yale resmi dump verir veya doğrudan AWS S3 bucket'larına erişim sağlar.
**Risk:** Düşük — Linked Art topluluğu işbirliğine açıktır.

### B) IIIF Change Discovery + ActivityStreams — Yale'in resmi senkronizasyon yolu

LUX'un kendi data-pipeline'ı (https://github.com/project-lux/data-pipeline) tüm dış kaynakları **ActivityStreams** üzerinden harvest ediyor. Yale **kendi datasetini de aynı protokolle dışarıya açıyor.** Bu, "milyonlarca kayıt indir" için doğru endüstri standardı.

**Endpoint'ler** (probe edilmesi gereken):
```
https://lux.collections.yale.edu/api/.well-known/activity-streams
https://lux.collections.yale.edu/data/activity-stream
https://lux.collections.yale.edu/activity-stream
```
*(Tam URL Yale'in sürekli olarak yayınlamadığı versiyona göre değişiyor — `discover_lux_endpoints.sh` ile probe edin.)*

**Format:** [IIIF Change Discovery 0.9 spec](https://iiif.io/api/discovery/0.9/). OrderedCollection → OrderedCollectionPage → her sayfada ~100-1000 Activity (Create/Update/Delete) → her Activity bir record URL'ine işaret eder.

**Yale'in kendi harvester'ı:** `project-lux/data-pipeline` reposundaki `sources/*/Harvester` class'ları bu protokolü implement ediyor. Bizimki için modifiye edilmiş bir versiyonu `migrate_lux_to_hg.py --mode activitystreams` modu olarak ekleyebilirim (aşağıda).

**Süre:** Tam dataset için ~3-4 gün (rate-limit'e bağlı).
**Avantaj:** Resume capability built-in; sadece değişen kayıtları çekme imkanı (incremental sync için zaten gereken altyapı bu).

### C) REST per-record crawl — başlatması en kolay

Her LUX kaydı `https://lux.collections.yale.edu/data/{type}/{uuid}` URL'inde JSON-LD olarak duruyor. Search API ile UUID'leri toplayıp, her birini paralel olarak indirebilirsiniz.

**Pilot için ideal:**
```bash
python migrate_lux_to_hg.py --mode crawl \
    --filter "religious heritage Nepal" \
    --concurrency 16 \
    --out /work/lux/lux_crawled.jsonl
```

**Tam dataset için:** Search API her sorguda ~200 kayıt veriyor (page boyutu). Çok kabaca 16M ÷ 200 = 80,000 sayfa. 80K HTTP request + 16M individual record fetch = ~16-17M HTTP. 100 req/s'de **~1.8 gün**. 50 req/s'de **~3.7 gün**. Yale'in rate-limit'i tam belli değil — kendi `data-pipeline`'larında varsayılan 10 req/s; biz buna saygı duymalıyız.

**Avantaj:** Hemen başlar, hiçbir koordinasyon gerektirmez.
**Dezavantaj:** Yavaş; rate-limit'le risk var; tüm dataseti çekiyorsa Yale'i rahatsız edebilir.

### D) LuxY Python wrapper — Yale'in resmi API library'si

[project-lux/luxy](https://github.com/project-lux/luxy) Yale'in kendi Python wrapper'ı. Bizim crawl modumuzla aynı işi yapar ama Yale-blessed, retry/throttle ile gelir.

```bash
pip install luxy
python -c "
from luxy import LuxClient
c = LuxClient()
for rec in c.search.objects(q='religious heritage'):
    print(rec['id'])
"
```

**Kullanım yerimiz:** `migrate_lux_to_hg.py --mode crawl` modunun bir varyantı olarak entegre edebiliriz. Bizim ham `requests`-tabanlı crawl'a göre daha "kibar" ve sürdürülebilir.

### E) Selective subset — sadece ilgi alanımızı çek

Pilot'tan sonra, full LUX yerine sadece **bizim ilgi alanımıza giren** LUX kayıtlarını alın:

```python
filters = [
    'classified_as:religious_object',          # AAT 300263552
    'classified_as:hindu OR buddhist',
    'place:nepal OR india OR tibet OR bhutan',
    'material:bronze OR stone OR thangka',
]
```

Tahmin: 16M total → ~50-200K Asya/dini miras kaydı. Crawl süresi: **~6-12 saat.**

**Bu büyük olasılıkla CAIR Nepal'ın gerçekten ihtiyaç duyduğu şey** — paper "we ingested LUX" demek için yeterli, ama Yale'in tamamını sunucuda host etmek hem disk hem semantic olarak savurganlık olabilir. Tek Raj'ın 8 Nisan'daki notu: "*we want to enrich our db with data*" — *zenginleştirme* için Asya odaklı subset zaten yeterli.

---

## Karar matrisi

| Yol | Süre | Risk | Ekibe önerim |
|---|---|---|---|
| **A** Yale'den dump iste | 1-2 hafta bekleme | düşük; akademik işbirliği | Paralel olarak gönder, bekleme yapma |
| **B** ActivityStreams | 3-4 gün | orta; rate-limit ihtimali | Yale resmi yolu; full migration için doğru seçenek |
| **C** REST crawl | 2-4 gün (full), 30 dk (pilot) | rate-limit; ToS ihlali ihtimali | Pilot için ideal, full için riskli |
| **D** LuxY wrapper | C ile aynı | düşük; Yale-blessed | Sürdürülebilir alternatif |
| **E** Selective subset | 6-12 saat | düşük | **Production için en pratik** |

**Benim tavsiyem:**

1. **Bu hafta:** Yale'e e-posta gönderin (A) + `discover_lux_endpoints.sh` ile gerçek endpoint'leri probe edin.
2. **Aynı zamanda:** REST crawl ile 10K-record pilot çalıştırın (C, pilot mod). Alignment'ın gerçek LUX verisinde çalıştığını doğrulayın.
3. **Yale yanıtı geldiğinde:** Bulk dump'ı kabul edin → `oxigraph load` ile yükleyin → 4-12 saatte bitirin.
4. **Yale yanıt vermezse:** ActivityStreams (B) ile devam edin ya da Selective subset (E) ile sınırlı kalın. Paper için "Nepal/Asya odaklı subset" daha güçlü bir hikaye.

---

## Şu anda yapmanız gerekenler — somut adımlar

```bash
# 1. Gerçek endpoint'leri probe et
cd docker
bash discover_lux_endpoints.sh > /tmp/lux_endpoints.log
cat /tmp/lux_endpoints.log

# 2. Yale'e e-posta gönder (yukarıdaki şablon)

# 3. Bu arada pilot crawl başlat (10K kayıt, Asya odaklı)
cp .env.example .env
# .env'de:  RING_MODE=crawl
#           LUX_FILTER="religious heritage"
#           LIMIT_PER_QUERY=10000
docker compose up -d
docker compose logs -f migrator

# 4. Yale'den dump gelirse:
#    mv /path/to/yale_dump.nq.gz docker/lux/
#    .env'de: RING_MODE=full,  LUX_DUMP_PATH=/work/lux/yale_dump.nq.gz
#    make reset && docker compose up -d migrator
```

---

## Düzeltilmiş dosyalar

Sahte dump URL'i kaldırıldı:

* `docker/.env.example` — `LUX_DUMP_URL` artık opsiyonel ve commented-out. Default mode `crawl` (önce probe et).
* `docker/migrator/entrypoint.sh` — `LUX_DUMP_URL` set edilmezse otomatik olarak crawl moduna düşer.
* `docker/discover_lux_endpoints.sh` — yeni script: gerçekten canlı endpoint'leri raporlar.

---

## Hukuki / etik not

LUX dataseti büyük ölçüde **CC BY 4.0** (Yale'in kendi metadata'sı) ama bazı kayıtlar 3. taraflardan geliyor (AAT, ULAN, Wikidata) ve onların ayrı lisansları var. Bulk re-hosting yapacaksanız:

* Yale'e kullanım niyetinizi bildirmek **zorunlu değil ama nazik**.
* `owl:sameAs` ile orijinal URI'leri korumamız (zaten migration'da yapıyoruz) provenance açısından kritik.
* HeritageGraph'ı public expose edecekseniz, Yale'in attribution metnini koyun.

Sources:
- [LUX: Yale Collections Discovery](https://lux.collections.yale.edu/)
- [project-lux/data-pipeline (Yale's harvester)](https://github.com/project-lux/data-pipeline)
- [project-lux/luxy (Python wrapper)](https://github.com/project-lux/luxy)
- [IIIF Change Discovery API 0.9](https://iiif.io/api/discovery/0.9/)
- [Yale's announcement of LUX](https://news.yale.edu/2023/06/01/17-million-reasons-love-lux-yales-new-collections-search-tool)
