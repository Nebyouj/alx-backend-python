#!/usr/bin/env python3
"""
Unit and integration tests for the GithubOrgClient class.

Includes:
- Unit tests using patch and parameterized decorators.
- Integration tests using fixtures and patching external requests.
"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
        """Test has_license correctly identifies license presence."""
        client = GithubOrgClient("google")
        self.assertTrue(client.has_license(
            {"license": {"key": "my_license"}},
            "my_license"
        ))
        self.assertFalse(client.has_license(
            {"license": {"key": "other_license"}},
            "my_license"
        ))


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get with side effects returning fixture data."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_resp = MagicMock()
            if url == f"https://api.github.com/orgs/google":
                mock_resp.json.return_value = cls.org_payload
            elif url == f"https://api.github.com/orgs/google/repos":
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repository names."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtered by license returns correct repos."""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()