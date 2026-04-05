"""
Deploy script: creates HF Space and uploads all project files.
"""
import os
import time
from pathlib import Path
from huggingface_hub import HfApi

TOKEN = os.environ.get("HF_TOKEN", "your_huggingface_token_here")
USERNAME = "Shibu-119"
REPO_NAME = "customer-email-triage"
REPO_ID = f"{USERNAME}/{REPO_NAME}"
PROJECT_ROOT = Path(__file__).parent


def main():
    api = HfApi(token=TOKEN)

    # Step 1: Create the Space
    print(f"Step 1: Creating Space {REPO_ID}...")
    try:
        url = api.create_repo(
            repo_id=REPO_ID,
            repo_type="space",
            space_sdk="docker",
            private=False,
            exist_ok=True,
        )
        print(f"  ✓ Space created/exists: {url}")
    except Exception as e:
        print(f"  ✗ Error creating repo: {e}")
        raise

    # Small delay to let HF finish creating the repo
    time.sleep(3)

    # Step 2: Upload README card first (as README.md)
    print("Step 2: Uploading README card...")
    api.upload_file(
        path_or_fileobj=str(PROJECT_ROOT / "README_HF.md"),
        path_in_repo="README.md",
        repo_id=REPO_ID,
        repo_type="space",
        commit_message="chore: add HF Space README card",
    )
    print("  ✓ README.md uploaded")

    # Step 3: Upload all other files
    print("Step 3: Uploading project files...")
    ignore = [
        "*.pyc",
        "**/__pycache__/**",
        "**/.git/**",
        "**/.venv/**",
        "**/venv/**",
        ".gitignore",
        "README_HF.md",
        "README.md",       # Already uploaded as card
        "deploy_to_hf.py",
        "test_env.py",
    ]
    api.upload_folder(
        folder_path=str(PROJECT_ROOT),
        repo_id=REPO_ID,
        repo_type="space",
        ignore_patterns=ignore,
        commit_message="feat: initial OpenEnv Customer Email Triage submission",
    )
    print("  ✓ All files uploaded")

    hf_url = f"https://huggingface.co/spaces/{REPO_ID}"
    api_url = f"https://shibu-119-customer-email-triage.hf.space"
    print(f"\n🎉 Deployment complete!")
    print(f"   HF Space:   {hf_url}")
    print(f"   API base:   {api_url}")
    print(f"   Dashboard:  {api_url}/web/")
    print(f"\n   Test reset endpoint:")
    print(f'   curl -X POST {api_url}/reset -H "Content-Type: application/json" -d \'{{"task":"priority-triage"}}\'')


if __name__ == "__main__":
    main()
