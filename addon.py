import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import fetchchannel

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

channel = fetchchannel.fetchChannel()

for item in channel['items']:
    li = xbmcgui.ListItem(item['title'], iconImage=item['thumbnail'])
    xbmcplugin.addDirectoryItem(handle=addon_handle, 
                                url=item['url'], 
                                listitem=li)
xbmcplugin.endOfDirectory(addon_handle)
    
