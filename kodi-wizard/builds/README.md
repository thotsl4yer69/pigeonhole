# 🏗️ Pigeon Build - Professional Builds

**RedWizard-style one-click Kodi builds**

---

## Quick Start

### Create Your First Build (1 hour)

**Step 1: Configure Kodi** (30 minutes)
```bash
# Launch Kodi
kodi &

# In Kodi:
# 1. Open Pigeon Build Wizard
# 2. Install Add-ons → The Crew
# 3. Install Add-ons → The Loop
# 4. Install Add-ons → Umbrella
# 5. Advanced Settings → Fire TV Stick 1GB → Apply
# 6. Close Kodi
```

**Step 2: Create Build** (10 minutes)
```bash
cd /home/mz1312/projects/pigeonhole/kodi-wizard/builds
./create_build.sh

# Select: 1) Pigeon Essential
```

**Step 3: Test Build** (15 minutes)
```bash
# Backup current Kodi
mv ~/.kodi ~/.kodi.backup

# Extract build
mkdir ~/.kodi
unzip output/pigeon-essential-*.zip -d ~/.kodi/

# Test
kodi &
# Verify all addons work

# Restore
pkill kodi
rm -rf ~/.kodi
mv ~/.kodi.backup ~/.kodi
```

**Step 4: Upload to GitHub** (10 minutes)
```bash
cd /home/mz1312/projects/pigeonhole

# Create release
gh release create v1.0 \
  --title "Pigeon Build v1.0" \
  --notes "Professional one-click Kodi builds"

# Upload build
gh release upload v1.0 \
  kodi-wizard/builds/output/pigeon-essential-*.zip
```

---

## Files

- **`create_build.sh`** - Automated build creator
- **`SETUP_GUIDE.txt`** - User setup instructions (included in builds)
- **`BUILD_CREATION_GUIDE.md`** - Complete build creation documentation
- **`INSTALLATION_WORKFLOW.md`** - Step-by-step workflow
- **`output/`** - Created build packages (generated)

---

## Build Types

### Pigeon Essential (Fire TV Stick 1GB)
- **Target**: Fire TV Stick 1GB RAM
- **Addons**: The Crew, The Loop, Umbrella
- **Size**: ~150MB
- **Setup**: 5-10 minutes

### Pigeon Pro (Fire TV 4K)
- **Target**: Fire TV Stick 4K 2GB RAM
- **Addons**: Essential + Seren, POV
- **Size**: ~250MB
- **Setup**: 5-10 minutes

### Pigeon Ultimate (Shield/PC)
- **Target**: Shield TV, PC 4GB+ RAM
- **Addons**: Pro + additional premium addons
- **Size**: ~400MB
- **Setup**: 5-10 minutes

---

## User Experience

**Before** (Current):
1. Install wizard
2. Install each addon manually
3. Configure Trakt, Real-Debrid for each
4. Apply settings
5. **Time: 30-45 minutes**

**After** (With builds):
1. Install wizard
2. Install build → Pigeon Essential
3. Configure Trakt + Real-Debrid (one-time)
4. Start streaming
5. **Time: 10 minutes** ✓

---

## Documentation

See `BUILD_CREATION_GUIDE.md` for complete instructions.

See `INSTALLATION_WORKFLOW.md` for step-by-step process.

---

## Quick Reference

### Create Build
```bash
./create_build.sh
```

### Create All Builds
```bash
./create_build.sh  # Select option 4
```

### Test Build
```bash
# Fresh test
rm -rf ~/.kodi
unzip output/pigeon-*.zip -d ~/.kodi/
kodi
```

### Upload to GitHub
```bash
gh release create v1.0 --title "Pigeon Build v1.0"
gh release upload v1.0 output/pigeon-*.zip
```

---

## Support

- GitHub: https://github.com/thotsl4yer69/pigeonhole
- Issues: https://github.com/thotsl4yer69/pigeonhole/issues

---

**Status**: Ready to create builds!

**Next**: Follow `INSTALLATION_WORKFLOW.md`
