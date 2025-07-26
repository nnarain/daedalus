#!/usr/bin/env python3
"""
Script to update PCB revision text automatically
This script can be run as a kibot preflight script or standalone
"""

import sys
import re
import subprocess
import os
from pathlib import Path

def get_revision_from_git():
    """Get revision from git tags, fallback to 'A' if no tags"""
    try:
        # Try to get the latest tag
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'], 
            capture_output=True, text=True, cwd=Path(__file__).parent.parent
        )
        if result.returncode == 0:
            tag = result.stdout.strip()
            # Remove 'v' prefix if present (e.g., 'v1.2' -> '1.2')
            return tag.lstrip('v')
    except Exception as e:
        print(f"Warning: Could not get git tag: {e}")
    
    # Fallback to 'A' if no git tags found
    return 'A'

def get_revision_from_env():
    """Get revision from environment variable, useful for CI/CD"""
    return os.environ.get('PCB_REVISION', get_revision_from_git())

def update_pcb_title_block(pcb_file, new_revision):
    """Update the revision field in the PCB title block"""
    if not os.path.exists(pcb_file):
        print(f"Error: PCB file {pcb_file} not found")
        return False
    
    try:
        with open(pcb_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update title block revision
        original_content = content
        content = re.sub(
            r'\(rev ".*?"\)',
            f'(rev "{new_revision}")',
            content
        )
        
        if content != original_content:
            with open(pcb_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated PCB title block revision to: {new_revision}")
            return True
        else:
            print("No revision field found in title block")
            return False
            
    except Exception as e:
        print(f"Error updating PCB file: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) > 1:
        pcb_file = sys.argv[1]
    else:
        pcb_file = "daedalus.kicad_pcb"
    
    if len(sys.argv) > 2:
        revision = sys.argv[2]
    else:
        revision = get_revision_from_env()
    
    print(f"Updating {pcb_file} with revision: {revision}")
    
    success = update_pcb_title_block(pcb_file, revision)
    if success:
        print("PCB revision updated successfully!")
        print("Note: If using text variables like ${REVISION}, they will automatically update")
    else:
        print("Failed to update PCB revision")
        sys.exit(1)

if __name__ == "__main__":
    main()