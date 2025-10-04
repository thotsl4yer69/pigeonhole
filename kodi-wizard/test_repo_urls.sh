#!/bin/bash

# Test script to verify all repository URLs are accessible
# Run this to ensure addon installations will work

echo "========================================="
echo "Testing Pigeon Build Repository URLs"
echo "========================================="
echo ""

test_url() {
    local name="$1"
    local url="$2"

    echo -n "Testing $name... "

    if curl -f -s -I "$url" > /dev/null 2>&1; then
        echo "✓ SUCCESS"
        return 0
    else
        echo "✗ FAILED"
        return 1
    fi
}

# Test all repository URLs
test_url "The Crew" "https://team-crew.github.io/repository.thecrew-0.3.8.zip"
test_url "The Loop" "https://loopaddon.uk/theloop/repository.loop-3.0.4.zip"
test_url "Umbrella" "https://umbrellaplug.github.io/repository.umbrella-2.2.6.zip"
test_url "Seren" "https://nixgates.github.io/packages/repository.nixgates-2.2.0.zip"
test_url "POV" "https://kodiyashimaru.github.io/repo/repository.kodifitzwell-0.0.1.zip"

echo ""
echo "========================================="
echo "Test Complete"
echo "========================================="
