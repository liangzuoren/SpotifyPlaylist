"""
Python Script to take a Youtube Playlist and either Add to an existing playlist or create a new Spotify Playlist
Step 1. Obtain Youtube playlist
Step 2. Create a new playlist or obtain an existing playlist
Step 3. Search for songs on Spotify
Step 4. Add song into Spotify
"""
import json
import requests
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl
from pick import pick

class CreatePlaylist:

    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = spotify_token
        self.song_info = {}
        self.key = API_KEY

    #Step 1. Grab video information from passed in Youtube Playlist ID and Create Dictionary of Song/Artist information
    def get_youtube_playlist(self, playlist_id):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        #From Youtube Data API
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

        request = youtube.playlists().list(
            part = "id,snippet,contentDetails",
            id = playlist_id
        )
        response = request.execute()

        #Grab title and url
        for item in response["items"]:
            title = item["snippet"]["title"]
            url = "https://www.youtube.com/watch?v={}".format(item["id"])

            #Use youtube_dl to get song name and artist name
            info = youtube_dl.YoutubeDL.extract_info(url,download=False)

            track = info["track"]
            artist = info["artist"]

            self.song_info[title] = {
                "url":url,
                "track":title,
                "artist":artist,
                "spotify_uri":self.get_spotify_uri(track,artist)
            }

        return response
    
    
    #Step 2. Obtain an existing playlist (Perhaps redundant)
    def get_spotify_playlist(self,playlist_id):
        #Send HTTP Get query using requets library
        query = "https://api.spotify.com/v1/playlists/{}".format(
            playlist_id
        )
        response = requests.get(
            query,
            headers = {
                "Content Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        return response_json["id"]

    #Step 2. Create a new playlist 
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
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()

        #Get playlist ID that was created
        return response_json["id"]


    #Step 3. Search for songs on Spotify
    def get_spotify_uri(self,track,artist):
        #Send HTTP Get query using requests library
        query = "https://api.spotify.com/v1/search?q=track%3A{}%2Bartist%3A{}&type=track%2Cartist&limit=10&offset=5".format(
            track,
            artist
        )
        response = requests.get(
            query,
            headers = {
                "Content Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        #Parse out the songs from the JSON response
        tracks = response_json["tracks"]["items"]
        #Grab first song uri that the query appears (assuming it is the correct one)
        track_uri = songs[0]['uri']

        return track_uri

    #Step 4. Add song into Spotify playlist
    def add_songs_to_spotify_playlist(self,playlist_id):
        uris = []
        for song,info in self.song_info.items():
            uris.append(info["spotify_uri"])

        request_body = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        response = requests.post(
            query,
            data = request_body,
            headers = {
                "Content Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()

        return response_json

    #Main function to run program
    def main():
        youtube_playlist_id = input("Enter Your Youtube Playlist ID: ")
        
        title = "Add to existing playlist or Create new playlist?"
        options = ['Add to existing playlist','Create new playlist']
        option,index = pick(options,title)

        #Option 1: Add to existing playlist
        if index == 0:
            spotify_playlist_id = input("Enter Your existing Spotify Playlist ID: ")

        #Option 2: Create new playlist
        if index == 1:
            spotify_playlist_id = create_spotify_playlist()

        get_youtube_playlist(youtube_playlist_id)
        add_songs_to_spotify_playlist(spotify_playlist_id)

        output = "Successfully added songs to Spotify playlist {} from Youtube playlist {}".format(spotify_playlist_id,youtube_playlist_id)
        print(output)
        
if __name__ == "__main__":
    main()