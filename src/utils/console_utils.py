"""This module contains the ConsoleManager class."""

import os
import sys


class ConsoleManager:
    """Handles console-related operations."""

    @staticmethod
    def block_print():
        """Block printing messages to the console."""
        sys.stdout = open(os.devnull, "w")

    @staticmethod
    def enable_print():
        """Restore printing to the console."""
        sys.stdout = sys.__stdout__
