# Naver blog automation

ChatGPT prepares Korean blog drafts; the user adds photos and publishes. This repository contains a **local Windows, human-approved draft-saving prototype**. It has not yet passed a live Naver SmartEditor test.

## Windows setup
1. Install Python 3.11+.
2. Open PowerShell in this repository.
3. Run `pip install -r requirements.txt`.
4. Run `python -m playwright install chromium`.
5. Run `python open_editor.py` and sign in to Naver manually, then close the browser using Enter. Never put credentials/cookies into Git.

## One-post trial
1. Edit `sample_draft.json` with `title` and `body` (UTF-8 text). The supplied sample is test content, not for publication.
2. Validate with `python naver_draft.py sample_draft.json --dry-run`.
3. Run `python naver_draft.py sample_draft.json`.
4. In the opened browser, sign in if needed. Complete or dismiss any draft-continuation popup yourself.
5. Inspect the visible title and body, then type **저장** in PowerShell to allow clicking **임시저장**. Any other response cancels.
6. In Naver's draft list, reopen the draft and verify both its first and last lines. Only then treat it as saved.

The script never clicks **발행**. It intentionally stops on uncertain selectors rather than risking edits to the wrong document. Screenshots `naver-before-save.png` and `naver-after-save.png` are saved locally for troubleshooting; do not commit them or private manuscripts.

## Troubleshooting
- If the title/body field cannot be found, Naver may have changed the SmartEditor markup. Report the error and inspect a screenshot locally.
- If the clipboard paste is blocked, update the editor input strategy and retest one post only.
- If a previous draft prompt appears, choose manually to avoid overwriting another post.
- This prototype is **not ready for unattended daily automation** until real draft reopen-and-verify testing succeeds.

## Tests
Run `python -m unittest -v test_naver_draft.py`.

Repository visibility is PUBLIC. Never commit passwords, browser profiles, cookies, unpublished personal content, or screenshots containing account details.
