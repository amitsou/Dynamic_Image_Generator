"""This module contains the ConsoleManager class."""

import os
import sys


class ConsoleManager:
    """Handles console-related operations."""

    @staticmethod
    def block_print() -> None:
        """Block printing messages to the console."""
        sys.stdout = open(os.devnull, "w")

    @staticmethod
    def enable_print() -> None:
        """Restore printing to the console."""
        sys.stdout = sys.__stdout__
