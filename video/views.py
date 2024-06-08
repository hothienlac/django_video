import os
import re
from django.http import FileResponse, Http404, HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django_video import settings
from .utils import list_videos, get_video
from django.core.files.storage import default_storage


class VideoView(APIView):
    def get(self, request):
        videos = list_videos()
        return Response(videos)

    def post(self, request):
        # This line fetches the uploaded file from the multipart form data
        video_file = request.FILES.get("file")
        if video_file:
            # Prepare the directory and path where files will be saved
            videos_path = os.path.join(settings.MEDIA_ROOT, "videos")
            if not os.path.exists(videos_path):
                os.makedirs(videos_path)  # Create the directory if it does not exist

            save_path = os.path.join(videos_path, video_file.name)
            # Save the file
            with open(save_path, "wb+") as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VideoDetail(APIView):
    def get(self, request, filename):
        video = get_video(filename)
        if video:
            return Response(video)
        return Response(status=status.HTTP_404_NOT_FOUND)


class StreamVideoView(View):
    def get(self, request, filename):
        # Define the path to your video files
        video_file, file_size = get_video(filename)

        # Set up the response as a streaming response
        response = FileResponse(video_file)

        # Get the 'Range' header from the request
        range_header = request.headers.get("Range")

        if range_header:
            # Parse the range header to get the byte range
            parts = range_header.replace("bytes=", "").split("-")
            start = int(parts[0])
            end = int(parts[1]) if parts[1] else file_size - 1

            # Calculate the content length
            content_length = end - start + 1

            # Set the appropriate headers for range fetching
            response.status_code = 206  # Partial Content
            response["Content-Length"] = str(content_length)
            response["Content-Range"] = f"bytes {start}-{end}/{file_size}"

            # Stream the specific range of the video
            video_file.seek(start)
            response.streaming_content = (chunk for chunk in iter(lambda: video_file.read(4096), b""))

        # Additional headers for proper streaming
        response["Accept-Ranges"] = "bytes"
        return response
