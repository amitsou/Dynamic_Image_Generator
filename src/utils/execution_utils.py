"""Contains utility classes for handling execution time."""


class ExecutionTimeHandler:
    """Handles execution time calculation."""

    @staticmethod
    def calculate_execution_time(start_time: float, end_time: float) -> tuple:
        """
        Calculate the execution time between two timestamps.
        Args:
            start_time (float): The start time in seconds.
            end_time (float): The end time in seconds.
        Returns:
            tuple: A tuple containing the execution time in minutes, seconds, and milliseconds.
        Prints:
            A formatted string displaying the execution time in minutes, seconds, and milliseconds.
        """
        execution_time = end_time - start_time
        minutes, seconds = divmod(execution_time, 60)
        seconds, milliseconds = divmod(seconds, 1)
        milliseconds = int(milliseconds * 1000)
        print(
            f"Program executed in {int(minutes)} minutes, {int(seconds)} seconds, and {milliseconds} milliseconds"
        )
        return int(minutes), int(seconds), milliseconds
