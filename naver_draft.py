"""Safely prepare and save one Naver SmartEditor draft on local Windows.

The user signs in manually. This program never publishes a post.
"""

import argparse
import json
from pathlib import Path

BLOG_ID = "lstldh"
EDITOR_URL = f"https://blog.naver.com/{BLOG_ID}/postwrite"


def read_draft(path: Path) -> tuple[str, str]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("원고는 JSON 객체여야 합니다.")
    title, body = data.get("title"), data.get("body")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("title에 제목을 입력하세요.")
    if not isinstance(body, str) or len(body.strip()) < 30:
        raise ValueError("body에 30자 이상의 본문을 입력하세요.")
    if len(title) > 200:
        raise ValueError("제목은 200자 이하여야 합니다.")
    return title.strip(), body.strip()


def editor_field(page, selectors: list[str], description: str):
    """Resolve a visible editable field using user-facing editor attributes."""
    for selector in selectors:
        loc = page.locator(selector)
        try:
            visible = loc.filter(visible=True)
            if visible.count() == 1:
                return visible
        except Exception:
            continue
    raise RuntimeError(f"{description} 입력창을 찾지 못했습니다. 편집기 구조를 확인하세요.")


def write_editor(page, title: str, body: str) -> None:
    title_loc = editor_field(page, [
        '[contenteditable="true"][data-placeholder="제목"]',
        '[contenteditable="true"][placeholder="제목"]',
        '.se-title-text [contenteditable="true"]',
        '.se-title [contenteditable="true"]',
    ], "제목")
    title_loc.click()
    title_loc.fill(title)

    body_loc = editor_field(page, [
        '[contenteditable="true"][data-placeholder*="글감과 함께"]',
        '[contenteditable="true"][placeholder*="글감과 함께"]',
        '.se-main-container .se-component-content [contenteditable="true"]',
        '.se-main-container [contenteditable="true"]',
    ], "본문")
    body_loc.click()
    # Real keystrokes/paste trigger the editor's input handlers; no DOM mutation.
    page.context.grant_permissions(["clipboard-read", "clipboard-write"], origin="https://blog.naver.com")
    page.evaluate("text => navigator.clipboard.writeText(text)", body)
    body_loc.press("ControlOrMeta+V")
    page.wait_for_timeout(1000)

    if title not in page.locator("body").inner_text():
        raise RuntimeError("제목 입력을 화면에서 확인하지 못했습니다.")
    first = body.splitlines()[0].strip()
    last = next((line.strip() for line in reversed(body.splitlines()) if line.strip()), "")
    visible_text = page.locator("body").inner_text()
    if first not in visible_text or last not in visible_text:
        raise RuntimeError("본문 첫 문장 또는 마지막 문장을 화면에서 확인하지 못했습니다.")


def main() -> None:
    parser = argparse.ArgumentParser(description="네이버 글 1편 임시저장 (발행 안 함)")
    parser.add_argument("draft", type=Path, help="UTF-8 JSON 원고 파일")
    parser.add_argument("--dry-run", action="store_true", help="원고 검사만 수행")
    args = parser.parse_args()
    title, body = read_draft(args.draft)
    print(f"원고 확인: {title} / 본문 {len(body)}자")
    if args.dry_run:
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Playwright가 없습니다. pip install -r requirements.txt 실행 후 다시 시도하세요.") from exc

    profile = Path.home() / ".naver_blog_automation_profile"
    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            str(profile), headless=False, locale="ko-KR"
        )
        page = context.pages[0] if context.pages else context.new_page()
        try:
            page.goto(EDITOR_URL, wait_until="domcontentloaded")
            print("브라우저에서 네이버 로그인을 완료하세요. 편집기가 보이면 Enter를 누르세요.")
            input()
            if "nid.naver.com" in page.url:
                raise RuntimeError("네이버 로그인이 완료되지 않았습니다.")
            # Existing-draft popups are user decisions: do not dismiss automatically.
            print("기존 글 이어쓰기 팝업이 있다면 직접 처리한 뒤 Enter를 누르세요.")
            input()
            write_editor(page, title, body)
            page.screenshot(path="naver-before-save.png", full_page=False)
            print("제목·본문이 화면에 입력되었습니다. 내용을 살펴보세요.")
            approval = input("이 글을 임시저장할까요? '저장'이라고 입력하세요: ").strip()
            if approval != "저장":
                print("취소: 임시저장 버튼을 누르지 않았습니다.")
                return
            save = page.get_by_role("button", name="임시저장", exact=True)
            if save.count() != 1:
                raise RuntimeError("임시저장 버튼을 정확히 찾지 못했습니다.")
            save.click()
            page.wait_for_timeout(1500)
            page.screenshot(path="naver-after-save.png", full_page=False)
            print("임시저장을 클릭했습니다. 저장 완료 여부는 임시글 목록에서 직접 재확인해야 합니다.")
            print("확인되지 않은 저장을 성공으로 보고하지 않습니다. 사진 첨부와 발행은 직접 하세요.")
            input("검증을 마쳤으면 Enter를 눌러 브라우저를 닫으세요.")
        finally:
            context.close()


if __name__ == "__main__":
    main()
