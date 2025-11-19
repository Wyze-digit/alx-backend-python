#!/usr/bin/env python3
"""
Test module for client.GithubOrgClient
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value"""
        # Set up the mock return value
        test_payload = {"login": org_name, "id": 12345}
        mock_get_json.return_value = test_payload

        # Create client instance and call org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Assert the result matches the mock return value
        self.assertEqual(result, test_payload)


if __name__ == '__main__':
    unittest.main()
