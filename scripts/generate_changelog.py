#!/usr/bin/env python3
"""
Generate changelog content for GitHub releases from git history.
"""

import argparse
import subprocess
import sys
from typing import List, Optional


def run_git_command(cmd: List[str]) -> str:
    """Run a git command and return the output."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, cwd="."
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {' '.join(cmd)}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        return ""


def get_latest_tag() -> Optional[str]:
    """Get the latest git tag."""
    output = run_git_command(["git", "describe", "--tags", "--abbrev=0"])
    return output if output else None


def get_previous_tag(current_tag: str) -> Optional[str]:
    """Get the previous tag before the current one."""
    # First try to get all tags sorted by version
    all_tags = run_git_command(["git", "tag", "-l", "--sort=-version:refname"])
    if not all_tags:
        return None
        
    tags = [tag.strip() for tag in all_tags.split('\n') if tag.strip()]
    
    try:
        current_index = tags.index(current_tag)
        if current_index + 1 < len(tags):
            return tags[current_index + 1]
    except ValueError:
        pass
    
    # Fallback to git describe method
    output = run_git_command([
        "git", "describe", "--tags", "--abbrev=0", f"{current_tag}^"
    ])
    return output if output else None


def get_commits_between_tags(from_tag: Optional[str], to_tag: str) -> List[str]:
    """Get commit messages between two tags."""
    if from_tag:
        range_spec = f"{from_tag}..{to_tag}"
    else:
        range_spec = to_tag
    
    output = run_git_command([
        "git", "log", range_spec, "--oneline", "--no-merges"
    ])
    
    if not output:
        return []
    
    return [line.strip() for line in output.split('\n') if line.strip()]


def format_changelog(tag: str, commits: List[str]) -> str:
    """Format the changelog content."""
    if not commits:
        return f"## {tag}\n\nNo changes recorded."
    
    changelog = [f"## {tag}\n"]
    
    # Group commits by type if they follow conventional commit format
    features = []
    fixes = []
    other = []
    
    for commit in commits:
        # Parse commit message (format: "hash message")
        parts = commit.split(' ', 1)
        if len(parts) < 2:
            continue
            
        message = parts[1]
        
        if message.lower().startswith(('feat:', 'feature:')):
            features.append(f"- {message}")
        elif message.lower().startswith(('fix:', 'bugfix:')):
            fixes.append(f"- {message}")
        else:
            other.append(f"- {message}")
    
    if features:
        changelog.append("\n### Features")
        changelog.extend(features)
    
    if fixes:
        changelog.append("\n### Bug Fixes")
        changelog.extend(fixes)
    
    if other:
        changelog.append("\n### Changes")
        changelog.extend(other)
    
    return '\n'.join(changelog)


def main():
    parser = argparse.ArgumentParser(
        description="Generate changelog for GitHub releases"
    )
    parser.add_argument(
        "--tag", 
        help="Tag to generate changelog for (defaults to latest tag)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "text"],
        default="markdown",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    # Determine the tag to use
    if args.tag:
        current_tag = args.tag
    else:
        current_tag = get_latest_tag()
        if not current_tag:
            print("No tags found in repository", file=sys.stderr)
            sys.exit(1)
    
    # Get the previous tag
    previous_tag = get_previous_tag(current_tag)
    
    # Get commits between tags
    commits = get_commits_between_tags(previous_tag, current_tag)
    
    # Generate changelog
    changelog = format_changelog(current_tag, commits)
    
    print(changelog)


if __name__ == "__main__":
    main()