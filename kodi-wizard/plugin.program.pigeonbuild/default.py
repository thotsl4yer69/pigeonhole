#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pigeon Build Wizard
Main entry point for the wizard addon
"""

import sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

# Import wizard modules
from resources.lib import wizard
from resources.lib import gui
import uservar

# Addon information
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = ADDON.getAddonInfo('path')

def main_menu():
    """Display the main wizard menu"""

    # Create menu items
    menu_items = [
        {
            'name': '[COLOR {}]Install Fresh Build[/COLOR]'.format(uservar.COLOR_ACCENT),
            'mode': 'installbuild',
            'icon': 'install.png',
            'fanart': 'fanart.png',
            'description': 'Install a fresh Pigeon Build on your device'
        },
        {
            'name': '[COLOR {}]Install Add-ons[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY),
            'mode': 'installaddon',
            'icon': 'addons.png',
            'fanart': 'fanart.png',
            'description': 'Install individual add-ons from Pigeon repository'
        },
        {
            'name': '[COLOR {}]Advanced Settings[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY),
            'mode': 'advanced',
            'icon': 'settings.png',
            'fanart': 'fanart.png',
            'description': 'Apply optimized advanced settings for your device'
        },
        {
            'name': '[COLOR {}]Maintenance[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY),
            'mode': 'maintenance',
            'icon': 'maintenance.png',
            'fanart': 'fanart.png',
            'description': 'Clear cache, packages, and optimize Kodi'
        },
        {
            'name': '[COLOR {}]Backup & Restore[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY),
            'mode': 'backup',
            'icon': 'backup.png',
            'fanart': 'fanart.png',
            'description': 'Backup your Kodi settings or restore from backup'
        },
        {
            'name': '[COLOR {}]Contact/Support[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY),
            'mode': 'support',
            'icon': 'support.png',
            'fanart': 'fanart.png',
            'description': 'Get help and support for Pigeon Build'
        },
        {
            'name': '[COLOR {}]Settings[/COLOR]'.format(uservar.COLOR_TEXT_SECONDARY),
            'mode': 'settings',
            'icon': 'icon.png',
            'fanart': 'fanart.png',
            'description': 'Configure wizard settings'
        }
    ]

    for item in menu_items:
        gui.add_dir(item['name'], item['mode'], item['icon'], item['fanart'], item['description'])

    gui.end_of_directory()

def router(paramstring):
    """Route to the appropriate function based on the provided paramstring"""
    params = dict(parse_qsl(paramstring))

    if not params:
        # No params, show main menu
        main_menu()
    else:
        mode = params.get('mode', '')

        if mode == 'installbuild':
            wizard.show_builds()
        elif mode == 'installaddon':
            wizard.show_addons()
        elif mode == 'advanced':
            wizard.show_advanced_settings()
        elif mode == 'maintenance':
            wizard.show_maintenance()
        elif mode == 'backup':
            wizard.show_backup()
        elif mode == 'support':
            wizard.show_support()
        elif mode == 'settings':
            ADDON.openSettings()
        elif mode == 'dobuild':
            wizard.install_build(params.get('name', ''))
        elif mode == 'doaddon':
            wizard.install_addon(params.get('addon_key', ''))
        elif mode == 'doadvanced':
            wizard.apply_advanced_settings(params.get('type', ''))
        elif mode == 'domaintenance':
            wizard.do_maintenance(params.get('action', ''))
        elif mode == 'dobackup':
            wizard.do_backup(params.get('action', ''))
        else:
            xbmcgui.Dialog().notification(
                uservar.ADDON_NAME,
                'Unknown action: {}'.format(mode),
                xbmcgui.NOTIFICATION_ERROR
            )

if __name__ == '__main__':
    # Log startup
    xbmc.log('[{}] Version {} started'.format(ADDON_NAME, ADDON_VERSION), xbmc.LOGINFO)

    # Check for first run
    if ADDON.getSetting('firstrun') != 'true':
        wizard.first_run()
        ADDON.setSetting('firstrun', 'true')

    # Route to appropriate function
    router(sys.argv[2][1:])
