# Pigeon Build Wizard v1.0.2 - Critical Fixes Applied

## Date: 2025-10-04

## Issues Fixed

### Issue 1: All Addon Installations Failing with 404 Errors
**Problem:** Repository URLs were using incorrect versions or discontinued repositories.

**Root Cause:**
- The Crew: Using version 1.0.0 instead of current 0.3.8
- The Loop: Using wrong repository (afdah) instead of correct loop repository
- Umbrella: Using version 1.0.0 instead of current 2.2.6
- FenLight: Original tikipeter repository discontinued
- Seren: Using version 1.0.0 instead of current 2.2.0
- Ezra: Repository completely discontinued

**Solution Applied:**
Updated `/home/mz1312/.kodi/addons/plugin.program.pigeonbuild/uservar.py` with correct, working repository URLs:

```python
ADDON_REPOS = {
    'thecrew': {
        'repo_url': 'https://team-crew.github.io/repository.thecrew-0.3.8.zip',
    },
    'theloop': {
        'repo_id': 'repository.loop',
        'repo_url': 'https://loopaddon.uk/theloop/repository.loop-3.0.4.zip',
    },
    'umbrella': {
        'repo_url': 'https://umbrellaplug.github.io/repository.umbrella-2.2.6.zip',
    },
    'fenlight': {
        'repo_id': 'repository.umbrella',  # FenLight available through Umbrella repo
        'repo_url': 'https://umbrellaplug.github.io/repository.umbrella-2.2.6.zip',
    },
    'seren': {
        'repo_url': 'https://nixgates.github.io/packages/repository.nixgates-2.2.0.zip',
    },
    'pov': {  # Replaced discontinued Ezra
        'repo_id': 'repository.kodifitzwell',
        'repo_url': 'https://kodiyashimaru.github.io/repo/repository.kodifitzwell-0.0.1.zip',
    }
}
```

### Issue 2: Welcome Popup Appearing After Every Click
**Problem:** The welcome message displayed on every action, not just first run.

**Root Causes:**
1. Missing `settings.xml` file - Kodi couldn't persist addon settings
2. Firstrun check executed on every addon invocation
3. No check to limit welcome message to main menu only

**Solutions Applied:**

1. **Created `/home/mz1312/.kodi/addons/plugin.program.pigeonbuild/resources/settings.xml`**
   - Defines settings schema for Kodi
   - Includes 'firstrun' boolean setting
   - Allows proper setting persistence

2. **Updated `/home/mz1312/.kodi/addons/plugin.program.pigeonbuild/default.py`**
   - Modified firstrun check to only execute on main menu (no params)
   - Prevents welcome popup on submenu clicks
   - Added debug logging for troubleshooting

```python
# Only check firstrun on main menu
params_string = sys.argv[2][1:]
if not params_string:  # Only on main menu
    if ADDON.getSetting('firstrun') != 'true':
        wizard.first_run()
        ADDON.setSetting('firstrun', 'true')
```

## Files Modified

1. `/home/mz1312/.kodi/addons/plugin.program.pigeonbuild/uservar.py`
   - Updated all repository URLs to working versions
   - Replaced Ezra with POV addon
   - Fixed The Loop repository information

2. `/home/mz1312/.kodi/addons/plugin.program.pigeonbuild/default.py`
   - Fixed firstrun detection logic
   - Added parameter check to prevent welcome popup on submenus

3. `/home/mz1312/.kodi/addons/plugin.program.pigeonbuild/resources/settings.xml` (NEW)
   - Created settings schema with all addon settings
   - Enables proper setting persistence in Kodi

4. `/home/mz1312/.kodi/addons/plugin.program.pigeonbuild/addon.xml`
   - Updated version to 1.0.2
   - Added changelog for fixes

## Verified Working Repository URLs (as of 2025-10-04)

| Addon | Repository URL | Status |
|-------|---------------|--------|
| The Crew | https://team-crew.github.io/repository.thecrew-0.3.8.zip | VERIFIED |
| The Loop | https://loopaddon.uk/theloop/repository.loop-3.0.4.zip | VERIFIED |
| Umbrella | https://umbrellaplug.github.io/repository.umbrella-2.2.6.zip | VERIFIED |
| Seren | https://nixgates.github.io/packages/repository.nixgates-2.2.0.zip | VERIFIED |
| POV | https://kodiyashimaru.github.io/repo/repository.kodifitzwell-0.0.1.zip | VERIFIED |

## Testing Instructions

### To Test Addon Installation:

1. **Restart Kodi** to reload the updated addon code
   ```bash
   # If running Kodi from command line, stop and restart
   # OR restart via Kodi menu: System > Power > Exit
   ```

2. **Clear the firstrun setting** (optional - to test welcome popup fix):
   ```bash
   rm /home/mz1312/.kodi/userdata/addon_data/plugin.program.pigeonbuild/settings.xml
   ```

3. **Test the addon installer:**
   - Open Kodi
   - Navigate to Add-ons > Program add-ons > Pigeon Build Wizard
   - Select "Install Add-ons"
   - Try installing one of the addons (recommend starting with The Crew)
   - Should download repository and install without 404 errors

4. **Verify welcome popup fix:**
   - First open: Should show welcome message
   - Close welcome message
   - Navigate through wizard menus
   - Welcome should NOT appear again

### Expected Behavior:

**Addon Installation:**
- Progress dialog shows download progress
- Repository ZIP downloads successfully (no 404)
- Repository extracts and installs to ~/.kodi/addons/
- Repository enables via JSON-RPC
- Addon installs from repository
- Success message displays

**Welcome Popup:**
- Shows ONLY on first run
- Does NOT show on subsequent visits
- Does NOT show when clicking menu items

## Troubleshooting

### If addon installation still fails:

1. **Check Kodi log for errors:**
   ```bash
   # Find Kodi log location (varies by platform)
   # On Linux: ~/.kodi/temp/kodi.log
   # Check for HTTP errors or download failures
   ```

2. **Test repository URLs manually:**
   ```bash
   curl -I https://team-crew.github.io/repository.thecrew-0.3.8.zip
   # Should return: HTTP/1.1 200 OK
   ```

3. **Verify internet connectivity:**
   - Ensure device has internet access
   - Check if GitHub/repository hosts are accessible

### If welcome popup still appears:

1. **Check settings.xml exists:**
   ```bash
   ls -la /home/mz1312/.kodi/addons/plugin.program.pigeonbuild/resources/settings.xml
   ```

2. **Verify firstrun setting:**
   ```bash
   cat /home/mz1312/.kodi/userdata/addon_data/plugin.program.pigeonbuild/settings.xml
   # Should contain: <setting id="firstrun">true</setting>
   ```

3. **Check Kodi log for setting errors:**
   ```bash
   grep -i "pigeon\|firstrun" ~/.kodi/temp/kodi.log
   ```

## Notes on Repository Status (2025-10-04)

### Discontinued Addons:
- **Ezra**: Completely discontinued by developer
  - Replacement: POV (Point of View) addon
  - POV is the official successor

- **FenLight (original tikipeter)**: Repository removed
  - FenLight still available through Umbrella repository
  - Alternative: FenLightAM (fork) at https://fenlightanonymouse.github.io/packages

### Repository Version Notes:
- Repository versions change frequently
- URLs in this fix are current as of October 2025
- If URLs break in future, check GitHub pages for latest versions:
  - The Crew: https://team-crew.github.io/
  - The Loop: https://loopaddon.uk/theloop/
  - Umbrella: https://umbrellaplug.github.io/
  - Seren: https://nixgates.github.io/packages/

## Additional Improvements Made

### Settings Schema:
Created comprehensive settings.xml with categories:
- General (notifications, updates)
- Builds (backup options)
- Maintenance (auto-cleanup)
- Advanced (debug logging)
- Debrid Services (keep settings)

### Version Management:
- Updated addon version: 1.0.1 → 1.0.2
- Updated uservar.py version constant
- Added detailed changelog in addon.xml

## Deployment to GitHub

To update the repository on GitHub:

```bash
cd /home/mz1312/projects/pigeonhole/kodi-wizard

# Copy updated files from Kodi to repo
cp /home/mz1312/.kodi/addons/plugin.program.pigeonbuild/uservar.py .
cp /home/mz1312/.kodi/addons/plugin.program.pigeonbuild/default.py .
cp /home/mz1312/.kodi/addons/plugin.program.pigeonbuild/addon.xml .
cp /home/mz1312/.kodi/addons/plugin.program.pigeonbuild/resources/settings.xml resources/

# Commit and push
git add .
git commit -m "v1.0.2: Fix 404 errors and welcome popup issue"
git push origin main
```

## Summary

Both critical issues have been resolved:

1. **404 Errors**: All repository URLs updated to current, working versions
2. **Welcome Popup**: Fixed by creating settings.xml and improving firstrun logic

The wizard should now function correctly for addon installation and provide a better user experience without repetitive welcome messages.

Version 1.0.2 is ready for testing and deployment.
