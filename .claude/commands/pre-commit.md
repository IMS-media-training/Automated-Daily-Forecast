# Pre-Commit Documentation Checklist

Before committing, review and update all affected documentation.

## Steps

1. **Check what changed**: Run `git status` and `git diff --stat` to see modified files

2. **Update documentation** based on what changed:

### Core Documentation
- [ ] **CLAUDE.md** - Update if:
  - Commands changed
  - Project structure changed
  - Critical implementation notes changed
  - New patterns/practices established

- [ ] **README.md** - Update if:
  - Features added/changed
  - Setup process changed
  - Architecture changed

- [ ] **CHANGELOG.md** - ALWAYS add entry to [Unreleased]:
  - Added: new features
  - Changed: modifications to existing
  - Fixed: bug fixes
  - Removed: removed features

### Detailed Documentation (docs/)
- [ ] **docs/SETUP.md** - Update if installation/configuration changed
- [ ] **docs/ARCHITECTURE.md** - Update if data flow/components changed
- [ ] **docs/DEVELOPMENT.md** - Update if dev practices changed
- [ ] **docs/DEPLOYMENT.md** - Update if GitHub Actions/deployment changed

3. **Stage documentation**: `git add` any updated docs

4. **Push to BOTH remotes**:
```bash
git push origin main && git push ims main
```

## Quick Reference

| If you changed... | Update these docs |
|-------------------|-------------------|
| New script/command | CLAUDE.md, README.md, CHANGELOG.md |
| Image generation | CLAUDE.md, ARCHITECTURE.md, CHANGELOG.md |
| Email/delivery | DEPLOYMENT.md, CHANGELOG.md |
| Dependencies | SETUP.md, CHANGELOG.md |
| Bug fix | CHANGELOG.md |

---

Now review your changes and update the relevant documentation before committing.
