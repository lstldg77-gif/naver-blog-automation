"""Local, human-approved Naver draft assistant. Never publishes or uploads images."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BLOG_URL = "https://blog.naver.com/lstldh"

def load_draft(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("원고는 JSON 객체여야 합니다.")
    for key in ("title", "body"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"{key} 값이 비어 있습니다.")
    if len(data["title"]) > 100:
        raise ValueError("제목이 너무 깁니다(100자 초과).")
    return {"title": data["title"].strip(), "body": data["body"].strip()}

def main():
    parser = argparse.ArgumentParser(description="Naver draft helper: dry-run by default")
    parser.add_argument("draft", help="UTF-8 JSON 원고 경로")
    parser.add_argument("--interactive", action="store_true", help="브라우저 열기 (임시저장은 수동 확인)")
    args = parser.parse_args()
    draft = load_draft(args.draft)
    print(f"원고 확인: {draft['title']} / 본문 {len(draft['body'])}자")
    if not args.interactive:
        print("DRY RUN: 네이버에 접속하거나 저장하지 않았습니다.")
        return
    print("로그인은 직접 하세요. 이 버전은 임시저장 자동화를 수행하지 않습니다.")
    profile = Path.home() / ".naver_blog_automation_profile"
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(str(profile), headless=False, locale="ko-KR")
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(BLOG_URL, wait_until="domcontentloaded")
        print("브라우저에서 네이버 글쓰기 화면을 열고 원고를 입력하세요.")
        input("작업을 마친 뒤 Enter를 눌러 브라우저를 종료합니다...")
        browser.close()

if __name__ == "__main__":
    main()
