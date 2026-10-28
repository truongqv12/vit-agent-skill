---
name: jenkins-build
description: "Trigger and track Jenkins builds over the REST API with an API token, no browser needed. List jobs in a view with their last build, start one or more jobs (with parameters), wait for the result, and report commit, image tag and failing log lines."
user-invocable: true
when_to_use: "Invoke when the user asks to build, rebuild or deploy a Jenkins job, check whether a job's last build includes a merge, wait for a running build, or read why a Jenkins build failed."
category: devops
keywords: [jenkins, build, ci, deploy, job, pipeline, api-token, ccdt]
license: MIT
metadata:
  author: tttruong
  version: "1.0.0"
  portability: standalone
---

# Jenkins Build

Run Jenkins from the terminal with `scripts/jenkins.py` (Python 3.8+, standard library only).
Use it instead of driving the Jenkins web UI.

## Setup

Credentials load in this order (later wins): skill `.env` → `.env` in the current directory →
environment variables. Copy `.env.example` to `.env` in this skill folder.

| Key | Meaning |
|---|---|
| `JENKINS_URL` | Base URL, e.g. `https://jenkins.example.com` |
| `JENKINS_USER` | Jenkins user id |
| `JENKINS_API_TOKEN` | API token (User → Configure → API Token → Add new token). Preferred: revocable and exempt from CSRF crumbs |
| `JENKINS_PASSWORD` | Fallback when no token; the client then fetches a crumb per session |
| `JENKINS_DEFAULT_VIEW` | View used by `jobs` when `--view` is omitted |
| `JENKINS_INSECURE` | `true` to skip TLS verification for self-signed HTTPS |

If credentials are missing, ask the user to create an API token and fill `.env`. Never ask them
to paste the token into the chat.

## Rules

1. **`build` is a write.** It starts real deploy pipelines. Run it only when the user asked for
   a build of that job or environment; otherwise list the jobs you would start and ask first.
   All other commands are read-only.
2. **Production needs explicit consent.** Jobs whose name has a `PROD` segment without `DEMO`
   are refused unless you pass `--allow-prod`. Pass it only when the user explicitly asked to
   build production in this conversation.
3. **Never print secrets.** Do not echo `.env`, the token or the Authorization header. Report
   only success or failure of authentication.
4. **Choose jobs deliberately.** A view usually maps to one environment (`views`). When the
   user names a job, build it. When they say "build environment X" or "build what changed",
   find the branch the jobs build (`log JOB --grep "FETCH_HEAD|Checking out"`), compare its
   latest commits (`git log origin/<branch>` when a checkout is available) with each job's last
   build time, and build the jobs whose service changed. If change cannot be determined, list
   the candidate jobs and ask.
5. Exit codes: `0` success, `1` build not `SUCCESS` or wait timed out, `2` config/auth/network
   error, or a production job without `--allow-prod`. Report failures with the log lines the
   script prints; do not retry blindly.

## Commands

Run from the skill folder, or call `python <skill_dir>/scripts/jenkins.py ...`. Add `--json` to
any command for machine-readable output.

```bash
# Views (usually one per environment: DEV, DEMO, PROD …) and their job counts
python scripts/jenkins.py views

# Jobs in the default view with last build number, result, start time, duration
python scripts/jenkins.py jobs
python scripts/jenkins.py jobs --view CCDT-DEV

# One build in detail: result, commit + branch, "Build tag"/"Image name" from the log, trigger cause
python scripts/jenkins.py status CCDT_DEV_NOTARY_TRANSACTION_SERVICE
python scripts/jenkins.py status CCDT_DEV_NOTARY_TRANSACTION_SERVICE --build 167

# Trigger (WRITE). --wait blocks until done and prints the summary; failures print the last 60 log lines
python scripts/jenkins.py build CCDT_DEV_NOTARY_TRANSACTION_SERVICE CCDT_DEV_FRONTEND_BUSINESS_WEB --wait
python scripts/jenkins.py build MY_PARAM_JOB -p BRANCH=dev -p SKIP_TESTS=true --wait --timeout 30

# Wait for a build that is already running
python scripts/jenkins.py wait CCDT_DEV_FRONTEND_BUSINESS_WEB --build 184

# Log tail, optionally filtered
python scripts/jenkins.py log CCDT_DEV_NOTARY_TRANSACTION_SERVICE --tail 80
python scripts/jenkins.py log CCDT_DEV_NOTARY_TRANSACTION_SERVICE --grep "error|fail"
```

`build` resolves the queue item to the exact build number, so `--wait` follows the build it
started rather than whatever ran last. Jobs inside folders use `folder/job` names.

The commit comes from the Git plugin's build data, or from `Checking out Revision` in the log.
Jobs that fetch sources with a shell script record neither; `revision` is then empty, and
the build start time is the evidence that a merge is included.

## Build then verify the deploy

Jobs that end with `kubectl set image` deploy on their own. After `build --wait` succeeds:

1. Take each job's `Build tag` from the summary.
2. Hand off to a deploy-monitoring capability with `deployment=tag` pairs. When the
   `rancher-watch` skill is present, run its `watch` command, which waits for the new pods and
   reports crash loops, image pull errors and probe failures with events and logs.
3. Without such a capability, report the build result and tags, and state that rollout was not
   verified.

## Report back

State which jobs ran, build numbers, results, commit (when known) and image tags. For failures,
quote the relevant log lines and the likely cause. Mention jobs you deliberately skipped.
