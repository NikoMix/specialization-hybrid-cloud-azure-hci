<!-- Innersource PR template — Azure Local specialization -->

## Summary

<!-- One paragraph: what changed and why. -->

## Engagement phase this maps to

- [ ] Pre-qualification
- [ ] Discovery
- [ ] Architecture / design
- [ ] Build / deploy
- [ ] Knowledge transfer / hypercare
- [ ] Audit submission / remediation
- [ ] Not engagement-phase-specific (innersource / governance / CI)

## Audit control this maps to (if applicable)

<!-- e.g. B.1.1, A.2.1; leave blank if not applicable -->

## Type of change

- [ ] New audit control content
- [ ] New / updated engagement playbook page
- [ ] New / updated customer deliverable template (`static/templates/`)
- [ ] New / updated reference architecture
- [ ] Lesson learned / common-gap update
- [ ] Build / CI / dependency change

## Lifecycle state of the changed page(s)

- [ ] Draft
- [ ] Reviewed
- [ ] Endorsed
- [ ] Deprecated

## Validation

- [ ] `hugo --gc` builds with no warnings
- [ ] `python scripts/check-tables.py` passes — every table reaches the HTML
- [ ] `python scripts/check-links.py` passes — no leading-slash shortcode hrefs
- [ ] `bash .github/scripts/test-create-issues.sh` passes if `create-issues.sh` changed
- [ ] Content follows `.github/memories/hugo-content.md` (tables at column 0, no
  dots in filenames, status icons, shortcode hrefs without a leading slash)
- [ ] New / updated workfiles open cleanly in Word / PowerPoint / Excel
- [ ] CODEOWNERS reviewers are tagged

## Linked issues

<!-- "Closes #123" / "Refs #456" -->
