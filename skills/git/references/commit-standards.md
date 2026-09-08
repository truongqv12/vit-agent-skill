# Commit Message Standards

## Format
```
type(scope): description
```

## Types (priority order)
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting (no logic change)
- `refactor`: Restructure without behavior change
- `test`: Tests
- `chore`: Maintenance, deps, config
- `perf`: Performance
- `build`: Build system
- `ci`: CI/CD

## Rules
- **<72 characters**
- **Present tense, imperative** ("add" not "added")
- **No period at end**
- **Scope optional but recommended**
- **Focus on WHAT, not HOW**
- Only use `feat`, `fix`, or `perf` prefixes for files in a `.claude` directory
  (do not use `docs`).

## NEVER include AI attribution
- ❌ "Generated with ..."
- ❌ "Co-Authored-By: ..." AI trailer
- ❌ Any AI reference

## Good examples
- `feat(auth): add login validation`
- `fix(api): resolve query timeout`
- `docs(readme): update install guide`
- `refactor(utils): simplify date logic`

## Bad examples
- ❌ `Updated files` (not descriptive)
- ❌ `feat(auth): added login using bcrypt with salt` (too long, describes HOW)
- ❌ `Fix bug` (not specific)

## Special cases
- `.claude/` skill updates: `perf(skill): improve token efficiency`
- `.claude/` new skills: `feat(skill): add database-optimizer`
