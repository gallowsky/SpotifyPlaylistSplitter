import spotipy
import math
import argparse
from spotipy.oauth2 import SpotifyOAuth
from collections import OrderedDict

def callAPI(scope):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENTID",
                                                   client_secret="YOUR_SECRET",
                                                   redirect_uri="http://localhost:9999/callback",
                                                   scope=scope))

    return sp

def convertToArtistList(dict):

    temp = []

    for artist in dict:
        temp.append(artist['name'])
    return temp

def createPlaylist(playlistName, userArtistList, playlistTracks):
    sp = callAPI("playlist-modify-public")
    userId = sp.me()['id']
    response = sp.user_playlist_create(userId, playlistName)
    playlistId = response['id']
    trackIds = []
    for i in range(len(playlistTracks)):
        playlistArtists = convertToArtistList(playlistTracks[i]['track']['artists'])
        compare = list(set(playlistArtists) & set(userArtistList))
        if compare:
            trackIds.append(playlistTracks[i]['track']['id'])

    totalCicles = int(math.ceil((len(trackIds) / 100)))

    for j in range(totalCicles):
        x = j * 100
        if x == 0:
            sp.playlist_add_items(playlistId, trackIds[x:99], position=None)
        elif x == (totalCicles - 100):
            x = x - 100
            z = (len(trackIds)) - 1
            sp.playlist_add_items(playlistId, trackIds[x:z], position=None)
            z = 0
        else:
            z = x + 100 - 1
            sp.playlist_add_items(playlistId, trackIds[x:z], position=None)
            z = 0

    print("Playlist " + playlistName + " is created!")
    return

def getSingularArtistList(trackList):

    playlistArtists = []

    for i in range(len(trackList)):
        artist = trackList[i]['track']['artists']
        if len(artist) > 1:
            for j in range(len(artist)):
                playlistArtists.append(artist[j])
        else:
            playlistArtists.append(artist[0])

    return playlistArtists

def getUserFollowedArtists():
    sp = callAPI("user-follow-read")
    id = ''
    userArtists = []
    while True:

        if id:
            response = sp.current_user_followed_artists(limit=1,after=id)
        else:
            response = sp.current_user_followed_artists(limit=1)
        total = response['artists']['total']
        name = response['artists']['items'][0]['name']
        id = response['artists']['items'][0]['id']
        userArtists.append(name)
        if total == (len(userArtists)-1):
            break

    return userArtists

def getPlaylistTracks(playlistId):
    sp = callAPI("playlist-read-private")
    offset = 0
    playlistTracks = OrderedDict()
    playlistTracks['item'] = []
    while True:

        response = sp.playlist_items(playlistId,
                                     offset=offset,
                                     fields='items.track.id,items.track.artists.name,total',
                                     additional_types=['track'])

        if len(response['items']) == 0:
            break

        offset = offset + len(response['items'])
        playlistTracks['item'] += response['items']

    return playlistTracks['item']

def getArgs():
    parser = argparse.ArgumentParser(description='Split playlist')
    parser.add_argument('-p', '--playlist', required=True,
                        help='Name of Playlist to analyze')
    parser.add_argument('-P', '--playlist_names', required=True,
                        help='Base name for the new playlist that will be created')
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()

    tracksOnPlaylist = getPlaylistTracks(args.playlist)
    artistsOnPlaylist = getSingularArtistList(tracksOnPlaylist)
    artistsTempList = convertToArtistList(artistsOnPlaylist)
    artistsUniqueOnPlaylist = list(set(artistsTempList))

    userArtists = getUserFollowedArtists()
    artistFollowedInPlaylist = (set(userArtists) & set(artistsUniqueOnPlaylist))
    artistNOTFollowedInPlaylist = (set(artistFollowedInPlaylist) ^ set(artistsUniqueOnPlaylist))

    createPlaylist(args.playlist_names + ' NOT Followed', artistNOTFollowedInPlaylist, tracksOnPlaylist)
    createPlaylist(args.playlist_names + ' Followed', artistFollowedInPlaylist, tracksOnPlaylist)

