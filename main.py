""" Main script to run the video processing pipeline.
    The modes of operation are:
        - get_frames: Extract frames from videos.
        - get_dyn_img: Create dynamic images from frames.
    In case of a dataset that contains RGB frames,
    the only mode that can be used is 'get_dyn_img'.
    Alternatively, if the dataset contains videos,
    the 'get_frames' mode should be used first to extract the frames
    and then create the dynamic images.
"""

import argparse
import os
import time

from image_generators.dynamic_image_generator import DynamicImageGenerator
from utils.console_utils import ConsoleManager
from utils.execution_utils import ExecutionTimeHandler
from utils.file_utils import FileManager
from video_processing.video_processor import VideoProcessor


def parse_args():
    """
    Parses command-line arguments.
    Returns:
        argparse.Namespace: A namespace object containing the parsed arguments.
            - input (str): Input path directory containing the videos.
            - print (bool): Flag to print messages.
            - mode (str): Mode of operation. Options are 'get_frames' or 'get_dyn_img'.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Input path directory containing the videos"
    )
    parser.add_argument(
        "-p", "--print", help="Flag to print messages", action="store_true"
    )
    parser.add_argument("-m", "--mode", help="Mode: [get_frames, get_dyn_img]")
    return parser.parse_args()


def process_datasets(input_dir: str, mode: str):
    extensions = {
        "get_frames": [".mp4", ".MP4"],
        "get_dyn_img": [".jpg", ".JPG", ".png", ".PNG"],
    }

    if "EPIC-KITCHENS" in input_dir:
        # TODO: Implementation for the EPIC-KITCHENS dataset
        # Structure of the dataset:
        pass

    elif "EGTEA" in input_dir:
        # TODO: Implementation for EGTEA dataset
        # Structure of the dataset:
        pass

    elif "BON" in input_dir:
        subdirs = ["Barcelona", "Nairobi", "Oxford"]
    elif "Charades" in input_dir:
        """
        Due to the reason that RGB frames are provided in the CharadesEgo dataset there is no need for extracting them.
        Thus, the only thing that needs to be done is to create the dynamic images.
        """
        subdirs = ["CharadesEgo_v1_rgb"]
    else:
        raise ValueError(f"Invalid input directory: {input_dir}")

    for subdir in subdirs:
        tmp_dir = "".join((input_dir, subdir))
        videos = FileManager.get_videos(tmp_dir, extensions.get(mode, []))

        if mode == "get_dyn_img" and "BON" in tmp_dir:
            output_dir = list(
                map(
                    lambda video: os.path.dirname(
                        video.replace(
                            "Datasets/Frames", "Datasets/Dynamic_Images"
                        ).replace("/Frames", "")
                    ),
                    videos,
                )
            )
        elif mode == "get_dyn_img" and "Charades" in tmp_dir:
            output_dir = list(
                map(
                    lambda video: os.path.dirname(
                        video.replace("Datasets", "Datasets/Dynamic_Images")
                    ),
                    videos,
                )
            )
        elif mode == "get_frames":
            output_dir = list(
                map(
                    lambda video: os.path.dirname(
                        video.replace("Datasets", "Datasets/Frames")
                    ),
                    videos,
                )
            )

        [
            FileManager.create_multiple_dirs(directory)
            for directory in sorted(list(set(output_dir)))
        ]

        functions = {
            "get_frames": VideoProcessor.extract_video_frames,
            "get_dyn_img": DynamicImageGenerator.create_dynamic_images,
        }
        functions[mode](videos, output_dir)


def main():
    start_time = time.time()
    args = parse_args()

    if args.print:
        ConsoleManager.block_print()

    process_datasets(str(args.input), str(args.mode))
    end_time = time.time()
    ExecutionTimeHandler.calculate_execution_time(start_time, end_time)


if __name__ == "__main__":
    main()
