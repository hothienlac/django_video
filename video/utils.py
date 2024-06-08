from datetime import datetime
import os
from django.conf import settings
from django.http import Http404

videos_path = os.path.join(settings.MEDIA_ROOT, "videos")


def list_videos():
    videos = []
    for filename in os.listdir(videos_path):
        if not filename.endswith(".mp4"):
            continue
        path = os.path.join(videos_path, filename)
        videos.append(
            {
                "name": filename,
                "created_at": datetime.fromtimestamp(os.path.getctime(path)),  # Getting creation time
            }
        )
    return videos


def get_video(video_name):
    video_path = os.path.join(videos_path, video_name)
    if not os.path.isfile(video_path):
        raise Http404("Video does not exist")

    video_file = open(video_path, "rb")
    file_size = os.path.getsize(video_path)
    return video_file, file_size
