#!/usr/bin/env python3
"""
Utility module providing helper functions for accessing nested dictionary data.

This module contains the `access_nested_map` function which retrieves values
from nested dictionaries using a tuple-based path.
It is designed to raise clear KeyError exceptions when invalid keys are accessed.
"""

from typing import Any, Mapping, Sequence


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """
    Retrieve a value from a nested dictionary following the provided path.

    Args:
        nested_map (Mapping[str, Any]): The dictionary containing nested data.
        path (Sequence[str]): A tuple representing the key path (e.g. ("a", "b")).

    Returns:
        Any: The value found at the end of the nested path.

    Raises:
        KeyError: If any key in the path does not exist in the dictionary.

    Example:
        >>> access_nested_map({"a": {"b": 2}}, ("a", "b"))
        2
    """
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map
    """

    current = nested_map
    for key in path:
        if not isinstance(current, Mapping):
            raise KeyError(key)
        if key not in current:
            raise KeyError(key)
        current = current[key]
    return current


