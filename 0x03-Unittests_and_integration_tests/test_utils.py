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
from unittest.mock import patch, Mock 
from utils import get_json
from utils import memoize


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

class TestGetJson(unittest.TestCase):
    """Test cases for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected result with mocked requests.get"""
        # Configure mock response
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Patch requests.get and test
        with patch('utils.requests.get') as mock_get:
            mock_get.return_value = mock_response
            
            # Call the function
            result = get_json(test_url)
            
            # Assert requests.get was called once with test_url
            mock_get.assert_called_once_with(test_url)
            
            # Assert the result matches test_payload
            self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()

class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator"""

    def test_memoize(self):
        """Test that memoize caches the result properly"""
        
        class TestClass:
            """Test class with memoized property"""
            
            def a_method(self):
                """Method to be memoized"""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method"""
                return self.a_method()

        # Create instance and mock a_method
        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42
            
            test_instance = TestClass()
            
            # Call a_property twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            
            # Assert both calls return correct result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            
            # Assert a_method was called only once
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
