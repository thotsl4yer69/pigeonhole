#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pigeon Build Wizard - Downloader Module
File download and extraction utilities
"""

import os
import sys
import zipfile
import shutil
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
except ImportError:
    from urllib2 import urlopen, Request, URLError, HTTPError

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import uservar

ADDON = xbmcaddon.Addon()


def download_file(url, destination, progress_dialog=None):
    """
    Download a file from URL to destination with progress tracking

    Args:
        url: URL to download from
        destination: Local file path to save to
        progress_dialog: Optional xbmcgui.DialogProgress instance

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        xbmc.log('[Pigeon Build] Downloading: {}'.format(url), xbmc.LOGINFO)

        # Create request with headers
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        # Open connection
        response = urlopen(req, timeout=30)

        # Get file size
        file_size = int(response.headers.get('Content-Length', 0))
        if file_size == 0:
            xbmc.log('[Pigeon Build] Warning: Content-Length is 0 or not provided', xbmc.LOGWARNING)

        # Create destination directory if needed
        dest_dir = os.path.dirname(destination)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Download file with progress
        downloaded = 0
        block_size = 8192

        with open(destination, 'wb') as f:
            while True:
                # Check if user cancelled
                if progress_dialog and progress_dialog.iscanceled():
                    xbmc.log('[Pigeon Build] Download cancelled by user', xbmc.LOGINFO)
                    response.close()
                    if os.path.exists(destination):
                        os.remove(destination)
                    return False

                # Read block
                buffer = response.read(block_size)
                if not buffer:
                    break

                # Write block
                f.write(buffer)
                downloaded += len(buffer)

                # Update progress
                if progress_dialog and file_size > 0:
                    percent = int((downloaded * 100) / file_size)
                    progress_dialog.update(
                        percent,
                        'Downloading...\n{:.2f} MB / {:.2f} MB'.format(
                            downloaded / (1024 * 1024),
                            file_size / (1024 * 1024)
                        )
                    )

        response.close()

        xbmc.log('[Pigeon Build] Download complete: {} ({} bytes)'.format(destination, downloaded), xbmc.LOGINFO)
        return True

    except HTTPError as e:
        xbmc.log('[Pigeon Build] HTTP Error {}: {}'.format(e.code, url), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Download failed: HTTP Error {}'.format(e.code),
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return False

    except URLError as e:
        xbmc.log('[Pigeon Build] URL Error: {}'.format(str(e.reason)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Download failed: Network error',
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return False

    except Exception as e:
        xbmc.log('[Pigeon Build] Download error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Download failed: {}'.format(str(e)),
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return False


def extract_zip(zip_path, extract_to, progress_dialog=None):
    """
    Extract a ZIP file with progress tracking

    Args:
        zip_path: Path to ZIP file
        extract_to: Directory to extract to
        progress_dialog: Optional xbmcgui.DialogProgress instance

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        xbmc.log('[Pigeon Build] Extracting: {} to {}'.format(zip_path, extract_to), xbmc.LOGINFO)

        if not os.path.exists(zip_path):
            xbmc.log('[Pigeon Build] ZIP file not found: {}'.format(zip_path), xbmc.LOGERROR)
            return False

        # Create extraction directory if needed
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)

        # Open ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files
            file_list = zip_ref.namelist()
            total_files = len(file_list)

            xbmc.log('[Pigeon Build] Extracting {} files...'.format(total_files), xbmc.LOGINFO)

            # Extract files with progress
            for index, file_name in enumerate(file_list):
                # Check if user cancelled
                if progress_dialog and progress_dialog.iscanceled():
                    xbmc.log('[Pigeon Build] Extraction cancelled by user', xbmc.LOGINFO)
                    return False

                # Extract file
                zip_ref.extract(file_name, extract_to)

                # Update progress
                if progress_dialog:
                    percent = int((index + 1) * 100 / total_files)
                    progress_dialog.update(
                        percent,
                        'Extracting files...\n{} / {}'.format(index + 1, total_files)
                    )

        xbmc.log('[Pigeon Build] Extraction complete: {} files extracted'.format(total_files), xbmc.LOGINFO)
        return True

    except zipfile.BadZipFile as e:
        xbmc.log('[Pigeon Build] Bad ZIP file: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Invalid or corrupted ZIP file',
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return False

    except Exception as e:
        xbmc.log('[Pigeon Build] Extraction error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Extraction failed: {}'.format(str(e)),
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return False


def download_and_extract(url, extract_to, progress_dialog=None, cleanup_zip=True):
    """
    Download a ZIP file and extract it

    Args:
        url: URL to download ZIP from
        extract_to: Directory to extract to
        progress_dialog: Optional xbmcgui.DialogProgress instance
        cleanup_zip: Delete ZIP file after extraction

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create temp directory
        temp_dir = os.path.join(uservar.ADDON_DATA, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Download file
        zip_name = os.path.basename(url)
        if not zip_name.endswith('.zip'):
            zip_name = 'download.zip'

        zip_path = os.path.join(temp_dir, zip_name)

        if progress_dialog:
            progress_dialog.update(10, 'Downloading file...')

        success = download_file(url, zip_path, progress_dialog)
        if not success:
            return False

        # Extract file
        if progress_dialog:
            progress_dialog.update(50, 'Extracting files...')

        success = extract_zip(zip_path, extract_to, progress_dialog)
        if not success:
            return False

        # Cleanup
        if cleanup_zip and os.path.exists(zip_path):
            try:
                os.remove(zip_path)
                xbmc.log('[Pigeon Build] Cleaned up ZIP file: {}'.format(zip_path), xbmc.LOGDEBUG)
            except Exception as e:
                xbmc.log('[Pigeon Build] Failed to cleanup ZIP: {}'.format(str(e)), xbmc.LOGWARNING)

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Download and extract error: {}'.format(str(e)), xbmc.LOGERROR)
        return False


def copy_directory(src, dst, excludes=None, progress_dialog=None):
    """
    Copy directory contents with exclusions and progress tracking

    Args:
        src: Source directory
        dst: Destination directory
        excludes: List of directory/file names to exclude
        progress_dialog: Optional xbmcgui.DialogProgress instance

    Returns:
        bool: True if successful, False otherwise
    """
    if excludes is None:
        excludes = []

    try:
        xbmc.log('[Pigeon Build] Copying: {} to {}'.format(src, dst), xbmc.LOGINFO)

        if not os.path.exists(src):
            xbmc.log('[Pigeon Build] Source directory not found: {}'.format(src), xbmc.LOGERROR)
            return False

        # Count total files for progress
        total_files = 0
        for root, dirs, files in os.walk(src):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in excludes]
            total_files += len(files)

        copied_files = 0

        # Copy files
        for root, dirs, files in os.walk(src):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in excludes]

            # Calculate relative path
            rel_path = os.path.relpath(root, src)
            dst_root = os.path.join(dst, rel_path) if rel_path != '.' else dst

            # Create destination directory
            if not os.path.exists(dst_root):
                os.makedirs(dst_root)

            # Copy files
            for file_name in files:
                # Check if user cancelled
                if progress_dialog and progress_dialog.iscanceled():
                    xbmc.log('[Pigeon Build] Copy cancelled by user', xbmc.LOGINFO)
                    return False

                # Skip excluded files
                if file_name in excludes:
                    continue

                src_file = os.path.join(root, file_name)
                dst_file = os.path.join(dst_root, file_name)

                # Copy file
                try:
                    shutil.copy2(src_file, dst_file)
                    copied_files += 1

                    # Update progress
                    if progress_dialog and total_files > 0:
                        percent = int((copied_files * 100) / total_files)
                        progress_dialog.update(
                            percent,
                            'Copying files...\n{} / {}'.format(copied_files, total_files)
                        )

                except Exception as e:
                    xbmc.log('[Pigeon Build] Failed to copy {}: {}'.format(file_name, str(e)), xbmc.LOGWARNING)

        xbmc.log('[Pigeon Build] Copy complete: {} files copied'.format(copied_files), xbmc.LOGINFO)
        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Copy directory error: {}'.format(str(e)), xbmc.LOGERROR)
        return False


def verify_file(file_path, min_size=1024):
    """
    Verify a file exists and has reasonable size

    Args:
        file_path: Path to file
        min_size: Minimum expected size in bytes

    Returns:
        bool: True if file is valid, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            xbmc.log('[Pigeon Build] File not found: {}'.format(file_path), xbmc.LOGERROR)
            return False

        file_size = os.path.getsize(file_path)
        if file_size < min_size:
            xbmc.log('[Pigeon Build] File too small: {} ({} bytes)'.format(file_path, file_size), xbmc.LOGERROR)
            return False

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] File verification error: {}'.format(str(e)), xbmc.LOGERROR)
        return False


def install_repository(repo_url, repo_name, progress_dialog=None):
    """
    Download and install a Kodi repository

    Args:
        repo_url: URL to repository ZIP file
        repo_name: Name of repository for logging
        progress_dialog: Optional progress dialog to update

    Returns:
        bool: True if successful, False otherwise
    """
    import os
    import xbmc
    import xbmcvfs

    try:
        xbmc.log('[Pigeon Build] Installing repository: {}'.format(repo_name), xbmc.LOGINFO)

        if progress_dialog:
            progress_dialog.update(10, 'Downloading {}...'.format(repo_name))

        # Create temp directory for download
        temp_dir = os.path.join(os.path.expanduser('~'), '.kodi', 'temp', 'repo_install')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Download repository ZIP
        repo_filename = os.path.basename(repo_url)
        repo_zip_path = os.path.join(temp_dir, repo_filename)

        xbmc.log('[Pigeon Build] Downloading from: {}'.format(repo_url), xbmc.LOGINFO)
        download_success = download_file(repo_url, repo_zip_path, progress_dialog)

        if not download_success:
            xbmc.log('[Pigeon Build] Repository download failed', xbmc.LOGERROR)
            return False

        if progress_dialog:
            progress_dialog.update(40, 'Extracting repository...')

        # Extract repository to temp location
        extract_dir = os.path.join(temp_dir, 'extracted')
        if os.path.exists(extract_dir):
            import shutil
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)

        extract_success = extract_zip(repo_zip_path, extract_dir)

        if not extract_success:
            xbmc.log('[Pigeon Build] Repository extraction failed', xbmc.LOGERROR)
            return False

        if progress_dialog:
            progress_dialog.update(60, 'Installing repository...')

        # Find the repository addon folder
        repo_folder = None
        for item in os.listdir(extract_dir):
            item_path = os.path.join(extract_dir, item)
            if os.path.isdir(item_path) and item.startswith('repository.'):
                repo_folder = item
                break

        if not repo_folder:
            xbmc.log('[Pigeon Build] Repository folder not found in ZIP', xbmc.LOGERROR)
            return False

        # Copy repository to Kodi addons folder
        addons_dir = os.path.join(os.path.expanduser('~'), '.kodi', 'addons')
        repo_source = os.path.join(extract_dir, repo_folder)
        repo_dest = os.path.join(addons_dir, repo_folder)

        if os.path.exists(repo_dest):
            xbmc.log('[Pigeon Build] Removing existing repository: {}'.format(repo_folder), xbmc.LOGINFO)
            import shutil
            shutil.rmtree(repo_dest)

        xbmc.log('[Pigeon Build] Copying repository to: {}'.format(repo_dest), xbmc.LOGINFO)
        import shutil
        shutil.copytree(repo_source, repo_dest)

        if progress_dialog:
            progress_dialog.update(80, 'Enabling repository...')

        # Enable the repository addon using JSON-RPC
        import json
        enable_cmd = json.dumps({
            "jsonrpc": "2.0",
            "method": "Addons.SetAddonEnabled",
            "params": {
                "addonid": repo_folder,
                "enabled": True
            },
            "id": 1
        })

        xbmc.executeJSONRPC(enable_cmd)
        xbmc.sleep(1000)

        # Update addon repositories
        xbmc.executebuiltin('UpdateAddonRepos')
        xbmc.sleep(2000)

        if progress_dialog:
            progress_dialog.update(100, 'Repository installed!')

        # Cleanup
        try:
            os.remove(repo_zip_path)
            import shutil
            shutil.rmtree(extract_dir)
        except:
            pass

        xbmc.log('[Pigeon Build] Repository installed successfully: {}'.format(repo_name), xbmc.LOGINFO)
        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Repository installation error: {}'.format(str(e)), xbmc.LOGERROR)
        return False
