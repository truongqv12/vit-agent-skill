# jenkins-build

Trigger and track Jenkins builds from the terminal over the Jenkins REST API.

[`SKILL.md`](./SKILL.md) is the authority for routing, safety rules and commands. This README
covers provenance, setup and portability.

## Provenance & Portability

- **Standalone.** One Python 3.8+ CLI (`scripts/jenkins.py`) plus a small client
  (`scripts/jenkins_client.py`), standard library only — no `pip install`.
- Authenticates with an API token (Basic auth), which Jenkins exempts from CSRF crumbs. A
  password also works; the client then fetches a crumb within the same cookie session.
- Built from the manual browser workflow used on the CCDT Jenkins (2.479.1): read view/job JSON,
  `POST /job/<name>/build`, follow the queue item to the build number, poll until done, read
  `consoleText` for `Build tag` / `Image name`.
- Works on Windows, macOS and Linux.

## Configuration

Copy `.env.example` to `.env` in this folder (git-ignored) or export the variables:

```bash
JENKINS_URL=https://jenkins.example.com
JENKINS_USER=your-user
JENKINS_API_TOKEN=<api-token>
JENKINS_DEFAULT_VIEW=CCDT-DEV
```

Create a token at **User → Configure → API Token → Add new token**. Revoke it there when it is
no longer needed.

## Dependencies

- `standalone`: no other skill required.
- `optional`: a deploy-monitoring skill such as `rancher-watch` to verify the rollout after a
  build. Without it the skill reports build results only.
