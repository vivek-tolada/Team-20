"""
GitHub integration using PyGithub.
Allows:
- Creating branches
- Committing new files
- Opening Pull Requests
"""

from github import Github
from .config import GITHUB_TOKEN


class GitHubClient:
    def __init__(self, token=None):
        self.token = token or GITHUB_TOKEN

        if not self.token:
            raise ValueError("GITHUB_TOKEN is missing! Add it in .env")

        self.gh = Github(self.token)

    def create_branch_and_pr(
        self,
        repo_full_name: str,
        base_branch: str,
        new_branch: str,
        files: dict,
        pr_title: str,
        pr_body: str
    ):
        """
        files = {
            "path/to/file.yaml": "file content here",
            ...
        }
        """

        repo = self.gh.get_repo(repo_full_name)

        # Get SHA of the base branch
        base = repo.get_branch(base_branch)
        base_sha = base.commit.sha

        # Create new branch
        try:
            repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=base_sha)
        except Exception:
            # If branch exists, ignore
            pass

        # Commit or update files
        for path, content in files.items():
            try:
                # Try update
                existing_file = repo.get_contents(path, ref=new_branch)
                repo.update_file(
                    path,
                    f"AI: Update {path}",
                    content,
                    existing_file.sha,
                    branch=new_branch
                )
            except Exception:
                # Else create file
                repo.create_file(
                    path,
                    f"AI: Add {path}",
                    content,
                    branch=new_branch
                )

        # Create Pull Request
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=new_branch,
            base=base_branch
        )

        return pr.html_url
