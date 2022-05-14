# SpotifyPlaylistSplitter

Often I find huge playlist on Spotify and I want to discover new artists. I made this script so I can split in half these playlists based by the artists I already follow.<br />
It will create 2 playlist taking 1 playlist as an argument:
- 1 playlist called "... Not Followed"
- 1 playlist called "... Followed"

the arguments of this script are:
* -p/--playlist = PlaylistID
* -P/--playlist_names = How the new playlists are going to be named
example:<br />
```
python main.py -p spotify:playlist:2BVkgRFCn2ojOlzugYyRDw -P Primavera
```
The result playlists are:
* Primavera NOT Followed
* Primavera Followed
## Requirements<br />
* you must substitute in main.py the ClietID and the ClientSecret. You can obtain it [here](https://developer.spotify.com/documentation/web-api/quick-start/)
* you have to enable the Redirect URIs(default http://localhost:9999/callback) on the [Spotify Dashboard](https://developer.spotify.com/dashboard/applications)
* install [spotipy](https://github.com/plamere/spotipy)</br>
```
pip install spotipy
```
## Notes <br />
The playlist are NOT overwritten! it will create each time a new playlist with the same name (id you did not change the paramenter playlist_names
