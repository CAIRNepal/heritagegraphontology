# Deploy to `server42.dnsbilisim.net`

Bu playbook stack'i `server42.dnsbilisim.net` üzerine, stock-pattern-scanner ile aynı düzende deploy eder:

```
/root/github/heritagegraph-lux-migration/
├── docker-compose.yml
├── .env                            ← gitignored, secrets içerir
├── alignment/HeritageGraph.ttl
├── alignment/heritagegraph-lux-alignment.ttl
├── queries/lux_to_hg_migration.sparql
├── queries/validation_queries.sparql
├── migrator/Dockerfile
├── migrator/entrypoint.sh
├── migrator/delta_loop.sh
├── migrator/migrate_lux_to_hg.py
├── Makefile
├── deploy.sh                       ← lokalden çalışır
├── server-bootstrap.sh             ← sunucuda tek-seferlik
└── discover_lux_endpoints.sh
```

## 0. Önkoşullar (lokal makineniz)

* SSH key'iniz `server42`'de `/root/.ssh/authorized_keys`'te olmalı. Test:
  ```bash
  ssh root@server42.dnsbilisim.net 'hostname && df -h / && free -h'
  ```
* `rsync` ve `bash` (Linux/macOS lokal). Windows için WSL veya Git Bash.

## 1. İlk kurulum — yalnızca bir kez

### 1a. Lokalden sunucuya bootstrap dosyalarını kopyala

```bash
cd <package>/docker
rsync -avz --progress \
      server-bootstrap.sh discover_lux_endpoints.sh \
      root@server42.dnsbilisim.net:/root/
```

### 1b. Sunucuda bootstrap'ı çalıştır

```bash
ssh root@server42.dnsbilisim.net
bash /root/server-bootstrap.sh
```

Bootstrap şunları yapar (idempotent, yeniden çalıştırılabilir):

1. Docker + Docker Compose v2 plugin kontrol/kurulum
2. `/root/github/heritagegraph-lux-migration/` dizinini oluştur
3. Disk + RAM sanity check
   * `< 100 GB free disk` → uyarı (pilot için yeter ama full migration için yetmez)
   * `< 16 GB RAM` → uyarı (full ring için yeter değil)
4. `.env.example` → `.env` (yoksa kopyala)
5. `HeritageGraph.ttl`'yi GitHub'dan indir → `alignment/`
6. `systemd` unit yükle (`/etc/systemd/system/heritagegraph-lux.service`)
7. `logrotate` config (`/etc/logrotate.d/heritagegraph-lux`) — `/root/github/heritagegraph-lux-migration/logs/*.log` 14 günlük rotate
8. `discover_lux_endpoints.sh` çalıştır → `/root/lux_endpoint_probe.log`'a yaz

Bootstrap çıktısında **sonraki adım komutu** verir, kopyala-yapıştır.

### 1c. LUX endpoint probe sonucunu incele

```bash
ssh root@server42.dnsbilisim.net 'cat /root/lux_endpoint_probe.log'
```

Probe sonucuna göre:
* Search API `✅` → `RING_MODE=crawl` ile devam edebilirsiniz
* ActivityStreams endpoint'lerinden biri `✅` → `RING_MODE=activitystreams` (henüz implement edilmedi; talep edilirse eklerim)
* Hiçbiri çalışmıyor → Yale ITS'e e-posta gönderin (`LUX_DATA_DOWNLOAD.md` → şablon A)

## 2. İlk deployment

### Seçenek 1 — rsync push (önerilen, github'a push gerektirmez)

Lokal makineden:

```bash
cd <package>/docker
./deploy.sh
```

`deploy.sh` şunları yapar:

1. Pre-flight (SSH erişim, .env mevcut mu, alignment/HeritageGraph.ttl mevcut mu)
2. rsync ile dosyaları `/root/github/heritagegraph-lux-migration/` altına kopyalar (`.env`, `logs/`, `state/`, `lux/`, `backups/` hariç — bunlar sunucuya özgü)
3. SSH ile sunucuda `docker compose up -d --build`
4. Migrator logu canlı tail eder (`Ctrl-C` ile kopuş normal — container devam eder)

### Seçenek 2 — git pull (sürdürülebilir, github repo gerekir)

Eğer kodu github'a (örn. `CAIRNepal/heritagegraph-migration`) push'larsanız:

```bash
# Sunucuda — ilk kurulum
ssh root@server42.dnsbilisim.net
cd /root/github
git clone https://github.com/CAIRNepal/heritagegraph-migration.git heritagegraph-lux-migration
cd heritagegraph-lux-migration
cp .env.example .env && $EDITOR .env
docker compose up -d --build

# Sunucuda — sonraki güncellemeler
cd /root/github/heritagegraph-lux-migration
git pull origin main
docker compose up -d --build
```

## 3. İlk run'da ne olur

`docker compose up -d --build` çalıştırıldığında:

1. **oxigraph** container ayağa kalkar (~30 s; ilk image pull birkaç dakika)
2. **migrator** healthcheck'i bekler, sonra 7 fazlı pipeline'ı çalıştırır:
   * P1 — `LUX_FILTER`'a göre REST crawl başlar (~30 dk, 10K kayıt, pilot mod)
   * P2 — JSON-LD'yi N-Quads'a çevirir, Oxigraph'a yükler
   * P3 — alignment.ttl + HeritageGraph.ttl yüklenir
   * P4 — batched INSERT WHERE (9 query, ~10-15 dk)
   * P5 — V1/V2 validation hard gate
   * P6 — snapshot reminder
   * P7 — `master.done` flag
3. **delta-syncer** migrator başarıyla bittiyse uyanır, supercronic ile haftalık beklemeye geçer
4. Migrator exit 0 yapar — container "Exited (0)" görünür, normaldir

İlk pilot ~30-45 dk sürer.

## 4. İzleme

### Canlı log

```bash
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && docker compose logs -f --tail=200'
# veya tek servis:
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && docker compose logs -f --tail=200 migrator'
```

### Durum

```bash
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && make status'
```

Output:
```
NAME              STATUS                       PORTS
hg-oxigraph       Up 12 minutes (healthy)      0.0.0.0:7878->7878/tcp
hg-migrator       Exited (0) 8 minutes ago
hg-delta-syncer   Up 7 minutes

Triple counts:
  https://lux.collections.yale.edu/                              3,210,000
  https://cair-nepal.org/heritagegraph/                                  120
  https://cair-nepal.org/heritagegraph/alignment/lux                     273
  https://cair-nepal.org/heritagegraph/imported/lux                  120,000
```

### Ad-hoc SPARQL sorgu

```bash
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && \
    make sparql Q="SELECT (COUNT(*) AS ?n) WHERE { GRAPH <https://cair-nepal.org/heritagegraph/imported/lux> { ?s a ?t } }"'
```

Lokalden SPARQL erişimi (Oxigraph 7878 portu sunucuda local-only; SSH tunnel ile aç):

```bash
ssh -L 7878:127.0.0.1:7878 root@server42.dnsbilisim.net
# Şimdi browser'da: http://localhost:7878/  — Oxigraph SPARQL UI
```

## 5. Pilot'tan full migration'a geçiş

Pilot başarılı olduktan ve V1/V2 PASS dedikten sonra:

```bash
ssh root@server42.dnsbilisim.net
cd /root/github/heritagegraph-lux-migration

# .env'yi düzenle:
$EDITOR .env
#   RING_MODE=crawl                       (Yale dump alabildiyseniz: full)
#   LIMIT_PER_QUERY=0                     (sınırsız)
#   LUX_FILTER="*"                        (filtre kaldır) veya hedefli kalsın
#   LUX_DUMP_PATH=/work/lux/yale.nq       (dump aldıysanız)
#   OXIGRAPH_MEM_LIMIT=128g               (host RAM'e göre)
#   MIGRATOR_MEM_LIMIT=16g

# Pilot state'i temizle (data kalır, yeniden transform için)
make reset

# Yeniden başlat
docker compose up -d migrator
docker compose logs -f migrator
```

## 6. Update / yeniden deploy

Kod değiştikten sonra:

### Lokal (rsync) yöntemi
```bash
cd <package>/docker
./deploy.sh
# Sadece bir servisi yeniden başlat:
./deploy.sh --service migrator
```

### Git yöntemi
```bash
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && \
    git pull origin main && docker compose up -d --build'
```

### Sadece config (alignment.ttl, queries, .env) değiştiyse — build yok
```bash
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && \
    docker compose up -d --no-deps migrator delta-syncer'
```

## 7. Reboot resilience

`server-bootstrap.sh` sistemd unit kuruyor:

```bash
ssh root@server42.dnsbilisim.net 'systemctl status heritagegraph-lux.service'
# Boot'ta otomatik start: zaten enabled
# Manuel:
ssh root@server42.dnsbilisim.net 'systemctl restart heritagegraph-lux.service'
ssh root@server42.dnsbilisim.net 'systemctl stop heritagegraph-lux.service'
```

systemd unit aslında `docker compose up -d` çalıştırıyor — restart policy `unless-stopped` zaten Compose'da var. Bu sadece reboot sonrası bir kez tetikleme garantisi için.

## 8. Backup

```bash
# Sunucuda
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && make backup'
# Çıktı: /root/github/heritagegraph-lux-migration/backups/oxigraph-<TS>.tar.gz
```

Önerilen: cron'la haftalık offsite kopyala (örn. S3'e veya başka sunucuya):

```bash
# /etc/cron.weekly/oxigraph-offsite-backup
#!/bin/bash
cd /root/github/heritagegraph-lux-migration && make backup
rclone copy backups/ remote:hg-backups/ --include "oxigraph-*.tar.gz"
```

## 9. Sorun giderme

| Belirti | Olası neden | Çözüm |
|---|---|---|
| migrator container "Exited (2)" | Oxigraph healthcheck'i 5 dakikada cevap vermedi | `docker compose logs oxigraph` — RAM yetersiz olabilir; `OXIGRAPH_MEM_LIMIT` artır |
| migrator "Exited (4)" | LUX raw graph'a 0 triple yüklendi | `docker compose logs migrator | grep P2` — dump bozuk veya crawl başarısız |
| validation V1 / V2 fail | Yeni LUX class tipi geldi veya sameAs eksik | `make validate` çıktısındaki "FAIL" satırlarını okuyun; alignment.ttl güncelleyip `make reset && docker compose up -d migrator` |
| disk %95 dolu | LUX dump + Oxigraph indices yer kapladı | `make backup && docker system prune -af --volumes` (DİKKAT: oxigraph_data volume'üne dokunmaz) |
| Oxigraph 7878 portu çakışıyor | Sunucuda başka bir servis kullanıyor | `.env`'de `OXIGRAPH_PORT=7879` (veya 0 ile sadece-internal) |
| Migration ortada durdu, devam etmiyor | state file bozuldu | `make reset` (data preserve edilir, transform yeniden başlar) |

## 10. Tamamen sıfırla (DİKKAT — tüm veriyi silersiniz)

```bash
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && make reset-everything'
# Sonra yeniden deploy:
./deploy.sh
```

## 11. Production hardening (opsiyonel)

* **TLS / reverse proxy**: server42 muhtemelen zaten nginx/Caddy çalıştırıyor (stock-pattern-scanner için). Oxigraph endpoint'ini `https://lux-sparql.heritagegraph.xyz` gibi bir hostname'e proxy edebilirsiniz. `docker-compose.yml`'de port mapping'i kaldırıp, reverse proxy'yi Compose network'üne ekleyin.
* **Basic auth**: Oxigraph 0.4 native auth desteklemez — nginx/Caddy seviyesinde basic auth ekleyin.
* **Monitoring**: `make status` çıktısını Prometheus textfile collector'a çevirmek mümkün; alternatif Grafana Loki için log shipper kurulabilir.
* **Backup offsite**: rclone + S3/B2/Wasabi. `make backup` haftalık çalışıyor zaten.
