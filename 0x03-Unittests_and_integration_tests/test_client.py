#!/usr/bin/env python3
"""
Unit and integration tests for client.py
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected JSON payload."""
        mock_get_json.return_value = {"login": org_name}
        client = GithubOrgClient(org_name)
        result = client.org
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected URL from org payload."""
        client = GithubOrgClient("google")
        with patch.object(GithubOrgClient, "org",
                          new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked_url.com"}
            self.assertEqual(client._public_repos_url, "http://mocked_url.com")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repository names."""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        client = GithubOrgClient("google")
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=unittest.mock.PropertyMock) as mock_url:
            mock_url.return_value = "http://mocked_url.com"
            repos = client.public_repos()
            mock_get_json.assert_called_once_with("http://mocked_url.com")
            self.assertEqual(repos, ["repo1", "repo2"])

    def test_has_license(self):
        """Test has_license checks if repo has the specified license."""
        client = GithubOrgClient("google")
        repo = {"license": {"key": "my_license"}}
        self.assertTrue(client.has_license(repo, "my_license"))
        self.assertFalse(client.has_license(repo, "other_license"))


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [fixtures.TEST_PAYLOAD[0]]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using test fixtures."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up mock for requests.get before all tests."""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url: str) -> Mock:
            if url.endswith("/repos"):
                return Mock(json=Mock(return_value=cls.repos_payload))
            return Mock(json=Mock(return_value=cls.org_payload))

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the mock after all tests."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test public_repos returns all repos from fixture."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test public_repos filters repos by license from fixture."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
