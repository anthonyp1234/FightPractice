# -*- coding: utf-8 -*-
 
import sys
from urllib import urlencode

from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import random
import re
import os
#from os import listdir
#from os.path import isfile, join

##Insecure HTTPS requests
import urllib3
urllib3.disable_warnings()


##Extra imports for getting random vid from youtube playlist
from bs4 import BeautifulSoup
import requests


media_directory = "/media/storage/fight_practice/"

####
##Change this to different directory
media_file = 'special://media/storage/fight_practice/background.jpg'


# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])


###method for getting a random youtube vid from playlist
def getPlaylistVid(url):
    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    domain = 'https://www.youtube.com'
    playlist = []
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            #print(link.string.strip())
            playlist.append(domain + href)
            
    pattern = "(https://www.youtube.com/watch\?v\=.+?)&"

    try:
        choice = re.search(pattern,random.choice(playlist)).group(1)
    except:
        choice = "EMpty"
        
    return choice





directories = [dir for dir in os.listdir(media_directory) if os.path.isdir(os.path.join(media_directory, dir))]
###Create structure of Videos
VIDEOS = {}
for directory in directories:
    VIDEOS[directory] = []
    ##Grab files in the directory
    for file in os.listdir(media_directory + directory):
        if not file.endswith("txt"):
            #print(media_directory + directory + file)
            VIDEOS[directory].append({"video": media_directory + directory + "/" + file })
        else:
            ##else it's a text file containing youtube uri's, put them into the list instead
            with open(media_directory + directory + "/" + file) as f:
                content = f.readlines()

                
            [VIDEOS[directory].append({"video":x.strip()}) for x in content]   
            ##[VIDEOS[directory].append(x.strip()) for x in content]  Previously, forgot the dict
            
            #dialog = xbmcgui.Dialog()
            #dialog.notification('Value is:', VIDEOS[directory][-1]["video"], xbmcgui.NOTIFICATION_INFO, 15000)
            
            

def get_youtube_url(action, video_url):

    try:
        videoid = re.search("""v\=(.*)$""",video_url).group(1)
    except:
        videoid = ""
        xbmc.log('Could not find video ID in: {0}'.format(video_url),level=xbmc.LOGERROR)
        
        
    return '{0}?{1}'.format(_url, urlencode({'action': action, 'videoid': videoid}))
    
    #string = """plugin://plugin.video.youtube/?action=play_video&videoid={0}""".format(videoid)
    #string = """plugin://plugin.video.youtube/play/?video_id={0}""".format(videoid)

    


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def get_categories():
    return VIDEOS.iterkeys()


def get_videos(category):

    return VIDEOS[category]


def list_categories():
    """
    Create the list of video categories in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(_handle, 'Practice Spar, BJJ or Stretch')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(_handle, 'videos')
    
    xbmcplugin.setPluginFanart(_handle, media_file, color2='0xFFFF3300')
    
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use the same image for all items for simplicity's sake.
        # In a real-life plugin you need to set each image accordingly.
        try:
            list_item.setArt({'thumb': media_directory + category + ".jpg",
                              'icon': media_directory + category + ".jpg",
                              'fanart': media_directory + category + ".jpg",
                              'banner': media_directory + category + ".jpg",
                              'poster': media_directory + category + ".jpg",
                              'clearart': media_directory + category + ".jpg",
                              'clearlogo': media_directory + category + ".jpg",
                              'landscape': media_directory + category + ".jpg"
                              })
        except:
            dialog = xbmcgui.Dialog()
            dialog.notification('Error', "Could not assign Thumb/icon/fanart. Check files in dir. Should be jpg", xbmcgui.NOTIFICATION_INFO, 15000)
        # Set additional info for the list item.
        # Here we use a category name for both properties for for simplicity's sake.
        # setInfo allows to set various information for an item.
        # For available properties see the following link:
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        
        
        chosen_video = VIDEOS[category][random.randint(0,len(VIDEOS[category])-1)]['video']
        
        
        ##Check to see if it's a Youtube playlist, if so select one video out of the playlist
        
        if "playlist" in chosen_video:
            chosen_video = getPlaylistVid(chosen_video)
        
        if "youtube" in chosen_video:         
            url = get_youtube_url(action='playyoutube', video_url=chosen_video)
            
        else:
            url = get_url(action='play', video=chosen_video)

        is_folder = False #do not open as a sub level
        # Add our item to the Kodi virtual folder listing.
        
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        
        
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    #dialog = xbmcgui.Dialog()
    #dialog.notification('The path is', path, xbmcgui.NOTIFICATION_INFO, 15000)
    
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    #xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

    xbmc.Player().play(path, play_item)


def play_youtube_video(video_id):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    string = """plugin://plugin.video.youtube/play/?video_id={0}""".format(video_id)
    
    xbmc.executebuiltin('PlayMedia({0})'.format(string))
    
    #play_item = xbmcgui.ListItem(path=path)
    #xbmc.Player().play(path, play_item)
    #pass
    #xbmc.executebuiltin('PlayMedia({0})'.format(path))
    
    
    
def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str 
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:

        
        if params['action'] == 'listing':
            #pass
            # Display the list of videos in a provided category.
            play_video(params['video'])

        elif params['action'] == 'play':
        # Play a video from a provided URL.
            play_video(params['video'])
            
        elif params['action'] == 'playyoutube':
            play_youtube_video(params['videoid'])
            #dialog = xbmcgui.Dialog()
            #dialog.notification('Youtube_play_video', paramstring, xbmcgui.NOTIFICATION_INFO, 60000)
            

        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_categories()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])

