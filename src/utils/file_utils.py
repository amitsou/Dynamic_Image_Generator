"""This module contains a class that handles file and directory-related operations."""

import os
import yaml

class FileManager:
    """Handles file and directory-related operations."""

    @staticmethod
    def media_path_crawler(
        root_dir: str, excluded_dirs: list, extensions: list) -> list[str]:
        """
        Recursively retrieves video file paths from a root directory, excluding specified subdirectories
        and filtering by file extensions.
        Args:
            root_dir (str): The root directory to search for video files.
            excluded_dirs (list[str], optional):
            A list of subdirectory names to exclude from the search.
            Defaults to ['.DS_Store'].
            extensions (list[str], optional):
            A list of file extensions to filter the video files. Defaults to ['.jpg', '.JPG', '.png', '.PNG'].
        Returns:
            list[str]: A list of absolute paths to the video files found.
        """
        if not excluded_dirs:
            excluded_dirs = [".DS_Store"]

        media_paths = []
        for dir_name, subdir_list, file_list in os.walk(root_dir):
            for subdir in (f.name for f in os.scandir(dir_name) if f.is_dir()):
                if subdir in excluded_dirs:
                    print(f"Excluding sub-directory: {subdir}")
                    subdir_list.remove(subdir)
                print("\t- subdirectory: %s" % subdir)

            for fname in file_list:
                if fname.endswith(tuple(extensions)):
                    file_path = os.path.abspath(os.path.join(dir_name, fname))
                    media_paths.append(file_path)
            print(f"\nNumber of videos found: {len(media_paths)}")
        return media_paths

    @staticmethod
    def load_config(config_path: str) -> dict:
        """Load configuration from a YAML file."""
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def create_multiple_dirs(path: str):
        """Create multiple directories recursively if they don't exist."""
        os.makedirs(path, exist_ok=True)
