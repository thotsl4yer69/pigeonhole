# Installing Pigeon Build on Fire TV Stick

## Quick Installation Guide

### Prerequisites
- Kodi 21.x (Omega) installed on Fire TV Stick
- ADB debugging enabled (optional, for easier installation)
- File manager app installed (Downloader or similar)

---

## 📥 Method 1: Via ADB (Easiest)

### Step 1: Connect to Fire TV Stick
```bash
adb connect <your-firestick-ip>:5555
```

### Step 2: Push Repository
```bash
cd /home/mz1312/projects/pigeonhole/kodi-wizard
adb push repo/repository.pigeonbuild-1.0.0.zip /sdcard/Download/
```

### Step 3: Install in Kodi
1. Open Kodi on Fire TV Stick
2. Go to **Settings** (gear icon) → **System** → **Add-ons**
3. Enable **Unknown sources** (if not already enabled)
   - Click OK when warned
4. Go back to **Settings** → **Add-ons**
5. Click **Install from zip file**
6. Navigate to **Download** folder
7. Select **repository.pigeonbuild-1.0.0.zip**
8. Wait for "Pigeon Build Repository installed" notification

### Step 4: Install Wizard
1. Click **Install from repository**
2. Select **Pigeon Build Repository**
3. Go to **Program add-ons**
4. Select **Pigeon Build Wizard**
5. Click **Install**
6. Wait for installation to complete

### Step 5: Launch Wizard
1. Press Home button
2. Go to **Add-ons**
3. Select **Program add-ons**
4. Select **Pigeon Build Wizard**
5. Follow the on-screen instructions!

---

## 📥 Method 2: Via Downloader App

### Step 1: Get the Repository URL
The repository zip needs to be hosted online. For now, you can use:
```
http://your-server.com/repository.pigeonbuild-1.0.0.zip
```

### Step 2: Download Repository
1. Open **Downloader** app on Fire TV Stick
2. Enter the URL above
3. Wait for download to complete
4. The zip should be saved automatically

### Step 3: Install in Kodi
1. Open Kodi
2. Go to **Settings** → **Add-ons**
3. Enable **Unknown sources**
4. Click **Install from zip file**
5. Navigate to where Downloader saved the file
6. Select **repository.pigeonbuild-1.0.0.zip**
7. Wait for notification

### Step 4-5: Same as Method 1

---

## 📥 Method 3: Via USB Stick

### Step 1: Prepare USB
1. Copy `repository.pigeonbuild-1.0.0.zip` to USB stick
2. Plug USB into Fire TV Stick

### Step 2: Access in Kodi
1. Open Kodi
2. Go to **Settings** → **Add-ons**
3. Enable **Unknown sources**
4. Click **Install from zip file**
5. Navigate to USB storage
6. Select the zip file

### Step 3-5: Same as Method 1

---

## 🎯 Recommended First Steps After Installation

### 1. Apply Optimized Settings
- Open Pigeon Build Wizard
- Select **Advanced Settings**
- Choose **Fire TV Stick (2GB RAM) / 4K** (or 1GB if older model)
- Confirm application
- Restart Kodi

### 2. Install Essential Add-ons
- Open Pigeon Build Wizard
- Select **Install Add-ons**
- Install:
  - The Crew
  - The Loop
  - FenLight

### 3. Configure Real-Debrid (Recommended)
For each add-on:
1. Open add-on settings
2. Go to **Accounts** → **Real-Debrid**
3. Click **Authorize**
4. Visit real-debrid.com/device
5. Enter the code shown
6. Enable **Real-Debrid only** in provider settings

### 4. Test Streaming
1. Open **The Loop**
2. Go to **Movies** → **Popular**
3. Select a recent movie
4. Should see RD+ links if Real-Debrid is configured
5. Playback should start within 5 seconds

---

## ⚠️ Troubleshooting

### Repository not installing?
- Make sure Unknown Sources is enabled
- Check the zip file isn't corrupted
- Try redownloading the zip

### Wizard not showing up?
- Go to Add-ons → My add-ons → Program add-ons
- Look for Pigeon Build Wizard
- If not there, reinstall from repository

### Buffering issues?
- Apply advanced settings for your device
- Check internet speed (15+ Mbps for 1080p)
- Use Real-Debrid for better quality

### Home button takes you to Amazon launcher?
- This is expected behavior on Fire TV
- Use Wolf Launcher or similar to override

---

## 📊 Fire TV Stick Models & Settings

| Model | RAM | Recommended Settings | Cache Size |
|-------|-----|---------------------|------------|
| Fire TV Stick (Gen 1-2) | 1GB | firestick_1gb | 75MB |
| Fire TV Stick 4K | 1.5GB | firestick_2gb | 150MB |
| Fire TV Stick 4K Max | 2GB | firestick_2gb | 150MB |
| Fire TV Cube | 2GB | firestick_2gb | 150MB |

---

## 🚀 Performance Tips

1. **Clear cache monthly** - Maintenance → Clear Cache
2. **Limit add-ons** - Only install what you use
3. **Use Real-Debrid** - Much faster and reliable
4. **Wired connection** - Use Ethernet adapter if possible
5. **Restart weekly** - Keeps Fire TV fresh

---

## 📞 Need Help?

- Check the main README.md for detailed documentation
- Report issues: https://github.com/mz1312/pigeonhole/issues
- Video guide: [Coming Soon]

---

**Happy Streaming!** 🐦
