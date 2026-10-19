# GitHub'a push etme

Repo lokalde hazır, `git init` + ilk commit yapıldı. GitHub'a aktarmak için iki yol var.

## Yol A — `gh` CLI (önerilen, 1 dakika)

GitHub CLI kuruluysa (https://cli.github.com/) ve giriş yapmışsanız:

```bash
cd /path/to/heritagegraph-lux-migration

# CAIRNepal organizasyonu altında public repo oluştur + push
gh repo create CAIRNepal/heritagegraph-lux-migration \
    --public \
    --description "Ontology alignment & migration pipeline: Yale LUX → CAIR Nepal HeritageGraph" \
    --source=. \
    --remote=origin \
    --push

# Verify
gh repo view CAIRNepal/heritagegraph-lux-migration --web
```

Kişisel hesabınıza koymak isterseniz `CAIRNepal/` kısmını kullanıcı adınızla değiştirin (örn. `semihyumusak/heritagegraph-lux-migration`) — daha sonra `gh repo transfer` ile CAIRNepal'a taşınabilir.

## Yol B — manuel (gh CLI yoksa)

1. **Tarayıcıda repo oluştur**: https://github.com/organizations/CAIRNepal/repositories/new (veya kişisel hesap için https://github.com/new)
   * Name: `heritagegraph-lux-migration`
   * Description: `Ontology alignment & migration pipeline: Yale LUX → CAIR Nepal HeritageGraph`
   * Public
   * **Hiçbir initialize seçeneğini işaretleme** (README/LICENSE/.gitignore zaten lokalde)
   * Create repository

2. **Lokalden push et**:
   ```bash
   cd /path/to/heritagegraph-lux-migration
   git remote add origin git@github.com:CAIRNepal/heritagegraph-lux-migration.git
   # veya HTTPS:
   # git remote add origin https://github.com/CAIRNepal/heritagegraph-lux-migration.git

   git push -u origin main
   ```

## Push sonrası ilk iş

### 1. CI'ın çalıştığını teyit et
Repo sayfasında **Actions** sekmesine girin. İlk push otomatik olarak `CI` workflow'unu tetikler. 5 job paralel çalışır:

* `ttl-parse` — rdflib ile alignment.ttl parse + istatistik kontrolü
* `python-lint` — `py_compile` + `ruff` + XLSX row-count drift detection
* `sparql-syntax` — her labelled block için `rdflib.plugins.sparql.prepareQuery/Update`
* `docker-lint` — `docker compose config` + `hadolint`
* `shell-syntax` — `bash -n` + `shellcheck`

Hepsi yeşil dönmeli. Yeşil dönmüyorsa Actions log'una bakıp düzeltin.

### 2. Repository ayarları

**Settings → General**:
* Default branch: `main` ✓ (zaten öyle)
* Features: Issues açık, Discussions opsiyonel, Wiki kapalı (docs/ klasörü zaten var)

**Settings → Branches → Branch protection rules** (önerilen):
* Branch name pattern: `main`
* ✓ Require a pull request before merging (en az 1 review)
* ✓ Require status checks to pass before merging — seçili check'ler: `ttl-parse`, `python-lint`, `sparql-syntax`, `docker-lint`, `shell-syntax`
* ✓ Require branches to be up to date before merging

**Settings → Actions → General**:
* Workflow permissions: Read repository contents (default, yeterli)

**Settings → Secrets and variables → Actions** (deploy için):
Eğer GitHub Actions'tan otomatik deploy etmek isterseniz (opsiyonel — şu an `deploy.sh` lokalden çalışıyor):
* `SSH_PRIVATE_KEY` — server42'ye erişim için
* `SERVER` — `root@server42.dnsbilisim.net`
* `REMOTE_DIR` — `/root/github/heritagegraph-lux-migration`

### 3. About panelini düzenle (sağ üst köşede ⚙️)
* Description: `Yale LUX → CAIR Nepal HeritageGraph migration: 273-triple OWL alignment + Docker pipeline targeting Oxigraph`
* Website: `https://heritagegraph.cair-nepal.org/` (veya boş)
* Topics: `cultural-heritage`, `linked-art`, `cidoc-crm`, `ontology-alignment`, `sparql`, `oxigraph`, `nepal`, `heritage-data`

### 4. Releases (paper submit'ten önce)
Paper submit sırasında DOI almak için Zenodo-GitHub entegrasyonu önerilir:
1. https://zenodo.org/account/settings/github/ → CAIRNepal/heritagegraph-lux-migration repo'sunu enable et
2. GitHub'da: Releases → Create a new release → tag `v0.1.0` → "Initial release matching the manuscript"
3. Zenodo otomatik bir DOI üretir; bunu paper'da cite edin.

## Sunucuya deploy

Repo GitHub'a girdikten sonra server42'de iki yol var:

### Lokalden rsync (mevcut deploy.sh — GitHub'a bağımlı değil)
```bash
cd heritagegraph-lux-migration
make deploy-bootstrap     # ilk sefer
make deploy
```

### Sunucuda git pull (alternatif)
```bash
ssh root@server42.dnsbilisim.net
cd /root/github
git clone https://github.com/CAIRNepal/heritagegraph-lux-migration.git
cd heritagegraph-lux-migration
cp docker/.env.example docker/.env && $EDITOR docker/.env
curl -L -o alignment/HeritageGraph.ttl https://raw.githubusercontent.com/CAIRNepal/heritagegraphontology/HeritageGraph/HeritageGraph.ttl
make up
```

Sonraki güncellemeler:
```bash
ssh root@server42.dnsbilisim.net 'cd /root/github/heritagegraph-lux-migration && git pull origin main && make up'
```

## Tipik geliştirme akışı

```bash
git checkout -b fix/sci-encounter-mapping
$EDITOR alignment/heritagegraph-lux-alignment.ttl
make ci-local                                  # lokal hızlı kontrol
git add alignment/ && git commit -m "fix(alignment): correct la:Encounter to sci:S19"
git push -u origin fix/sci-encounter-mapping
gh pr create --title "Fix la:Encounter mapping" --body "Closes #N"
# CI yeşil olunca merge
gh pr merge --squash
git checkout main && git pull
```

## Repo'yu private başlatıp sonra public yapmak

Eğer paper review süresince private tutmak isterseniz:

```bash
gh repo create CAIRNepal/heritagegraph-lux-migration --private ...
# review bitince:
gh repo edit CAIRNepal/heritagegraph-lux-migration --visibility=public --accept-visibility-change-consequences
```

## Sorun giderme

| Belirti | Çözüm |
|---|---|
| `gh: command not found` | https://cli.github.com/ kur, `gh auth login` |
| `Permission denied (publickey)` | SSH key GitHub'a eklenmiş mi? `gh ssh-key list` veya https://github.com/settings/keys |
| CI'ın `python-lint` job'ı "row count drift" der | Lokalde `python mapping/build_mapping.py` çalıştırıp commit'le |
| CI'ın `sparql-syntax` fail eder | `make sparql-check` ile lokalde tekrarla, hatalı bloğu bul |
| `docker-lint` hadolint warning | `docker/migrator/Dockerfile`'ı düzelt, ya da workflow'ta `failure-threshold: error` yap |
