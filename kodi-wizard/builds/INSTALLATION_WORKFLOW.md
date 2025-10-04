# 🚀 Professional Build Creation Workflow

**Step-by-step guide to create RedWizard-quality builds**

---

## Phase 1: Prepare Kodi Installation

### Step 1.1: Fresh Kodi Setup

We'll use the Kodi installation already on this Raspberry Pi, but configure it properly.

```bash
# Check current Kodi status
ls -la ~/.kodi/addons/ | grep -E "thecrew|theloop|umbrella"
```

**If addons not installed**: Continue to Step 1.2
**If addons installed**: Skip to Phase 2

---

### Step 1.2: Launch Kodi and Install Addons

**Action Required - Do This Now**:

1. **Open Kodi**
   ```bash
   # If Kodi not running:
   pkill kodi 2>/dev/null
   sleep 2
   kodi &
   ```

2. **Open Pigeon Build Wizard**
   - Go to: Add-ons → Program Add-ons
   - Select: Pigeon Build Wizard
   - Click to launch

3. **Install The Crew**
   - Select: Install Add-ons
   - Select: The Crew Repository
   - Wait for installation (2-3 minutes)
   - ✓ Should see "The Crew has been installed successfully!"

4. **Install The Loop**
   - Install Add-ons → The Loop Repository
   - Wait for installation
   - ✓ Confirm success

5. **Install Umbrella**
   - Install Add-ons → Umbrella Repository
   - Wait for installation
   - ✓ Confirm success

**For Pigeon Pro/Ultimate also install**:
- Seren
- POV

**Estimated time**: 15-20 minutes

---

### Step 1.3: Verify Installations

**Check in Kodi**:
- Go to: Add-ons → Video add-ons
- You should see:
  - The Crew ✓
  - The Loop ✓
  - Umbrella ✓
  - [Pro/Ultimate: Seren, POV]

**Test launching**:
- Open The Crew
- Should load without errors
- Close and return to home

---

## Phase 2: Configure Addons (Essential Build)

### Step 2.1: The Crew Configuration

**Open The Crew** → **Settings** (gear icon)

**General Settings**:
- Auto Play: ON
- Quality: 1080p
- Sorting: Best quality first

**Accounts** (Skip for now - users will configure):
- Trakt: [Not configured]
- Real-Debrid: [Not configured]

**Providers**:
- Enable all providers: ON
- Scraper timeout: 30 seconds

**Playback**:
- Auto resume: ON
- Next episode notification: 30 seconds

**Save and exit**

---

### Step 2.2: The Loop Configuration

**Open The Loop** → **Settings**

**Playback**:
- Quality: 1080p
- Enable cache: ON

**Save and exit**

---

### Step 2.3: Umbrella Configuration

**Open Umbrella** → **Tools** → **Settings**

**General**:
- Auto Play: ON
- Quality: 1080p

**Playback**:
- Resume playback: ON

**Save and exit**

---

## Phase 3: Apply Advanced Settings

### Step 3.1: Apply Settings via Wizard

**In Kodi**:
1. Open Pigeon Build Wizard
2. Select: Advanced Settings
3. Select: Fire TV Stick 1GB
4. Confirm application
5. **Restart Kodi when prompted**

**Wait for Kodi to restart** (about 30 seconds)

---

### Step 3.2: Verify Advanced Settings

After restart:
```bash
cat ~/.kodi/userdata/advancedsettings.xml
```

Should show cache settings like:
```xml
<memorysize>78643200</memorysize>  <!-- 75MB -->
<buffermode>2</buffermode>
<readfactor>1000</readfactor>
```

---

## Phase 4: Customize Interface

### Step 4.1: Create Favorites

**In Kodi Main Menu**:
1. Right-click (or long-press) on The Crew
2. Select: Add to Favourites
3. Repeat for The Loop, Umbrella

### Step 4.2: Customize Home Screen (Optional)

- Settings → Interface → Skin → Configure Skin
- Customize widgets, menu items
- Remove unused items

**For Essential build**: Keep it simple, default Estuary skin is fine

---

## Phase 5: Create Build Package

### Step 5.1: Run Build Creator

**Close Kodi first**:
```bash
pkill kodi
sleep 5  # Wait for Kodi to fully close
```

**Create Essential Build**:
```bash
cd /home/mz1312/projects/pigeonhole/kodi-wizard/builds
./create_build.sh
```

**Select option 1**: Pigeon Essential (Fire TV Stick 1GB)

**Script will**:
1. Copy Kodi configuration
2. Clean cache and sensitive data
3. Apply build-specific settings
4. Add setup guide
5. Create ZIP package
6. Calculate checksums

**Output**: `builds/output/pigeon-essential-YYYYMMDD.zip`

---

### Step 5.2: Verify Build Package

```bash
cd builds/output
ls -lh *.zip

# Check contents
unzip -l pigeon-essential-*.zip | head -30
```

Should show:
```
  addons/plugin.video.thecrew/
  addons/plugin.video.theloop/
  addons/plugin.video.umbrella/
  addons/repository.thecrew/
  addons/repository.loop/
  addons/repository.umbrella/
  userdata/advancedsettings.xml
  userdata/addon_data/
  SETUP_GUIDE.txt
  BUILD_INFO.txt
```

---

## Phase 6: Test Build (Crucial!)

### Step 6.1: Test on Same System

**Backup current Kodi**:
```bash
mv ~/.kodi ~/.kodi.backup-$(date +%Y%m%d)
```

**Extract build**:
```bash
mkdir -p ~/.kodi
unzip builds/output/pigeon-essential-*.zip -d ~/.kodi/
```

**Launch Kodi**:
```bash
kodi &
```

**Test checklist**:
- [  ] Kodi starts without errors
- [  ] All addons visible in Video Add-ons
- [  ] The Crew opens successfully
- [  ] Can browse content in The Crew
- [  ] Advanced settings applied (check cache)
- [  ] No crash errors

**If all tests pass**: Build is good! ✓

**Restore original Kodi** (if needed):
```bash
pkill kodi
rm -rf ~/.kodi
mv ~/.kodi.backup-$(date +%Y%m%d) ~/.kodi
```

---

## Phase 7: Create Pro and Ultimate Builds

### Step 7.1: Enhanced Configuration

**For Pro build**:
1. Restore configured Kodi (or start fresh)
2. Install additional addons: Seren, POV
3. Apply Fire TV 4K advanced settings
4. Run build creator → Option 2

**For Ultimate build**:
1. Configure all addons
2. Apply PC 4GB+ advanced settings
3. Optional: Install premium skin (Arctic Zephyr)
4. Run build creator → Option 3

**Or create all at once**:
```bash
./create_build.sh
# Select option 4: Create all builds
```

---

## Phase 8: Upload to GitHub

### Step 8.1: Create GitHub Release

```bash
cd /home/mz1312/projects/pigeonhole

# Create release v1.0
gh release create v1.0 \
  --title "Pigeon Build v1.0 - Professional Builds" \
  --notes "One-click Kodi builds optimized for streaming.

**Builds Included:**
- Pigeon Essential (Fire TV Stick 1GB) - Lightweight
- Pigeon Pro (Fire TV Stick 4K 2GB) - Balanced
- Pigeon Ultimate (Shield/PC 4GB+) - Full-featured

**Features:**
- The Crew, The Loop, Umbrella pre-installed
- Advanced settings pre-configured
- One-click install and stream
- Complete setup guide included

**Setup Time:** 5-10 minutes (Trakt + Real-Debrid authorization)

See SETUP_GUIDE.txt in each build for instructions."
```

### Step 8.2: Upload Build Files

```bash
gh release upload v1.0 \
  kodi-wizard/builds/output/pigeon-essential-*.zip \
  kodi-wizard/builds/output/pigeon-pro-*.zip \
  kodi-wizard/builds/output/pigeon-ultimate-*.zip \
  --clobber
```

**Files will be available at**:
```
https://github.com/thotsl4yer69/pigeonhole/releases/download/v1.0/pigeon-essential-YYYYMMDD.zip
https://github.com/thotsl4yer69/pigeonhole/releases/download/v1.0/pigeon-pro-YYYYMMDD.zip
https://github.com/thotsl4yer69/pigeonhole/releases/download/v1.0/pigeon-ultimate-YYYYMMDD.zip
```

---

## Phase 9: Update Wizard URLs

### Step 9.1: Update uservar.py

```bash
cd /home/mz1312/projects/pigeonhole/kodi-wizard/plugin.program.pigeonbuild
```

**Edit uservar.py** - Update BUILDS with actual filenames:

```python
BUILDS = [
    {
        'name': 'Pigeon Essential (Fire TV Stick)',
        'version': '1.0',
        'url': 'https://github.com/thotsl4yer69/pigeonhole/releases/download/v1.0/pigeon-essential-20251004.zip',
        'gui': '',
        'theme': '',
        'icon': 'https://raw.githubusercontent.com/thotsl4yer69/pigeonhole/main/kodi-wizard/branding/icon.png',
        'fanart': 'https://raw.githubusercontent.com/thotsl4yer69/pigeonhole/main/kodi-wizard/branding/fanart.png',
        'preview': '',
        'adult': False,
        'info': 'Lightweight build optimized for Fire TV Stick with essential streaming add-ons',
        'description': 'The perfect starter build for Fire TV Stick users. Includes The Crew, The Loop, and optimized settings for smooth 1080p streaming.'
    },
    # ... repeat for pro and ultimate
]
```

### Step 9.2: Update builds.txt

```bash
cd /home/mz1312/projects/pigeonhole/kodi-wizard
```

**Edit builds.txt** with actual URLs

### Step 9.3: Commit and Push

```bash
git add plugin.program.pigeonbuild/uservar.py builds.txt builds/
git commit -m "Add professional builds v1.0"
git push
```

---

## Phase 10: Test Complete Workflow

### Step 10.1: End-to-End Test

**On Fire TV Stick** (or test device):

1. **Install Pigeon Repository**
   - From wizard repository ZIP

2. **Install Pigeon Wizard**
   - From repository

3. **Install Build**
   - Open Pigeon Wizard
   - Install Fresh Build
   - Select "Pigeon Essential"
   - Wait for download and installation
   - Restart Kodi

4. **Follow Setup Guide**
   - Authorize Trakt
   - Add Real-Debrid
   - Test streaming

**Expected result**: Streaming in under 10 minutes total ✓

---

## Timeline

**Today (Day 1)**:
- ✓ Create build scripts
- [ ] Configure Kodi with addons (30 min)
- [ ] Create Essential build (10 min)
- [ ] Test Essential build (15 min)
- **Total: ~1 hour**

**Tomorrow (Day 2)**:
- [ ] Create Pro build (20 min)
- [ ] Create Ultimate build (20 min)
- [ ] Upload to GitHub (10 min)
- [ ] Update wizard URLs (10 min)
- **Total: ~1 hour**

**Day 3**:
- [ ] Deploy to Fire TV Stick
- [ ] Real-world testing
- [ ] Adjustments and refinement

---

## Success Criteria

Each build must:
- [  ] Install without errors
- [  ] All addons load and launch
- [  ] Scraping works (with Real-Debrid)
- [  ] Playback smooth
- [  ] Settings applied correctly
- [  ] User setup under 10 minutes
- [  ] Professional quality matching RedWizard

---

## Ready to Start!

**Next action**: Configure Kodi with addons (Phase 1-2)

**Estimated time to first build**: 1 hour

**Let's build!** 🏗️
