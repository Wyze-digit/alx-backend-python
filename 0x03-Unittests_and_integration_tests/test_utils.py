#!/usr/bin/env python3
"""
Unit tests for the utils.access_nested_map function.
This module tests the behavior of the `access_nested_map` utility function
to ensure it correctly retrieves nested dictionary values based on a provided path.
All tests follow Python's unittest framework and conform to pycodestyle 2.5.
"""

import unittest
from parameterized import parameterized
from typing import Any, Dict, Tuple
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the access_nested_map function.
    It verifies that nested map lookups return expected values.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any],
                               path: Tuple[str, ...], expected: Any) -> None:
        """
        Test that access_nested_map returns the correct result
        for different levels of nested dictionaries.
        """
        result = access_nested_map(nested_map, path); self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()


"""
Unit tests for the utils.access_nested_map function.

This module tests both successful and exceptional cases
for the `access_nested_map` utility function to ensure
it correctly retrieves nested dictionary values and raises
appropriate exceptions for invalid paths.
"""


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the access_nested_map function.
    Verifies both normal return values and KeyError handling.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Dict[str, Any],
                               path: Tuple[str, ...], expected: Any) -> None:
        """
        Test that access_nested_map returns the correct result
        for different levels of nested dictionaries.
        """
        result = access_nested_map(nested_map, path); self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map: Dict[str, Any],
                                         path: Tuple[str, ...],
                                         expected_message: str) -> None:
        """
        Test that access_nested_map raises KeyError with the correct message
        when trying to access a non-existent key in the nested map.
        """
        with self.assertRaises(KeyError) as exc:
            access_nested_map(nested_map, path)
        self.assertEqual(str(exc.exception), expected_message)


if __name__ == "__main__":
    unittest.main()   