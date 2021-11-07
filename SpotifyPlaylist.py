"""
Python Script to take a Youtube Playlist and either Add to an existing playlist or create a new Spotify Playlist
Step 1. Obtain Youtube playlist
Step 2. Grab videos in playlist
Step 3. Obtain song/artist name from playlist
Step 4. Create a new playlist or obtain an existing playlist
Step 5. Search for songs on Spotify
Step 6. Add song into Spotify
"""
import json
import requests
class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token

    # Log into youtube
    def get_youtube_client(self):
        pass
    
    #Step 1. Obtain Youtube playlist
    def get_youtube_playlist(self):
        pass
    
    #Step 4. Create a new playlist or obtain an existing playlist
    def get_spotify_playlist(self):
        pass


    #Step 4. Create a new playlist 
    def create_spotify_playlist(self):
        #Format Playlist information based on Spotify Playlist requirements
        request_body = json.dumps({
            "name": "Youtube Playlist Video",
            "description": "Youtube Playlist Video",
            "public": True
        })
        #Send HTTP post request using requests library
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data = request_body,
            headers = {
                "Content Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()

        #Get playlist ID that was created
        return response_json["id"]


    #Step 5. Search for songs on Spotify
    def get_spotify_uri(self,track,artist):
        #Send HTTP Get query using requests library
        query = "https://api.spotify.com/v1/search?q=track%3A{}%2Bartist%3A{}&type=track%2Cartist&limit=10&offset=5".format(
            track,
            artist
        )
        response = requests.get(
            query,
            data = request_body,
            headers = {
                "Content Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        #Parse out the songs from the JSON response
        tracks = response_json["tracks"]["items"]
        #Grab first song uri that the query appears (assuming it is the correct one)
        track_uri = songs[0]['uri']

        return track_uri

    #Step 6. Add song into Spotify
    def add_song_to_spotify_playlist(self):
        pass