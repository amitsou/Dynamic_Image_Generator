"""
This script is used to extract frames from videos and create dynamic images from frames.
The script supports two modes of operation: 'frames' and 'dynamic'.
In 'frames' mode, the script extracts frames from videos at a specified frame rate.
In 'dynamic' mode, the script creates dynamic images from frames.

The script requires the following arguments:
    -i, --input: Input directory.
    -o, --output: Output directory.
    -m, --mode: Mode of operation ('frames' or 'dynamic').
    -d, --dataset: Dataset name (e.g., 'EPIC-KITCHENS', 'EGTEA').
    -fps, --frame_rate: Frame rate for extracting frames (required for 'frames' mode).
    -b, --block_console_msg: Block console messages.

Example usage of the script:
    python main.py -i path/to/input -o path/to/output -m frames -d EPIC-KITCHENS -fps 30
    python main.py -i path/to/input -o path/to/output -m dynamic -d EPIC-KITCHENS

Note: The script uses a configuration file (config.yaml) to load dataset-specific configurations.
"""

import argparse
import os

import yaml

from src.image_generators.dynamic_image_generator import DynamicImageGenerator
from src.utils.console_utils import ConsoleManager
from src.utils.execution_utils import ExecutionTimeHandler
from src.utils.file_utils import FileManager
from src.video_processing.video_processor import VideoProcessor


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from a YAML file."""
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Video processing pipeline.")
    parser.add_argument("-i", "--input", required=True, help="Input directory.")
    parser.add_argument("-o", "--output", required=True, help="Output directory.")
    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        choices=["frames", "dynamic"],
        help="Mode of operation.",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        required=True,
        help="Dataset name (e.g., 'EPIC-KITCHENS', 'EGTEA').",
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
    input_dir: str, output_dir: str, frame_rate: int, extensions: list
) -> None:
    """Extracts frames from videos."""
    videos = FileManager.media_path_crawler(input_dir, extensions)
    video_processor = VideoProcessor()

    for video_path in videos:
        destination_dir = video_path.replace(input_dir, output_dir).split(".")[0]
        FileManager.create_multiple_dirs(destination_dir)
        video_processor.extract_video_frames(
            [video_path], destination_dir, fps=frame_rate
        )


def process_dynamic_images(input_dir: str, output_dir: str, extensions: list) -> None:
    """Creates dynamic images from frames."""
    if not os.path.exists(input_dir) or not os.listdir(input_dir):
        raise FileNotFoundError(
            f"Input directory '{input_dir}' is empty or doesn't exist. "
            "Run the script in 'frames' mode first."
        )

    dynamic_image_generator = DynamicImageGenerator()
    dynamic_image_generator.create_dynamic_images(input_dir, output_dir)


@ExecutionTimeHandler.timeit
def main() -> None:
    args = parse_args()
    if args.block_console_msg:
        ConsoleManager.block_print()

    config = load_config()

    if args.dataset not in config["datasets"]:
        raise ValueError(f"Unsupported dataset: {args.dataset}")
    if args.mode not in config["datasets"][args.dataset]:
        raise ValueError(f"Unsupported mode: {args.mode} for dataset {args.dataset}")

    dataset_config = config["datasets"][args.dataset][args.mode]
    input_dir = os.path.join(args.input, dataset_config["input_subdir"])
    output_dir = os.path.join(args.output, dataset_config["output_subdir"])
    extensions = dataset_config["supported_extensions"]

    if args.mode == "frames":
        if not args.frame_rate:
            raise ValueError("Frame rate (--frame_rate) is required for 'frames' mode.")
        process_frames(input_dir, output_dir, args.frame_rate, extensions)
    elif args.mode == "dynamic":
        process_dynamic_images(input_dir, output_dir, extensions)


if __name__ == "__main__":
    main()
