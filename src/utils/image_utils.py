"""Utility functions related to image manipulation."""

from typing import List

import cv2
import numpy as np
from numba import njit

class ImageManager:
    """Utility functions related to image manipulation."""

    @staticmethod
    def get_dynamic_image(frames: list[np.ndarray], normalized=True) -> np.ndarray:
        """
        Generate a dynamic image from a sequence of frames.
        A dynamic image is a single image that summarizes the motion information
        contained in a sequence of frames.
        Args:
            frames (list of numpy.ndarray): A list of frames (images) from which to compute the dynamic image.
            normalized (bool, optional): Whether to normalize the resulting dynamic image to the range [0, 255].
                                         Defaults to True.
        Returns:
            numpy.ndarray: The computed dynamic image.
        """
        num_channels = frames[0].shape[2]
        channel_frames = ImageManager.get_channel_frames(frames, num_channels)
        channel_dynamic_images = [
            ImageManager.compute_dynamic_image(channel) for channel in channel_frames
        ]
        dynamic_image = cv2.merge(tuple(channel_dynamic_images))
        if normalized:
            dynamic_image = cv2.normalize(
                dynamic_image, None, 0, 255, norm_type=cv2.NORM_MINMAX
            )
            dynamic_image = dynamic_image.astype("uint8")
        return dynamic_image

    @staticmethod
    def get_channel_frames(iter_frames: iter, num_channels: int) -> List[np.ndarray]:
        """
        Splits each frame in the iterable into its respective channels (for example RGB channels) and groups them.
        Args:
            iter_frames (iterable): An iterable of frames, where each frame is a multi-channel image.
            num_channels (int): The number of channels in each frame.
        Returns:
            list: A list of numpy arrays, where each array contains the frames for a specific channel.
        """
        frames = [[] for _ in range(num_channels)]
        for frame in iter_frames:
            for channel_frames, channel in zip(frames, cv2.split(frame)):
                channel_frames.append(channel.reshape((*channel.shape[0:2], 1)))
        return [np.array(channel_frames) for channel_frames in frames]

    #TODO: Test this function using numba
    @njit
    @staticmethod
    def compute_dynamic_image(frames: np.ndarray) -> np.ndarray:
        """
        Compute a dynamic image from a sequence of frames.
        A dynamic image is a single image that summarizes the motion information
        contained in a sequence of frames. This function computes the dynamic image
        by applying a set of coefficients to the frames and summing the result.
        Args:
            frames (numpy.ndarray): A 4D numpy array of shape (num_frames, height, width, channels)
                                    representing the sequence of frames.
        Returns:
            numpy.ndarray: A 3D numpy array of shape (height, width, channels) representing
                           the computed dynamic image.
        """
        num_frames, _, _, _ = frames.shape

        # Compute the coefficients for the frames.
        coefficients = np.zeros(num_frames)
        for n in range(num_frames):
            cumulative_indices = np.array(range(n, num_frames)) + 1
            coefficients[n] = np.sum(
                ((2 * cumulative_indices) - num_frames) / cumulative_indices
            )

        # Multiply by the frames by the coefficients and sum the result.
        x1 = np.expand_dims(frames, axis=0)
        x2 = np.reshape(coefficients, (num_frames, 1, 1, 1))
        result = x1 * x2
        return np.sum(result[0], axis=0).squeeze()
