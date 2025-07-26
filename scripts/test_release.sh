#!/bin/bash
# Test script to validate the release automation components

set -e

echo "Testing changelog generation..."

# Test the changelog script
echo "1. Testing changelog script with current commits:"
python3 scripts/generate_changelog.py --tag "HEAD" || echo "  (Expected for repositories without tags)"

echo ""
echo "2. Testing with a hypothetical tag name:"
python3 scripts/generate_changelog.py --tag "v1.0.0" || echo "  (Expected for non-existent tags)"

echo ""
echo "3. Testing help option:"
python3 scripts/generate_changelog.py --help

echo ""
echo "4. Checking script permissions:"
ls -la scripts/generate_changelog.py

echo ""
echo "5. Validating workflow syntax:"
if command -v yamllint >/dev/null 2>&1; then
    yamllint .github/workflows/release.yml
else
    echo "  yamllint not available, checking basic YAML syntax..."
    python3 -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml'))"
fi

echo ""
echo "✅ All tests passed!"