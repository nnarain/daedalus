# Automating Revision Text Updates in KiCad PCBs with Kibot

This document outlines methods to automatically update revision text on PCB silk layers using KiCad text variables and Kibot automation tools.

## Current State

The Daedalus PCB currently has:
- Manual revision text on F.SilkS layer: `"daedalus :: Rev A\nnnarain"`
- Title block with revision field: `(rev "A")` in the PCB file
- Empty text variables section in the KiCad project file

## Available Approaches

### 1. KiCad Text Variables (Recommended)

KiCad supports built-in text variables that automatically update based on project settings.

#### Supported Variables:
- `${REVISION}` - Pulls from title block revision field
- `${DATE}` - Pulls from title block date field  
- `${TITLE}` - Pulls from title block title field
- `${COMPANY}` - Pulls from title block company field
- `${PROJECTNAME}` - Project name from .kicad_pro file
- `${COMMENT1}` through `${COMMENT9}` - Title block comments

#### Implementation:
1. Replace manual text with: `"daedalus :: Rev ${REVISION}\nnnarain"`
2. Update title block revision field when needed
3. Text automatically updates in all outputs

#### Pros:
- Native KiCad feature
- Automatically updates across all outputs
- No additional scripting required
- Version controlled with the PCB file

#### Cons:
- Requires manual update of title block revision field
- Limited to KiCad's built-in variables

### 2. Kibot Text Replacement Filters

Kibot can replace text during output generation using various sources.

#### Example Configuration:

```yaml
kibot:
  version: 1

# Global variables
global:
  # Can pull revision from git tags, environment, etc.
  revision: 'B'

preflight:
  run_erc: false
  run_drc: false
  # Update KiCad text variables before processing
  set_text_variables:
    - variable: 'REVISION'
      value: '${global.revision}'
      # Or from git: 'git describe --tags --abbrev=0'

outputs:
  - name: gerbers
    comment: Gerbers with updated revision
    type: gerber
    dir: fab/gerbers
    # Text variables are resolved during generation
```

#### Pros:
- Can pull revision from multiple sources (git tags, CI environment, etc.)
- Flexible and scriptable
- Can update multiple text elements simultaneously

#### Cons:
- More complex configuration
- Requires understanding of Kibot variables system
- May need custom scripting for complex scenarios

### 3. Pre-flight Scripts

Custom scripts run before Kibot processing to modify PCB files.

#### Example Script (Python):

```python
#!/usr/bin/env python3
import sys
import re
import subprocess

def get_git_revision():
    """Get the latest git tag as revision"""
    try:
        result = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], 
                              capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return "A"  # Default fallback

def update_pcb_revision(pcb_file, new_revision):
    """Update revision in PCB file"""
    with open(pcb_file, 'r') as f:
        content = f.read()
    
    # Update title block revision
    content = re.sub(
        r'\(rev ".*?"\)',
        f'(rev "{new_revision}")',
        content
    )
    
    # Update silk text if using variables
    # Text variables will automatically use the updated title block
    
    with open(pcb_file, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    revision = get_git_revision()
    update_pcb_revision("daedalus.kicad_pcb", revision)
    print(f"Updated revision to: {revision}")
```

#### Kibot Configuration:
```yaml
preflight:
  run_erc: false
  run_drc: false
  # Run custom script before processing
  run_script: ['python3', 'update_revision.py']
```

#### Pros:
- Maximum flexibility
- Can integrate with any external system
- Can update multiple files/fields

#### Cons:
- Requires custom scripting
- More maintenance overhead
- Risk of corrupting PCB files if script has bugs

## Recommended Implementation

### Phase 1: KiCad Text Variables (Immediate)

1. Update the PCB text element to use variables:
   ```
   (gr_text "daedalus :: Rev ${REVISION}\nnnarain"
   ```

2. This provides automatic updates whenever the title block revision is changed.

### Phase 2: Automated Title Block Updates (Advanced)

1. Add a pre-flight script to update the title block revision from git tags:
   ```yaml
   preflight:
     run_erc: false
     run_drc: false
     set_text_variables:
       - variable: 'REVISION'
         command: 'git describe --tags --abbrev=0 | sed s/v//'
   ```

2. This automatically pulls the revision from git tags during CI/CD.

## Testing the Implementation

### Test KiCad Text Variables:
1. Create a copy of the PCB file
2. Replace the manual text with variable text
3. Verify the variable resolves correctly in KiCad
4. Test with Kibot output generation

### Test Kibot Integration:
1. Add variable configuration to kibot.yaml
2. Run kibot with test configuration
3. Verify outputs contain correct revision information

## Integration with CI/CD

The GitHub workflow already runs kibot on tag pushes. With automated revision updates:

1. Developer creates a new release tag (e.g., `v1.1`)
2. GitHub Actions triggers kibot processing
3. Pre-flight script updates title block revision to "1.1"
4. Text variables automatically update silk layer text
5. All outputs (Gerbers, PDFs, etc.) contain correct revision

This ensures consistency between git tags, documentation, and manufactured PCBs.