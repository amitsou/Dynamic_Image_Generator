"""This module contains the DynamicImageGenerator class,
which is responsible for generating dynamic images from video frames.
"""

import sys
import os
import random
from collections import defaultdict

import cv2

from src.utils.file_utils import FileManager
from src.utils.image_utils import ImageManager


class DynamicImageGenerator:
    """Generates and handles dynamic images from frames."""

    @staticmethod
    def create_dynamic_images(
        input_dir: str,
        output_dir: str,
        max_samples: int,
        file_extentions: list
    ) -> None:
        """
        Generates dynamic images from video frames and saves them to the specified output directory.
        Args:
            input_dir (str): The directory containing the input video frames.
            output_dir (str): The directory where the generated dynamic images will be saved.
        Returns:
            None
        """
        frame_dirs = FileManager.media_path_crawler(input_dir,[],file_extentions)
        frame_dirs = sorted(list(set(frame_dirs)))

        groupped_frame_dirs = defaultdict(list)
        for frame_path in frame_dirs:
            directory = os.path.dirname(frame_path)
            groupped_frame_dirs[directory].append(frame_path)
        groupped_frame_dirs = dict(groupped_frame_dirs)

        for input_dir, frame_dirs in groupped_frame_dirs.items():
            output_dir = input_dir.replace("frames", "dynamic_images")
            FileManager.create_multiple_dirs(output_dir)

            sampled_frame_dirs = DynamicImageGenerator.stratified_sample_frames(
                sorted(frame_dirs),
                max_samples
            )

            print(f"Processing directory: {input_dir} with {len(frame_dirs)} frames.")
            print(
                f"Sampled {len(sampled_frame_dirs)} frames from {len(frame_dirs)} available."
            )

            frames = [
                cv2.imread(frame_path)
                for frame_path in sampled_frame_dirs
                if cv2.imread(frame_path) is not None
            ]
            if not frames:
                print(f"No valid frames found in {input_dir}")
                continue

            output_filename = os.path.basename(input_dir) + ".jpg"
            try:
                DynamicImageGenerator.save_dynamic_image(
                    frames, output_dir, output_filename
                )
                print(
                    f"Dynamic image saved to {os.path.join(output_dir, output_filename)} \n"
                )
            except Exception as e:
                print(f"Failed to create dynamic image for {input_dir}: {e}")
            frames.clear()

    @staticmethod
    def stratified_sample_frames(frame_paths: list, max_samples: int = 100) -> list:
        """
        Randomly samples frames from the start, middle, and end of the video frames.
        Args:
            frame_paths (list): List of absolute paths to the frames.
            max_samples (int): Maximum number of frames to sample.
        Returns:
            list: A stratified sampled subset of frame paths.
        """
        num_frames = len(frame_paths)
        if num_frames <= max_samples:
            return frame_paths

        """
        Split the frames into three segments
        Start, middle, and end
        Because the frames depcit a human action
        """
        third = num_frames // 3
        start_frames = frame_paths[:third]
        middle_frames = frame_paths[third : 2 * third]
        end_frames = frame_paths[2 * third :]
        samples_per_segment = (
            max_samples // 3
        )  # Calc. how many samples to get from each segment

        try:
            sampled_frames = (  # Randomly sample from each segment
                random.sample(start_frames, min(len(start_frames), samples_per_segment))
                + random.sample(
                    middle_frames, min(len(middle_frames), samples_per_segment)
                )
                + random.sample(end_frames, min(len(end_frames), samples_per_segment))
            )
        except ValueError:
            raise ValueError("Cannot sample from empty frame segments.")
        return sampled_frames

    @staticmethod
    def save_dynamic_image(frames: list, output_directory: str, filename: str) -> None:
        """
        Generates and saves a dynamic image from a list of frames.
        Args:
            frames (list):
            A list of frames (images) to generate the dynamic image from.
            output_directory (str):
            The directory where the dynamic image will be saved.
            filename (str):
            The name of the file to save the dynamic image as.
        Returns:
            None
        """
        dyn_image = ImageManager.get_dynamic_image(frames, normalized=True)
        output_path = os.path.join(output_directory, filename)

        if not os.path.exists(output_path):
            cv2.imwrite(output_path, dyn_image)
