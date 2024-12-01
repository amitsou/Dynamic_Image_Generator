# Dynamic Image Generator

## Overview

Dynamic Image Generator is a Python-based tool for creating dynamic images and extracting frames from video datasets. This project simplifies the processing of video data and is compatible with datasets like `EPIC-KITCHENS` and `EGTEA Gaze +`.

## Features

- **Frame Extraction:** Extract frames from videos at a specified frame rate.
- **Dynamic Image Generation:** Create dynamic images using pre-extracted frames.

## Quick Start

### Prerequisites

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the input directories are organized as required. The input directories should follow the conventions and file structure used in datasets such as **EPIC-KITCHENS** and **EGTEA Gaze+**. Refer to these datasets for proper organization and directory naming standards.

### Usage

Run the script using the following command:

```bash
python main.py -i <input_directory> -o <output_directory> -m <mode> -d <dataset>
```

#### Arguments
- `-i` / `--input`: Directory containing input videos or frames.
- `-o` / `--output`: Directory for saving processed outputs.
- `-m` / `--mode`: Choose `frames` for frame extraction or `dynamic` for dynamic image generation.
- `-d` / `--dataset`: Specify the dataset (e.g., `EPIC-KITCHENS`, `EGTEA`).

### Examples

1. Extract frames:
   ```bash
   python main.py -i path/to/videos -o path/to/output -m frames -d EPIC-KITCHENS
   ```

2. Generate dynamic images:
   ```bash
   python main.py -i path/to/frames -o path/to/output -m dynamic -d EGTEA
   ```

### Sample Outputs

- **Dynamic Image Sample:**
  ![Dynamic Image Sample](images/dyanmic_image_sample.jpg)

## Notes

- For `dynamic` mode, frames must be pre-extracted using the `frames` mode.
