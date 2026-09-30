# Contribution & Development Workflow

To maintain traceability, quality, and clean git history throughout this DevSecOps platform project, all development must adhere strictly to the following GitHub Flow lifecycle.

---

## 1. Issue-Driven Development

Every task, feature, phase deliverable, or bug fix must start with an Issue:
1. Navigate to **[Issues](https://github.com/echoenvoy/SecOps-Pipeline/issues)**.
2. Click **New Issue** and select the appropriate template (Feature / Phase Task or Bug Report).
3. Assign a descriptive title, e.g.:
   - `[FEAT]: Phase 1 — Target Application and Dockerization`
   - `[BUG]: Fix SonarQube Scanner token authentication failure`
4. Note the generated **Issue number** (e.g., `#1`, `#5`).

---

## 2. Dedicated Branching

Never commit directly to `main` for new features or bug fixes. Always create an isolated branch from the latest `main`:

```bash
git checkout main
git pull origin main
git checkout -b feat/phase-1-target-app
# Or for a bug fix:
# git checkout -b fix/issue-5-login-form
```

Branch naming convention:
- Features / Phases: `feat/<short-description>` or `feature/issue-<num>-<desc>`
- Bug fixes: `fix/<short-description>` or `fix/issue-<num>-<desc>`
- Documentation: `docs/<short-description>`

---

## 3. Development, Testing & Commits

1. Implement the feature or fix.
2. Run local validation checkpoints (e.g. docker build, tests, linters).
3. Commit with semantic commit messages:
   ```bash
   git add <modified-files>
   git commit -m "feat(app): implement vulnerable authentication endpoint (closes #1)"
   ```
4. Push the branch to GitHub:
   ```bash
   git push -u origin feat/phase-1-target-app
   ```

---

## 4. Open a Pull Request (PR)

1. Navigate to the GitHub repository and open a Pull Request from your branch into `main`.
2. The PR description template will automatically load.
3. **CRUCIAL STEP**: In the description box, ensure the closing keyword is present:
   ```text
   Closes #<issue_number>
   ```
   *(e.g., `Closes #1` or `Closes #5`)*
4. Fill in the summary of changes and the validation checklist.
5. Review the PR, verify CI checks pass, and merge into `main`.
6. Once merged, GitHub will automatically close the linked issue.
