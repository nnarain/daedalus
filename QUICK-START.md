# Quick Reference: Revision Automation Methods

## Method 1: KiCad Text Variables (Simplest)

**Change this:**
```
(gr_text "daedalus :: Rev A\nnnarain"
```

**To this:**
```
(gr_text "daedalus :: Rev ${REVISION}\nnnarain"
```

**Benefits:** 
- Minimal change
- Native KiCad feature
- Automatically updates when title block changes

## Method 2: Automated Script + Text Variables (Recommended)

**Step 1:** Use text variables (same as Method 1)

**Step 2:** Run automation script:
```bash
python3 scripts/update_revision.py daedalus.kicad_pcb
```

**Step 3:** Use enhanced kibot config:
```bash
kibot -c daedalus-with-auto-revision.kibot.yaml
```

**Benefits:**
- Fully automated
- Pulls from git tags
- CI/CD ready
- No manual updates needed

## Method 3: CI/CD Integration

**Workflow:**
1. Create git tag: `git tag v1.2`
2. Push: `git push --tags` 
3. GitHub Actions runs automatically
4. Script updates title block to `(rev "1.2")`
5. Text variable shows `daedalus :: Rev 1.2`
6. All outputs have correct revision

**Benefits:**
- Zero manual intervention
- Version control integrated
- Consistent across all outputs
- Error-free

## Files to Use

- **Script:** `scripts/update_revision.py`
- **Enhanced Config:** `daedalus-with-auto-revision.kibot.yaml`
- **Documentation:** `README-revision-automation.md`
- **Examples:** `examples/implementation-examples.md`

## Testing Commands

```bash
# Test script
cp daedalus.kicad_pcb test.kicad_pcb
python3 scripts/update_revision.py test.kicad_pcb "Test Rev"
grep -A2 -B2 "(rev" test.kicad_pcb

# Test with git tags
git tag v2.0
python3 scripts/update_revision.py test.kicad_pcb
```