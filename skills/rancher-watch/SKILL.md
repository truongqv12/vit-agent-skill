---
name: rancher-watch
description: "Monitor Kubernetes deployments through the Rancher API with an API key, read-only and without a browser. List deployments and pods, show the configuration applied to a service with secrets masked, wait for a rollout to reach a new image tag, and on failure report the cause with pod events and container logs."
user-invocable: true
when_to_use: "Invoke when the user asks whether a deploy finished, wants to watch pods roll out after a build, asks why a pod is crashing or not ready, wants pod logs or warning events, or asks which configuration or environment variables a service is running with on a Rancher-managed cluster."
category: devops
keywords: [rancher, kubernetes, k8s, deploy, rollout, pod, logs, events, monitoring, ccdt]
license: MIT
metadata:
  author: tttruong
  version: "1.0.0"
  portability: standalone
---

# Rancher Watch

Watch deploys from the terminal with `scripts/rancher.py` (Python 3.8+, standard library only).
It calls the Kubernetes API through Rancher's proxy at `/k8s/clusters/<cluster>/...` and never
changes the cluster: no restart, scale, edit or exec.

## Setup

Credentials load in this order (later wins): skill `.env` → `.env` in the current directory →
environment variables. Copy `.env.example` to `.env` in this skill folder.

| Key | Meaning |
|---|---|
| `RANCHER_URL` | Rancher base URL, e.g. `https://rancher.example.com` |
| `RANCHER_TOKEN` | API key `token-xxxxx:secret` (avatar → Account & API Keys → Create, scope to the cluster, set an expiry) |
| `RANCHER_USER` / `RANCHER_PASSWORD` | Fallback for local-provider accounts: the script logs in for a 1-hour token and logs out when done |
| `RANCHER_CLUSTER` | Cluster id, default `local` |
| `RANCHER_NAMESPACE` | Default namespace for every command (`-n` overrides) |
| `RANCHER_INSECURE` | `true` to skip TLS verification |

Accounts are often limited to their project's namespaces, so a cluster-wide listing returns 403.
Always work inside a namespace. A 403 on a namespace means this account cannot see that
environment: say so and report what the build side shows. Do not guess pod state. If credentials are missing, ask the user to create an API key
and fill `.env`. Never ask them to paste it into the chat.

## Rules

1. Read-only. If the user wants a restart, rollback or scale, report what you found and leave
   the action to them.
2. Never print secrets: no `.env` contents, tokens or Authorization headers.
3. Exit codes: `0` healthy, `1` rollout failed or timed out (diagnosis is printed), `2`
   config/auth/permission/network error.

## Commands

Add `--json` for machine-readable output and `-n NS` to target another namespace.

```bash
# Deployments: image tag, ready/desired, rollout state (OK / đang rollout / LỖI)
python scripts/rancher.py deployments

# Pods, optionally of one deployment: phase, ready, restarts, tag, age, detected problem
python scripts/rancher.py pods --deployment notary-transaction-service

# Wait for a rollout. deployment=TAG waits until the deployment switches to that image tag first
python scripts/rancher.py watch notary-transaction-service=20261028_102703 business-web=20261028_102702
python scripts/rancher.py watch api-gateway --timeout 10

# Logs of a pod, or of every pod of a deployment (ANSI colors stripped)
python scripts/rancher.py logs notary-transaction-service --since 30m --grep "ERROR|Exception"
python scripts/rancher.py logs notary-transaction-service-6f58db66b5-7kgvc --previous --tail 300

# Warning events (all events with --all), optionally for one object
python scripts/rancher.py events --for notary-transaction-service-6f58db66b5-7kgvc

# Configuration applied to a deployment: image, command, ports, resources, env (literal or
# from which ConfigMap/Secret key), envFrom ConfigMaps with values, Secrets with key names only, mounts
python scripts/rancher.py config notary-transaction-service
python scripts/rancher.py config identity-admin-service --grep "OIDC|SSO"
```

## Secrets in `config` output

Secret values are never fetched into output; only their key names are listed. Literal env
values and ConfigMap values are shown except when the name looks sensitive (password, secret,
token, credential, private, jwt, cert, license, `*_KEY`), the value is a PEM block or a long
opaque base64/hex string, or a URL contains `user:password@` (the password part is masked).
The masking is a safety net, not a guarantee: do not paste full `config` output into tickets or
chat without reading it, and never try to recover masked values.

## What `watch` treats as a failure

`watch` finishes OK only when, as with `kubectl rollout status`, the new spec is observed,
every replica runs the new template, no old pods remain, and all replicas are available.

It stops early with `FAILED` when a pod running the new image shows:

- a waiting reason that never clears on its own: `CrashLoopBackOff`, `ImagePullBackOff`,
  `ErrImagePull`, `InvalidImageName`, `CreateContainerConfigError`, `CreateContainerError` or
  `RunContainerError`;
- two or more restarts with a recorded termination reason, such as `OOMKilled` or `Error`;
- phase `Failed`, or the deployment condition `ProgressDeadlineExceeded`.

On `FAILED` or `TIMEOUT` it prints the deployment message, Warning events, and the last log
lines of each problem pod. It reads the previous container's log when the pod has restarted.
A readiness-probe warning while Spring Boot is still starting is normal. Judge it by whether the
pod becomes ready before the timeout.

`TIMEOUT` with "image vẫn là tag …" means the deployment never received the new image. Check
the build/deploy job rather than the pods.

## After a Jenkins build

Pair each job's `Build tag` with its deployment and run one `watch` for all of them. Report per
deployment: final status, tag, ready count, and for failures the cause plus the key log lines.
