# rancher-watch

Read-only deploy monitoring for Kubernetes workloads managed by Rancher.

[`SKILL.md`](./SKILL.md) is the authority for routing, safety rules and commands. This README
covers provenance, setup and portability.

## Provenance & Portability

- **Standalone.** One Python 3.8+ CLI (`scripts/rancher.py`) plus a client
  (`scripts/rancher_client.py`), standard library only — no `pip install`, no `kubectl`.
- Calls the Kubernetes API through Rancher's authenticated proxy
  `/k8s/clusters/<cluster>/...` with a Rancher API key, so it works for accounts that only have
  project/namespace access and no kubeconfig.
- Never mutates the cluster. Secret values are never printed (`config` lists Secret key names
  only and masks sensitive literals).
- Offline logic tests: `python scripts/test_rancher.py`.

## Configuration

Copy `.env.example` to `.env` in this folder (git-ignored) or export the variables:

```bash
RANCHER_URL=https://rancher.example.com
RANCHER_TOKEN=token-xxxxx:<secret>
RANCHER_CLUSTER=local
RANCHER_NAMESPACE=ccdt-dev
```

Create a key at **avatar → Account & API Keys → Create API Key**. Scope it to the cluster and
set an expiry. Accounts on the local auth provider can use `RANCHER_USER` / `RANCHER_PASSWORD`
instead; the script then logs in for a 1-hour token and logs out after each run.

## Dependencies

- `standalone`: no other skill required. Pairs with `jenkins-build` (build → watch rollout).
