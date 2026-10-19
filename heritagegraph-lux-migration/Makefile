# LUX → HeritageGraph migration — convenience targets.
# Use `make help` to see what each does.
# Run from the REPO ROOT (this directory).

SHELL          := /usr/bin/env bash
COMPOSE        := docker compose -f docker/docker-compose.yml --project-directory docker
PROJECT        := heritagegraph-lux-migration
BACKUP_DIR     ?= ./backups
TIMESTAMP      := $(shell date -u +%FT%H%MZ)

# ---- Deploy / remote ---------------------------------------------------------
SERVER     ?= root@server42.dnsbilisim.net
REMOTE_DIR ?= /root/github/heritagegraph-lux-migration

.PHONY: help up down logs status migrate validate snapshot backup restore reset reset-everything \
        shell sparql delta-now reload-alignment ssh-reload-alignment \
        ttl-check sparql-check py-check ci-local \
        deploy deploy-no-build deploy-migrator deploy-dry-run deploy-bootstrap \
        ssh ssh-logs ssh-logs-migrator ssh-status ssh-shell ssh-backup-pull ssh-tunnel

help:                                       ## Show this help.
	@awk 'BEGIN{FS=":.*?##"} /^[a-zA-Z0-9_-]+:.*?##/ {printf "  \033[36m%-20s\033[0m %s\n",$$1,$$2}' $(MAKEFILE_LIST)

# ---- Local stack ------------------------------------------------------------

up:                                         ## Start oxigraph + migrator + delta-syncer.
	@test -f docker/.env || (echo "ERROR: docker/.env missing. Run: cp docker/.env.example docker/.env" && exit 1)
	@test -f alignment/HeritageGraph.ttl || \
	  echo "WARN: alignment/HeritageGraph.ttl not present. Drop it in before running migrate."
	$(COMPOSE) up -d

down:                                       ## Stop everything (data preserved).
	$(COMPOSE) down

logs:                                       ## Tail logs from all services.
	$(COMPOSE) logs -f --tail=200

status:                                     ## Show service status + key counts.
	@$(COMPOSE) ps
	@echo
	@echo "Triple counts:"
	@curl -sf -G http://localhost:$${OXIGRAPH_PORT:-7878}/query \
	      --data-urlencode 'query=SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g' \
	      -H 'Accept: application/sparql-results+json' \
	  | python3 -c "import json,sys; [print('  %-60s %s' % (r['g']['value'], r['n']['value'])) for r in json.load(sys.stdin)['results']['bindings']]" \
	  || echo "  (Oxigraph not reachable yet)"

migrate:                                    ## Re-run the migrator (one-shot).
	$(COMPOSE) run --rm migrator

validate:                                   ## Run validation queries on the live store.
	$(COMPOSE) run --rm --entrypoint /work/bin/migrate_lux_to_hg.py migrator \
	  --mode validate \
	  --endpoint http://oxigraph:7878 \
	  --queries  /work/queries/validation_queries.sparql

delta-now:                                  ## Trigger an immediate delta sync.
	$(COMPOSE) exec delta-syncer /work/bin/run_delta.sh

ALIGN_GRAPH ?= https://w3id.org/heritagegraph/alignment/lux
ALIGN_TTL   ?= alignment/heritagegraph-lux-alignment.ttl

reload-alignment:                           ## Clear and reload the alignment named graph from $(ALIGN_TTL).
	@test -f $(ALIGN_TTL) || (echo "ERROR: $(ALIGN_TTL) not found" && exit 1)
	@echo "Clearing graph <$(ALIGN_GRAPH)>"
	@curl -sSf -X POST "http://localhost:$${OXIGRAPH_PORT:-7878}/update" \
	      --data-urlencode 'update=CLEAR GRAPH <$(ALIGN_GRAPH)>' \
	      -H 'Content-Type: application/x-www-form-urlencoded' \
	  && echo "  cleared"
	@echo "Loading $(ALIGN_TTL) into <$(ALIGN_GRAPH)>"
	@curl -sSf -X POST "http://localhost:$${OXIGRAPH_PORT:-7878}/store?graph=$(ALIGN_GRAPH)" \
	      -H 'Content-Type: text/turtle' \
	      --data-binary @$(ALIGN_TTL) \
	  && echo "  loaded"
	@echo
	@curl -sf -G "http://localhost:$${OXIGRAPH_PORT:-7878}/query" \
	      --data-urlencode 'query=SELECT (COUNT(*) AS ?n) WHERE { GRAPH <$(ALIGN_GRAPH)> { ?s ?p ?o } }' \
	      -H 'Accept: application/sparql-results+json' \
	  | python3 -c "import json,sys; r=json.load(sys.stdin)['results']['bindings'][0]; print(f'  → alignment graph now has {r[\"n\"][\"value\"]} triples')"

ssh-reload-alignment:                       ## Reload alignment graph on $(SERVER) (after a git pull).
	ssh $(SERVER) 'cd $(REMOTE_DIR) && make reload-alignment'

snapshot backup:                            ## Snapshot the Oxigraph data volume to BACKUP_DIR.
	@mkdir -p $(BACKUP_DIR)
	docker run --rm \
	  -v $(PROJECT)_oxigraph_data:/data:ro \
	  -v $(abspath $(BACKUP_DIR)):/backup \
	  busybox sh -c \
	  "tar czf /backup/oxigraph-$(TIMESTAMP).tar.gz -C /data ."
	@echo "  → $(BACKUP_DIR)/oxigraph-$(TIMESTAMP).tar.gz"

restore:                                    ## Restore from a snapshot. Usage: make restore FILE=backups/oxigraph-XXX.tar.gz
	@test -n "$(FILE)" || (echo "ERROR: pass FILE=path/to/backup.tar.gz" && exit 1)
	$(COMPOSE) down
	docker volume rm $(PROJECT)_oxigraph_data || true
	docker volume create $(PROJECT)_oxigraph_data
	docker run --rm \
	  -v $(PROJECT)_oxigraph_data:/data \
	  -v $(abspath $(FILE)):/backup.tar.gz:ro \
	  busybox sh -c "tar xzf /backup.tar.gz -C /data"
	$(COMPOSE) up -d

reset:                                      ## Wipe migration state (forces full re-run, data preserved).
	$(COMPOSE) run --rm --entrypoint sh migrator -c \
	  "rm -f /work/state/*.done /work/state/migration.state.json && echo 'state cleared'"

reset-everything:                           ## DANGER: also wipes the Oxigraph triplestore.
	$(COMPOSE) down -v
	@echo "All volumes dropped."

shell:                                      ## Open an interactive shell inside the migrator image.
	$(COMPOSE) run --rm --entrypoint bash migrator

sparql:                                     ## Ad-hoc SELECT. Usage: make sparql Q="SELECT * WHERE {?s ?p ?o} LIMIT 10"
	@test -n "$(Q)" || (echo "ERROR: pass Q='SELECT ...'" && exit 1)
	@curl -sS -G http://localhost:$${OXIGRAPH_PORT:-7878}/query \
	  --data-urlencode "query=$(Q)" \
	  -H 'Accept: application/sparql-results+json' \
	| python3 -m json.tool

# ---- CI-style local checks --------------------------------------------------

ttl-check:                                  ## Parse every .ttl in alignment/ with rdflib.
	@for f in alignment/*.ttl; do \
	  echo "==> $$f"; \
	  python3 -c "import rdflib; g=rdflib.Graph(); g.parse('$$f', format='turtle'); print(f'  {len(g)} triples — OK')" || exit 1; \
	done

sparql-check:                               ## Parse every .sparql in queries/ (syntax only).
	@python3 -c "import rdflib.plugins.sparql as p; \
import pathlib, sys; \
errs=0; \
for f in pathlib.Path('queries').glob('*.sparql'): \
    text=f.read_text(); \
    blocks=[b for b in text.split(';\n\n') if any(k in b.upper() for k in ('SELECT','CONSTRUCT','INSERT','DELETE','ASK'))]; \
    for i,b in enumerate(blocks): \
        try: p.prepareQuery(b) if 'SELECT' in b.upper() or 'CONSTRUCT' in b.upper() or 'ASK' in b.upper() else p.prepareUpdate(b); \
        except Exception as e: print(f'  {f.name} block {i}: {e}'); errs+=1; \
    print(f'  {f.name}: {len(blocks)} blocks'); \
sys.exit(1 if errs else 0)"

py-check:                                   ## Syntax-check Python scripts.
	@python3 -m py_compile scripts/migrate_lux_to_hg.py mapping/build_mapping.py && echo "  python syntax OK"

ci-local: ttl-check py-check                ## Run all local CI checks.
	@echo "  ✓ local CI passed"

# ---- Remote deployment to server42 ------------------------------------------

deploy:                                     ## Push code + (re)deploy on $(SERVER). Reads .deploy.env.
	./deploy.sh

deploy-no-build:                            ## Push code + recreate without rebuilding images.
	./deploy.sh --no-build

deploy-migrator:                            ## Re-deploy only the migrator service.
	./deploy.sh --service migrator

deploy-dry-run:                             ## Show what deploy would change, without applying.
	./deploy.sh --dry-run

deploy-bootstrap:                           ## First-time only: copy bootstrap script and run it on $(SERVER).
	rsync -avz --progress scripts/server-bootstrap.sh scripts/discover_lux_endpoints.sh $(SERVER):/root/
	ssh -t $(SERVER) 'bash /root/server-bootstrap.sh'

ssh:                                        ## Open an interactive shell on $(SERVER) in $(REMOTE_DIR).
	ssh -t $(SERVER) 'cd $(REMOTE_DIR) && exec bash -l'

ssh-logs:                                   ## Tail all docker compose logs on $(SERVER).
	ssh -t $(SERVER) 'cd $(REMOTE_DIR) && docker compose -f docker/docker-compose.yml --project-directory docker logs -f --tail=200'

ssh-logs-migrator:                          ## Tail only migrator logs on $(SERVER).
	ssh -t $(SERVER) 'cd $(REMOTE_DIR) && docker compose -f docker/docker-compose.yml --project-directory docker logs -f --tail=200 migrator'

ssh-status:                                 ## Show docker compose ps + triple counts on $(SERVER).
	ssh $(SERVER) 'cd $(REMOTE_DIR) && make status'

ssh-shell:                                  ## Open bash inside the migrator container on $(SERVER).
	ssh -t $(SERVER) 'cd $(REMOTE_DIR) && docker compose -f docker/docker-compose.yml --project-directory docker run --rm --entrypoint bash migrator'

ssh-backup-pull:                            ## Make a snapshot on $(SERVER) and pull it locally.
	ssh $(SERVER) 'cd $(REMOTE_DIR) && make backup'
	@mkdir -p backups
	rsync -avz --progress $(SERVER):$(REMOTE_DIR)/backups/oxigraph-*.tar.gz backups/
	@echo "Backups in ./backups/:"
	@ls -la backups/oxigraph-*.tar.gz | tail -5

ssh-tunnel:                                 ## Forward Oxigraph 7878 from $(SERVER) to localhost.
	@echo "Oxigraph SPARQL UI will be at http://localhost:7878/  (Ctrl-C to close tunnel)"
	ssh -N -L 7878:127.0.0.1:7878 $(SERVER)
