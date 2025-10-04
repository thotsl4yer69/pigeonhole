#!/bin/bash
#
# Daily Repository Update Script
# Checks for updates and downloads new versions
# Run daily via cron: 0 2 * * * /path/to/daily_update.sh
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Log file with date
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/update_$(date +%Y-%m-%d).log"

echo "======================================" | tee -a "$LOG_FILE"
echo "Repository Update - $(date)" | tee -a "$LOG_FILE"
echo "======================================" | tee -a "$LOG_FILE"

# Run the Python downloader
python3 download_repos.py 2>&1 | tee -a "$LOG_FILE"

# Check if any files were updated
if [ -f "$SCRIPT_DIR/repo_hashes.json" ]; then
    CHANGES=$(git -C "$SCRIPT_DIR/.." status --porcelain repo-mirror/repositories/ 2>/dev/null | wc -l)
    if [ "$CHANGES" -gt 0 ]; then
        echo "Changes detected - repositories updated" | tee -a "$LOG_FILE"

        # Optional: Commit to git if in a repo
        if [ -d "$SCRIPT_DIR/../.git" ]; then
            cd "$SCRIPT_DIR/.."
            git add repo-mirror/repositories/*.zip repo-mirror/index.html repo-mirror/repo_hashes.json
            git commit -m "Auto-update: Kodi repositories $(date +%Y-%m-%d)" 2>&1 | tee -a "$LOG_FILE"
            echo "Git commit created" | tee -a "$LOG_FILE"
        fi
    else
        echo "No changes detected" | tee -a "$LOG_FILE"
    fi
fi

# Clean old logs (keep 30 days)
find "$LOG_DIR" -name "update_*.log" -mtime +30 -delete

echo "Update complete: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
