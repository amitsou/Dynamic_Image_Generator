"""This module contains the DynamicImageGenerator class,
which is responsible for generating dynamic images from video frames.
"""

from utils.image_utils import ImageManager
from typing import Union

import os
import glob
import cv2
import numpy as np


class DynamicImageGenerator:
    """Generates and handles dynamic images from frames."""

    def create_dynamic_images(self, input_dir: str, output_dir: str) -> None:
        """
        Generates dynamic images from video frames and saves them to the specified output directory.
        Args:
            input_dir (str): The directory containing the input video frames.
            output_dir (str): The directory where the generated dynamic images will be saved.
        Returns:
            None
        """
        video_directories = [os.path.dirname(video) for video in input_dir]
        video_directories = sorted(list(set(video_directories)))
        output_dir = sorted(list(set(output_dir)))

        frames = []
        for video_dir, out_dir in zip(video_directories, output_dir):
            file_pattern = os.path.join(video_dir, "**", "*.jpg")
            video_files = glob.glob(file_pattern, recursive=True)

            frames.extend([cv2.imread(f) for f in video_files])
            filename = os.path.basename(video_dir).split("/")[-1]
            filename = f"{filename}.jpg"

            self.save_dynamic_image(frames, out_dir, filename)
            frames.clear()

    def save_dynamic_image(
        self, frames: list, output_directory: str, filename: str
    ) -> None:
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

    def show_dynamic_image(self, frames: Union[list, np.ndarray]) -> None:
        """
        Displays a dynamic image generated from a sequence of frames.
        Args:
            frames (Union[list, numpy.ndarray]):
            A list or array of frames from which the dynamic image will be generated.
            The function uses ImageUtils.get_dynamic_image to generate the dynamic image
            and then displays it using OpenCV's imshow.
            The display window will remain open until a key is pressed or
            the window is closed manually.
        """
        dyn_image = ImageManager.get_dynamic_image(frames, normalized=True)

        cv2.imshow("", dyn_image)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key != 255:
                break
            if cv2.getWindowProperty("", cv2.WND_PROP_VISIBLE) < 1:
                break
        cv2.destroyAllWindows()
