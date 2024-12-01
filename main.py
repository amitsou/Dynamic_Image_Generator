"""
This script is used to extract frames from videos and create dynamic images from frames.
"""

import sys
import argparse
import os

from src.image_generators.dynamic_image_generator import DynamicImageGenerator
from src.utils.console_utils import ConsoleManager
from src.utils.execution_utils import ExecutionTimeHandler
from src.utils.file_utils import FileManager
from src.video_processing.video_processor import VideoProcessor


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Video processing pipeline.")
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input directory."
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory."
    )
    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        choices=["frames", "dynamic","pre_extracted_frames"],
        help="Mode of operation.",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        required=True,
        help="Dataset name (e.g., 'EPIC_KITCHENS', 'EGTEA').",
    )
    parser.add_argument(
        "-fps",
        "--frame_rate",
        type=int,
        help="Frame rate for extracting frames (required for 'frames' mode).",
    )
    parser.add_argument(
        "-b", "--block_console_msg", action="store_true", help="Block console messages."
    )
    return parser.parse_args()

def process_frames(
    input_dir: str,
    output_dir: str,
    frame_rate: int,
    extensions: list
) -> None:
    """Extracts frames from videos."""
    videos = FileManager.media_path_crawler(input_dir,[],extensions)
    video_processor = VideoProcessor()

    for video_path in videos:
        destination_dir = video_path.replace(input_dir, output_dir).split(".")[0]
        FileManager.create_multiple_dirs(destination_dir)
        video_processor.extract_video_frames([video_path], destination_dir, fps=frame_rate)

def process_dynamic_images(
    input_dir: str,
    output_dir: str,
    max_samples:int,
    extentions:list
) -> None:
    """Creates dynamic images from frames."""
    if not os.path.exists(input_dir) or not os.listdir(input_dir):
        raise FileNotFoundError(
            f"Input directory '{input_dir}' is empty or doesn't exist. "
            "Run the script in 'frames' mode first."
        )
    dynamic_image_generator = DynamicImageGenerator()
    dynamic_image_generator.create_dynamic_images(
        input_dir,
        output_dir,
        max_samples,
        extentions
    )

@ExecutionTimeHandler.timeit
def main() -> None:
    args = parse_args()
    if args.block_console_msg:
        ConsoleManager.block_print()

    config = FileManager.load_config("./config/config.yaml")
    if args.dataset not in config["datasets"]:
        raise ValueError(f"Unsupported dataset: {args.dataset}")
    if args.mode not in config["datasets"][args.dataset]:
        raise ValueError(f"Unsupported mode: {args.mode} for dataset {args.dataset}")

    dataset_config = config["datasets"][args.dataset][args.mode]
    input_dir = os.path.join(args.input, dataset_config["input_subdir"])
    output_dir = input_dir.replace(args.input, args.output)

    if args.mode == "frames":
        if not args.frame_rate:
            raise ValueError("Frame rate (--frame_rate) is required for 'frames' mode.")
        output_dir = output_dir.replace("videos", dataset_config["output_subdir"])
        extentions = config["datasets"]["video_extentions"]["supported_extentions"]
        process_frames(input_dir, output_dir, args.frame_rate, extentions)

    elif args.mode in ["pre_extracted_frames", "dynamic"]: # Generate dynamic images from frames or pre-extracted frames
        if args.mode == "pre_extracted_frames" and args.dataset == "EPIC_KITCHENS": # Suport only for EPIC_KITCHENS dataset for now
            output_dir = output_dir.replace("frames_rgb_flow/rgb", "dynamic_images")

        if args.mode == "dynamic":
            output_dir = output_dir.replace("frames", dataset_config["output_subdir"])
        max_samples = config["dynamic_image"]["max_samples"]
        extentions = config["datasets"]["image_extentions"]["supported_extentions"]
        process_dynamic_images(input_dir, output_dir, max_samples, extentions)

if __name__ == "__main__":
    main()
