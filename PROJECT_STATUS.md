# Project Status

**Last Updated**: 2026-05-17

---

## 🎯 Current Task

Working on: 同期生専用ページ（groupinfo）の整備完了  
Next: 本番ページで各リンクの動作確認、同期生への周知

---

**プロジェクト概要**: [README.md](README.md) と [COPILOT-INIT.md](COPILOT-INIT.md) を参照してください。

---

## 🔑 Current Focus

### 同期生専用ページ（docs/groupinfo/）

- ✅ パスワード認証ページ（`index.html`）
- ✅ 名簿：Google Drive リンク方式（パスワード保護済みPDF）
- ✅ 写真集：イベント別 Google Drive フォルダリンク（14件）
- ✅ メーリングリストアドレス表示＋コピーボタン

**パスワード**: `ohtoshi2026`  
**名簿PDF**: `H:\マイドライブ\Shudo\草野作業室\名簿　　草野\関東修道２５回（251122）_protected.pdf`（保護済み）

---

## 📋 最近の作業

| 日付 | 内容 |
|---|---|
| 2026-05-17 | 同期生専用ページ：Google Drive方式移行（名簿・写真集14件・コピーボタン追加） |
| 2026-03-23 | 同期会向けレストラン情報調査（広島風お好み焼き・大人数対応） |

---

## ⏳ Next Steps

### Immediate (This Session)
1. ✅ Create COPILOT-INIT.md with static conventions
2. ✅ Create PROJECT_STATUS.md with dynamic state
3. ✅ Add initialization reference to README.md
4. ⏳ Test initialization with Copilot ("Please read COPILOT-INIT.md to initialize")

### Short-term (Next Few Sessions)
- Review and refine INIT/STATUS content boundaries
- Update as work progresses on website or AI assistant
- Document any new conventions discovered
- Track compliance with AI Context Standard

### Medium-term (This Month)
- Continue website content updates as needed
- AI assistant development if needed
- Maintain separation: STATIC conventions in INIT, DYNAMIC state in STATUS

### Maintenance
- Update PROJECT_STATUS.md after each session (current task, recent work)
- Update COPILOT-INIT.md only when conventions change (rare)
- Keep clear boundary between static and dynamic content

---

## 📊 Status Summary

**Repository Health**: ✅ Active, well-organized

**Major Components**:
- Website (docs/): ✅ Stable, deployed
- AI Assistant v2 (ai_v2/): 🔬 Development, functional
- AI Assistant v1 (ai_codes/): 📦 Legacy, maintained
- Presentation Tools (present/): ✅ Stable (v3 final)
- Utilities (codes/): ✅ Functional

**Current Priorities**:
1. Context management implementation (in progress)
2. Website maintenance (as needed)
3. AI development (as needed)

**Blockers**: None

**Notes**: 
- AI Context Standard v0.4 adopted 2026-02-11
- Added axiomatic principles for human-AI collaboration
- First repository to implement this standard (and contribute to its evolution)
- COPILOT-PREMIUM-REQUEST-POLICY.md は古い情報（無視する）

---

## 📝 Session Notes

### How to Use This File

**At session start**:
1. Say: "Please read COPILOT-INIT.md to initialize"
2. Copilot reads INIT.md (conventions) and this file (status)
3. Check "Current Task" section for where to resume

**At session end**:
1. Update "Current Task" section with current state
2. Add achievement to "Recent Work" with date
3. Update "Last Updated" date at top
4. Commit changes

**This file should change frequently** (DYNAMIC content):
- Current focus shifts
- Recent work accumulates
- Next steps evolve
- Status summary updates

**COPILOT-INIT.md should rarely change** (STATIC content):
- Conventions stable over time
- Structure doesn't change often
- Only update when working patterns change

---

**For more details on this pattern**: See [AI_CONTEXT_STANDARD.md](AI_CONTEXT_STANDARD.md)