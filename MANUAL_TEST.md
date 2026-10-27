# 네이버 임시저장 수동 검증 체크리스트

1. 로컬 PC에서 `pip install -r requirements.txt` 및 `playwright install chromium` 실행
2. `python -m unittest discover -s tests`로 원고 검증 테스트
3. `python draft_tool.py drafts/example.json`으로 dry-run 확인
4. `python draft_tool.py drafts/example.json --interactive`로 로컬 브라우저 열기
5. 네이버에 직접 로그인하고 글쓰기 화면 진입
6. **자동 임시저장은 아직 구현되지 않음**. 수동 입력/임시저장 테스트는 사용자 승인 하에만 수행
7. Codex가 에디터 DOM을 점검한 뒤 입력과 임시저장 자동화를 구현하고, 제목과 본문을 다시 열어 검증해야 함
8. 사진 첨부와 발행은 사용자가 직접 진행. 자동 발행 기능 금지

오류 시 비밀번호, 세션 쿠키, 브라우저 프로필을 로그나 GitHub에 올리지 않습니다.
