import os
from googleapiclient.discovery import build


class ApiSettings:
    api_key = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls):
        you_tube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        return you_tube
