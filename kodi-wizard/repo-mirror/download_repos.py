#!/usr/bin/env python3
"""
Repository Mirror Downloader
Downloads and maintains Kodi addon repositories for local hosting
"""

import os
import sys
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path

# Directories
SCRIPT_DIR = Path(__file__).parent
REPOS_DIR = SCRIPT_DIR / 'repositories'
ADDONS_DIR = SCRIPT_DIR / 'addons'
SOURCES_FILE = SCRIPT_DIR / 'sources' / 'repo_sources.json'
LOG_FILE = SCRIPT_DIR / 'download_log.txt'

def log(message):
    """Log message to console and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] {message}"
    print(log_msg)
    with open(LOG_FILE, 'a') as f:
        f.write(log_msg + '\n')

def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

def download_file(url, destination, repo_name):
    """Download file with progress"""
    try:
        log(f"Downloading {repo_name} from {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        with open(destination, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        sys.stdout.write(f"\r  Progress: {progress:.1f}%")
                        sys.stdout.flush()

        if total_size > 0:
            print()  # New line after progress

        file_size = os.path.getsize(destination)
        log(f"✓ Downloaded {repo_name}: {file_size:,} bytes")
        return True

    except Exception as e:
        log(f"✗ Failed to download {repo_name}: {str(e)}")
        return False

def download_all_repositories():
    """Download all repositories from sources.json"""

    # Load sources
    if not SOURCES_FILE.exists():
        log("ERROR: repo_sources.json not found!")
        return False

    with open(SOURCES_FILE, 'r') as f:
        sources = json.load(f)

    log("=" * 60)
    log("KODI REPOSITORY MIRROR - DOWNLOAD SESSION")
    log("=" * 60)

    repositories = sources.get('repositories', {})
    success_count = 0
    fail_count = 0

    for repo_key, repo_info in repositories.items():
        if repo_info.get('status') != 'active':
            log(f"Skipping {repo_info['name']} (status: {repo_info.get('status')})")
            continue

        repo_url = repo_info['repo_url']
        repo_filename = f"{repo_info['repo_id']}.zip"
        destination = REPOS_DIR / repo_filename

        # Download repository
        if download_file(repo_url, destination, repo_info['name']):
            # Calculate hash
            file_hash = get_file_hash(destination)
            log(f"  MD5: {file_hash}")
            success_count += 1
        else:
            fail_count += 1

    log("=" * 60)
    log(f"SUMMARY: {success_count} successful, {fail_count} failed")
    log("=" * 60)

    return fail_count == 0

def check_for_updates():
    """Check if any repositories have been updated"""
    log("Checking for repository updates...")

    # Load current hashes
    hash_file = SCRIPT_DIR / 'repo_hashes.json'
    current_hashes = {}

    if hash_file.exists():
        with open(hash_file, 'r') as f:
            current_hashes = json.load(f)

    new_hashes = {}
    updates_found = []

    # Calculate current hashes
    for repo_file in REPOS_DIR.glob('*.zip'):
        file_hash = get_file_hash(repo_file)
        repo_name = repo_file.stem
        new_hashes[repo_name] = file_hash

        if repo_name in current_hashes:
            if current_hashes[repo_name] != file_hash:
                updates_found.append(repo_name)
                log(f"UPDATE DETECTED: {repo_name}")

    # Save new hashes
    with open(hash_file, 'w') as f:
        json.dump(new_hashes, f, indent=2)

    if updates_found:
        log(f"Found {len(updates_found)} updated repositories")
    else:
        log("No updates found")

    return updates_found

def generate_index():
    """Generate index.html with download links"""

    html = """<!DOCTYPE html>
<html>
<head>
    <title>Pigeon Build - Repository Mirror</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #1a1a1a; color: #fff; }
        h1 { color: #10A5B5; }
        .repo { background: #2a2a2a; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .repo h3 { color: #7B2CBF; margin: 0 0 10px 0; }
        .download { background: #10A5B5; color: #fff; padding: 8px 15px; text-decoration: none; border-radius: 3px; display: inline-block; margin-top: 10px; }
        .download:hover { background: #0d8a96; }
        .info { color: #C77DFF; font-size: 0.9em; }
        .updated { color: #888; font-size: 0.8em; }
    </style>
</head>
<body>
    <h1>🕊️ Pigeon Build Repository Mirror</h1>
    <p class="info">Self-hosted Kodi addon repositories - Updated daily</p>
    <p class="updated">Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
"""

    # Load sources
    with open(SOURCES_FILE, 'r') as f:
        sources = json.load(f)

    for repo_key, repo_info in sources.get('repositories', {}).items():
        if repo_info.get('status') != 'active':
            continue

        repo_filename = f"{repo_info['repo_id']}.zip"
        repo_path = REPOS_DIR / repo_filename

        if repo_path.exists():
            file_size = os.path.getsize(repo_path) / 1024 / 1024  # MB

            html += f"""
    <div class="repo">
        <h3>{repo_info['name']}</h3>
        <p>{repo_info.get('notes', '')}</p>
        <p class="info">Addons: {', '.join(repo_info.get('addons', []))}</p>
        <p class="info">Size: {file_size:.2f} MB</p>
        <a href="repositories/{repo_filename}" class="download">Download Repository</a>
    </div>
"""

    html += """
</body>
</html>
"""

    index_file = SCRIPT_DIR / 'index.html'
    with open(index_file, 'w') as f:
        f.write(html)

    log(f"Generated index.html with repository list")

if __name__ == '__main__':
    # Ensure directories exist
    REPOS_DIR.mkdir(exist_ok=True)
    ADDONS_DIR.mkdir(exist_ok=True)

    # Download all repositories
    success = download_all_repositories()

    # Check for updates
    check_for_updates()

    # Generate index page
    generate_index()

    if success:
        log("\n✓ All repositories downloaded successfully!")
        log(f"Repository mirror ready at: {SCRIPT_DIR}")
        sys.exit(0)
    else:
        log("\n✗ Some repositories failed to download")
        sys.exit(1)
