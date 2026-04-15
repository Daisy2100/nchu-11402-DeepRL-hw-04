#!/bin/bash
# ending.sh - End of development session

echo "========================================"
echo "   🏁 Wrapping Up Session   "
echo "========================================"

# 1. Update tasks.md
# Search for the latest active change folder
latest_change=$(ls -td openspec/changes/*/ 2>/dev/null | head -n 1)
if [ -n "$latest_change" ]; then
    echo "Latest change detected: $latest_change"
    if [ -f "${latest_change}tasks.md" ]; then
        echo "Found tasks.md, checking completion status..."
        # Extract progress if possible (OpenSpec usually manages this)
    fi
fi

# 2. Archive if everything is complete
# This usually requires interaction, so we'll just check if it's potentially ready
echo "Checking for completed changes to archive..."
# Npx openspec list usually shows a list of changes
npx openspec list

# 3. Generate Handover Document
echo ""
echo "📝 Writing handover.md..."
{
    echo "# Handover Document - $(date +'%Y-%m-%d %H:%M')"
    echo ""
    echo "## Recent Achievements"
    echo "Session completed. Code changes summarized in OpenSpec."
    echo ""
    echo "## Current State"
    npx openspec list | sed 's/^/ - /'
    echo ""
    echo "## Next Steps"
    echo "- review the latest specs and continue implementation."
    echo "- [ ] Next task here."
} > handover.md

# 4. Git Push
echo ""
echo "📤 Pushing changes to GitHub..."
git add .
# Using -n to check if there are changes to commit
if ! git diff --cached --quiet; then
    git commit -m "chore: session handover $(date +'%Y-%m-%d')"
    git push origin main
else
    echo "No changes to commit."
fi

echo ""
echo "✅ Session wrapped up. Goodbye!"
echo "========================================"
