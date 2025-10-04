#!/bin/bash
#
# Setup daily update via systemd timer or cron
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPDATE_SCRIPT="$SCRIPT_DIR/daily_update.sh"

echo "================================================"
echo "Kodi Repository Mirror - Daily Update Setup"
echo "================================================"

# Check if systemd is available
if command -v systemctl &> /dev/null; then
    echo ""
    echo "Option 1: systemd timer (Recommended)"
    echo "  - Runs at 2 AM daily"
    echo "  - Integrated with system services"
    echo "  - View logs: journalctl -u repo-update.service"
    echo ""
    echo "To set up systemd timer:"
    echo ""
    echo "sudo tee /etc/systemd/system/repo-update.service > /dev/null <<EOF
[Unit]
Description=Kodi Repository Mirror Update
After=network.target

[Service]
Type=oneshot
User=$(whoami)
WorkingDirectory=$SCRIPT_DIR
ExecStart=$UPDATE_SCRIPT

[Install]
WantedBy=multi-user.target
EOF"
    echo ""
    echo "sudo tee /etc/systemd/system/repo-update.timer > /dev/null <<EOF
[Unit]
Description=Daily Kodi Repository Update
Requires=repo-update.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
EOF"
    echo ""
    echo "sudo systemctl daemon-reload"
    echo "sudo systemctl enable repo-update.timer"
    echo "sudo systemctl start repo-update.timer"
    echo ""
fi

echo "Option 2: cron job"
echo "  - Traditional Unix scheduling"
echo "  - Runs at 2 AM daily"
echo ""
echo "To set up cron job:"
echo ""
echo "crontab -e"
echo ""
echo "Add this line:"
echo "0 2 * * * $UPDATE_SCRIPT"
echo ""

echo "================================================"
echo "Manual Update"
echo "================================================"
echo ""
echo "To manually update repositories:"
echo "  cd $SCRIPT_DIR"
echo "  ./daily_update.sh"
echo ""
echo "Or:"
echo "  python3 download_repos.py"
echo ""
