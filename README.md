# Dynamic Image Generator

## Overview

This repository provides tools for processing video datasets to generate dynamic images and extract frames. It supports two main modes of operation:

- **Frames Mode:** Extracts frames from videos at a specified frame rate.
- **Dynamic Mode:** Creates dynamic images from video frames.

The script is designed for datasets such as `EPIC-KITCHENS` and `EGTEA`, but it is configurable for other datasets through a `config.yaml` file.

## Repository Structure

The repository is organized into several directories and files:

### Default Directories

1. **`data/`**: Placeholder directory for raw or processed data.
2. **`config/`**: Contains the `config.yaml` file for dataset-specific configurations.
3. **`src/`**: Main source code directory with submodules:
   - **`image_generators/`**: Implements the `DynamicImageGenerator` class.
   - **`utils/`**: Provides utility functions for file handling, console management, and image processing.
   - **`video_processing/`**: Includes functionality for extracting frames from videos.
4. **`main.py`**: Entry point for executing the video processing pipeline.
5. **`requirements.txt`**: Lists dependencies required to run the project.

## Inputs and Outputs

### Inputs

- **Video Files**: Stored in the input directory. Supported formats are specified in **`config.yaml`.**
- **Configuration File (`config.yaml`)**: Defines dataset-specific settings such as subdirectories and supported file types.

### Outputs

- **Frames Mode**: Extracted frames stored in the output directory named `frames`.
- **Dynamic Mode**: Generated dynamic images saved in the output directory named `dynamic_images`.

## Configuration

The `config/config.yaml` file defines the structure for datasets. For example:

```yaml
datasets:
  EPIC-KITCHENS:
    frames:
      input_subdir: "EPIC_KITCHENS/videos"
      output_subdir: "frames"
      supported_extensions: [".mp4", ".MP4"]
    dynamic:
      input_subdir: "EPIC_KITCHENS/frames"
      output_subdir: "dynamic_images"
      supported_extensions: [".jpg", ".JPG", ".png", ".PNG"]
  EGTEA:
    frames:
      input_subdir: "EGTEA_GAZE_PLUS/Raw_Videos"
      output_subdir: "frames"
      supported_extensions: [".mp4", ".MP4"]
    dynamic:
      input_subdir: "EGTEA_GAZE_PLUS/frames"
      output_subdir: "dynamic_images"
      supported_extensions: [".jpg", ".JPG", ".png", ".PNG"]
```

## How to Execute

### Prerequisites

1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Ensure the `config.yaml` file is properly configured for the dataset.

### Usage

Run the script using the following command:

```bash
python main.py -i <input_directory> -o <output_directory> -m <mode> -d <dataset> [optional_args]
```

#### Arguments

- `-i` / `--input`: Input directory.
- `-o` / `--output`: Output directory.
- `-m` / `--mode`: Mode of operation (`frames` or `dynamic`).
- `-d` / `--dataset`: Dataset name (`EPIC-KITCHENS`, `EGTEA`, etc.).
- `-fps` / `--frame_rate`: Frame rate for extracting frames (required for `frames` mode).
- `-b` / `--block_console_msg`: Suppress console messages (optional).

#### Examples

1. Extract frames:

   ```bash
   python main.py -i path/to/input -o path/to/output -m frames -d EPIC-KITCHENS -fps 30
   ```
2. Generate dynamic images:

   ```bash
   python main.py -i path/to/input -o path/to/output -m dynamic -d EPIC-KITCHENS
   ```

## Notes

- Ensure input directories are correctly structured as per `config.yaml`.
- For `dynamic` mode, **ensure frames are pre-generated** using `frames` mode.

---

For further details, explore the repository and consult the individual module documentation.
