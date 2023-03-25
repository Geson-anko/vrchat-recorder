from datetime import datetime


def get_now_str(format: str = "%Y-%m-%d-%H-%M-%S-%f") -> str:
    """Get the current time as a string.

    Args:
        format (str): The format of the time string.
    Returns:
        now_str (str): The current time as a string.
    """
    now = datetime.now()
    now_str = now.strftime(format)
    return now_str
