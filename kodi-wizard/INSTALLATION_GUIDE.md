# Pigeon Build Wizard - Installation Guide

**Fast Streaming • Zero Buffer • Optimized for Fire TV Stick**

---

## 📋 Table of Contents

1. [Quick Install (Recommended)](#quick-install-recommended)
2. [Manual Installation](#manual-installation)
3. [Fire TV Stick Installation via ADB](#fire-tv-stick-installation-via-adb)
4. [First Time Setup](#first-time-setup)
5. [Features Overview](#features-overview)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Install (Recommended)

### Method 1: Install Repository from File Manager

1. **Download the Repository ZIP**
   - Download: `repository.pigeonbuild-1.0.0.zip`
   - Save to a location you can access in Kodi

2. **Enable Unknown Sources** (if not already enabled)
   - Go to Kodi **Settings** → **System** → **Add-ons**
   - Enable **Unknown Sources**
   - Click **Yes** when warned

3. **Install from ZIP File**
   - Go to Kodi **Settings** → **Add-ons**
   - Click **Install from zip file**
   - Navigate to where you saved the repository ZIP
   - Select `repository.pigeonbuild-1.0.0.zip`
   - Wait for "Pigeon Build Repository installed" notification

4. **Install the Wizard**
   - Click **Install from repository**
   - Select **Pigeon Build Repository**
   - Go to **Program add-ons**
   - Select **Pigeon Build Wizard**
   - Click **Install**
   - Wait for installation to complete

5. **Launch the Wizard**
   - Go to **Add-ons** → **Program add-ons**
   - Select **Pigeon Build Wizard**
   - Click to launch

---

## 🔧 Manual Installation

### Prerequisites
- Kodi 19 (Matrix) or newer
- Internet connection
- 500MB+ free storage (for builds)

### Step-by-Step

1. **Download Files**
   ```
   repository.pigeonbuild-1.0.0.zip
   ```

2. **Transfer to Device**
   - **Fire TV Stick**: Use file manager app (like FileLinked, Downloader, or ADB)
   - **Android**: Download directly or transfer via USB
   - **PC/Mac**: Download to local storage
   - **Shield**: Use file manager or network transfer

3. **Install in Kodi**
   - Settings → Add-ons → Install from zip file
   - Navigate to downloaded ZIP
   - Install repository first
   - Then install wizard from repository

---

## 📱 Fire TV Stick Installation via ADB

**For advanced users or bulk deployments**

### Prerequisites
- ADB installed on your computer
- Fire TV Stick with ADB debugging enabled
- Fire TV Stick and computer on same network

### Enable ADB on Fire TV Stick

1. Go to **Settings** → **My Fire TV** → **Developer Options**
2. Turn on **ADB Debugging**
3. Turn on **Apps from Unknown Sources**
4. Note your Fire TV IP address (Settings → My Fire TV → About → Network)

### Install via ADB

```bash
# Connect to Fire TV Stick
adb connect <firestick-ip>:5555

# Verify connection
adb devices

# Push repository to Fire TV
adb push repository.pigeonbuild-1.0.0.zip /sdcard/Download/

# Optional: Push wizard directly (for manual install)
adb push plugin.program.pigeonbuild-1.0.0.zip /sdcard/Download/
```

### Install in Kodi

1. Open Kodi on Fire TV Stick
2. Go to Settings → Add-ons → Install from zip file
3. Navigate to `/sdcard/Download/`
4. Install `repository.pigeonbuild-1.0.0.zip`
5. Then install wizard from the repository

---

## 🎯 First Time Setup

### Welcome Screen

When you first launch Pigeon Build Wizard, you'll see a welcome message. This only appears once.

### Recommended First Steps

1. **Apply Advanced Settings** (Most Important!)
   - Main Menu → Advanced Settings
   - Select your device:
     - **Fire TV Stick (1GB RAM)** - Original Fire TV Stick/Lite
     - **Fire TV Stick (2GB RAM) / 4K** - Fire TV Stick 4K, 4K Max
     - **NVIDIA Shield (3GB RAM)** - Shield TV/Pro
     - **PC/Desktop (4GB+ RAM)** - Windows, Mac, Linux
   - Confirm to apply settings
   - **Restart Kodi** for settings to take effect

2. **Run Maintenance** (Optional but Recommended)
   - Main Menu → Maintenance → Clear Cache
   - Main Menu → Maintenance → Clear Thumbnails
   - This cleans up any existing junk from previous installations

3. **Create a Backup** (Recommended)
   - Main Menu → Backup & Restore → Create New Backup
   - This saves your current Kodi configuration
   - Useful if you want to try builds but return to current setup

4. **Install Add-ons** (Optional)
   - Main Menu → Install Add-ons
   - Select from popular streaming add-ons:
     - The Crew
     - The Loop
     - FenLight
     - Seren (requires Real-Debrid)

---

## 🎨 Features Overview

### 1. Advanced Settings ⚙️

**What it does:** Optimizes Kodi cache settings for your specific device

**Device Profiles:**
- **Fire TV Stick 1GB**: 75MB cache, conservative settings
- **Fire TV Stick 2GB/4K**: 150MB cache, balanced performance
- **Shield 3GB**: 250MB cache, enhanced features
- **PC 4GB+**: 512MB cache, maximum performance

**Benefits:**
- Reduces buffering during video playback
- Improves streaming reliability
- Optimizes memory usage for your device
- Better overall Kodi performance

### 2. Maintenance Tools 🧹

**Clear Cache**
- Removes temporary files
- Frees up storage space
- Improves Kodi performance
- Recommended: Weekly

**Clear Packages**
- Removes downloaded addon installers
- Frees up storage space
- Safe to run anytime

**Clear Thumbnails**
- Deletes all cached images
- Purges textures database
- Frees significant space
- Thumbnails will regenerate automatically
- Recommended: Monthly

**Purge Old Databases**
- Removes obsolete database files
- Frees up space
- Improves database performance
- Safe to run periodically

**Fresh Start** ⚠️ CAUTION
- Resets Kodi to factory defaults
- **DESTRUCTIVE**: Removes all addons and settings
- Creates automatic backup first
- Use only when troubleshooting severe issues

### 3. Install Add-ons 📦

Quick install for popular streaming add-ons:
- **The Crew** - Extensive content library, well-maintained
- **The Loop** - Excellent Real-Debrid support
- **FenLight** - Lightweight, fast performance
- **Seren** - Premium addon for debrid users with Trakt

**Note:** Some add-ons require their own repositories to be installed first.

### 4. Backup & Restore 💾

**Create New Backup**
- Full backup of Kodi userdata
- Preserves all settings and addons
- Compressed ZIP format
- Stored in Kodi's backup folder

**Restore from Backup**
- Select from available backups
- Restores complete Kodi configuration
- Automatic safety checks
- Creates pre-restore backup

**View Backups**
- See all available backups
- Shows backup size and date
- Easy management

**Delete Backup**
- Remove old backups to free space
- Automatic cleanup (keeps last 3)

### 5. Install Fresh Build 🏗️

**Note:** Build installation requires hosted build files (not yet available)

Pre-configured complete Kodi setups:
- **Pigeon Essential** - Fire TV Stick optimized
- **Pigeon Pro** - Fire TV 4K enhanced
- **Pigeon Ultimate** - Shield/PC complete

**Features when active:**
- Automatic backup before install
- Selective preservation of Trakt/Debrid settings
- Optimized settings included
- Pre-installed popular add-ons

---

## 🔥 Fire TV Stick Optimization Tips

### Best Practices

1. **Always apply advanced settings** after fresh Kodi install
2. **Clear cache weekly** to prevent performance degradation
3. **Disable automatic updates** in Kodi settings (manual is better)
4. **Use Real-Debrid** for best streaming quality and reliability
5. **Close Kodi completely** when not in use to save memory
6. **Restart Fire TV** once a week for optimal performance

### Recommended Settings

**Kodi Settings → Player → Videos:**
- Adjust display refresh rate: **On start/stop**
- Sync playback to display: **Enabled**

**Kodi Settings → System → Add-ons:**
- Unknown sources: **Enabled** (for wizard installation)
- Automatic updates: **Off** (prevent unwanted updates)

**Fire TV Stick Settings:**
- Developer Options → Stay Awake: **On** (prevents sleep during streaming)
- Display → Sleep: **Never**
- Privacy Settings → Device Usage Data: **Off**
- Privacy Settings → Collect App Usage Data: **Off**

---

## 🐛 Troubleshooting

### Wizard Won't Install

**Problem:** "Installation failed" when installing repository

**Solutions:**
1. Enable Unknown Sources: Settings → System → Add-ons → Unknown Sources
2. Check Kodi version (requires Kodi 19+)
3. Verify ZIP file is not corrupted (re-download)
4. Check file location is accessible in Kodi

### Welcome Message Keeps Appearing

**Problem:** Welcome screen shows every time wizard launches

**Solution:**
- This was a bug in earlier versions
- Update to latest version
- Or manually set first run: Add-on Settings → Advanced → Mark as first run complete

### Advanced Settings Not Working

**Problem:** Applied settings but still buffering

**Solutions:**
1. **Restart Kodi** after applying settings (required!)
2. Verify correct device profile selected
3. Check available RAM on device
4. Clear cache and thumbnails
5. Test with different video source

### Add-on Won't Install

**Problem:** Add-on installation fails

**Solutions:**
1. Some add-ons require their own repositories first
2. Check Kodi log for specific errors
3. Ensure internet connection is stable
4. Try installing from the add-on's official source
5. Use maintenance tools to clear cache first

### Fire TV Stick Still Slow

**Problem:** Performance issues persist

**Solutions:**
1. Clear cache and thumbnails
2. Check Fire TV storage (Settings → My Fire TV → About)
3. Uninstall unused apps on Fire TV
4. Factory reset Fire TV if necessary
5. Consider upgrading to Fire TV 4K (better performance)

### Backup Fails

**Problem:** Cannot create or restore backup

**Solutions:**
1. Check available storage space (need 500MB+)
2. Verify SD card is writable (if using)
3. Try smaller backup (disable builds folder)
4. Check file permissions
5. Use different backup location

### Build Installation Fails

**Problem:** Build won't download or install

**Solutions:**
1. **Currently:** Build files are not yet hosted (feature coming soon)
2. Check internet connection and speed
3. Ensure sufficient storage space (1GB+ recommended)
4. Create backup first (automatic safety)
5. Check Kodi log for specific errors

---

## 📞 Support & Resources

### Getting Help

- **GitHub Issues**: https://github.com/mz1312/pigeonhole/issues
- **GitHub Repository**: https://github.com/mz1312/pigeonhole

### Useful Links

- **Kodi Wiki**: https://kodi.wiki/
- **Fire TV Stick Optimization**: https://kodi.wiki/view/Amazon_Fire_TV
- **Real-Debrid**: https://real-debrid.com/

### Reporting Bugs

When reporting issues, please include:
1. Your device type (Fire TV Stick 4K, Shield, etc.)
2. Kodi version
3. What you were doing when error occurred
4. Kodi log file (enable debug logging first)

**To get Kodi log:**
1. Settings → System → Logging → Enable debug logging
2. Reproduce the issue
3. Get log file from userdata/temp/kodi.log

---

## 📝 FAQ

**Q: Is Pigeon Build legal?**
A: Yes. Pigeon Build is a configuration tool only. We don't host, create, or distribute any copyrighted content.

**Q: Do I need Real-Debrid?**
A: Not required but highly recommended for best quality and reliability.

**Q: Will this work on Kodi 20 (Nexus)?**
A: Yes, fully compatible with Kodi 19 (Matrix), 20 (Nexus), and newer.

**Q: Can I use this on Raspberry Pi?**
A: Yes! Use the PC/Desktop advanced settings profile.

**Q: How often should I run maintenance?**
A: Clear cache weekly, thumbnails monthly, or when experiencing issues.

**Q: Can I uninstall the wizard after applying settings?**
A: Yes, but keep it installed for easy maintenance and updates.

**Q: Does this work with VPN?**
A: Yes, use VPN before launching Kodi for best privacy.

**Q: Can I install multiple builds?**
A: No, builds replace your entire Kodi configuration. Use backups to switch between setups.

**Q: How do I completely remove Pigeon Build?**
A: Uninstall the wizard addon and repository from Kodi's add-on manager.

**Q: Where are backups stored?**
A: In Kodi's userdata folder: `userdata/addon_data/plugin.program.pigeonbuild/backups/`

---

## 🎉 Post-Installation

After installation, your wizard is ready to use! Here's what to do next:

### Immediate Actions:
1. ✅ Apply advanced settings for your device
2. ✅ Restart Kodi
3. ✅ Test streaming performance

### Optional But Recommended:
4. 📦 Install The Crew or The Loop
5. 💾 Create a backup
6. 🧹 Run cache maintenance

### Enjoy!

You're now ready to enjoy smooth, buffer-free streaming with Pigeon Build!

---

**Pigeon Build** - *Delivering streams faster than a homing pigeon!* 🐦

Version 1.0.0 | Last Updated: 2025-10-04
