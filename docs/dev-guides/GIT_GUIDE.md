# Git Guide for Beginners

> A practical guide to Git version control for the IMS Weather Forecast Automation project

## What is Git?

**Git** is version control software that helps you:

- Track changes to your code over time
- Save "snapshots" (commits) of your project at different stages
- Revert to previous versions if something breaks
- Work on new features without breaking the main code
- Collaborate with others (when ready)

Think of it like "Track Changes" in Word, but much more powerful and designed for code.

## Basic Concepts

### Repository (Repo)

Your project folder with Git tracking enabled. The `.git` folder inside contains all the history.

### Commit

A snapshot of your project at a specific point in time, with a message describing what changed.

### Staging Area

A "waiting room" where you prepare files before committing them.

### Branch

A parallel version of your code where you can experiment without affecting the main version.

## The Git Workflow

```plain text
1. Make changes to files
   ↓
2. Stage the changes (git add)
   ↓
3. Commit the changes (git commit)
   ↓
4. (Optional) Push to remote server (git push)
```

## Essential Git Commands

### Checking Status

```bash
# See what files have changed
git status

# See what lines have changed
git diff
```

**Use this:** Before every commit to see what you're about to save.

### Staging Files

```bash
# Stage a specific file
git add filename.py

# Stage all changed files
git add .

# Stage multiple specific files
git add file1.py file2.py file3.py
```

**Use this:** To prepare files for committing.

### Committing Changes

```bash
# Commit staged files with a message
git commit -m "Add weather icon mapping function"

# Commit with a longer message (opens editor)
git commit
```

**Good commit messages:**

- ✅ "Fix Hebrew text encoding in extract_forecast.py"
- ✅ "Add dry-run mode to workflow script"
- ✅ "Update README with installation instructions"

**Bad commit messages:**

- ❌ "fixed stuff"
- ❌ "update"
- ❌ "asdf"

### Viewing History

```bash
# See commit history
git log

# See compact history
git log --oneline

# See history with file changes
git log --stat

# See last 5 commits
git log -5
```

### Undoing Changes

```bash
# Discard changes to a file (CAREFUL: can't undo this!)
git checkout -- filename.py

# Unstage a file (keep changes, just remove from staging)
git reset filename.py

# Unstage all files
git reset
```

### Viewing Differences

```bash
# See changes in working directory
git diff

# See changes that are staged
git diff --staged

# See changes in a specific file
git diff filename.py
```

## Common Workflows

### After Working on Code

```bash
# 1. Check what you changed
git status
git diff

# 2. Stage your changes
git add utils.py extract_forecast.py

# 3. Commit with a clear message
git commit -m "Add temperature validation to extract_forecast.py"

# 4. Verify it worked
git log -1
```

### Before Starting a New Feature

```bash
# Check you don't have uncommitted changes
git status

# If you do, commit them first
git add .
git commit -m "Save current work before new feature"
```

### Checking Your Work

```bash
# See what files are tracked
git ls-files

# See what changed in last commit
git show

# See history of a specific file
git log -- filename.py
```

## Best Practices for This Project

### 1. Commit Often

- Commit after completing a logical chunk of work
- Don't wait until the end of the day
- Small, focused commits are better than large ones

### 2. Write Clear Commit Messages

```bash
# Start with a verb, be specific
git commit -m "Add error handling for missing XML files"
git commit -m "Update documentation with Phase 2 status"
git commit -m "Fix temperature sorting bug"
```

### 3. Check Before You Commit

```bash
# Always run these before committing:
git status   # What files are changed?
git diff     # What exactly changed?
```

### 4. Don't Commit These Files

The `.gitignore` file already handles this, but be aware:

- ❌ Log files (`logs/*.log`)
- ❌ Generated images (`output/*.jpg`)
- ❌ Downloaded XML data files
- ❌ `__pycache__/` folders
- ✅ DO commit: Python code, documentation, README files

## Phase-Based Commit Strategy

### Completing a Phase

```bash
# When you complete a major phase:
git add .
git commit -m "Complete Phase 2: Single city image generation

- Implement Pillow image creation
- Add Hebrew font support (Rubik)
- Create weather icon mapping
- Generate proof-of-concept image
- Add comprehensive tests

Closes Phase 2 milestone"
```

### During Development

```bash
# Regular development commits:
git commit -m "Add weather emoji icons dictionary"
git commit -m "Implement image canvas creation"
git commit -m "Fix Hebrew text alignment issue"
```

## Understanding the .gitignore File

The `.gitignore` file tells Git which files to ignore. Example:

```gitignore
# Ignore Python cache
__pycache__/

# Ignore log files
logs/*.log

# But keep the README
!logs/README.md
```

**Why ignore files?**

- Log files change constantly (not useful to track)
- Generated files can be recreated
- Large data files slow down the repository
- Temporary files clutter the history

## Branching (Advanced - For Later)

When you're ready to experiment without affecting your main code:

```bash
# Create a new branch
git branch feature-instagram-integration

# Switch to that branch
git checkout feature-instagram-integration

# Make changes, commit them...
git add .
git commit -m "Add Instagram API integration"

# Switch back to main branch
git checkout main

# Merge the feature branch into main (when ready)
git merge feature-instagram-integration
```

**Use branches for:**

- Experimenting with new features
- Testing major changes
- Working on Phase 2 while keeping Phase 1 stable

## Remote Repositories (Future)

Later, you might want to:

- Back up your code to GitHub/GitLab
- Share with the IT team
- Collaborate with others

Basic remote commands (for later):

```bash
# Add a remote repository
git remote add origin https://github.com/username/project.git

# Push your commits to remote
git push origin main

# Pull changes from remote
git pull origin main
```

## Troubleshooting

### "I committed the wrong files!"

```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Re-stage the right files
git add correct_file.py
git commit -m "Correct commit message"
```

### "I want to see what I changed yesterday"

```bash
# Show commits from yesterday
git log --since="yesterday"

# Show changes from a specific commit
git show COMMIT_HASH
```

### "I deleted a file by accident!"

```bash
# If not committed yet:
git checkout -- deleted_file.py

# If already committed:
git log -- deleted_file.py  # Find when it was deleted
git checkout COMMIT_HASH -- deleted_file.py  # Restore from that commit
```

### "My working directory is messy, start fresh"

```bash
# See what would be removed
git clean -n

# Remove untracked files (CAREFUL!)
git clean -f
```

## Quick Reference Cheat Sheet

```bash
# Status and Info
git status              # What's changed?
git log --oneline       # Commit history
git diff                # What changed (unstaged)?
git diff --staged       # What changed (staged)?

# Staging and Committing
git add filename.py     # Stage specific file
git add .               # Stage everything
git commit -m "msg"     # Commit with message
git commit              # Commit with editor

# Undoing (use carefully!)
git checkout -- file    # Discard changes to file
git reset file          # Unstage file
git reset --soft HEAD~1 # Undo last commit, keep changes

# History and Comparison
git log                 # Full history
git log --stat          # History with file changes
git show                # Show last commit details
git show COMMIT_HASH    # Show specific commit

# Branches
git branch              # List branches
git branch name         # Create branch
git checkout name       # Switch to branch
git merge name          # Merge branch into current
```

## Learning Resources

### Official Git Documentation

- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

### Interactive Tutorials

- [Learn Git Branching](https://learngitbranching.js.org/) - Visual, interactive
- [GitHub Git Handbook](https://guides.github.com/introduction/git-handbook/)

### When You Get Stuck

1. Run `git status` - it often tells you what to do
2. Run `git log` - see what happened recently
3. Google the error message - Git errors are well-documented
4. Use `git --help` or `git <command> --help` for built-in help

## Tips for This Project

### Daily Workflow

```bash
# Start of day
git status  # See where you left off

# During development
# (make changes to code...)
git status  # Check what changed
git diff    # Review changes
git add .
git commit -m "Descriptive message"

# End of day
git status  # Make sure everything is committed
git log -3  # Review what you accomplished today
```

### Before Deploying to Server

```bash
# Make sure everything is committed
git status

# Tag the version
git tag -a v1.0.0 -m "Phase 1 complete - ready for deployment"

# View all tags
git tag
```

### Regular Maintenance

```bash
# Weekly: Review your progress
git log --since="1 week ago" --oneline

# Clean up (be careful!)
git clean -n  # Preview what would be removed
```

---

**Remember:** Git is a safety net, not a burden. Commit early, commit often!

**Next Steps:**

1. Practice with small commits
2. Read commit messages later to remember what you did
3. When comfortable, explore branching
4. Eventually, consider GitHub for backup and collaboration

---

**Last Updated:** October 15, 2025
**For:** IMS Weather Forecast Automation Project
