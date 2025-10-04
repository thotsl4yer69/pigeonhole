#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pigeon Build Wizard - Main Wizard Module
Core wizard functionality
"""

import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import uservar
from resources.lib import gui

ADDON = xbmcaddon.Addon()

def first_run():
    """Handle first run of the wizard"""
    message = (
        '[B]Welcome to Pigeon Build Wizard![/B]\n\n'
        'This wizard will help you set up Kodi for the ultimate streaming experience.\n\n'
        '[COLOR {}]Features:[/COLOR]\n'
        '• Pre-configured builds for Fire TV Stick\n'
        '• Optimized settings for smooth streaming\n'
        '• Easy add-on installation\n'
        '• Maintenance tools\n'
        '• Backup & restore functionality\n\n'
        'Get started by selecting "Install Fresh Build" from the main menu.'
    ).format(uservar.COLOR_ACCENT)

    gui.show_text_box('Welcome to Pigeon Build', message)

def show_builds():
    """Display available builds"""
    for build in uservar.BUILDS:
        name = '[COLOR {}]{}[/COLOR] - v{}'.format(
            uservar.COLOR_ACCENT,
            build['name'],
            build['version']
        )

        description = build['description']

        gui.add_item(
            name=name,
            mode='dobuild',
            icon=build.get('icon', 'icon.png'),
            fanart=build.get('fanart', 'fanart.png'),
            description=description,
            params={'name': build['name'], 'url': build['url']}
        )

    gui.end_of_directory()

def show_addons():
    """Display available add-ons"""
    # Use the new ADDON_REPOS dictionary with full repository information
    for addon_key, addon_info in uservar.ADDON_REPOS.items():
        name = '[COLOR {}]{}[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY, addon_info['name'])

        gui.add_item(
            name=name,
            mode='doaddon',
            icon='addons.png',
            fanart='fanart.png',
            description=addon_info['description'],
            params={'addon_key': addon_key}
        )

    gui.end_of_directory()

def show_advanced_settings():
    """Display advanced settings options"""
    settings_options = [
        {
            'name': 'Fire TV Stick (1GB RAM)',
            'type': 'firestick_1gb',
            'description': 'Optimized settings for Fire TV Stick with 1GB RAM'
        },
        {
            'name': 'Fire TV Stick (2GB RAM) / 4K',
            'type': 'firestick_2gb',
            'description': 'Optimized settings for Fire TV Stick 4K and newer models'
        },
        {
            'name': 'NVIDIA Shield (3GB RAM)',
            'type': 'shield_3gb',
            'description': 'Optimized settings for NVIDIA Shield TV'
        },
        {
            'name': 'PC/Desktop (4GB+ RAM)',
            'type': 'pc_4gb_plus',
            'description': 'Optimized settings for desktop computers'
        }
    ]

    for setting in settings_options:
        name = '[COLOR {}]{}[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY, setting['name'])

        gui.add_item(
            name=name,
            mode='doadvanced',
            icon='settings.png',
            fanart='fanart.png',
            description=setting['description'],
            params={'type': setting['type']}
        )

    gui.end_of_directory()

def show_maintenance():
    """Display maintenance options"""
    maintenance_options = [
        {
            'name': 'Clear Cache',
            'action': 'clearcache',
            'description': 'Clear Kodi temporary cache files'
        },
        {
            'name': 'Clear Packages',
            'action': 'clearpackages',
            'description': 'Remove downloaded addon packages'
        },
        {
            'name': 'Clear Thumbnails',
            'action': 'clearthumbs',
            'description': 'Delete all thumbnails and purge textures database'
        },
        {
            'name': 'Purge Old Databases',
            'action': 'purgedb',
            'description': 'Remove obsolete database files to free space'
        },
        {
            'name': 'Fresh Start (Nuclear Option)',
            'action': 'freshstart',
            'description': 'Reset Kodi to factory defaults - USE WITH CAUTION!'
        }
    ]

    for option in maintenance_options:
        name = '[COLOR {}]{}[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY, option['name'])

        gui.add_item(
            name=name,
            mode='domaintenance',
            icon='maintenance.png',
            fanart='fanart.png',
            description=option['description'],
            params={'action': option['action']}
        )

    gui.end_of_directory()


def do_maintenance(action):
    """Execute maintenance action"""
    from resources.lib import maintenance

    if action == 'clearcache':
        maintenance.clear_cache()
    elif action == 'clearpackages':
        maintenance.clear_packages()
    elif action == 'clearthumbs':
        maintenance.clear_thumbnails()
    elif action == 'purgedb':
        maintenance.purge_old_databases()
    elif action == 'freshstart':
        maintenance.fresh_start()
    else:
        gui.show_ok_dialog('Error', 'Unknown maintenance action: {}'.format(action))

def show_backup():
    """Display backup/restore options"""
    backup_options = [
        {
            'name': 'Create New Backup',
            'action': 'createbackup',
            'description': 'Create a complete backup of your Kodi configuration'
        },
        {
            'name': 'Restore from Backup',
            'action': 'restorebackup',
            'description': 'Restore Kodi from a previous backup'
        },
        {
            'name': 'View Backups',
            'action': 'viewbackups',
            'description': 'View details of available backups'
        },
        {
            'name': 'Delete Backup',
            'action': 'deletebackup',
            'description': 'Remove a backup to free up space'
        }
    ]

    for option in backup_options:
        name = '[COLOR {}]{}[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY, option['name'])

        gui.add_item(
            name=name,
            mode='dobackup',
            icon='backup.png',
            fanart='fanart.png',
            description=option['description'],
            params={'action': option['action']}
        )

    gui.end_of_directory()


def do_backup(action):
    """Execute backup action"""
    from resources.lib import backup

    if action == 'createbackup':
        backup.create_backup()
    elif action == 'restorebackup':
        backup.restore_backup()
    elif action == 'viewbackups':
        backup.view_backups()
    elif action == 'deletebackup':
        backup.delete_backup()
    else:
        gui.show_ok_dialog('Error', 'Unknown backup action: {}'.format(action))

def show_support():
    """Display support/contact information"""
    support_text = (
        '[B][COLOR {}]Pigeon Build Support[/COLOR][/B]\n\n'
        '[COLOR {}]GitHub:[/COLOR] https://github.com/mz1312/pigeonhole\n'
        '[COLOR {}]Issues:[/COLOR] https://github.com/mz1312/pigeonhole/issues\n\n'
        '[B]Common Issues:[/B]\n'
        '• Buffering: Try applying advanced settings for your device\n'
        '• No streams: Check your internet connection and Real-Debrid\n'
        '• Crashes: Clear cache and packages from maintenance\n\n'
        '[B]Tips:[/B]\n'
        '• Use Real-Debrid for best quality and reliability\n'
        '• Keep your builds and add-ons updated\n'
        '• Run maintenance tools monthly\n'
    ).format(uservar.COLOR_ACCENT, uservar.COLOR_TEXT_SECONDARY, uservar.COLOR_TEXT_SECONDARY)

    gui.show_text_box('Support & Help', support_text)

def install_build(build_name):
    """Install a selected build"""
    from resources.lib import downloader
    from resources.lib import maintenance
    from resources.lib import backup
    import os
    import shutil

    # Find the build in the list
    build = None
    for b in uservar.BUILDS:
        if b['name'] == build_name:
            build = b
            break

    if not build:
        gui.show_ok_dialog('Error', 'Build not found')
        return

    # Confirm installation
    confirmed = gui.show_yes_no_dialog(
        'Install Build',
        '[B]{}[/B]\n\n{}\n\n'
        'This will replace your current Kodi configuration.\n\n'
        'Create a backup first (recommended)?'.format(
            build_name,
            build.get('description', '')
        )
    )

    if not confirmed:
        return

    # Offer to create backup
    create_backup = gui.show_yes_no_dialog(
        'Create Backup?',
        'Would you like to create a backup before installing the build?\n\n'
        'Highly recommended in case you want to restore later.'
    )

    try:
        # Show progress
        progress = gui.show_progress_dialog('Installing {}'.format(build_name))
        progress.update(0, 'Starting installation...')
        xbmc.sleep(500)

        # Create backup if requested
        if create_backup:
            progress.update(5, 'Creating backup...')
            # Create backup silently (without prompts)
            backup.ensure_backup_dir()
            backup_name = backup.get_backup_name()
            backup_path = os.path.join(backup.BACKUP_DIR, backup_name)

            import zipfile
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup.USER_PATH):
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive_name = os.path.relpath(file_path, backup.USER_PATH)
                        try:
                            zipf.write(file_path, archive_name)
                        except:
                            pass

            xbmc.log('[Pigeon Build] Pre-install backup created: {}'.format(backup_name), xbmc.LOGINFO)

        # Download build
        progress.update(10, 'Downloading build files...')
        xbmc.log('[Pigeon Build] Downloading build from: {}'.format(build['url']), xbmc.LOGINFO)

        temp_dir = os.path.join(uservar.ADDON_DATA, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        build_zip = os.path.join(temp_dir, 'build.zip')

        # Download the build ZIP
        download_success = downloader.download_file(build['url'], build_zip, progress)

        if not download_success:
            progress.close()
            gui.show_ok_dialog(
                'Download Failed',
                'Failed to download build files.\n\nPlease check your internet connection and try again.'
            )
            return

        # Extract build
        progress.update(40, 'Extracting build files...')
        xbmc.log('[Pigeon Build] Extracting build...', xbmc.LOGINFO)

        extract_dir = os.path.join(temp_dir, 'build_extract')
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)

        extract_success = downloader.extract_zip(build_zip, extract_dir, progress)

        if not extract_success:
            progress.close()
            gui.show_ok_dialog(
                'Extraction Failed',
                'Failed to extract build files.\n\nThe ZIP file may be corrupted.'
            )
            return

        # Clean Kodi (fresh start without full wipe)
        progress.update(60, 'Preparing Kodi for new build...')
        xbmc.log('[Pigeon Build] Performing selective clean...', xbmc.LOGINFO)

        # Note: We're not doing a full fresh start, just cleaning what the build will replace
        # Clear cache and thumbnails
        maintenance.clear_cache()
        if os.path.exists(maintenance.THUMBNAILS_PATH):
            shutil.rmtree(maintenance.THUMBNAILS_PATH)

        # Copy build files
        progress.update(70, 'Installing build files...')
        xbmc.log('[Pigeon Build] Copying build files to Kodi...', xbmc.LOGINFO)

        # Copy files from extract directory to Kodi home
        # Exclude wizard and repository addons as per uservar.EXCLUDES
        kodi_home = os.path.join(os.path.expanduser('~'), '.kodi')

        copy_success = downloader.copy_directory(
            extract_dir,
            kodi_home,
            excludes=uservar.EXCLUDES,
            progress_dialog=progress
        )

        if not copy_success:
            progress.close()
            gui.show_ok_dialog(
                'Installation Failed',
                'Failed to copy build files.\n\nPlease check the Kodi log for details.'
            )
            return

        # Apply GUI settings if provided
        if 'gui' in build and build['gui']:
            progress.update(85, 'Applying GUI settings...')
            gui_xml_path = os.path.join(uservar.ADDON_USERDATA, 'guisettings.xml')
            gui_download = downloader.download_file(build['gui'], gui_xml_path)
            if gui_download:
                xbmc.log('[Pigeon Build] GUI settings applied', xbmc.LOGINFO)

        # Cleanup temp files
        progress.update(95, 'Cleaning up...')
        try:
            if os.path.exists(build_zip):
                os.remove(build_zip)
            if os.path.exists(extract_dir):
                shutil.rmtree(extract_dir)
        except:
            pass

        progress.update(100, 'Installation complete!')
        xbmc.sleep(1000)
        progress.close()

        # Show completion message
        gui.show_ok_dialog(
            'Installation Complete',
            '[B]{} has been installed successfully![/B]\n\n'
            'Kodi will now force close.\n'
            'Restart Kodi to enjoy your new build!'.format(build_name)
        )

        xbmc.log('[Pigeon Build] Build installation complete: {}'.format(build_name), xbmc.LOGINFO)

        xbmc.sleep(2000)

        # Force close Kodi to apply changes
        os._exit(1)

    except Exception as e:
        xbmc.log('[Pigeon Build] Build installation error: {}'.format(str(e)), xbmc.LOGERROR)
        if 'progress' in locals():
            progress.close()
        gui.show_ok_dialog(
            'Installation Error',
            'Failed to install build.\n\nError: {}\n\nCheck the Kodi log for details.'.format(str(e))
        )

def install_addon(addon_key):
    """Install a selected addon (with automatic repository installation)"""
    from resources.lib import downloader

    try:
        # Get addon info from ADDON_REPOS
        if addon_key not in uservar.ADDON_REPOS:
            gui.show_ok_dialog('Error', 'Add-on information not found')
            return

        addon_info = uservar.ADDON_REPOS[addon_key]
        addon_name = addon_info['name']
        repo_url = addon_info['repo_url']
        repo_name = addon_info['name']
        addon_id = addon_info['addon_id']

        xbmc.log('[Pigeon Build] Installing addon: {} from {}'.format(addon_name, repo_name), xbmc.LOGINFO)

        # Show info and confirm
        confirmed = gui.show_yes_no_dialog(
            'Install {}?'.format(addon_name),
            '[B]{}[/B]\n\n'
            '{}\n\n'
            'This will:\n'
            '1. Download and install {} repository\n'
            '2. Install {} addon from the repository\n'
            '3. May require additional setup (Trakt, Real-Debrid, etc.)\n\n'
            'Continue?'.format(
                addon_name,
                addon_info['description'],
                repo_name,
                addon_name
            )
        )

        if not confirmed:
            return

        # Show progress
        progress = gui.show_progress_dialog('Installing {}'.format(addon_name))
        progress.update(5, 'Preparing installation...')

        # Step 1: Install repository
        progress.update(10, 'Installing {} repository...'.format(repo_name))
        xbmc.log('[Pigeon Build] Installing repository: {}'.format(repo_url), xbmc.LOGINFO)

        repo_success = downloader.install_repository(repo_url, repo_name, progress)

        if not repo_success:
            progress.close()
            gui.show_ok_dialog(
                'Repository Installation Failed',
                'Failed to install {} repository.\n\n'
                'Please check your internet connection and try again.\n\n'
                'You can also install the repository manually.'.format(repo_name)
            )
            return

        # Wait for repository to register
        progress.update(70, 'Waiting for repository to register...')
        xbmc.sleep(3000)

        # Step 2: Install addon from repository
        progress.update(75, 'Installing {} addon...'.format(addon_name))
        xbmc.log('[Pigeon Build] Installing addon: {}'.format(addon_id), xbmc.LOGINFO)

        # Use Kodi's built-in addon installer
        xbmc.executebuiltin('InstallAddon({})'.format(addon_id))

        # Wait for installation
        progress.update(80, 'Installing addon from repository...')
        xbmc.sleep(5000)

        progress.update(100, 'Installation complete!')
        xbmc.sleep(1000)
        progress.close()

        # Show completion message
        gui.show_ok_dialog(
            '{} Installed!'.format(addon_name),
            '[B]{} has been installed successfully![/B]\n\n'
            'Next steps:\n'
            '• Find it in Add-ons → Video add-ons\n'
            '• Configure settings if needed (Trakt, Real-Debrid, etc.)\n'
            '• Some addons may require first-time setup\n\n'
            'Check Kodi notifications for any additional messages.'.format(addon_name)
        )

        xbmc.log('[Pigeon Build] Addon installation complete: {}'.format(addon_name), xbmc.LOGINFO)

    except Exception as e:
        xbmc.log('[Pigeon Build] Addon installation error: {}'.format(str(e)), xbmc.LOGERROR)
        if 'progress' in locals():
            progress.close()
        gui.show_ok_dialog(
            'Installation Error',
            'Failed to install add-on.\n\nError: {}'.format(str(e))
        )

def apply_advanced_settings(setting_type):
    """Apply advanced settings for device type"""
    from resources.lib import maintenance

    # Confirm application
    confirmed = gui.show_yes_no_dialog(
        'Apply Settings',
        'Apply optimized advanced settings for {}?'.format(setting_type.replace('_', ' ').title())
    )

    if not confirmed:
        return

    # Apply settings using maintenance module
    success = maintenance.apply_advanced_settings(setting_type)

    if success:
        gui.show_notification('Advanced settings applied!', icon=xbmcgui.NOTIFICATION_INFO)

        gui.show_ok_dialog(
            'Settings Applied',
            'Advanced settings have been applied.\n\nRestart Kodi for changes to take effect.'
        )
    else:
        gui.show_ok_dialog(
            'Error',
            'Failed to apply advanced settings.\n\nPlease check the Kodi log for details.'
        )
