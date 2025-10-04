# Pigeon Build Wizard - Quick Fix Summary

## Version 1.0.2 - Critical Issues Fixed

### What Was Broken:
1. All addon installations failed with 404 errors
2. Welcome popup appeared after every click

### What Was Fixed:
1. Updated all repository URLs to working versions
2. Fixed welcome popup to only show once

---

## How to Apply the Fixes

### If Kodi is Running:
**RESTART KODI** to load the updated addon code.

### If You Already Saw the Welcome Popup:
It won't appear again. The fix prevents it from showing on every click.

---

## Working Addons (as of Oct 2025)

| Addon | Status | Notes |
|-------|--------|-------|
| The Crew | ✓ Working | Most popular, great sources |
| The Loop | ✓ Working | Live sports streaming |
| Umbrella | ✓ Working | Feature-rich, debrid-friendly |
| Seren | ✓ Working | Premium debrid addon |
| POV | ✓ Working | Replaces discontinued Ezra |
| FenLight | ⚠ Via Umbrella | Original repo discontinued |

---

## Quick Test

1. Restart Kodi
2. Open Pigeon Build Wizard
3. Select "Install Add-ons"
4. Try installing "The Crew"
5. Should work without 404 errors

---

## Updated Repository URLs

```
The Crew:  https://team-crew.github.io/repository.thecrew-0.3.8.zip
The Loop:  https://loopaddon.uk/theloop/repository.loop-3.0.4.zip
Umbrella:  https://umbrellaplug.github.io/repository.umbrella-2.2.6.zip
Seren:     https://nixgates.github.io/packages/repository.nixgates-2.2.0.zip
POV:       https://kodiyashimaru.github.io/repo/repository.kodifitzwell-0.0.1.zip
```

All URLs verified working on 2025-10-04.

---

## Changed Files

These files were updated in your Kodi installation:

```
~/.kodi/addons/plugin.program.pigeonbuild/
├── addon.xml (version updated to 1.0.2)
├── uservar.py (repository URLs fixed)
├── default.py (firstrun logic fixed)
└── resources/
    └── settings.xml (NEW - enables settings persistence)
```

---

## Need Help?

Check the detailed documentation:
- Full analysis: `/home/mz1312/projects/pigeonhole/kodi-wizard/FIXES_APPLIED.md`
- Test URLs: Run `/home/mz1312/projects/pigeonhole/kodi-wizard/test_repo_urls.sh`

---

**TL;DR**: Restart Kodi. Try installing addons. They should work now.
