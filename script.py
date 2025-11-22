from pathlib import Path
from re import search, sub


def main():
    project_root = Path(__file__).parent
    uv_lock_path = project_root / "uv.lock"
    pre_commit_config_path = project_root / ".pre-commit-config.yaml"

    if not uv_lock_path.exists():
        print("uv.lock not found.")
        return

    if not pre_commit_config_path.exists():
        print(".pre-commit-config.yaml not found.")
        return

    # Read uv.lock to find ruff version
    uv_lock_content = uv_lock_path.read_text(encoding="utf-8")

    # Look for the ruff package block
    # [[package]]
    # name = "ruff"
    # version = "0.14.4"
    matched = search(r'name = "ruff"\nversion = "([^"]+)"', uv_lock_content)
    if not matched:
        print("ruff version not found in uv.lock")
        return

    ruff_version = matched.group(1)
    print(f"Found ruff version in uv.lock: {ruff_version}")

    # Read .pre-commit-config.yaml
    config_content = pre_commit_config_path.read_text(encoding="utf-8")

    # Pattern to find the ruff-pre-commit repo and its rev
    # We look for the repo url, then capture the rev line following it
    # We use a non-greedy match for content between repo and rev
    pattern = r"(repo: https://github\.com/astral-sh/ruff-pre-commit\s+rev: )v?[\d.]+"

    if search(pattern, config_content):
        new_content = sub(pattern, f"\\1v{ruff_version}", config_content)

        if new_content != config_content:
            pre_commit_config_path.write_text(new_content, encoding="utf-8")
            print(f"Updated .pre-commit-config.yaml ruff rev to v{ruff_version}")
        else:
            print(".pre-commit-config.yaml is already up to date.")
    else:
        print("ruff-pre-commit repo not found in .pre-commit-config.yaml")


if __name__ == "__main__":
    main()
