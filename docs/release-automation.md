# Release Automation

This document describes the automated release generation process for the Daedalus project.

## Features

The release automation provides the following enhancements:

- **Automated Changelog**: Generates changelog content from git commit history between tags
- **3D PCB Render**: Automatically attaches the 3D render of the PCB to releases
- **Rich Release Descriptions**: Creates detailed release descriptions with embedded images
- **Asset Organization**: Properly organizes and names release assets

## How It Works

### Changelog Generation

The `scripts/generate_changelog.py` script:
- Extracts commits between the current and previous git tags
- Groups commits by type (features, fixes, other changes)
- Generates markdown-formatted changelog content
- Handles edge cases like first releases without previous tags

### 3D Render Attachment

The workflow:
- Uses the existing KiBot `render3d` output configuration
- Extracts the 3D render PNG from `output/renders/daedalus.png`
- Renames it to `daedalus-3d-render.png` for release attachment
- Embeds the image in the release description

### Release Body Format

Each release includes:
- Release title with version
- Embedded 3D PCB render image
- Generated changelog content
- Downloads section describing each asset

## Usage

The automation runs automatically when:
- A git tag is pushed to the repository
- The workflow is manually triggered via `workflow_dispatch`

### Manual Testing

Run the test suite to validate components:

```bash
# Run comprehensive tests
./scripts/test_comprehensive.sh

# Test changelog generation specifically
python3 scripts/generate_changelog.py --tag HEAD
```

## File Structure

```
scripts/
├── generate_changelog.py      # Main changelog generation script
├── test_comprehensive.sh      # Full test suite
└── test_release.sh           # Basic component tests

.github/workflows/
└── release.yml               # Enhanced workflow with automation
```

## Customization

### Changelog Format

Edit `scripts/generate_changelog.py` to modify:
- Commit grouping logic
- Markdown formatting
- Section headers

### Release Description

Edit `.github/workflows/release.yml` to customize:
- Release body template
- Asset descriptions
- Image placement

## Troubleshooting

- **No changelog generated**: Ensure the repository has commit history and proper git tag structure
- **Missing 3D render**: Verify the KiBot configuration generates output in `renders/daedalus.png`
- **Workflow fails**: Check that all required files exist and scripts have proper permissions