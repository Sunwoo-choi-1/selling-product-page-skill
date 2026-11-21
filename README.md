# 잘 팔리는 상세페이지 스킬 세트

질문 10개에 답하면 **기획안 → 상세페이지 HTML → 스마트스토어·쿠팡 업로드 이미지**까지 만들어 주는 AI 스킬 (Claude Code · Codex).

- `selling-product-page/` — 상세페이지 스킬 (템플릿 4종: 연출형·정보설득형·매거진형·실사형, 카테고리 15종)
- `impeccable/` — 디자인 마감 스킬 (Apache 2.0)

버전 **2026-11-21** · 자세한 설치·사용법은 [`INSTALL.txt`](INSTALL.txt)

## 준비물

| | 필요한 것 |
|---|---|
| 꼭 | Claude Code(Pro 이상) 또는 Codex(ChatGPT 유료) |
| 꼭 | Python 3.10+ 와 `pip install playwright pillow` (업로드 이미지 뽑기). Windows는 Edge, Mac은 Chrome(없으면 `python -m playwright install chromium`) |
| AI 이미지 | 힉스필드(Higgsfield) 유료 구독 **또는** GPT 이미지(ChatGPT) — 둘 다 없으면 내 사진만으로 |
| 선택 | Git(깃허브 설치·업데이트), Node.js(힉스필드 CLI 방식일 때만) |

## 설치 (Claude Code)

**zip:** [Releases](../../releases)에서 `sangsepage-skill-set.zip` 받기 → 압축 풀고 두 폴더를 `~/.claude/skills/`에 넣기 → Claude Code 재시작

**git:**

```powershell
# Windows (PowerShell)
git clone https://github.com/Sunwoo-choi-1/selling-product-page-skill.git $HOME\sangsepage
Copy-Item -Recurse -Force $HOME\sangsepage\selling-product-page, $HOME\sangsepage\impeccable $HOME\.claude\skills\
```

```bash
# Mac
git clone https://github.com/Sunwoo-choi-1/selling-product-page-skill.git ~/sangsepage
mkdir -p ~/.claude/skills && cp -R ~/sangsepage/selling-product-page ~/sangsepage/impeccable ~/.claude/skills/
```

업데이트는 `git pull` 후 같은 복사 명령.

## 힉스필드 연결 (Claude)

MCP 주소 `https://mcp.higgsfield.ai/mcp` (API 키 없음, 로그인으로 연결)

1. **claude.ai / 데스크톱 앱:** 설정 → 커넥터 → 커스텀 커넥터 추가 → URL 붙여넣기 → 로그인·승인. 같은 계정의 Claude Code에도 그대로 보임.
2. **Claude Code 직접:** `claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp` → Claude Code에서 `/mcp`로 로그인.
3. **CLI 방식(Node.js):** `npm i -g @higgsfield/cli` → `higgsfield auth login` → `npx skills add higgsfield-ai/skills`

## Codex

두 폴더를 `~/.agents/skills/`(Windows `C:\Users\<이름>\.agents\skills\`)에 넣고 Codex 재시작 → `/skills`로 확인, `$selling-product-page`로 호출.
힉스필드: `codex mcp add higgsfield --url https://mcp.higgsfield.ai/mcp` → `codex mcp login higgsfield`.

## 사용

`/selling-product-page` 또는 "상세페이지 만들어줘"
