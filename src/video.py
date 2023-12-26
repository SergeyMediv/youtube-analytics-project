import json

from src.apisettings import ApiSettings


class Video(ApiSettings):

    def __init__(self, user_video_id):
        video_id = user_video_id
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id).execute()
        self.video_id = user_video_id
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.video_title

    def printj(self):
        data = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=self.video_id).execute()
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        return self.printj()


class PLVideo(Video):

    def __init__(self, user_video_id, user_playlist_id):
        video_id = user_video_id
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id).execute()
        super().__init__(user_video_id)
        self.playlist_id = user_playlist_id
        self.video_id = user_video_id
        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
