# Troubleshooting

## A statistics card shows an error or never loads

The public GitHub Readme Stats and Activity Graph instances are shared and are sometimes rate limited or offline. Try again later, or self-host the service on your own Vercel account and replace the host in the URL.

## Snake animation is broken

- Run **Actions → Contribution Snake → Run workflow** once.
- Confirm **Settings → Actions → General → Workflow permissions** is set to *Read and write*.
- Confirm the `output` branch exists.

## Certificate images show a broken icon

The file is missing or misnamed. Run `python scripts/validate_assets.py`; it lists every missing path.

## Markdown check fails on a pull request or push

Read the log of the failing step. *Lint Markdown* reports the file and line; *Validate local links* reports the missing path.

## Git Bash says the push was rejected

The remote has commits you do not have locally. Run `git pull --rebase origin main` and push again.
