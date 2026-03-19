#!/usr/bin/env python3
"""Sync the PR description with the matching Speckit spec summary.

Uses PyGithub to update the pull-request body so reviewers always see
the latest specification context.

Environment variables:
  GITHUB_TOKEN  – Personal access token or GITHUB_TOKEN from Actions.
  GITHUB_REPO   – owner/repo string, e.g. "octocat/hello-world".
  PR_NUMBER     – Pull-request number to update.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from github import Github


def _find_spec(branch_name: str) -> str | None:
    """Return the spec summary for the branch, or None."""
    # Convention: branch name matches a directory under specs/
    spec_dir = Path("specs") / branch_name
    spec_file = spec_dir / "spec.md"

    if not spec_file.exists():
        # Fallback: look for any spec whose name is a substring of the branch
        for candidate in Path("specs").glob("*/spec.md"):
            if candidate.parent.name in branch_name:
                spec_file = candidate
                break
        else:
            return None

    content = spec_file.read_text(encoding="utf-8")
    # Extract everything up to the first "##" after the title
    match = re.match(r"(#[^\n]+\n(?:.*?\n)*?)(?=\n## |\Z)", content, re.DOTALL)
    return match.group(0).strip() if match else content[:500]


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN", "")
    repo_name = os.environ.get("GITHUB_REPO", "")
    pr_number = os.environ.get("PR_NUMBER", "")

    if not all([token, repo_name, pr_number]):
        print("Missing GITHUB_TOKEN, GITHUB_REPO, or PR_NUMBER — skipping.")
        sys.exit(0)

    gh = Github(token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))

    spec_summary = _find_spec(pr.head.ref)
    if not spec_summary:
        print(f"No spec found for branch '{pr.head.ref}' — skipping.")
        return

    marker = "<!-- speckit-sync -->"
    new_body = f"{marker}\n\n{spec_summary}\n\n{marker}"

    current_body = pr.body or ""
    if marker in current_body:
        # Replace existing spec section
        pattern = re.compile(rf"{re.escape(marker)}.*?{re.escape(marker)}", re.DOTALL)
        updated = pattern.sub(new_body, current_body)
    else:
        updated = f"{current_body}\n\n{new_body}"

    pr.edit(body=updated)
    print(f"PR #{pr_number} description updated with spec from '{pr.head.ref}'.")


if __name__ == "__main__":
    main()
