from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from specsfy_cli.github import api_headers


class GitHubAuthenticationTests(unittest.TestCase):
    def test_prefers_gh_token_environment_variable(self) -> None:
        with patch.dict(
            "os.environ",
            {"GH_TOKEN": "primary", "GITHUB_TOKEN": "secondary"},
            clear=True,
        ):
            headers = api_headers("specsfy-test")

        self.assertEqual("Bearer primary", headers["Authorization"])

    def test_uses_authenticated_gh_session_as_fallback(self) -> None:
        result = Mock(returncode=0, stdout="from-gh\n")
        with (
            patch.dict("os.environ", {}, clear=True),
            patch("specsfy_cli.github.shutil.which", return_value="/usr/bin/gh"),
            patch("specsfy_cli.github.subprocess.run", return_value=result) as runner,
        ):
            headers = api_headers("specsfy-test")

        self.assertEqual("Bearer from-gh", headers["Authorization"])
        runner.assert_called_once_with(
            ["/usr/bin/gh", "auth", "token"],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_keeps_public_request_usable_without_credentials(self) -> None:
        with (
            patch.dict("os.environ", {}, clear=True),
            patch("specsfy_cli.github.shutil.which", return_value=None),
        ):
            headers = api_headers("specsfy-test")

        self.assertNotIn("Authorization", headers)
        self.assertEqual("application/vnd.github+json", headers["Accept"])


if __name__ == "__main__":
    unittest.main()
