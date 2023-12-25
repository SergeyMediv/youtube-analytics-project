import json
import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        you_tube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        return you_tube

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        pl_info = self.get_service().playlists().list(id=playlist_id, part='snippet,contentDetails',
                                                      maxResults=50).execute()
        self.title = pl_info['items'][0]['snippet']['title']

    @property
    def total_duration(self):
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)).execute()
        total_seconds = timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_seconds += duration

        return total_seconds

    def show_best_video(self):
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)).execute()
        top_like = 0
        top_video = None
        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > top_like:
                top_like = int(video['statistics']['likeCount'])
                top_video = video['id']

        return f'https://youtu.be/{top_video}'

    def print_res(self):
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)).execute()

        for video in video_response['items']:
            print(video['id'])

    def printj(self):
        data = self.playlist_videos
        print(json.dumps(data, indent=2, ensure_ascii=False))
