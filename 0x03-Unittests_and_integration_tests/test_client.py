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

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the expected value
        based on the mocked org payload
        """
        # Known payload with specific repos_url
        test_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos",
            "login": "testorg",
            "id": 12345
        }
        
        # Patch GithubOrgClient.org as a context manager
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            # Set the mock to return our test payload
            mock_org.return_value = test_payload
            
            # Create client instance
            client = GithubOrgClient("testorg")
            
            # Access the _public_repos_url property (this should use the mocked org)
            result = client._public_repos_url
            
            # Assert the result is the expected repos_url from our test payload
            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
            
            # Verify the org property was accessed (since _public_repos_url depends on it)
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected list of repos
        and that the mocked methods are called once
        """
        # Test payload with repository data
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        
        expected_repos = ["repo1", "repo2", "repo3"]
        test_url = "https://api.github.com/orgs/testorg/repos"
        
        # Mock _public_repos_url as context manager
        with patch('client.GithubOrgClient._public_repos_url', 
                  new_callable=PropertyMock) as mock_public_repos_url:
            
            # Set up the mocks
            mock_public_repos_url.return_value = test_url
            mock_get_json.return_value = test_payload
            
            # Create client and call the method
            client = GithubOrgClient("testorg")
            result = client.public_repos()
            
            # Assert the list of repos is as expected
            self.assertEqual(result, expected_repos)
            
            # Assert that get_json was called once with the correct URL
            mock_get_json.assert_called_once_with(test_url)
            
            # Assert that _public_repos_url was accessed once
            mock_public_repos_url.assert_called_once()


if __name__ == '__main__':
    unittest.main()
