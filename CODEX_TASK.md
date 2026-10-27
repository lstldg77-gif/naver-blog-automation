# Codex development task

Implement an opt-in **Naver SmartEditor draft-save workflow** on the user's local Windows computer using Playwright.

Requirements:
- Browser authentication is completed by the user manually; never collect or store credentials in code.
- Read a UTF-8 JSON draft file (title, body, optional photo-placement markers); validate input.
- Navigate to Naver blog writing UI for the user's own blog; robustly handle iframe/contenteditable UI, avoid hardcoded brittle selectors where possible.
- Fill title and full body; click **임시저장** only after preview/explicit approval.
- NEVER click 발행; no auto publishing.
- Reopen the Naver draft list and verify saved title/body, or report exact failure and retain source draft.
- Do not run unattended until interactive verification is successful.
- Log non-sensitive status/error messages; don't log cookies or passwords.
- Keep images as human-editable placeholders; no image downloading/uploading.
- Create unit tests for JSON validation and dry-run, plus a human-in-the-loop manual smoke-test protocol.
- Provide Korean Windows setup/run instructions.

Current status: starter only; no successful Naver editor or draft-save test.
