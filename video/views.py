import os
from datetime import datetime

from django.conf import settings
from django.http import FileResponse, Http404
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

videos_path = os.path.join(settings.MEDIA_ROOT, "videos")
if not os.path.exists(videos_path):
    os.makedirs(videos_path)


class VideoView(APIView):
    def get(self, request):
        videos = []
        for filename in os.listdir(videos_path):
            if filename.endswith(".mp4"):
                path = os.path.join(videos_path, filename)
                videos.append(
                    {
                        "name": filename,
                        "created_at": datetime.fromtimestamp(os.path.getctime(path)),
                    }
                )
        return Response(videos)

    def post(self, request):
        video_file = request.FILES.get("file")
        if not video_file:
            return Response(
                {"message": "No file provided in the request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        save_path = os.path.join(videos_path, video_file.name)
        with open(save_path, "wb+") as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        return Response(status=status.HTTP_201_CREATED)


class DeleteVideoView(APIView):
    def delete(self, request, filename):
        video_path = os.path.join(settings.MEDIA_ROOT, "videos", filename)
        if os.path.exists(video_path):
            os.remove(video_path)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class StreamVideoView(View):
    def get(self, request, filename):
        video_path = os.path.join(videos_path, filename)
        if not os.path.isfile(video_path):
            raise Http404("Video does not exist")

        video_file = open(video_path, "rb")
        file_size = os.path.getsize(video_path)
        response = FileResponse(video_file)
        range_header = request.headers.get("Range")

        if range_header:
            parts = range_header.replace("bytes=", "").split("-")
            start = int(parts[0])
            end = int(parts[1]) if parts[1] else file_size - 1
            content_length = end - start + 1

            response.status_code = 206
            response["Content-Length"] = str(content_length)
            response["Content-Range"] = f"bytes {start}-{end}/{file_size}"
            video_file.seek(start)
            response.streaming_content = (chunk for chunk in iter(lambda: video_file.read(4096), b""))

        response["Accept-Ranges"] = "bytes"
        return response
