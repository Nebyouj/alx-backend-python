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
    """Unit tests for GithubOrgClient methods and properties."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """Test that org method returns the expected organization payload."""
        expected = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self) -> None:
        """Test that the _public_repos_url property returns correct URL."""
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: Mock) -> None:
        """Test that public_repos returns repo names and uses correct URL."""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]
        with patch.object(
            GithubOrgClient, "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "dummy_url"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("dummy_url")

    @parameterized.expand([
        ("has_license", {"license": {"key": "my_license"}},
         "my_license", True),
        ("no_license", {"license": {"key": "other_license"}},
         "my_license", False),
    ])
    def test_has_license(
        self, name: str, repo: dict,
        license_key: str, expected: bool
    ) -> None:
        """Test has_license returns True if repo has specified license."""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key), expected
        )


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
