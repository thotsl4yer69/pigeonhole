# Pigeon Build Wizard - Diagnostic Report

## Problem Summary
The Pigeon Build Wizard looks good cosmetically but **doesn't actually do anything**. It's essentially a UI shell with no functional implementation.

## Missing Functionality

### 1. Build Installation (CRITICAL)
**Current Status:** Fake progress dialog, no actual download or installation

**File:** `resources/lib/wizard.py` line 202-252
```python
# TODO: Implement actual download and installation
```

**What's Missing:**
- Download build ZIP from URL
- Extract ZIP to temporary directory
- Backup current userdata
- Copy extracted files to Kodi directories
- Apply GUI settings
- Apply theme settings
- Force Kodi reload

**RedWizard Implementation:**
- Uses `urllib` or `requests` to download files
- Uses `zipfile` module to extract
- Uses `shutil` to copy files
- Uses `xbmc.executebuiltin()` to reload Kodi

### 2. Advanced Settings (CRITICAL)
**Current Status:** Shows confirmation dialog but doesn't apply anything

**File:** `resources/lib/wizard.py` line 263-280
```python
# TODO: Implement actual settings application
```

**What's Missing:**
- Apply cache settings via JSON-RPC
- Set buffer mode, memory size, read factor
- Update advancedsettings.xml

**RedWizard Implementation:**
```python
# From maintenance.py line 54-77
def advanced_set(buffer, ram, read):
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"filecache.buffermode","value":%s},"id":1}' %(buffer))
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"filecache.memorysize","value":%s},"id":1}' %(ram))
    xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{"setting":"filecache.readfactor","value":%s},"id":1}' %(read))
```

**Device-Specific Settings:**
- Fire TV Stick 1GB: buffermode=2, memorysize=128MB, readfactor=1000
- Fire TV Stick 2GB/4K: buffermode=2, memorysize=192MB, readfactor=1000
- Shield 3GB: buffermode=2, memorysize=256MB, readfactor=1000

### 3. Add-on Installation (HIGH PRIORITY)
**Current Status:** Shows notification but doesn't install anything

**File:** `resources/lib/wizard.py` line 254-261
```python
# TODO: Implement actual addon installation
```

**What's Missing:**
- Download addon repository ZIP
- Install repository via Kodi's addon installer
- Install specific addons from repository

**RedWizard Implementation:**
- Uses `xbmc.executebuiltin('InstallAddon(repository.id)')`
- Uses JSON-RPC to enable addons
- Monitors addon installation status

### 4. Maintenance Functions (NOT IMPLEMENTED)
**Current Status:** Menu items exist but no actions implemented

**File:** `resources/lib/wizard.py` line 138-160
- Clear Cache: Not implemented
- Clear Packages: Not implemented
- Clear Thumbnails: Not implemented
- Purge Databases: Not implemented
- Fresh Start: Not implemented

**RedWizard Implementation:**
```python
# Clear Thumbnails
def clear_thumbnails():
    if os.path.exists(os.path.join(user_path, 'Thumbnails')):
        shutil.rmtree(os.path.join(user_path, 'Thumbnails'))
    purge_db(textures_db)

# Purge Database
def purge_db(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    for table in cur.fetchall():
        if table[0] != 'version':
            cur.execute("DELETE FROM %s" % table[0])
    conn.execute('VACUUM')
```

### 5. Backup/Restore (NOT IMPLEMENTED)
**Current Status:** Menu items exist but no functionality

**What's Missing:**
- Create ZIP backup of Kodi userdata
- Save to backup location
- List available backups
- Restore from backup ZIP

### 6. First Run Welcome Message Loop
**Current Status:** Welcome message keeps appearing on every launch

**File:** `default.py` line 135-137
```python
if not ADDON.getSetting('firstrun'):
    wizard.first_run()
    ADDON.setSetting('firstrun', 'true')
```

**Issue:** `getSetting()` might return empty string instead of boolean False
**Fix:** Change to:
```python
if ADDON.getSetting('firstrun') != 'true':
    wizard.first_run()
    ADDON.setSetting('firstrun', 'true')
```

## What Actually Works
✅ Main menu navigation
✅ GUI/cosmetic elements
✅ Color scheme and branding
✅ Dialog boxes and notifications
✅ Settings addon structure

## What Doesn't Work
❌ Install Fresh Build - shows fake progress
❌ Install Add-ons - does nothing
❌ Advanced Settings - doesn't apply settings
❌ Maintenance - all options non-functional
❌ Backup & Restore - not implemented
❌ First run flag - keeps resetting

## Comparison to RedWizard

| Feature | RedWizard | Pigeon Build |
|---------|-----------|--------------|
| Build Installation | ✅ Full implementation | ❌ TODO only |
| Advanced Settings | ✅ JSON-RPC | ❌ TODO only |
| Maintenance Tools | ✅ Working | ❌ Not implemented |
| Backup/Restore | ✅ Working | ❌ Not implemented |
| Add-on Installation | ✅ Working | ❌ TODO only |
| Visual Polish | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Actual Functionality | ⭐⭐⭐⭐⭐ | ⭐ |

## Priority Implementation Order

### Phase 1: Critical Fixes
1. **Fix first run loop** (5 minutes)
2. **Implement Advanced Settings** (30 minutes) - Most impactful for users
3. **Implement Clear Cache/Thumbnails** (30 minutes) - Basic maintenance

### Phase 2: Core Features
4. **Implement Add-on Installation** (2 hours) - Repository-based addon installation
5. **Implement Clear Packages** (30 minutes)
6. **Implement Purge Databases** (1 hour)

### Phase 3: Advanced Features
7. **Implement Build Installation** (4-6 hours) - Complex, requires hosting
8. **Implement Backup/Restore** (2-3 hours)

### Phase 4: Polish
9. **Create actual build ZIPs** (variable time)
10. **Host files on GitHub/web server** (variable time)
11. **Test on actual Fire TV Stick** (ongoing)

## Recommended Immediate Actions

1. **Fix the welcome message loop** - Quick win
2. **Implement advanced settings** - Provides immediate value to users
3. **Implement basic maintenance** - Cache clearing is essential
4. **Either:**
   - a) Implement full functionality (12-20 hours work)
   - b) Remove non-working menu items temporarily
   - c) Add "Coming Soon" notices to non-working features

## Code Files Needing Updates

- `default.py` - Fix first run check
- `resources/lib/wizard.py` - Implement all TODO functions
- Create `resources/lib/downloader.py` - Build download/extraction
- Create `resources/lib/maintenance.py` - Maintenance functions (based on RedWizard)
- `uservar.py` - Update build URLs to actual hosted files

## Conclusion

The Pigeon Build Wizard is a **beautiful but empty shell**. It needs substantial implementation work to match the functionality of RedWizard. The good news is the UI/UX is excellent - it just needs the backend implementation.

Estimated total implementation time: **15-25 hours** for full feature parity with RedWizard.
