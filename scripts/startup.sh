#!/bin/bash
# startup.sh - Start of development session

echo "========================================"
echo "   🚀 Starting Development Session   "
echo "========================================"

# 1. Pull code from GitHub
echo "Syncing with remote repository..."
git pull origin main

# 2. Read handover document
if [ -f "handover.md" ]; then
    echo ""
    echo "📋 Handover Document Found:"
    echo "----------------------------------------"
    cat handover.md
    echo "----------------------------------------"
    
    # 3. Suggest next actions
    echo ""
    echo "💡 Suggested Next Actions:"
    grep -A 5 "## Next Steps" handover.md | grep "-" || echo "- Continue with the current OpenSpec change."
else
    echo ""
    echo "ℹ️ No handover.md found. Starting fresh."
fi

# 4. OpenSpec Init
echo ""
echo "🛠️ Initializing/Updating OpenSpec..."
npx openspec init . --tools gemini --force

echo ""
echo "✅ Startup complete. Ready to code!"
echo "========================================"
