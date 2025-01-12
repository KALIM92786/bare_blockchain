# condition.py

def always_true():
    """
    A condition that always returns True. Useful for testing.
    """
    return True

def greater_than_threshold(value, threshold=10):
    """
    Checks if a value is greater than a threshold.
    :param value: The value to evaluate.
    :param threshold: The threshold to compare against (default: 10).
    :return: True if value > threshold, else False.
    """
    return value > threshold

def within_range(value, min_value, max_value):
    """
    Checks if a value is within a specified range.
    :param value: The value to evaluate.
    :param min_value: The minimum acceptable value.
    :param max_value: The maximum acceptable value.
    :return: True if min_value <= value <= max_value, else False.
    """
    return min_value <= value <= max_value
