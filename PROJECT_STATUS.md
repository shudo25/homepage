# Project Status

**Last Updated**: 2026-10-17

---

## 🎯 Current Task

Working on: 同期生専用ページの情報構成とアクセス管理方針の検討

Next: まず現行の利用しやすさを保ち、運営側で段階的に検討する

---

**プロジェクト概要**: [README.md](README.md) と [COPILOT-INIT.md](COPILOT-INIT.md) を参照してください。

---

## 🔑 Current Focus

### 同期生専用ページ（docs/groupinfo/）

- 現在の掲載対象：名簿、写真集、動画・議論の記録
- 2026-10-19 準備幹事会ページに、同期生専用情報の掲載とアクセス管理方針を記録
- セキュリティと利用しやすさのバランスを重視し、当面は認証方式を変更しない
- 将来の選択肢として Google アカウント／Google Groups による限定共有を検討
- Google Groups 共有では、メンバーがGoogleアカウントで認証する必要がある。Gmail以外のアドレスもGoogleアカウントに登録できるが、利用者への案内・導入負担を確認してから判断する
- NHK動画は、共有フォルダの一覧をリンクから確認できることを確認済み。動画の掲載・共有方法は、アクセス制限と権利・利用条件を分けて検討する

---

## 📋 最近の作業

| 日付 | 内容 |
|---|---|
| 2026-10-17 | 同期生専用ページの今後の情報構成とアクセス管理方針を検討。認証方式は当面変更せず、段階的に進める方針を2026-10-19準備幹事会ページに記録 |
| 2026-05-17 | 同期生専用ページ：Google Drive方式移行（名簿・写真集14件・コピーボタン追加） |
| 2026-03-23 | 同期会向けレストラン情報調査（広島風お好み焼き・大人数対応） |

---

## ⏳ Next Steps

### Immediate
- 2026-10-19 準備幹事会で、同期生専用情報の掲載方針とアクセス管理について意見を確認
- 利用状況や同期生の負担を見ながら、認証方式の変更は急がず段階的に判断
- 動画・議論の記録セクションは、掲載内容と共有方法を整理してから追加を検討

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