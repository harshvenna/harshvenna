# Setup

## Requirements

- A GitHub account (`harshvenna`)
- Git for Windows (includes Git Bash)
- Python 3.9 or newer (only to run the local validation script)

## Steps

1. Create a **public** repository named exactly `harshvenna` (same as your username). GitHub shows its `README.md` on your profile.
2. The certificate and badge images are already included under `assets/badges/` and `assets/certificates/`. If you replace one (for example with the original file from the issuer), keep the same file name.
3. Run `python scripts/validate_assets.py` and fix anything it reports.
4. Commit and push (see below).
5. In the repository's **Actions** tab, run **Contribution Snake** once with *Run workflow*. This creates the `output` branch used by the snake animation.

## Workflow permissions

If the snake workflow fails with a permission error, open **Settings → Actions → General → Workflow permissions** and select **Read and write permissions**.

## Deploying from Git Bash (Windows)

```bash
git clone https://github.com/harshvenna/harshvenna.git
cd harshvenna
git status
# unzip the revised archive somewhere temporary, then copy over the clone, keeping .git:
unzip /c/Users/YOUR_NAME/Downloads/harshvenna-github-profile.zip -d /tmp/hv
cp -r /tmp/hv/harshvenna/. .
python scripts/validate_assets.py
git add .
git commit -m "Build premium GitHub developer profile"
git push origin main
```

If the repository already has a `README.md` you want to keep, copy it elsewhere before the `cp -r` step. If the repository does not exist yet, create it on GitHub first (public, named `harshvenna`, no initial files).
