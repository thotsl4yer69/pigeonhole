# 🏗️ Pigeon Build - Professional Build Creation Guide

**Creating RedWizard-style one-click builds**

---

## Overview

We're creating 3 professional Kodi builds:
1. **Pigeon Essential** - Fire TV Stick 1GB (lightweight)
2. **Pigeon Pro** - Fire TV Stick 4K 2GB (balanced)
3. **Pigeon Ultimate** - Shield/PC 4GB+ (full-featured)

Each build will be a complete, pre-configured Kodi installation that users can install and stream immediately.

---

## Build Creation Workflow

### Phase 1: Base Configuration (All Builds)

1. **Fresh Kodi Installation**
   - Start with clean Kodi 20.5 (Nexus)
   - Install base dependencies

2. **Install Core Addons** (via Pigeon Wizard)
   - The Crew
   - The Loop
   - Umbrella
   - Seren
   - POV

3. **Configure Addons**
   - Default settings optimized
   - Trakt setup guide included
   - Real-Debrid setup guide included

4. **Apply Advanced Settings**
   - Device-specific cache settings
   - Network optimization
   - Playback settings

5. **Customize Interface**
   - Skin configuration
   - Menu customization
   - Shortcuts setup

6. **Create Backup**
   - Use Pigeon wizard backup function
   - Creates complete userdata ZIP

---

## Phase 2: Build-Specific Configuration

### Pigeon Essential (Fire TV 1GB)

**Target Device**: Fire TV Stick (1st/2nd gen), 1GB RAM

**Addons Included**:
- The Crew (primary)
- The Loop (sports)
- Umbrella (backup)

**Advanced Settings**:
- Buffer mode: 2 (network + local)
- Cache: 75MB
- Read factor: 1000

**Skin**: Estuary (default, lightweight)

**Size Target**: ~150MB ZIP

---

### Pigeon Pro (Fire TV 4K)

**Target Device**: Fire TV Stick 4K/Max, 2GB RAM

**Addons Included**:
- The Crew
- The Loop
- Umbrella
- Seren (debrid optimized)
- POV

**Advanced Settings**:
- Buffer mode: 2
- Cache: 192MB
- Read factor: 1000

**Skin**: Estuary or Arctic Zephyr

**Additional Features**:
- Trakt integration ready
- Real-Debrid optimized

**Size Target**: ~250MB ZIP

---

### Pigeon Ultimate (Shield/PC)

**Target Device**: Shield TV, PC, 4GB+ RAM

**Addons Included**:
- All from Pro +
- Additional premium addons
- Content aggregators

**Advanced Settings**:
- Buffer mode: 2
- Cache: 512MB
- Read factor: 1000

**Skin**: Arctic Zephyr or Aura MOD

**Additional Features**:
- Premium skins
- Advanced customization
- Dolby Vision support

**Size Target**: ~400MB ZIP

---

## Phase 3: Build Packaging

### Directory Structure

```
pigeon-essential-firestick/
├── addons/
│   ├── plugin.video.thecrew/
│   ├── plugin.video.theloop/
│   ├── plugin.video.umbrella/
│   ├── repository.thecrew/
│   ├── repository.loop/
│   ├── repository.umbrella/
│   └── plugin.program.pigeonbuild/    (wizard included!)
├── userdata/
│   ├── addon_data/
│   │   ├── plugin.video.thecrew/
│   │   │   └── settings.xml
│   │   ├── plugin.video.theloop/
│   │   │   └── settings.xml
│   │   └── plugin.video.umbrella/
│   │       └── settings.xml
│   ├── advancedsettings.xml
│   ├── guisettings.xml
│   ├── favourites.xml
│   └── sources.xml
└── SETUP_GUIDE.txt                    (Trakt/Debrid instructions)
```

### What Gets Pre-Configured

✅ **Automatic** (No user setup needed):
- All addons installed
- Repositories installed
- Cache settings optimized
- Playback settings configured
- Skin customized
- Menu items organized
- Favorites created

⚠️ **User Setup Required** (One-time, 5 minutes):
- Trakt authorization (per addon)
- Real-Debrid API key (per addon)
- Optional: Premiumize, All-Debrid

---

## Phase 4: Testing & Validation

### Quality Checklist

Each build must pass:

1. **Installation Test**
   - Extracts properly
   - No file corruption
   - All addons load

2. **Performance Test**
   - Kodi starts quickly
   - UI responsive
   - No crashes

3. **Addon Test**
   - The Crew opens
   - Can browse content
   - Scraping works (with Debrid)
   - Playback works

4. **Settings Test**
   - Advanced settings applied
   - Cache working
   - No conflicts

5. **Size Test**
   - Within target size
   - Compressed efficiently

---

## Phase 5: Deployment

### Upload to GitHub

```bash
# Create release
gh release create v1.0 \
  --title "Pigeon Build v1.0 - Professional Builds" \
  --notes "One-click Kodi builds optimized for streaming"

# Upload builds
gh release upload v1.0 \
  pigeon-essential-firestick.zip \
  pigeon-pro-firestick4k.zip \
  pigeon-ultimate-pc.zip
```

### Update Wizard

Update `uservar.py`:
```python
BUILDS = [
    {
        'name': 'Pigeon Essential (Fire TV Stick)',
        'version': '1.0',
        'url': 'https://github.com/thotsl4yer69/pigeonhole/releases/download/v1.0/pigeon-essential-firestick.zip',
        # ... rest of config
    }
]
```

---

## User Experience After Installation

### 1. User Installs Build

```
Pigeon Wizard → Install Fresh Build → Pigeon Essential
  ↓ Downloads build (150MB)
  ↓ Extracts to Kodi
  ↓ Restarts Kodi
  ↓ Build installed!
```

### 2. First Launch Setup (5 minutes)

**Welcome Screen** shows:
```
🐦 Welcome to Pigeon Essential!

Quick Setup (5 minutes):

1. Trakt Authorization
   - Open The Crew → Settings → Accounts → Trakt
   - Visit: https://trakt.tv/activate
   - Enter code shown on screen
   - Click Authorize

2. Real-Debrid Setup (Recommended)
   - Open The Crew → Settings → Accounts → Real-Debrid
   - Visit: https://real-debrid.com/apitoken
   - Copy API token
   - Paste into The Crew

3. Start Streaming!
   - Go to The Crew → Movies or TV Shows
   - Find something to watch
   - Enjoy!

Pro Tip: Real-Debrid gives you 1080p/4K streams with zero buffering.
```

### 3. User Streams Immediately

```
Open The Crew → Movies → Trending
  ↓ Select movie
  ↓ Auto-scrapes with Real-Debrid
  ↓ 50+ 1080p links found
  ↓ Plays instantly
  ↓ Zero buffering
```

**Total time from install to streaming: ~10 minutes** (vs RedWizard's ~5 minutes)

---

## Build Creation Steps (Detailed)

### Step 1: Prepare Kodi

```bash
# Backup current Kodi (if needed)
cp -r ~/.kodi ~/.kodi.backup

# Or start fresh
rm -rf ~/.kodi
kodi  # Launches, creates fresh profile
```

### Step 2: Install Pigeon Wizard

```bash
# Install repository
# Install wizard addon
# Launch wizard
```

### Step 3: Install Addons via Wizard

```
Pigeon Wizard → Install Add-ons
  - The Crew ✅
  - The Loop ✅
  - Umbrella ✅
  (For Pro/Ultimate: Also install Seren, POV)
```

### Step 4: Configure Each Addon

**The Crew**:
- Settings → Playback → Auto Play: ON
- Settings → Playback → Quality: 1080p
- Settings → Providers → Enable all
- Settings → Scraper → Timeout: 30 seconds

**The Loop**:
- Settings → Quality: 1080p
- Settings → Cache: ON

**Umbrella**:
- Settings → Accounts → (Leave for user)
- Settings → Playback → Auto Play: ON

### Step 5: Apply Advanced Settings

```
Pigeon Wizard → Advanced Settings
  - Select device type
  - Apply settings
  - Restart Kodi
```

### Step 6: Customize Interface

- **Favorites**: Add quick shortcuts
- **Menu**: Remove unused items
- **Skin**: Configure colors to Pigeon branding

### Step 7: Create Build Backup

```
Pigeon Wizard → Backup & Restore → Create Backup
  - Name: pigeon-essential-firestick
  - Include: All addons, settings, data
  - Create ZIP
```

### Step 8: Extract and Clean

```bash
# Extract the backup
unzip backup.zip -d build-temp/

# Remove user-specific data
rm -rf build-temp/addon_data/*/settings.xml  # Will be template
rm -rf build-temp/addon_data/*/cache/
rm -rf build-temp/Thumbnails/

# Add setup guide
cp SETUP_GUIDE.txt build-temp/

# Re-package
cd build-temp
zip -r ../pigeon-essential-firestick.zip .
```

### Step 9: Test Build

```bash
# Fresh Kodi installation
rm -rf ~/.kodi

# Extract build
unzip pigeon-essential-firestick.zip -d ~/.kodi/

# Launch and test
kodi
```

---

## Automation Script

We'll create a script that:
1. Takes current Kodi configuration
2. Creates optimized build for each device type
3. Packages with setup guides
4. Validates build integrity
5. Uploads to GitHub

---

## Timeline

**Day 1** (Today):
- Create build creation scripts
- Set up Kodi with The Crew
- Configure and test The Crew
- Create Pigeon Essential build
- Test on this device

**Day 2**:
- Create Pigeon Pro build
- Create Pigeon Ultimate build
- Upload to GitHub releases
- Update wizard

**Day 3**:
- Deploy to Fire TV Stick
- Real-world testing
- Adjustments

---

## Success Criteria

Each build must:
✅ Install in under 5 minutes
✅ All addons load without errors
✅ Scraping works (with Debrid)
✅ Playback smooth and buffer-free
✅ Settings applied correctly
✅ User setup takes under 5 minutes
✅ Professional branding throughout

---

**Ready to start building!** 🏗️
