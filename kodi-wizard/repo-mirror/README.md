# 🕊️ Pigeon Build - Kodi Repository Mirror

**Self-hosted Kodi addon repositories with daily automated updates**

## Overview

This directory contains a complete repository mirroring system that:
- ✅ Downloads addon repositories from official sources
- ✅ Hosts them locally for maximum reliability
- ✅ Updates daily via automated scripts
- ✅ Eliminates 404 errors and broken external links
- ✅ Tracks repository changes with MD5 hashing
- ✅ Generates HTML index for easy browsing

---

## Directory Structure

```
repo-mirror/
├── repositories/          # Downloaded repository ZIP files
│   ├── repository.thecrew.zip
│   ├── repository.loop.zip
│   ├── repository.umbrella.zip
│   ├── repository.nixgates.zip
│   └── repository.kodifitzwell.zip
├── addons/               # (Future) Individual addon ZIPs
├── sources/              # Repository source definitions
│   └── repo_sources.json
├── logs/                 # Update logs (created on first run)
├── download_repos.py     # Main download script
├── daily_update.sh       # Daily update wrapper script
├── setup_daily_update.sh # Setup guide for automated updates
├── index.html            # Generated repository listing
├── repo_hashes.json      # MD5 hashes for change detection
└── README.md             # This file
```

---

## Quick Start

### Download All Repositories

```bash
cd /home/mz1312/projects/pigeonhole/kodi-wizard/repo-mirror
python3 download_repos.py
```

This will:
1. Download all active repositories from `sources/repo_sources.json`
2. Save them to `repositories/`
3. Calculate MD5 hashes
4. Generate `index.html`
5. Log results to `download_log.txt`

### Manual Daily Update

```bash
./daily_update.sh
```

### Setup Automated Daily Updates

```bash
./setup_daily_update.sh
```

Follow the instructions to set up either:
- **systemd timer** (recommended) - runs at 2 AM daily
- **cron job** - traditional Unix scheduling

---

## Repository Sources

All repository sources are defined in `sources/repo_sources.json`.

### Currently Mirrored

| Repository | Addons | Source | Status |
|------------|--------|--------|--------|
| **The Crew** | The Chains, The Gears, Jokers Absolution, Genocide, Coalition, Ghost, Homelander, Luffy, Zoro | http://team-crew.github.io | ✅ Active |
| **The Loop** | The Loop | https://loopaddon.uk | ✅ Active |
| **Umbrella** | Umbrella, FenLight | https://umbrellaplug.github.io | ✅ Active |
| **Seren** | Seren | https://nixgates.github.io | ✅ Active |
| **POV** | POV (Point of View) | https://kodiyashimaru.github.io | ✅ Active |

---

## Adding New Repositories

### Method 1: Edit repo_sources.json

```json
{
  "repositories": {
    "newrepo": {
      "name": "New Repository Name",
      "repo_id": "repository.newrepo",
      "repo_url": "https://example.com/repository.newrepo-1.0.0.zip",
      "telegram_source": "Telegram Channel Name",
      "addons": [
        "Addon 1",
        "Addon 2"
      ],
      "status": "active",
      "last_checked": "2025-10-04",
      "notes": "Description of repository"
    }
  }
}
```

### Method 2: Quick Add Script

```bash
# Coming soon: add_repo.sh script
```

After adding, run:
```bash
python3 download_repos.py
```

---

## Telegram Integration

Repository links are tracked from Telegram channels where addon developers post updates.

### Recommended Telegram Channels

- **The Crew One Clicks**: https://t.me/+3Sa1tUs9wbBiZGQ8
- Check `sources/repo_sources.json` for more channels

### Getting New Links from Telegram

1. Join relevant Telegram channels
2. Watch for repository URL updates
3. Update `sources/repo_sources.json` with new URLs
4. Run `python3 download_repos.py` to download

---

## Automated Daily Updates

### systemd Timer (Recommended)

Set up once:

```bash
sudo tee /etc/systemd/system/repo-update.service > /dev/null <<EOF
[Unit]
Description=Kodi Repository Mirror Update
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$PWD
ExecStart=$PWD/daily_update.sh

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/repo-update.timer > /dev/null <<EOF
[Unit]
Description=Daily Kodi Repository Update
Requires=repo-update.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable repo-update.timer
sudo systemctl start repo-update.timer
```

Check status:
```bash
sudo systemctl status repo-update.timer
journalctl -u repo-update.service
```

### Cron Job

```bash
crontab -e
```

Add:
```
0 2 * * * /home/mz1312/projects/pigeonhole/kodi-wizard/repo-mirror/daily_update.sh
```

---

## Wizard Integration

The Pigeon Build Wizard automatically uses these self-hosted repositories.

### Configuration

In `plugin.program.pigeonbuild/uservar.py`:

```python
REPO_MIRROR_BASE = 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/repo-mirror/repositories'

ADDON_REPOS = {
    'thecrew': {
        'repo_url': f'{REPO_MIRROR_BASE}/repository.thecrew.zip',
        # ...
    }
}
```

### Deployment Workflow

1. **Download/Update Repositories**
   ```bash
   python3 download_repos.py
   ```

2. **Commit to Git**
   ```bash
   cd /home/mz1312/projects/pigeonhole
   git add kodi-wizard/repo-mirror/repositories/*.zip
   git commit -m "Update Kodi repositories $(date +%Y-%m-%d)"
   git push
   ```

3. **GitHub Serves Files**
   - Wizard downloads from `raw.githubusercontent.com`
   - No 404 errors!
   - Full control over availability

---

## Monitoring

### Check for Updates

```bash
python3 download_repos.py
```

Look for "UPDATE DETECTED" messages in output.

### View Logs

```bash
# Latest log
cat download_log.txt

# Daily update logs
ls -l logs/
cat logs/update_2025-10-04.log
```

### Check Repository Status

```bash
ls -lh repositories/

# Check MD5 hashes
cat repo_hashes.json
```

---

## Troubleshooting

### Repository Download Fails

**Problem**: `✗ Failed to download Repository Name: HTTP Error 404`

**Solutions**:
1. Check if source URL changed (common for community repos)
2. Visit Telegram channel for updated link
3. Update URL in `sources/repo_sources.json`
4. Set `status: "inactive"` if repository is permanently down

### Old Logs Filling Disk

Logs older than 30 days are automatically cleaned by `daily_update.sh`.

Manual cleanup:
```bash
find logs/ -name "update_*.log" -mtime +30 -delete
```

### Git Conflicts

The `daily_update.sh` script auto-commits changes. If you get conflicts:

```bash
cd /home/mz1312/projects/pigeonhole
git pull --rebase
git push
```

---

## Maintenance Schedule

### Daily (Automated)
- Download repository updates
- Check for changes
- Commit to git if changed
- Clean old logs (30+ days)

### Weekly (Manual Recommended)
- Check Telegram channels for announcements
- Verify all repositories still accessible
- Test wizard addon installation

### Monthly (Manual Recommended)
- Review `sources/repo_sources.json` for discontinued repos
- Add new popular addons
- Check for new addon releases

---

## Statistics

### Current Mirror Size

```bash
du -sh repositories/
# ~3.5 MB total (as of 2025-10-04)
```

### Individual Repository Sizes

```
repository.thecrew.zip     2.9 MB  (largest - includes 9 addons)
repository.loop.zip        420 KB
repository.umbrella.zip    161 KB
repository.nixgates.zip    6.3 KB
repository.kodifitzwell.zip  15 KB
```

---

## Benefits vs. External Links

### Before (External Links)
❌ Repositories go offline randomly
❌ 404 errors frustrate users
❌ URLs change without notice
❌ No control over availability
❌ Wizard looks broken

### After (Self-Hosted Mirror)
✅ Full control over repository files
✅ No 404 errors
✅ Daily automated updates
✅ Version tracking with MD5 hashes
✅ Professional, reliable wizard
✅ Works even if original source goes down (temporarily)

---

## Future Enhancements

- [ ] Mirror individual addon ZIPs (not just repositories)
- [ ] Add checksumverification
- [ ] Create backup mirror on secondary server
- [ ] API for checking repository status
- [ ] Email notifications on update failures
- [ ] Web dashboard for repository health

---

## Support

### Questions or Issues?

1. Check Telegram channels for addon updates
2. Review Kodi logs: `~/.kodi/temp/kodi.log`
3. Check update logs: `repo-mirror/logs/`
4. Verify repository sources: `sources/repo_sources.json`

### Contributing New Repositories

If you find a new repository or updated URL:

1. Fork the project
2. Update `sources/repo_sources.json`
3. Test with `python3 download_repos.py`
4. Submit a pull request

---

**Last Updated**: 2025-10-04
**Maintained By**: Pigeon Build Team
**Repository**: https://github.com/mz1312/pigeonhole

---

## License

Repository mirror system: GPL-3.0
Mirrored repositories: Licensed by their original authors
