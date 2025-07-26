# Practical Example: Before and After

## Current State (Manual)

**PCB Text Element:**
```
(gr_text "daedalus :: Rev A\nnnarain"
    (at 131.3 67.3 0)
    (layer "F.SilkS")
    ...
)
```

**Title Block:**
```
(title_block
    (date "2025-06-28")
    (rev "A")
    (comment 1 "Author: Natesh Narain")
)
```

**Problem:** To update revision to "B", you must manually edit both:
1. The text element: `"daedalus :: Rev A"` → `"daedalus :: Rev B"`
2. The title block: `(rev "A")` → `(rev "B")`

This is error-prone and doesn't scale with CI/CD.

## With Text Variables (Automated)

**PCB Text Element (one-time change):**
```
(gr_text "daedalus :: Rev ${REVISION}\nnnarain"
    (at 131.3 67.3 0)
    (layer "F.SilkS")
    ...
)
```

**Title Block (updated by script):**
```
(title_block
    (date "2025-06-28")
    (rev "B")  # Updated by script
    (comment 1 "Author: Natesh Narain")
)
```

**Result:** The text variable `${REVISION}` automatically resolves to "B", so the silk layer shows "daedalus :: Rev B".

## Automation Script Impact

**Running:**
```bash
python3 scripts/update_revision.py daedalus.kicad_pcb "1.5"
```

**Updates title block to:**
```
(title_block
    (date "2025-06-28")
    (rev "1.5")  # Automatically updated
    (comment 1 "Author: Natesh Narain")
)
```

**Text variable resolves to:**
- Silk layer displays: `daedalus :: Rev 1.5`
- All kibot outputs show: `1.5`

## CI/CD Integration Impact  

**Git workflow:**
```bash
git tag v2.1
git push --tags
```

**GitHub Actions automatically:**
1. Runs: `python3 scripts/update_revision.py daedalus.kicad_pcb`
2. Script detects tag `v2.1` and updates title block to `(rev "2.1")`
3. Kibot generates all outputs with revision `2.1`
4. Gerber files, PDFs, etc. all show `daedalus :: Rev 2.1`

**Benefits:**
- Single source of truth (git tags)
- No manual editing
- Consistent across all outputs
- Version controlled
- CI/CD ready

This transforms revision management from a manual, error-prone process into a fully automated, version-controlled workflow.