# Git Safety Protocols

## Secret detection patterns

### Scan command
```bash
git diff --cached | grep -iE "(AKIA|api[_-]?key|token|password|secret|credential|private[_-]?key|mongodb://|postgres://|mysql://|redis://|-----BEGIN)"
```

### Patterns to detect

| Category | Pattern | Example |
|----------|---------|---------|
| API Keys | `api[_-]?key`, `apiKey` | `API_KEY=abc123` |
| AWS | `AKIA[0-9A-Z]{16}` | `AKIAIOSFODNN7EXAMPLE` |
| Tokens | `token`, `auth_token`, `jwt` | `AUTH_TOKEN=xyz` |
| Passwords | `password`, `passwd`, `pwd` | `DB_PASSWORD=secret` |
| Private Keys | `-----BEGIN PRIVATE KEY-----` | PEM files |
| DB URLs | `mongodb://`, `postgres://`, `mysql://` | Connection strings |
| OAuth | `client_secret`, `oauth_token` | `CLIENT_SECRET=abc` |

### Files to warn about
- `.env`, `.env.*` (except `.env.example`)
- `*.key`, `*.pem`, `*.p12`
- `credentials.json`, `secrets.json`
- `config/private.*`

### Action on detection
1. **BLOCK commit immediately**
2. Show matching lines: `git diff --cached | grep -B2 -A2 <pattern>`
3. Suggest: "Add to .gitignore or use environment variables"
4. Offer to unstage: `git reset HEAD <file>`

## Branch protection

### Never force push to
- `main`, `master`, `production`, `prod`, `release/*`

### Pre-merge checks
```bash
# Check for conflicts before merge
git merge --no-commit --no-ff origin/{branch} && git merge --abort
```

### Remote-first operations
Always use `origin/{branch}` for comparisons:
- ✅ `git diff origin/main...origin/feature`
- ❌ `git diff main...HEAD` (includes local uncommitted)

## Error recovery

### Undo last commit (unpushed)
```bash
git reset --soft HEAD~1  # Keep changes staged
git reset HEAD~1         # Keep changes unstaged
```

### Abort merge
```bash
git merge --abort
```

### Discard local changes
```bash
git checkout -- <file>   # Single file
git reset --hard HEAD    # All files (DANGER)
```

**Always confirm with the user before destructive operations.**
