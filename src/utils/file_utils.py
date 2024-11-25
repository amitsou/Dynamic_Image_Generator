"""This module contains a class that handles file and directory-related operations."""

import os


class FileManager:
    """Handles file and directory-related operations."""

    @staticmethod
    def media_path_crawler(
        root_dir: str, excluded_dirs: list[str] = None, extensions: list[str] = None
    ) -> list[str]:
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
        if excluded_dirs is None:
            excluded_dirs = [".DS_Store"]
        if extensions is None:
            extensions = [".jpg", ".JPG", ".png", ".PNG"]

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
    def is_dir(directory: str) -> bool:
        """
        Check if the given path is a directory.
        Args:
            directory (str): The path to check.
        Returns:
            bool: True if the path is a directory, False otherwise.
        """
        return os.path.isdir(directory)

    @staticmethod
    def is_file(filename: str) -> bool:
        """
        Check if a given path is a file.
        Args:
            filename (str): The path to the file.
        Returns:
            bool: True if the path is a file, False otherwise.
        """
        return os.path.isfile(path=filename)

    @staticmethod
    def create_multiple_dirs(path: str):
        """Create multiple directories recursively if they don't exist."""
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def create_dir(directory: str):
        """
        Creates a directory with the specified path.
        Args:
            directory (str): The path of the directory to create.
        Returns:
            bool: True if the directory was created successfully, False if the directory already exists.
        Raises:
            OSError: If the directory cannot be created for reasons other than it already existing.
        """
        try:
            return os.mkdir(directory)
        except FileExistsError:
            print(f"{directory} already exists")
            return False

    @staticmethod
    def crawl_directory(directory: str, extension: str = None) -> list:
        """
        Recursively crawls through a directory and collects files with a specific extension.
        Args:
            directory (str): The root directory to start crawling from.
            extension (str, optional): The file extension to filter by.
            If None, all files are collected. Defaults to None.
        Returns:
            list: A list of file paths that match the specified extension.
        """
        tree = []
        subdirs = [folder[0] for folder in os.walk(directory)]

        for subdir in subdirs:
            files = next(os.walk(subdir))[2]
            for _file in files:
                lowercase_extension = extension.lower() if extension else ""
                uppercase_extension = extension.upper() if extension else ""
                if _file.endswith(lowercase_extension) or _file.endswith(
                    uppercase_extension
                ):
                    tree.append(os.path.join(subdir, _file))
                else:
                    tree.append(os.path.join(subdir, _file))

        if tree:
            print(f"Found {len(tree)} files in {directory}")
        return tree
