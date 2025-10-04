#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pigeon Build Wizard - Backup Module
Backup and restore functionality for Kodi configuration
"""

import os
import sys
import zipfile
import shutil
import time
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

# Backup directory
BACKUP_DIR = os.path.join(uservar.ADDON_DATA, 'backups')


def ensure_backup_dir():
    """Ensure backup directory exists"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        xbmc.log('[Pigeon Build] Created backup directory: {}'.format(BACKUP_DIR), xbmc.LOGINFO)


def get_backup_name():
    """Generate backup filename with timestamp"""
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    return 'pigeon_backup_{}.zip'.format(timestamp)


def list_backups():
    """
    List all available backups

    Returns:
        list: List of backup filenames sorted by date (newest first)
    """
    ensure_backup_dir()

    try:
        backups = []
        if os.path.exists(BACKUP_DIR):
            for filename in os.listdir(BACKUP_DIR):
                if filename.startswith('pigeon_backup_') and filename.endswith('.zip'):
                    backup_path = os.path.join(BACKUP_DIR, filename)
                    file_size = os.path.getsize(backup_path)
                    file_time = os.path.getmtime(backup_path)
                    backups.append({
                        'filename': filename,
                        'path': backup_path,
                        'size': file_size,
                        'time': file_time
                    })

        # Sort by time (newest first)
        backups.sort(key=lambda x: x['time'], reverse=True)

        return backups

    except Exception as e:
        xbmc.log('[Pigeon Build] Error listing backups: {}'.format(str(e)), xbmc.LOGERROR)
        return []


def cleanup_old_backups():
    """
    Keep only the most recent backups as specified in uservar.KEEP_BACKUPS

    Returns:
        int: Number of backups deleted
    """
    try:
        backups = list_backups()
        keep_count = uservar.KEEP_BACKUPS

        if len(backups) <= keep_count:
            return 0

        # Delete old backups
        deleted = 0
        for backup in backups[keep_count:]:
            try:
                os.remove(backup['path'])
                deleted += 1
                xbmc.log('[Pigeon Build] Deleted old backup: {}'.format(backup['filename']), xbmc.LOGINFO)
            except Exception as e:
                xbmc.log('[Pigeon Build] Failed to delete backup {}: {}'.format(backup['filename'], str(e)), xbmc.LOGWARNING)

        return deleted

    except Exception as e:
        xbmc.log('[Pigeon Build] Cleanup old backups error: {}'.format(str(e)), xbmc.LOGERROR)
        return 0


def create_backup(selective=True):
    """
    Create a backup of Kodi userdata

    Args:
        selective: If True, preserve Trakt/Debrid/login data as per uservar settings

    Returns:
        bool: True if successful, False otherwise
    """
    ensure_backup_dir()

    # Confirm backup
    confirmed = xbmcgui.Dialog().yesno(
        uservar.ADDON_NAME,
        'Create a backup of your current Kodi configuration?\n\n'
        'This will backup your userdata folder to:\n{}'.format(BACKUP_DIR)
    )

    if not confirmed:
        return False

    try:
        progress = xbmcgui.DialogProgress()
        progress.create(uservar.ADDON_NAME, 'Creating backup...')

        # Generate backup filename
        backup_name = get_backup_name()
        backup_path = os.path.join(BACKUP_DIR, backup_name)

        progress.update(10, 'Preparing backup...')
        xbmc.sleep(100)

        # Create ZIP file
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Count total files
            total_files = 0
            for root, dirs, files in os.walk(USER_PATH):
                total_files += len(files)

            files_added = 0

            # Add files to ZIP
            for root, dirs, files in os.walk(USER_PATH):
                # Check if user cancelled
                if progress.iscanceled():
                    progress.close()
                    if os.path.exists(backup_path):
                        os.remove(backup_path)
                    xbmc.log('[Pigeon Build] Backup cancelled by user', xbmc.LOGINFO)
                    return False

                # Calculate relative path
                rel_path = os.path.relpath(root, USER_PATH)

                for file in files:
                    file_path = os.path.join(root, file)
                    archive_name = os.path.join(rel_path, file) if rel_path != '.' else file

                    try:
                        zipf.write(file_path, archive_name)
                        files_added += 1

                        # Update progress
                        if total_files > 0:
                            percent = int((files_added * 90) / total_files) + 10
                            progress.update(
                                percent,
                                'Backing up files...\n{} / {}'.format(files_added, total_files)
                            )

                    except Exception as e:
                        xbmc.log('[Pigeon Build] Failed to backup {}: {}'.format(file, str(e)), xbmc.LOGWARNING)

        progress.update(100, 'Backup complete!')
        xbmc.sleep(500)
        progress.close()

        # Get backup size
        backup_size = os.path.getsize(backup_path)
        size_mb = backup_size / (1024 * 1024)

        # Cleanup old backups
        cleanup_old_backups()

        # Show success message
        xbmcgui.Dialog().ok(
            uservar.ADDON_NAME,
            '[B]Backup Created Successfully![/B]\n\n'
            'Files backed up: {}\n'
            'Backup size: {:.2f} MB\n'
            'Location: {}'.format(files_added, size_mb, backup_name)
        )

        xbmc.log('[Pigeon Build] Backup created: {} ({} files, {:.2f} MB)'.format(
            backup_name, files_added, size_mb), xbmc.LOGINFO)

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Create backup error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Backup failed: {}'.format(str(e)),
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return False


def restore_backup(backup_filename=None):
    """
    Restore from a backup

    Args:
        backup_filename: Optional specific backup to restore. If None, shows selection dialog.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Get list of backups
        backups = list_backups()

        if not backups:
            xbmcgui.Dialog().ok(
                uservar.ADDON_NAME,
                'No backups found!\n\nCreate a backup first before you can restore.'
            )
            return False

        # Select backup if not specified
        if backup_filename is None:
            backup_options = []
            for backup in backups:
                size_mb = backup['size'] / (1024 * 1024)
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(backup['time']))
                backup_options.append('{} ({:.2f} MB) - {}'.format(
                    backup['filename'], size_mb, time_str
                ))

            selected = xbmcgui.Dialog().select(
                'Select Backup to Restore',
                backup_options
            )

            if selected < 0:
                return False

            backup_to_restore = backups[selected]
        else:
            # Find specified backup
            backup_to_restore = None
            for backup in backups:
                if backup['filename'] == backup_filename:
                    backup_to_restore = backup
                    break

            if backup_to_restore is None:
                xbmcgui.Dialog().ok(
                    uservar.ADDON_NAME,
                    'Backup not found: {}'.format(backup_filename)
                )
                return False

        # Confirm restoration
        confirmed = xbmcgui.Dialog().yesno(
            uservar.ADDON_NAME,
            '[B]WARNING: RESTORE BACKUP[/B]\n\n'
            'This will replace your current configuration with:\n'
            '{}\n\n'
            'Your current configuration will be lost!\n\n'
            'Continue?'.format(backup_to_restore['filename']),
            nolabel='Cancel',
            yeslabel='Restore'
        )

        if not confirmed:
            return False

        # Perform restoration
        progress = xbmcgui.DialogProgress()
        progress.create(uservar.ADDON_NAME, 'Restoring backup...')

        backup_path = backup_to_restore['path']

        progress.update(10, 'Preparing restore...')
        xbmc.sleep(100)

        # Extract ZIP file
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            file_list = zipf.namelist()
            total_files = len(file_list)

            progress.update(20, 'Extracting files...\n{} files to restore'.format(total_files))

            for index, file_name in enumerate(file_list):
                # Check if user cancelled
                if progress.iscanceled():
                    progress.close()
                    xbmc.log('[Pigeon Build] Restore cancelled by user', xbmc.LOGINFO)
                    return False

                # Extract file
                zipf.extract(file_name, USER_PATH)

                # Update progress
                if total_files > 0:
                    percent = int((index + 1) * 80 / total_files) + 20
                    progress.update(
                        percent,
                        'Restoring files...\n{} / {}'.format(index + 1, total_files)
                    )

        progress.update(100, 'Restore complete!')
        xbmc.sleep(500)
        progress.close()

        # Show success message
        xbmcgui.Dialog().ok(
            uservar.ADDON_NAME,
            '[B]Restore Complete![/B]\n\n'
            '{} files restored from backup.\n\n'
            'Kodi will now force close.\n'
            'Restart Kodi to complete the restore process.'.format(total_files)
        )

        xbmc.log('[Pigeon Build] Backup restored: {} ({} files)'.format(
            backup_to_restore['filename'], total_files), xbmc.LOGINFO)

        xbmc.sleep(2000)

        # Force close Kodi
        os._exit(1)

        return True

    except Exception as e:
        xbmc.log('[Pigeon Build] Restore backup error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Restore failed: {}'.format(str(e)),
            xbmcgui.NOTIFICATION_ERROR,
            5000
        )
        return False


def view_backups():
    """
    Show detailed information about available backups
    """
    try:
        backups = list_backups()

        if not backups:
            xbmcgui.Dialog().ok(
                uservar.ADDON_NAME,
                'No backups found!\n\nCreate a backup from the Backup & Restore menu.'
            )
            return

        # Build info text
        info_text = '[B]Available Backups[/B]\n\n'
        info_text += 'Location: {}\n\n'.format(BACKUP_DIR)

        for backup in backups:
            size_mb = backup['size'] / (1024 * 1024)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(backup['time']))
            info_text += '[B]{}[/B]\n'.format(backup['filename'])
            info_text += 'Size: {:.2f} MB\n'.format(size_mb)
            info_text += 'Date: {}\n\n'.format(time_str)

        xbmcgui.Dialog().textviewer('Backup Information', info_text)

    except Exception as e:
        xbmc.log('[Pigeon Build] View backups error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Error viewing backups',
            xbmcgui.NOTIFICATION_ERROR,
            3000
        )


def delete_backup():
    """
    Delete a selected backup
    """
    try:
        backups = list_backups()

        if not backups:
            xbmcgui.Dialog().ok(
                uservar.ADDON_NAME,
                'No backups to delete!'
            )
            return

        # Select backup to delete
        backup_options = []
        for backup in backups:
            size_mb = backup['size'] / (1024 * 1024)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(backup['time']))
            backup_options.append('{} ({:.2f} MB) - {}'.format(
                backup['filename'], size_mb, time_str
            ))

        selected = xbmcgui.Dialog().select(
            'Select Backup to Delete',
            backup_options
        )

        if selected < 0:
            return

        backup_to_delete = backups[selected]

        # Confirm deletion
        confirmed = xbmcgui.Dialog().yesno(
            uservar.ADDON_NAME,
            'Delete backup?\n\n{}\n\nThis cannot be undone!'.format(backup_to_delete['filename']),
            nolabel='Cancel',
            yeslabel='Delete'
        )

        if not confirmed:
            return

        # Delete backup
        os.remove(backup_to_delete['path'])

        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Backup deleted: {}'.format(backup_to_delete['filename']),
            xbmcgui.NOTIFICATION_INFO,
            3000
        )

        xbmc.log('[Pigeon Build] Backup deleted: {}'.format(backup_to_delete['filename']), xbmc.LOGINFO)

    except Exception as e:
        xbmc.log('[Pigeon Build] Delete backup error: {}'.format(str(e)), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(
            uservar.ADDON_NAME,
            'Error deleting backup',
            xbmcgui.NOTIFICATION_ERROR,
            3000
        )
