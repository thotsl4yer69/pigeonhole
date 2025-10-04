#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pigeon Build Wizard - GUI Module
Functions for creating and managing GUI elements
"""

import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

try:
    from urllib.parse import quote_plus, urlencode
except ImportError:
    from urllib import quote_plus, urlencode

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
HANDLE = int(sys.argv[1])

def get_icon_path(icon_name):
    """Get full path to icon file"""
    icon_path = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', icon_name)
    if not os.path.exists(icon_path):
        icon_path = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', 'icon.png')
    return icon_path

def get_fanart_path(fanart_name='fanart.png'):
    """Get full path to fanart file"""
    fanart_path = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', fanart_name)
    if not os.path.exists(fanart_path):
        fanart_path = ''
    return fanart_path

def build_url(query):
    """Build plugin URL with query parameters"""
    base_url = sys.argv[0]
    return base_url + '?' + urlencode(query)

def add_dir(name, mode, icon='', fanart='', description='', isFolder=True):
    """Add a directory item to the list"""
    url = build_url({'mode': mode})

    list_item = xbmcgui.ListItem(name)

    # Set icon
    if icon:
        icon_path = get_icon_path(icon)
    else:
        icon_path = get_icon_path('icon.png')

    # Set fanart
    if fanart:
        fanart_path = get_fanart_path(fanart)
    else:
        fanart_path = get_fanart_path()

    list_item.setArt({
        'icon': icon_path,
        'thumb': icon_path,
        'fanart': fanart_path
    })

    # Set info
    if description:
        list_item.setInfo('video', {'plot': description})

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=url,
        listitem=list_item,
        isFolder=isFolder
    )

def add_item(name, mode, url='', icon='', fanart='', description='', params=None):
    """Add a playable/executable item to the list"""
    if params is None:
        params = {}

    params['mode'] = mode
    if url:
        params['url'] = url

    plugin_url = build_url(params)

    list_item = xbmcgui.ListItem(name)

    # Set icon
    if icon:
        icon_path = get_icon_path(icon)
    else:
        icon_path = get_icon_path('icon.png')

    # Set fanart
    if fanart:
        fanart_path = get_fanart_path(fanart)
    else:
        fanart_path = get_fanart_path()

    list_item.setArt({
        'icon': icon_path,
        'thumb': icon_path,
        'fanart': fanart_path
    })

    # Set info
    if description:
        list_item.setInfo('video', {'plot': description})

    xbmcplugin.addDirectoryItem(
        handle=HANDLE,
        url=plugin_url,
        listitem=list_item,
        isFolder=False
    )

def end_of_directory(succeeded=True, update_listing=False, cache_to_disk=True):
    """Signal end of directory listing"""
    xbmcplugin.endOfDirectory(
        HANDLE,
        succeeded=succeeded,
        updateListing=update_listing,
        cacheToDisc=cache_to_disk
    )

def show_text_box(heading, text):
    """Show a text box dialog"""
    dialog = xbmcgui.Dialog()
    dialog.textviewer(heading, text)

def show_notification(message, heading='Pigeon Build', icon='', time=5000, sound=True):
    """Show a notification"""
    if not icon:
        icon = get_icon_path('icon.png')

    xbmcgui.Dialog().notification(
        heading,
        message,
        icon,
        time,
        sound
    )

def show_ok_dialog(heading, message):
    """Show an OK dialog"""
    dialog = xbmcgui.Dialog()
    dialog.ok(heading, message)

def show_yes_no_dialog(heading, message):
    """Show a Yes/No dialog"""
    dialog = xbmcgui.Dialog()
    return dialog.yesno(heading, message)

def show_progress_dialog(heading):
    """Create and return a progress dialog"""
    dialog = xbmcgui.DialogProgress()
    dialog.create(heading)
    return dialog

def select_dialog(heading, options):
    """Show a select dialog and return selected index"""
    dialog = xbmcgui.Dialog()
    return dialog.select(heading, options)
