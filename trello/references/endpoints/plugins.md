# Trello API — Plugins

Base URL `https://api.trello.com/1`. Every call needs `key` + `token` (auto-added
by the wrapper scripts). Call with `scripts/trello.sh` (macOS/Linux) or
`scripts/trello.ps1` (Windows). Plugins are Power-Ups — third-party extensions
listed on the Power-Up directory.

## GET /plugins/{id}/ — Get a Plugin
Path params: `id` (required).

```bash
scripts/trello.sh GET "/plugins/<id>/"
```

## PUT /plugins/{id}/ — Update a Plugin
Path params: `id` (required).

```bash
scripts/trello.sh PUT "/plugins/<id>/"
```

## GET /plugins/{id}/compliance/memberPrivacy — Get Plugin's Member privacy compliance
Path params: `id` (required).

```bash
scripts/trello.sh GET "/plugins/<id>/compliance/memberPrivacy"
```

## POST /plugins/{idPlugin}/listing — Create a Listing for Plugin
Path params: `idPlugin` (required). Request body (JSON): `description`, `locale`, `overview`, `name` (all optional).

```bash
scripts/trello.sh POST "/plugins/<idPlugin>/listing"
```

## PUT /plugins/{idPlugin}/listings/{idListing} — Updating Plugin's Listing
Path params: `idPlugin` (required), `idListing` (required). Request body (JSON): `description`, `locale`, `overview`, `name` (all optional).

```bash
scripts/trello.sh PUT "/plugins/<idPlugin>/listings/<idListing>"
```
