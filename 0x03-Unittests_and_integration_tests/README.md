# 0x03. Unittests and Integration Tests

## Description

This project focuses on writing unit tests and integration tests for Python functions and classes. It demonstrates testing techniques including:

- Parameterized tests
- Mocking HTTP requests
- Testing exceptions
- Memoization testing
- Testing class methods and properties
- Integration testing using fixtures

All tests are designed to work with Python 3.7 and follow `pycodestyle` (PEP8) conventions.

---

## Contents

### `utils.py` (Functions under test)
- `access_nested_map(nested_map, path)`: Safely access a value in a nested dictionary.
- `get_json(url)`: Fetch and return a JSON payload from a URL.
- `memoize`: A decorator for caching method results.

### `client.py` (Class under test)
- `GithubOrgClient`: A class to interact with the GitHub API and retrieve organization information and repositories.

---

## Test Files

### `test_utils.py`
- Unit tests for `utils.py` functions.
- Tests include:
  - Accessing nested maps (with exceptions)
  - Mocking `requests.get` for `get_json`
  - Testing the `memoize` decorator

### `test_client.py`
- Unit and integration tests for `GithubOrgClient`.
- Tests include:
  - Mocking `get_json` for `.org` property
  - Testing `_public_repos_url`
  - Mocking `_public_repos_url` and validating repo list
  - Checking if a repo has a specific license
  - Integration tests with fixtures (`fixtures.py`)

---

## Setup & Run

Make sure you have `Python 3.7` and the required modules:

```bash
pip install parameterized
