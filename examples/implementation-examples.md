# Implementation Examples

## Example 1: KiCad Text Variables Only (Simple)

This is the minimal change approach - just update the text to use variables.

### Step 1: Update PCB Text Element

Change the manual text from:
```
(gr_text "daedalus :: Rev A\nnnarain"
```

To:
```
(gr_text "daedalus :: Rev ${REVISION}\nnnarain"
```

### Step 2: Update Title Block as Needed

When you want to update the revision, change the title block:
```
(title_block
    (date "2025-06-28")
    (rev "B")  # Change this manually
    (comment 1 "Author: Natesh Narain")
)
```

The silk layer text will automatically update to show the new revision.

## Example 2: Automated with Script (Recommended)

This approach automates the title block updates from git tags or environment.

### Step 1: Use the Provided Script

Run the script to update the title block:
```bash
python3 scripts/update_revision.py daedalus.kicad_pcb
```

Or specify a custom revision:
```bash
python3 scripts/update_revision.py daedalus.kicad_pcb "1.2"
```

### Step 2: Integrate with Kibot

Use the enhanced kibot configuration that runs the script automatically:
```bash
kibot -c daedalus-with-auto-revision.kibot.yaml
```

### Step 3: CI/CD Integration  

The script will automatically:
1. Get the latest git tag (e.g., "v1.2")
2. Strip the "v" prefix to get "1.2"
3. Update the title block with `(rev "1.2")`
4. Text variables automatically update silk layer to show "Rev 1.2"

## Testing the Implementation

1. **Test the script:**
   ```bash
   # Make a copy to test
   cp daedalus.kicad_pcb test.kicad_pcb
   
   # Update to revision B
   python3 scripts/update_revision.py test.kicad_pcb B
   
   # Check it worked
   grep -A3 -B1 "(rev" test.kicad_pcb
   ```

2. **Test with text variables:**
   First update the PCB to use `${REVISION}` in the text, then run:
   ```bash
   # This would require KiCad GUI to verify variable substitution
   # Or use kibot to generate outputs and check results
   ```

3. **Test with git tags:**
   ```bash
   # Create a test tag
   git tag v1.5
   
   # Run script (should pick up v1.5 and use "1.5")
   python3 scripts/update_revision.py test.kicad_pcb
   ```