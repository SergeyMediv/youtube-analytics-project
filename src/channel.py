import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

from src.apisettings import ApiSettings


class Channel(ApiSettings):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.view_count = channel['items'][0]['statistics']['viewCount']
        self.description = channel['items'][0]['snippet']['description']
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        return self.printj()

    def printj(self):
        data = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        channel_data = {"channel_id": self.__channel_id,
                        "title": self.title,
                        "description": self.description,
                        "ulr": self.url,
                        "subscriber_count": self.subscriber_count,
                        "video_count": self.video_count,
                        "view_count": self.view_count}
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_data, file, indent=4, ensure_ascii=False)

    @property
    def channel_id(self):
        return self.__channel_id
