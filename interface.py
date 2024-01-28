import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

default_update_time = 2
reduced_update_time = 10

class ServiceInterface():
    def __init__(self) -> None:
        load_dotenv()
        scope = "user-read-currently-playing user-modify-playback-state user-read-playback-state"

        self.client = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope, open_browser=False))

        self.update_time = default_update_time

        self.current_volume = 50

    def previous(self):
        try:
            self.client.previous_track()
        except spotipy.SpotifyException as e:
            print(e)

    def pause_play(self):
        try:
            if self.get_is_playing():
                self.client.pause_playback()
            else:
                self.client.start_playback()
        except spotipy.SpotifyException as e:
            print(e)

    def next(self):
        try:
            self.client.next_track()
        except spotipy.SpotifyException as e:
            print(e)

    def get_is_playing(self) -> bool:
        playback = self.client.current_playback()
        return playback['is_playing'] if playback != None else False

    def change_volume(self, delta : int) -> None:
        self.current_volume += delta

        # limit the volume between 0 and 100
        self.current_volume = min(100, max(0, self.current_volume))
        
        try:
            self.client.volume(self.current_volume)
        except spotipy.SpotifyException as e:
            print(e)

    def get_info(self) -> dict:
        try:
            playback : dict = self.client.current_playback()

            self.update_time = default_update_time

            return {
                "is_playing" : playback['is_playing'],
                "song_name" : playback['item']['name'],
                "song_duration" : playback['item']['duration_ms'],
                "song_progress" : playback['progress_ms'],
                "artist_names" : [str(i['name']) for i in playback['item']['artists']]
            }

        except:
            self.update_time = reduced_update_time

            return {
                "is_playing" : False,
                "song_name" : "",
                "song_duration" : 1,
                "song_progress" : 1,
                "artist_names" : [""]
            }
