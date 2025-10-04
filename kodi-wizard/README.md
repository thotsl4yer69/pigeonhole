# Pigeon Build - Kodi Wizard

![Pigeon Build Logo](branding/banner.png)

**Fast Streaming • Zero Buffer • Optimized for Fire TV Stick**

---

## 📋 Overview

Pigeon Build is a custom Kodi wizard optimized for Fire TV Stick and streaming devices. It provides:

- 🚀 **Pre-configured builds** for different devices (Fire TV Stick, Shield, PC)
- ⚙️ **Optimized advanced settings** for smooth streaming
- 📦 **Easy add-on installation** (The Crew, The Loop, FenLight, etc.)
- 🔧 **Maintenance tools** (clear cache, packages, etc.)
- 💾 **Backup & restore** functionality
- 🎨 **Custom branding** with professional UI

---

## 📥 Installation

### Method 1: Install from File (Recommended)

1. **Download the repository zip:**
   - Download `repository.pigeonbuild-1.0.0.zip` from the repo folder

2. **Transfer to your device:**
   - Fire TV Stick: Use adb or file manager app
   - PC: Download directly

3. **Install in Kodi:**
   - Go to **Settings** → **Add-ons**
   - Enable **Unknown Sources** (if not already enabled)
   - Click **Install from zip file**
   - Navigate to the downloaded zip and install it
   - Wait for the "Pigeon Build Repository installed" notification

4. **Install the Wizard:**
   - Click **Install from repository**
   - Select **Pigeon Build Repository**
   - Go to **Program add-ons**
   - Install **Pigeon Build Wizard**

5. **Launch the Wizard:**
   - Go to **Add-ons** → **Program add-ons**
   - Select **Pigeon Build Wizard**

### Method 2: Install via ADB (Fire TV Stick)

```bash
# Push repository to Fire TV Stick
adb connect <firestick-ip>:5555
adb push repo/repository.pigeonbuild-1.0.0.zip /sdcard/Download/

# Then follow steps 3-5 from Method 1
```

---

## 🎯 Features

### 1. Install Fresh Build
Choose from optimized builds:
- **Pigeon Essential** - Fire TV Stick (lightweight, 1GB RAM)
- **Pigeon Pro** - Fire TV Stick 4K (enhanced, 2GB RAM)
- **Pigeon Ultimate** - Shield/PC (full-featured, 4GB+ RAM)

### 2. Advanced Settings
Apply optimized settings based on your device:
- Fire TV Stick 1GB RAM: 75MB cache
- Fire TV Stick 2GB/4K: 150MB cache
- NVIDIA Shield 3GB: 250MB cache
- PC 4GB+: 512MB cache

### 3. Add-on Installation
Quick install popular streaming add-ons:
- The Crew
- The Loop
- FenLight
- Seren (debrid users)

### 4. Maintenance Tools
- Clear cache
- Clear packages
- Clear thumbnails
- Purge databases
- Fresh start (nuclear option)

### 5. Backup & Restore
- Create backups of your Kodi configuration
- Restore from previous backups
- View all available backups

---

## 📁 Project Structure

```
kodi-wizard/
├── plugin.program.pigeonbuild/    # Main wizard addon
│   ├── addon.xml                   # Addon metadata
│   ├── default.py                  # Entry point
│   ├── uservar.py                  # Configuration
│   └── resources/
│       ├── lib/
│       │   ├── gui.py             # GUI functions
│       │   └── wizard.py          # Wizard logic
│       └── media/                 # Branding assets
│
├── repository.pigeonbuild/        # Repository addon
│   └── addon.xml
│
├── repo/                          # Repository files
│   ├── addons.xml                 # Addon listing
│   ├── addons.xml.md5            # Checksum
│   ├── plugin.program.pigeonbuild-1.0.0.zip
│   └── repository.pigeonbuild-1.0.0.zip
│
├── advanced_settings/             # Optimized settings
│   ├── firestick_1gb.xml
│   ├── firestick_2gb.xml
│   ├── shield_3gb.xml
│   └── pc_4gb_plus.xml
│
└── branding/                      # Visual assets
    ├── icon.png (512x512)
    ├── fanart.png (1920x1080)
    └── banner.png (1000x200)
```

---

## 🎨 Branding

### Color Scheme
- **Primary:** `#7B2CBF` (Deep Purple)
- **Secondary:** `#9D4EDD` (Mid Purple)
- **Accent:** `#10A5B5` (Cyan)
- **Background:** `#1a1a1a` (Dark Charcoal)
- **Text:** `#FFFFFF` / `#C77DFF`

### Assets
- Logo/Icon: 512x512px
- Fanart: 1920x1080px
- Banner: 1000x200px

All assets feature a pigeon theme with modern, tech-forward design.

---

## ⚙️ Configuration

### Edit uservar.py to customize:

```python
# Build URLs
BUILDFILE = 'https://your-server.com/builds.txt'

# Repository
REPO_ZIP_URL = 'https://your-server.com/repository.pigeonbuild.zip'

# Advanced Settings URLs
ADVANCED_SETTINGS = {
    'firestick_2gb': 'https://your-server.com/firestick_2gb.xml',
    # ... more settings
}
```

---

## 🚀 Development

### Testing Locally

1. **Copy addon to Kodi:**
   ```bash
   cp -r plugin.program.pigeonbuild ~/.kodi/addons/
   ```

2. **Reload Kodi skin:**
   - Settings → System → Developer → Reload skin

3. **Check logs:**
   ```bash
   tail -f ~/.kodi/temp/kodi.log
   ```

### Building Zips

```bash
# Build wizard addon
cd kodi-wizard
zip -r repo/plugin.program.pigeonbuild-1.0.0.zip plugin.program.pigeonbuild/ -x "*.pyc" -x "*__pycache__*"

# Build repository
zip -r repo/repository.pigeonbuild-1.0.0.zip repository.pigeonbuild/

# Generate MD5
md5sum repo/addons.xml | awk '{print $1}' > repo/addons.xml.md5
```

---

## 📝 TODO

- [ ] Implement actual build download/extraction
- [ ] Add Trakt/Debrid settings preservation
- [ ] Create build files (essential, pro, ultimate)
- [ ] Set up GitHub Pages for hosting
- [ ] Add YouTube preview videos
- [ ] Implement auto-update checking
- [ ] Add skin customization options
- [ ] Create installation video tutorial

---

## 📄 License

GPL-3.0

---

## 🙏 Credits

- Built with ❤️ for the streaming community
- Inspired by RedWizard and other popular Kodi wizards
- Optimized for Fire TV Stick users

---

## 📞 Support

- **GitHub:** https://github.com/mz1312/pigeonhole
- **Issues:** https://github.com/mz1312/pigeonhole/issues

---

**Pigeon Build** - *Delivering streams faster than a homing pigeon* 🐦
