# w3id.org configuration for HeritageGraph

Ready-to-submit Apache rules live in `w3id/heritagegraph/.htaccess`.

## Deploy steps

1. Tag release `v1.0.0` on `CAIRNepal/heritagegraphontology`.
2. Fork [perma-id/w3id](https://github.com/perma-id/w3id).
3. Copy `w3id/heritagegraph/.htaccess` to `heritagegraph/.htaccess` in your fork.
4. Open a PR to perma-id/w3id (describe the ontology namespace and CC-BY-4.0 licence).

## Redirect map

| Path | Target |
|------|--------|
| `/heritagegraph/ontology` | `HeritageGraph.ttl` @ tag `v1.0.0` |
| `/heritagegraph/ontology/1.0.0` | Versioned ontology document |
| `/heritagegraph/alignment` | `HeritageGraph-alignment.ttl` |
| `/heritagegraph/edm-profile` | `HeritageGraph-edm.ttl` |
| `/heritagegraph/dataset` | `heritagegraph-metadata.ttl` |
| `/heritagegraph/` | GitHub Pages documentation |

> Source layout note: the v1.0.0 targets resolve at the repo root (frozen tag).
> Since the 2026-06 restructure the source files live under `ontology/` on the
> default branch; future release tags redirect to `…/<tag>/ontology/<file>`.
