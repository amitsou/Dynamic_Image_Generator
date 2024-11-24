"""This module contains the VideoProcessor class for video processing."""

from typing import Tuple
from utils.utils import create_multiple_dirs

import os
import cv2
import datetime


class VideoProcessor:
    """Handles video processing such as frame extraction and playback."""

    def extract_video_frames(self, video_dir: str, output_dir: str) -> None:
        """
        Extracts frames from videos and saves them as images in the specified output directory.
        Parameters:
        video_dir (str): Directory containing the input video files.
        output_dir (str): Directory where the extracted frames will be saved.
        The function processes each video in the video_dir, determines the maximum duration among all videos,
        and adjusts the frame extraction rate based on the duration. Frames are saved as JPEG images in the
        corresponding subdirectory within the output_dir.
        The extraction rate is set to:
        - 1 frame per second if the maximum video duration is greater than 10 seconds.
        - 1 frame per second divided by the maximum duration if the maximum video duration is less than 2 seconds.
        - 1 frame every 0.5 seconds otherwise.
        The function creates necessary directories for saving frames and ensures no frame is overwritten.
        """
        seconds = []
        for video in video_dir:
            _, sec = self.get_video_duration(video)
            seconds.append(sec)
        max_duration = max(seconds)
        del seconds

        for video, out_dir in zip(video_dir, output_dir):
            filename = os.path.basename(video).split(".")[0]
            out_dir = "/".join((out_dir, filename))
            create_multiple_dirs(out_dir)

            vidcap = cv2.VideoCapture(video)
            frame_rate = vidcap.get(cv2.CAP_PROP_FPS)
            extraction_rate = 0.5

            if max_duration > 10:
                extraction_rate = 1
            elif max_duration < 2:
                extraction_rate = 1 / max_duration

            success, image = vidcap.read()
            count = 0
            time_elapsed = 0

            while success:
                if time_elapsed >= extraction_rate:
                    frame_path = os.path.join(out_dir, f"frame{count}.jpg")

                    if not os.path.exists(frame_path):
                        cv2.imwrite(frame_path, image)
                    time_elapsed = 0

                success, image = vidcap.read()
                count += 1
                time_elapsed += 1 / frame_rate
            vidcap.release()

    @staticmethod
    def get_video_duration(self, video_path: str) -> Tuple[datetime.timedelta, int]:
        """
        Calculate the duration of a video.
        Args:
            video_path (str): The path to the video file.
        Returns:
            tuple: A tuple containing:
                - video_time (datetime.timedelta): The duration of the video as a timedelta object.
                - seconds (int): The duration of the video in seconds.
        """
        data = cv2.VideoCapture(video_path)
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = data.get(cv2.CAP_PROP_FPS)
        seconds = round(frames / fps)
        video_time = datetime.timedelta(seconds=seconds)
        return video_time, seconds
