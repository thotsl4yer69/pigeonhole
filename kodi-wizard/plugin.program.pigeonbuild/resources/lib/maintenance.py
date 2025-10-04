#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pigeon Build Wizard - Maintenance Module
Core maintenance functions for Kodi optimization
Based on RedWizard maintenance.py with Pigeon Build adaptations
"""

import os
import sys
import shutil
import sqlite3
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import uservar

ADDON = xbmcaddon.Addon()
HOME = os.path.expanduser('~')

# Kodi paths
KODI_HOME = os.path.join(HOME, '.kodi')
USER_PATH = os.path.join(KODI_HOME, 'userdata')
ADDON_DATA = os.path.join(USER_PATH, 'addon_data')
THUMBNAILS_PATH = os.path.join(USER_PATH, 'Thumbnails')
DATABASE_PATH = os.path.join(USER_PATH, 'Database')
PACKAGES_PATH = os.path.join(KODI_HOME, 'addons', 'packages')
ADDONS_DB = os.path.join(DATABASE_PATH, 'Addons33.db')
TEXTURES_DB = os.path.join(DATABASE_PATH, 'Textures13.db')


def purge_db(db_path):
    """
    Purge all data from a database except version table

    Args:
        db_path: Path to the SQLite database file

    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(db_path):
        xbmc.log('[Pigeon Build] Database not found: {}'.format(db_path), xbmc.LOGINFO)
        return False

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Get all tables
        cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = cur.fetchall()

        # Clear all tables except 'version'
        for table in tables:
            table_name = table[0]
            if table_name == 'version':
                xbmc.log('[Pigeon Build] Skipping version table: {}'.format(table_name), xbmc.LOGDEBUG)
            else:
                try:
                    cur.execute("DELETE FROM {}".format(table_name))
                    conn.commit()
                    xbmc.log('[Pigeon Build] Cleared table: {}'.format(table_name), xbmc.LOGDEBUG)
                except Exception as e:
                    xbmc.log('[Pigeon Build] Error clearing table {}: {}'.format(table_name, str(e)), xbmc.LOGERROR)

        # Vacuum to reclaim space
        conn.execute('VACUUM')
        conn.close()

        xbmc.log('[Pigeon Build] Database purged successfully: {}'.format(db_path), xbmc.LOGINFO)
        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Database purge error: {}'.format(str(e)), xbmc.LOGERROR)
        return False


def clear_cache():
    """
    Clear Kodi cache files

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cache_paths = [
            os.path.join(USER_PATH, 'Temp'),
            os.path.join(KODI_HOME, 'temp')
        ]

        files_cleared = 0

        for cache_path in cache_paths:
            if os.path.exists(cache_path):
                for root, dirs, files in os.walk(cache_path):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            files_cleared += 1
                        except Exception as e:
                            xbmc.log('[Pigeon Build] Failed to delete cache file {}: {}'.format(file, str(e)), xbmc.LOGDEBUG)

        xbmc.log('[Pigeon Build] Cache cleared: {} files removed'.format(files_cleared), xbmc.LOGINFO)

        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Cache cleared! ({} files removed)'.format(files_cleared),
            xbmcgui.NOTIFICATION_INFO,
            3000
        )

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Clear cache error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Error clearing cache',
            xbmcgui.NOTIFICATION_ERROR,
            3000
        )
        return False


def clear_thumbnails():
    """
    Clear Kodi thumbnails and purge textures database

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Remove thumbnails directory
        if os.path.exists(THUMBNAILS_PATH):
            shutil.rmtree(THUMBNAILS_PATH)
            xbmc.log('[Pigeon Build] Thumbnails directory removed', xbmc.LOGINFO)

        # Purge textures database
        if os.path.exists(TEXTURES_DB):
            purge_db(TEXTURES_DB)

        xbmc.sleep(500)

        xbmcgui.Dialog().ok(
            uservar.ADDON_NAME,
            'Thumbnails cleared successfully!\n\nKodi will regenerate thumbnails as needed.'
        )

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Clear thumbnails error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Error clearing thumbnails',
            xbmcgui.NOTIFICATION_ERROR,
            3000
        )
        return False


def clear_packages():
    """
    Clear addon packages directory

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(PACKAGES_PATH):
            xbmcgui.Dialog().notification(
                uservar.ADDON_NAME,
                'No packages to clear',
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
            return True

        file_count = 0

        for filename in os.listdir(PACKAGES_PATH):
            file_path = os.path.join(PACKAGES_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    file_count += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    file_count += 1
            except Exception as e:
                xbmc.log('[Pigeon Build] Failed to delete package {}: {}'.format(filename, str(e)), xbmc.LOGDEBUG)

        xbmc.log('[Pigeon Build] Packages cleared: {} items removed'.format(file_count), xbmc.LOGINFO)

        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            '{} packages cleared!'.format(file_count),
            xbmcgui.NOTIFICATION_INFO,
            3000
        )

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Clear packages error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Error clearing packages',
            xbmcgui.NOTIFICATION_ERROR,
            3000
        )
        return False


def purge_old_databases():
    """
    Purge old/obsolete databases to free up space

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not os.path.exists(DATABASE_PATH):
            return True

        # Find all database files
        db_files = [f for f in os.listdir(DATABASE_PATH) if f.endswith('.db')]

        # Databases to keep (latest versions)
        keep_patterns = [
            'Addons',
            'Textures',
            'MyVideos',
            'MyMusic',
            'TV',
            'Epg'
        ]

        # Find the highest version number for each type
        db_versions = {}
        for db_file in db_files:
            for pattern in keep_patterns:
                if db_file.startswith(pattern):
                    # Extract version number
                    version_str = db_file.replace(pattern, '').replace('.db', '')
                    try:
                        version = int(version_str) if version_str else 0
                        if pattern not in db_versions or version > db_versions[pattern]:
                            db_versions[pattern] = version
                    except ValueError:
                        pass

        # Delete old versions
        deleted_count = 0
        for db_file in db_files:
            for pattern in keep_patterns:
                if db_file.startswith(pattern):
                    version_str = db_file.replace(pattern, '').replace('.db', '')
                    try:
                        version = int(version_str) if version_str else 0
                        # Keep latest version and one version back for safety
                        if version < db_versions.get(pattern, 0) - 1:
                            db_path = os.path.join(DATABASE_PATH, db_file)
                            os.remove(db_path)
                            deleted_count += 1
                            xbmc.log('[Pigeon Build] Deleted old database: {}'.format(db_file), xbmc.LOGINFO)
                    except ValueError:
                        pass

        if deleted_count > 0:
            xbmcgui.Dialog().notification(
                uservar.ADDON_NAME,
                '{} old databases removed!'.format(deleted_count),
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
        else:
            xbmcgui.Dialog().notification(
                uservar.ADDON_NAME,
                'No old databases found',
                xbmcgui.NOTIFICATION_INFO,
                3000
            )

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Purge databases error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Error purging databases',
            xbmcgui.NOTIFICATION_ERROR,
            3000
        )
        return False


def fresh_start():
    """
    Nuclear option - completely reset Kodi to fresh state
    Preserves wizard and repository addons

    Returns:
        bool: True if successful, False otherwise
    """
    # Confirm action
    confirmed = xbmcgui.Dialog().yesno(
        uservar.ADDON_NAME,
        '[B]WARNING: FRESH START[/B]\n\n'
        'This will delete ALL Kodi data and reset to factory defaults.\n\n'
        'The following will be PRESERVED:\n'
        '- Pigeon Build Wizard\n'
        '- Pigeon Repository\n\n'
        'Everything else will be DELETED!\n\n'
        'Are you absolutely sure?',
        nolabel='Cancel',
        yeslabel='Yes, Reset Everything'
    )

    if not confirmed:
        return False

    # Second confirmation
    confirmed2 = xbmcgui.Dialog().yesno(
        uservar.ADDON_NAME,
        '[B]FINAL WARNING[/B]\n\n'
        'This cannot be undone!\n\n'
        'Proceed with Fresh Start?',
        nolabel='Cancel',
        yeslabel='Yes, I\'m Sure'
    )

    if not confirmed2:
        return False

    try:
        progress = xbmcgui.DialogProgress()
        progress.create(uservar.ADDON_NAME, 'Performing Fresh Start...')

        progress.update(10, 'Deleting files and folders...')
        xbmc.sleep(100)

        # Delete files in userdata (excluding wizard addon data)
        for root, dirs, files in os.walk(USER_PATH, topdown=True):
            # Exclude wizard addon data directory
            dirs[:] = [d for d in dirs if not d == 'addon_data' or os.path.join(root, d) != ADDON_DATA]

            for name in files:
                file_path = os.path.join(root, name)
                # Skip wizard-related files
                if uservar.ADDON_ID not in file_path and uservar.REPO_ID not in file_path:
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        xbmc.log('[Pigeon Build] Failed to delete {}: {}'.format(name, str(e)), xbmc.LOGDEBUG)

        progress.update(40, 'Removing addon data...')
        xbmc.sleep(100)

        # Remove addon_data directories (except wizard and repo)
        if os.path.exists(ADDON_DATA):
            for addon_dir in os.listdir(ADDON_DATA):
                if addon_dir not in [uservar.ADDON_ID, uservar.REPO_ID] and addon_dir not in uservar.EXCLUDES:
                    addon_path = os.path.join(ADDON_DATA, addon_dir)
                    try:
                        shutil.rmtree(addon_path)
                    except Exception as e:
                        xbmc.log('[Pigeon Build] Failed to delete addon data {}: {}'.format(addon_dir, str(e)), xbmc.LOGDEBUG)

        progress.update(70, 'Clearing databases...')
        xbmc.sleep(100)

        # Clear thumbnails
        if os.path.exists(THUMBNAILS_PATH):
            shutil.rmtree(THUMBNAILS_PATH)

        # Purge databases
        if os.path.exists(TEXTURES_DB):
            purge_db(TEXTURES_DB)

        progress.update(90, 'Clearing packages...')
        xbmc.sleep(100)

        # Clear packages
        if os.path.exists(PACKAGES_PATH):
            for filename in os.listdir(PACKAGES_PATH):
                file_path = os.path.join(PACKAGES_PATH, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    xbmc.log('[Pigeon Build] Failed to delete package {}: {}'.format(filename, str(e)), xbmc.LOGDEBUG)

        progress.update(100, 'Fresh Start complete!')
        xbmc.sleep(1000)
        progress.close()

        # Show completion message
        xbmcgui.Dialog().ok(
            uservar.ADDON_NAME,
            '[B]Fresh Start Complete![/B]\n\n'
            'Kodi has been reset to factory defaults.\n\n'
            'Kodi will now force close.\n'
            'Restart Kodi to complete the process.'
        )

        xbmc.sleep(2000)

        # Force close Kodi
        xbmc.log('[Pigeon Build] Fresh Start complete - forcing Kodi exit', xbmc.LOGINFO)
        os._exit(1)

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Fresh start error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Error performing fresh start',
            xbmcgui.NOTIFICATION_ERROR,
            3000
        )
        return False


def apply_advanced_settings(device_type):
    """
    Apply optimized advanced settings for device type using JSON-RPC

    Args:
        device_type: One of 'firestick_1gb', 'firestick_2gb', 'shield_3gb', 'pc_4gb_plus'

    Returns:
        bool: True if successful, False otherwise
    """
    # Settings map based on RedWizard implementation
    settings_map = {
        'firestick_1gb': {
            'buffer': 2,
            'memory': 128 * 1024 * 1024,  # 128MB in bytes
            'readfactor': 1000,
            'chunksize': 131072
        },
        'firestick_2gb': {
            'buffer': 2,
            'memory': 192 * 1024 * 1024,  # 192MB in bytes
            'readfactor': 1000,
            'chunksize': 131072
        },
        'shield_3gb': {
            'buffer': 2,
            'memory': 256 * 1024 * 1024,  # 256MB in bytes
            'readfactor': 1000,
            'chunksize': 131072
        },
        'pc_4gb_plus': {
            'buffer': 2,
            'memory': 512 * 1024 * 1024,  # 512MB in bytes
            'readfactor': 1000,
            'chunksize': 131072
        }
    }

    if device_type not in settings_map:
        xbmc.log('[Pigeon Build] Invalid device type: {}'.format(device_type), xbmc.LOGERROR)
        return False

    try:
        settings = settings_map[device_type]

        # Apply settings via JSON-RPC
        xbmc.executeJSONRPC(
            '{{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{{"setting":"filecache.buffermode","value":{}}},"id":1}}'.format(settings['buffer'])
        )

        xbmc.executeJSONRPC(
            '{{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{{"setting":"filecache.memorysize","value":{}}},"id":1}}'.format(settings['memory'])
        )

        xbmc.executeJSONRPC(
            '{{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{{"setting":"filecache.readfactor","value":{}}},"id":1}}'.format(settings['readfactor'])
        )

        xbmc.executeJSONRPC(
            '{{"jsonrpc":"2.0","method":"Settings.SetSettingValue","params":{{"setting":"filecache.chunksize","value":{}}},"id":1}}'.format(settings['chunksize'])
        )

        # Refresh settings display (triggers settings save)
        xbmc.executebuiltin('ActivateWindowAndFocus(servicesettings), True')
        xbmc.sleep(100)
        xbmc.executebuiltin('Action(Back)')

        xbmc.log('[Pigeon Build] Advanced settings applied for: {}'.format(device_type), xbmc.LOGINFO)

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Apply advanced settings error: {}'.format(str(e)), xbmc.LOGERROR)
        return False
