from gmusicapi import Mobileclient

global library

api = Mobileclient()
#login to the client, must enter your own gmail address/password below and enable "Access for less secure apps" in your gmail settings
api.login('user@gmail.com', 'password')
#obtain a listing of all songs in the current library
library = api.get_all_songs()

def getLibrary():
    '''Returns a dictionary list of all songs saved to the Google music account.'''
    library = api.get_all_songs()
    return library

def searchLibrary(searchTerm):
    '''Searches the library for artist names matching the input'''
    track_ids = list()
    for track in library:
        if track['artist'].upper() == searchTerm.upper():
            track_ids.append(track)
    return track_ids

def getPlaylists():
    '''Gets a listing of all available saved playlists and their track contents'''
    playlist = api.get_all_user_playlist_contents()
    return playlist

def savePlaylist(playList, name):
    '''Saves the passed playlist as the passed name.'''
    #create the new empty playlist with the passed name
    playlist_id = api.create_playlist(name)
    #create a list filled with the song ID's that are in the passed playlist
    songList = [track['id'] for track in playList]
    #add songs to the new playlist being saved
    api.add_songs_to_playlist(playlist_id, songList)