#!/usr/bin/env python3
"""
Unit tests for utils.py
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function from utils module."""

    @parameterized.expand([
        ("simple_map", {"a": 1}, ("a",), 1),
        ("nested_map_level1", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("nested_map_level2", {"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
        self, name: str, nested_map: dict, path: tuple, expected: object
        ) -> None:
        """Test correct retrieval from nested maps."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ("missing_key", {}, ("a",)),
        ("missing_nested_key", {"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(
        self, name: str, nested_map: dict, path: tuple
    ) -> None:
        """Test KeyError raised for invalid path in nested maps."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Test the get_json function which fetches JSON from a URL."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(
        self, test_url: str, test_payload: dict, mock_get: Mock
    ) -> None:
        """Test get_json returns correct payload using mocked requests.get."""
        mock_get.return_value = Mock(json=Mock(return_value=test_payload))
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test the memoize decorator to ensure function result is cached."""

    def test_memoize(self) -> None:
        """Test that the memoized method is only called once."""

        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(TestClass, "a_method") as mock_method:
            mock_method.return_value = 42
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()
