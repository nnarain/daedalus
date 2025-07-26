# Automating PCB Revision Text Updates

This document provides a complete solution for automatically updating revision text on the Daedalus PCB's silk layer using KiCad text variables and Kibot automation.

## Problem Statement

The current PCB has manually hardcoded revision text on the F.SilkS layer:
```
(gr_text "daedalus :: Rev A\nnnarain"
```

This needs to be manually updated for each revision, which is error-prone and doesn't integrate well with version control or CI/CD workflows.

## Solution Overview

The solution uses KiCad's built-in text variables combined with automated scripts to:
1. Replace hardcoded text with KiCad variables
2. Automatically update the title block revision field
3. Integrate with git tags and CI/CD workflows

## Quick Start

### Option 1: Manual Text Variables (Minimal Change)

1. **Update the PCB text element** to use variables:
   ```
   (gr_text "daedalus :: Rev ${REVISION}\nnnarain"
   ```

2. **Update title block manually** when needed:
   ```
   (rev "B")  # Change A to B, etc.
   ```

The silk layer text will automatically show the correct revision.

### Option 2: Fully Automated (Recommended)

1. **Update the PCB text** to use variables (same as Option 1)

2. **Use the automation script:**
   ```bash
   python3 scripts/update_revision.py daedalus.kicad_pcb
   ```

3. **Run kibot with automation:**
   ```bash
   kibot -c daedalus-with-auto-revision.kibot.yaml
   ```

## Implementation Details

### Files Provided

- `scripts/update_revision.py` - Python script to update title block revision
- `daedalus-with-auto-revision.kibot.yaml` - Enhanced kibot config with automation
- `docs/revision-automation.md` - Detailed technical documentation
- `examples/implementation-examples.md` - Step-by-step examples

### How It Works

1. **KiCad Text Variables**: KiCad supports variables like `${REVISION}` that automatically pull values from the title block
2. **Title Block Update**: The Python script updates the title block revision field
3. **Git Integration**: Script can automatically pull revision from git tags
4. **Kibot Integration**: Enhanced configuration runs the script before generating outputs

### Revision Sources

The script can get revision information from:

1. **Git tags** (default): `git describe --tags --abbrev=0`
   - Tag `v1.2` becomes revision `1.2`
   - Tag `rev-B` becomes revision `rev-B`

2. **Environment variable**: `PCB_REVISION`
   ```bash
   PCB_REVISION=1.5 python3 scripts/update_revision.py
   ```

3. **Command line argument**:
   ```bash
   python3 scripts/update_revision.py daedalus.kicad_pcb "Rev C"
   ```

4. **Fallback**: Uses `A` if no other source available

## Testing

### Test the Script

```bash
# Test with specific revision
cp daedalus.kicad_pcb test.kicad_pcb
python3 scripts/update_revision.py test.kicad_pcb "Test Rev"

# Verify it worked
grep -A2 -B2 "(rev" test.kicad_pcb
```

### Test with Git Tags

```bash
# Create a test tag
git tag v2.0

# Test script picks it up
python3 scripts/update_revision.py test.kicad_pcb

# Should show revision "2.0"
grep -A2 -B2 "(rev" test.kicad_pcb
```

### Test Kibot Integration

```bash
# Run with automation (requires KiCad installation)
kibot -c daedalus-with-auto-revision.kibot.yaml

# Check that outputs contain updated revision
# Look in fab/gerbers/ for F.SilkS gerber file
```

## CI/CD Integration

### GitHub Actions Integration

The existing `.github/workflows/release.yml` can be enhanced:

```yaml
jobs:
  generate-outputs:
    name: "KiCAD Outputs"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
          
      # Optional: Set revision from tag
      - name: Set revision from tag
        run: |
          if [[ ${GITHUB_REF} == refs/tags/* ]]; then
            export PCB_REVISION=${GITHUB_REF#refs/tags/v}
            echo "PCB_REVISION=${PCB_REVISION}" >> $GITHUB_ENV
          fi
          
      - uses: INTI-CMNB/KiBot@v2_k9
        with:
          config: daedalus-with-auto-revision.kibot.yaml  # Use enhanced config
          dir: output
          schema: 'daedalus.kicad_sch'
          board: 'daedalus.kicad_pcb'
          verbose: 1
```

### Workflow

1. Developer creates git tag: `git tag v1.3 && git push --tags`
2. GitHub Actions triggers
3. Script updates title block to `(rev "1.3")`
4. KiCad text variables resolve `${REVISION}` to `1.3`
5. Silk layer shows `daedalus :: Rev 1.3`
6. All outputs (Gerbers, PDFs, etc.) have correct revision

## Benefits

- **Consistency**: Revision is consistent across all outputs
- **Automation**: No manual updates required
- **Version Control**: Tied to git tags
- **Error Reduction**: Eliminates manual copy/paste errors
- **CI/CD Ready**: Integrates with existing workflows

## Advanced Usage

### Custom Text Variables

You can add more text variables to the KiCad project:

```json
"text_variables": {
  "CUSTOM_REV": "Rev ${REVISION}",
  "BUILD_DATE": "${DATE}",
  "PROJECT": "${PROJECTNAME}"
}
```

Then use them in PCB text: `${CUSTOM_REV}` or `Build: ${BUILD_DATE}`

### Multiple Revision Texts

If you have multiple text elements that need revision updates, they can all use `${REVISION}` and will automatically stay in sync.

### Integration with Other Tools

The script can be easily modified to:
- Pull revision from build systems
- Update multiple PCB files
- Generate revision changelogs
- Send notifications

## Troubleshooting

### Script Issues

- **"No revision field found"**: The PCB file doesn't have a title block with revision field
- **"PCB file not found"**: Check file path and working directory
- **"Git tag not found"**: Script falls back to revision "A"

### KiCad Text Variables

- Variables only work in KiCad v6.0 and later
- Text must be exactly `${REVISION}` (case sensitive)
- Variables are resolved when outputs are generated

### Kibot Issues

- Ensure Python script is executable: `chmod +x scripts/update_revision.py`
- Check working directory in kibot config
- Verify KiCad installation for kibot

## Migration Guide

### From Manual Text

1. Identify all hardcoded revision text in PCB
2. Replace with `${REVISION}` variable
3. Test with different revision values
4. Integrate script into workflow

### Existing Projects

The solution is designed to be non-invasive:
- Original PCB files remain valid
- Script only updates title block
- Can be gradually rolled out

This approach provides a robust, automated solution for keeping PCB revision text synchronized with project versioning.