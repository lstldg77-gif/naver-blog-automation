"""Experimental Naver draft saver. No publishing or photo uploads."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

PROFILE = Path.home() / ".naver_blog_automation_profile"
WRITE_URL = "https://blog.naver.com/lstldh?Redirect=Write&"

def load(path):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("JSON 객체가 필요합니다")
    for field in ("title", "body"):
        if not isinstance(obj.get(field), str) or not obj[field].strip():
            raise ValueError(f"{field} 누락")
    return obj

def fill_editor(page, title, body):
    for frame in page.frames:
        try:
            heading = frame.locator('.se-section-documentTitle .se-text-paragraph, .se-documentTitle .se-text-paragraph, [data-placeholder="제목"]').first
            content = frame.locator('.se-section-text .se-text-paragraph, .se-component-content .se-text-paragraph').first
            if not heading.count() or not content.count():
                continue
            heading.click(timeout=3000)
            page.keyboard.insert_text(title)
            content.click(timeout=3000)
            page.keyboard.insert_text(body)
            return True
        except Exception:
            continue
    return False

def save_draft(page):
    for frame in page.frames:
        try:
            button = frame.get_by_text("임시저장", exact=True).first
            if button.count() and button.is_visible():
                button.click(timeout=4000)
                return True
        except Exception:
            continue
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("draft")
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()
    data = load(args.draft)
    print(f"원고: {data['title']} / 본문 {len(data['body'])}자")
    if not args.interactive:
        print("DRY RUN: 네이버에 접속하거나 저장하지 않았습니다.")
        return
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(str(PROFILE), headless=False, locale="ko-KR")
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(WRITE_URL, wait_until="domcontentloaded")
        input("직접 로그인하고 글쓰기 화면을 연 뒤 Enter를 누르세요...")
        if not fill_editor(page, data["title"], data["body"]):
            print("에디터 자동 입력 실패. 저장하지 않았습니다.")
        else:
            print("브라우저에서 제목과 본문을 확인하세요.")
            if input("임시저장 승인: SAVE 입력 > ") == "SAVE":
                if save_draft(page):
                    print("임시저장 버튼 클릭됨. 실제 저장 여부는 아직 미확인입니다.")
                    print("네이버 임시저장 목록에서 제목과 본문을 확인하세요.")
                else:
                    print("임시저장 버튼을 찾지 못했습니다.")
            else:
                print("승인하지 않아 저장하지 않았습니다.")
        input("Enter를 누르면 브라우저를 닫습니다...")
        browser.close()

if __name__ == "__main__":
    main()
