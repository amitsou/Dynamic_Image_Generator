"""This module contains the VideoProcessor class for video processing."""

import os
from typing import List

import cv2

from src.utils.file_utils import FileManager


class VideoProcessor:
    """Handles video processing such as frame extraction and playback."""

    """
    The EPIC-KITCHENS dataset uses 60 fps for the RGB frames in their preprocessing pipeline.
    They also compute TV-L1 optical flow at 30 fps. This implies that they extracted frames at
    a high frame rate (one frame every 1/60th of a second for RGB and one frame every 1/30th of
    a second for optical flow) to provide a dense and detailed representation of the videos
    """

    def extract_video_frames(
        self,
        video_dir: List[str],
        output_dir: str,
        fps: int = 60,
        max_frames: int = None,
    ) -> None:
        """
        Extracts frames from videos at a specified frame rate and saves them as images in the output directory.

        Parameters:
        video_dir (List[str]): List of paths to the input video files.
        output_dir (str): Directory where the extracted frames will be saved.
        fps (int): Frame rate for extracting frames (default is 60).
        max_frames (int): Maximum number of frames to extract (optional).
        """
        for video in video_dir:
            FileManager.create_multiple_dirs(output_dir)

            vidcap = cv2.VideoCapture(video)
            input_fps = vidcap.get(cv2.CAP_PROP_FPS)
            total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
            video_duration = total_frames / input_fps

            # Adjust FPS dynamically if max_frames is provided
            if max_frames:
                fps = min(fps, max_frames / video_duration)

            frame_interval = input_fps / fps if fps < input_fps else 1

            success, image = vidcap.read()
            frame_count = 0
            extracted_count = 0

            while success:
                if frame_count % int(frame_interval) == 0:
                    frame_path = os.path.join(
                        output_dir, f"frame{extracted_count:05d}.jpg"
                    )
                    cv2.imwrite(frame_path, image)
                    extracted_count += 1
                    if max_frames and extracted_count >= max_frames:
                        break

                success, image = vidcap.read()
                frame_count += 1

            vidcap.release()
            print(f"Extracted {extracted_count} frames from {video}.")
