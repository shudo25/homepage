# Project Status

**Last Updated**: 2026-03-23

---

## 🎯 Current Task

Working on: 同期会（首都圏メンバー）向けレストラン情報調査
Next: 次の同期会イベント企画への対応
See: [COPILOT-INIT.md](COPILOT-INIT.md), [PROJECT_STATUS.md](PROJECT_STATUS.md), [AI_CONTEXT_STANDARD.md](AI_CONTEXT_STANDARD.md)

---

**プロジェクト概要**: [README.md](README.md) と [COPILOT-INIT.md](COPILOT-INIT.md) を参照してください。

---

## 🔑 Current Focus

### AI Context Management Implementation (2026-02-11)

このレポジトリに AI Context Standard v0.3 パターン（INIT.md + STATUS.md）を実装中：

- ✅ AI_CONTEXT_STANDARD.md を追加（標準の提案文書）
- ✅ COPILOT-INIT.md を作成（静的な作業規約）
- ✅ PROJECT_STATUS.md を作成（動的な状態トラッキング）
- ⏳ README.md への参照追加（次のステップ）

**目的**: 
- Copilot セッション間でのコンテキスト維持
- 静的な作業規約と動的な状態の明確な分離
- より一貫性のあるAIアシスタントの動作

---

## 🎯 Recent Work

### 2026-03-23: 同期会向けレストラン情報調査
- 大利君の要望：お好み焼き会の会場拡大（ソニア新橋5丁目が8名ギリギリのため）
- 条件：広島風お好み焼き、大人数対応（10名以上）
- 調査結果（2候補）：
  - **花子 飯田橋店**（九段下駅5分）: 広島風専門、貸切20〜50名可、食べログ百名店選出
    https://tabelog.com/tokyo/A1309/A130906/13267964/
  - **うさぎ**（原宿駅3分）: 広島風専門、コース最大18名、貸切20〜50名可
    https://tabelog.com/tokyo/A1306/A130601/13129954/

### 2026-02-11: AI Context Standard v0.4 Update
- Enhanced AI_CONTEXT_STANDARD.md with "How to Use This Standard" section
- Added axiomatic principles for human-AI collaboration (like mathematical axioms)
- Clarified distinction: "apparent high performance" (template application) vs "true high performance" (creative adaptation)
- Emphasized that AI capability requires axiomatic approach to achieve true collaboration
- Templates are examples to illustrate, not rules to copy
- Updated COPILOT-INIT.md to reference v0.4
- Maintained simplicity: ~300 words added, foundational changes with explicit warning about mechanical vs collaborative AI use

### 2026-02-11: AI Context Standard Implementation
- Added AI_CONTEXT_STANDARD.md (v0.3 proposal document)
- Created COPILOT-INIT.md with repository conventions
- Created PROJECT_STATUS.md for dynamic state tracking
- Documented website structure, AI development setup, and common tasks
- Established failure recovery protocol (stop after 3 failures)

### Earlier Work (Before Status Tracking)

このファイル作成以前の作業履歴はGitログを参照してください。主な内容：

- **Website content**: 修道25回生サイトのコンテンツ開発
- **AI assistant development**: 
  - ai_codes/ - 初期バージョン（音声認識、Zoomエージェント）
  - ai_v2/ - 改良バージョン（サーバーアーキテクチャ、TTS分離）
- **Presentation tools**: PowerPoint自動生成ツール（v3 final）
- **Utilities**: PDF/写真暗号化、メンバーリスト管理

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