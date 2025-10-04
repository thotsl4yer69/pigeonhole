#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pigeon Build Wizard Configuration
User variables and settings for the Pigeon Build wizard
"""

import os

# Addon Information
ADDON_ID = 'plugin.program.pigeonbuild'
ADDON_NAME = 'Pigeon Build Wizard'
ADDON_VERSION = '1.0.2'

# Wizard Settings
WIZARD_NAME = 'Pigeon Build'
WIZARD_SHORT = 'Pigeon'

# Build Information
BUILDFILE = 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/builds.txt'
BUILDTHEME = 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/theme.xml'
NOTIFICATION_FILE = 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/notify.txt'
ADDONFILE = 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/addons.txt'

# Repository Information
REPO_ID = 'repository.pigeonbuild'
REPO_NAME = 'Pigeon Build Repository'
REPO_ZIP_URL = 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/repo/repository.pigeonbuild-1.0.0.zip'

# YouTube Settings
YOUTUBE_CHANNEL_ID = ''  # Add your YouTube channel ID if you have one
YOUTUBE_API_KEY = ''

# Paths
HOME = os.path.expanduser('~')
ADDON_PATH = os.path.join(HOME, '.kodi', 'addons', ADDON_ID)
ADDON_DATA = os.path.join(HOME, '.kodi', 'userdata', 'addon_data', ADDON_ID)
PACKAGES = os.path.join(HOME, '.kodi', 'addons', 'packages')
ADDON_USERDATA = os.path.join(HOME, '.kodi', 'userdata')

# Color Scheme (matching branding)
COLOR_BACKGROUND = '#1a1a1a'
COLOR_PRIMARY = '#7B2CBF'      # Deep purple
COLOR_SECONDARY = '#9D4EDD'    # Mid purple
COLOR_ACCENT = '#10A5B5'       # Cyan
COLOR_TEXT_PRIMARY = '#FFFFFF'
COLOR_TEXT_SECONDARY = '#C77DFF'

# Advanced Settings Templates
ADVANCED_SETTINGS = {
    'firestick_1gb': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/advanced_settings/firestick_1gb.xml',
    'firestick_2gb': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/advanced_settings/firestick_2gb.xml',
    'shield_3gb': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/advanced_settings/shield_3gb.xml',
    'pc_4gb_plus': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/advanced_settings/pc_4gb_plus.xml',
}

# Builds List
# NOTE: Builds are currently placeholders. Create actual build ZIPs and host them
# to enable build installation. For now, users can use individual features like
# advanced settings, maintenance tools, and addon installation.
BUILDS = [
    {
        'name': 'Pigeon Essential (Fire TV Stick)',
        'version': '1.0',
        'url': 'https://github.com/mz1312/pigeonhole/releases/download/v1.0/pigeon-essential-firestick.zip',
        'gui': '',  # Optional: GUI settings XML
        'theme': '',  # Optional: Theme XML
        'icon': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/branding/icon.png',
        'fanart': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/branding/fanart.png',
        'preview': '',  # Optional: YouTube preview
        'adult': False,
        'info': 'Lightweight build optimized for Fire TV Stick with essential streaming add-ons',
        'description': 'The perfect starter build for Fire TV Stick users. Includes The Crew, The Loop, and optimized settings for smooth 1080p streaming.'
    },
    {
        'name': 'Pigeon Pro (Fire TV Stick 4K)',
        'version': '1.0',
        'url': 'https://github.com/mz1312/pigeonhole/releases/download/v1.0/pigeon-pro-firestick4k.zip',
        'gui': '',
        'theme': '',
        'icon': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/branding/icon.png',
        'fanart': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/branding/fanart.png',
        'preview': '',
        'adult': False,
        'info': 'Enhanced build for Fire TV Stick 4K with advanced features',
        'description': 'Full-featured build with The Crew, The Loop, FenLight, Seren, and more. Optimized for 4K streaming with Real-Debrid support.'
    },
    {
        'name': 'Pigeon Ultimate (Shield/PC)',
        'version': '1.0',
        'url': 'https://github.com/mz1312/pigeonhole/releases/download/v1.0/pigeon-ultimate-pc.zip',
        'gui': '',
        'theme': '',
        'icon': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/branding/icon.png',
        'fanart': 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/branding/fanart.png',
        'preview': '',
        'adult': False,
        'info': 'Complete build for Shield TV and PC users',
        'description': 'Everything you need including premium skins, advanced add-ons, Dolby Vision support, and all the bells and whistles.'
    }
]

# Popular Add-on Repositories
# Self-hosted on GitHub - updated daily from official sources
# Base URL for self-hosted repositories
REPO_MIRROR_BASE = 'https://raw.githubusercontent.com/mz1312/pigeonhole/main/kodi-wizard/repo-mirror/repositories'

ADDON_REPOS = {
    'thecrew': {
        'name': 'The Crew Repository',
        'repo_id': 'repository.thecrew',
        'repo_url': f'{REPO_MIRROR_BASE}/repository.thecrew.zip',
        'addon_id': 'plugin.video.thecrew',
        'description': 'The Crew - Extensive content library with reliable sources. Includes: The Chains, The Gears, Jokers Absolution, Genocide, Coalition, Ghost, Homelander, Luffy, Zoro',
        'source': 'http://team-crew.github.io'
    },
    'theloop': {
        'name': 'The Loop Repository',
        'repo_id': 'repository.loop',
        'repo_url': f'{REPO_MIRROR_BASE}/repository.loop.zip',
        'addon_id': 'plugin.video.theloop',
        'description': 'The Loop - Live sports and events streaming',
        'source': 'https://loopaddon.uk'
    },
    'umbrella': {
        'name': 'Umbrella Repository',
        'repo_id': 'repository.umbrella',
        'repo_url': f'{REPO_MIRROR_BASE}/repository.umbrella.zip',
        'addon_id': 'plugin.video.umbrella',
        'description': 'Umbrella - Feature-rich addon with extensive customization',
        'source': 'https://umbrellaplug.github.io'
    },
    'fenlight': {
        'name': 'FenLight',
        'repo_id': 'repository.umbrella',
        'repo_url': f'{REPO_MIRROR_BASE}/repository.umbrella.zip',
        'addon_id': 'plugin.video.fenlight',
        'description': 'FenLight - Lightweight and fast (available through Umbrella repository)',
        'source': 'https://umbrellaplug.github.io'
    },
    'seren': {
        'name': 'Seren Repository',
        'repo_id': 'repository.nixgates',
        'repo_url': f'{REPO_MIRROR_BASE}/repository.nixgates.zip',
        'addon_id': 'plugin.video.seren',
        'description': 'Seren - Premium addon for debrid users with Trakt integration',
        'source': 'https://nixgates.github.io'
    },
    'pov': {
        'name': 'POV Repository',
        'repo_id': 'repository.kodifitzwell',
        'repo_url': f'{REPO_MIRROR_BASE}/repository.kodifitzwell.zip',
        'addon_id': 'plugin.video.pov',
        'description': 'POV (Point of View) - Successor to Ezra, optimized for debrid services',
        'source': 'https://kodiyashimaru.github.io'
    }
}

# Maintenance Settings
EXCLUDES = [
    ADDON_ID,
    REPO_ID,
    'plugin.program.super.favourites',
    'plugin.video.youtube',
    'plugin.program.autowidget'
]

EXCLUDE_TEXT = [
    'script.extendedinfo',
    'script.artwork.beef',
    'context.item.extras'
]

# Notification Messages
NOTIFICATIONS_ENABLED = True
CHECK_NOTIFICATIONS = True

# Wizard Features
ENABLE_LOGINIT = True
ENABLE_KEEPTRAKT = True
ENABLE_KEEPDEBRID = True
ENABLE_KEEPLOGIN = True

# Force Settings
FORCE_CLOSE_KODI = False
FORCE_UPDATE_ADDONS = True
FORCE_UNINSTALL_ON_REINSTALL = False

# Backup Settings
BACKUP_ENABLED = True
KEEP_BACKUPS = 3

# Developer Settings
DEBUG_MODE = False
VERBOSE_LOGGING = False

# Error Handling
HIDE_ERRORS = False
SEND_ERROR_REPORTS = False
