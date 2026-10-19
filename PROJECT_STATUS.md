# Project Status

**Last Updated**: 2026-10-19

---

## 🎯 Current Task

Working on: 基調コンセプト「倫理とAI」の背景を別ページの考察メモに記録し、同期会ページからリンク

Next: 今晩の準備幹事会で「倫理とAI」のコンセプト案とサイト改訂を共有する。今晩の準備はいったん完了し、幹事会の意見を受けて内容を具体化する。

---

**プロジェクト概要**: [README.md](README.md) と [COPILOT-INIT.md](COPILOT-INIT.md) を参照してください。

---

## 🔑 Current Focus

### 同期生専用ページ（docs/groupinfo/）

- 現在の掲載対象：名簿・連絡先、集いの記録、同期生の知恵と情報
- 2026-10-19：情報共有の目的と最初のテーマ（ネットの安全対策）、情報提供の窓口を追加。個別動画の内容・再生時間・推奨順は未確認のため準備中と明示
- 「集いの記録」に気楽に集まる会の報告への入口を追加。公開側には活動紹介と同期生ページへの導線を設置
- 気楽に集まる会の既存報告・写真はまだ公開状態。認証・保管先は変更せず、公開範囲を各画面に明示。今回の導線変更は非公開化ではない
- 同期生情報ページに「動画集」を追加し、Google Driveの動画フォルダへのリンクと「動画共有についての議論の記録」（要約・折りたたみ表示）を設置。動画ファイルの取得・再配信や認証方式の変更は行っていない
- 検証済み：ローカルブラウザーで320px・390px・1280px幅の同期生ページを確認し、横はみ出しなし。既存の名簿・写真14件のリンク設定、未認証時のログインページへの遷移、議論記録の開閉、変更対象HTMLの内部リンク・アンカーとIDの重複なしを確認。Drive内の動画の実再生は未確認
- 2026-10-19 準備幹事会ページに、同期生専用情報の掲載とアクセス管理方針を記録
- セキュリティと利用しやすさのバランスを重視し、当面は認証方式を変更しない
- 将来の選択肢として Google アカウント／Google Groups による限定共有を検討
- Google Groups 共有では、メンバーがGoogleアカウントで認証する必要がある。Gmail以外のアドレスもGoogleアカウントに登録できるが、利用者への案内・導入負担を確認してから判断する
- NHK動画は、共有フォルダの一覧をリンクから確認できることを確認済み。動画の掲載・共有方法は、アクセス制限と権利・利用条件を分けて検討する

### 運営ミーティングの一覧

- メモは公開を維持し、トップページには更新時点の直近１年分を掲載する。2026-10-19更新時は2025-10-19以降の８件を掲載し、今晩の第２回準備幹事会を先頭に追加。
- それ以前の５件は `docs/meetings/archive.html` に整理。元のメモのURLは変更しない。
- 静的HTMLのため、次回一覧を更新する際にも直近１年の境界を見直し、古い項目をアーカイブに移す。

### 2026-11-28 同期会ページ

- 昨年の構成をもとに、ささらの画像、会場情報・画像、基調コンセプト、進行概要、BGMを今年のページに仮置き。画像は既存の昨年のファイルを参照し、重複保存しない。
- 日付は2026-11-28（土）、参加登録先は今年の伝助に更新。開催時間・会場は引き続き予定として掲載。
- 昨年と同じOZmallプランをベースに、メイン料理を「鶏もも肉グリル」から山形牛へ変更。これに伴い会費を6,000円から6,500円へ変更した旨を会場欄に注記（高橋さんからの情報）。
- 昨年の集合写真は今年のページには掲載しない。昨年の記録ページや元画像は変更・削除しない。
- 基調コンセプトを今年の提案「倫理とAI」に更新。昨年のCI構想を変更せず、倫理の角度から提案する意図。
- 起点は鈴木俊貴さんのほぼ日インタビュー（2025-08-01、https://www.1101.com/n/s/toshitaka_suzuki/2025-08-01.html）。記事の鳥の欺きの事例を確認し要約。倫理の起源・生命／宇宙進化への接続は発信者の哲学的な問いであり、記事が証明する事実とは区別する。
- 鳥の欺き → 倫理の起源・進化 → AIによる変化 → 悪用への対処 → 同期生の助け合い、という14分＋予備1分の構成案を掲載。原稿・演出・ささらの担当は未確定。その他の進行とBGMは昨年をもとにした仮案のまま。
- 発信の狙いは、倫理を人間社会だけの問題ではなく、生命・宇宙進化に関わる根底的な問いとして捉え、AIによる大きな変化と悪用への対処を同期生どうしで考えるきっかけにすること。昨年のCI構想を、別の角度から提案する。
- 時間配分のたたき台：小鳥の「嘘」2分、倫理の起源・進化3分、AIによる変化3分、悪用への対処4分、同期生の助け合い2分、予備1分。宇宙進化の詳細な講義ではなく、問いの提示から身近な確認・相談・助け合いへつなぐ構成案。
- 2026-10-19朝：高橋さんが今晩の準備として十分と判断し、ここでいったん区切った。コンセプト案・進行項目・構成案はコミット `26ec203` で `main` にプッシュ済み。幹事会での承認や講演原稿の完成を意味しない。
- その後の対話を [考察メモ](docs/events/20261128/ethics-and-ai.html) に整理し、基調コンセプトからリンク。「鳥に倫理観があるか」ではなく「嘘の発生が倫理という問題を提起する」という高橋さんの視点を記録。
- 情報伝達と欺きの対のほぼ同時の発生、生物とウイルスの起源をめぐる着想を記録。構造上の可能性と歴史的な同時発生、自然の説明と善悪の判断を区別。ウイルスの起源は未検証であり確定した事実とせず、AIへの接続も哲学的考察として扱う。
- 考察メモに『論語』衛霊公篇の「恕」「己の欲せざる所人に施すこと勿かれ」を追加。倫理は結局「恕」に尽きるのではないかという高橋さんの考えを記録し、欺きの問題とAIを作る・提供する・使う側の姿勢につなげた。

### 利用促進とアクセス管理の進め方（2026-10-19 高橋さんとの相談で合意）

- まず同期生に使ってもらい、役立つ情報共有の場に育てる。セキュリティの厳密性を先行させて、ウェブサイトの活用を妨げないことを重視する。
- 「リンクを知っている全員」が閲覧できる共有設定の改善には時間をかける。当面は、既存の認証方式やGoogleドライブの共有設定を変更しない。
- 詳しい活動記録は同期生向けの情報として整理する。ただし、技術的に同期生だけに閲覧を制限できているとは説明しない。導線の整理と実際のアクセス制限は区別する。
- 氏名・写真などの掲載範囲に配慮し、特に機微な情報は現行の共有方法では掲載しない。
- 利用状況や同期生の声、導入の負担を見ながら、必要なところからアクセス管理を段階的に改善する。
- 画面では「何に役立つか」「どう使えるか」を前面に出し、運営上の注意は簡潔にまとめる。ただし、閲覧制限の実態について誤解を招く表示はしない。
- これは高橋さんとAIアシスタントの相談で合意した作業方針であり、幹事会で承認済みの決定ではない。アクセス管理と、資料の著作権・利用条件の確認は別の論点として扱う。

---

## 📋 最近の作業

| 日付 | 内容 |
|---|---|
| 2026-10-19 | 基調コンセプト案「倫理とAI」を追加。起点の記事を確認し、記事の事例と哲学的な問いを区別した15分以内の構成案・進行項目を掲載 |
| 2026-10-19 | 11/28同期会ページに昨年の内容を仮置き。日付・参加登録先を更新し、集合写真は掲載せず、未確定の内容を明示 |
| 2026-10-19 | 運営ミーティング一覧を直近１年の８件と過去５件に分割。本日の幹事会リンク、公開アーカイブ、サイトマップの項目を追加 |
| 2026-10-19 | 同期生ページの目的別構成と情報共有テーマを追加。活動紹介と詳しい記録の入口を整理し、既存報告・写真が公開のままであることを明示。限定共有への移行は未実施 |
| 2026-10-18 | 「動画集」の名称を決定。同期生情報ページにDriveフォルダへの導線と動画共有についての議論の要約を追加。動画の要旨は未掲載、実機での動画再生は未確認 |
| 2026-10-17 | 同期生専用ページの今後の情報構成とアクセス管理方針を検討。認証方式は当面変更せず、段階的に進める方針を2026-10-19準備幹事会ページに記録 |
| 2026-05-17 | 同期生専用ページ：Google Drive方式移行（名簿・写真集14件・コピーボタン追加） |
| 2026-03-23 | 同期会向けレストラン情報調査（広島風お好み焼き・大人数対応） |

---

## ⏳ Next Steps

### Immediate
- 2026-10-19 準備幹事会で「倫理とAI」の基調コンセプト案と15分以内の構成案を共有し、意見を確認。原稿・ささらとの役割分担の具体化はその後に進める。
- 2026-10-19 準備幹事会で、同期生専用情報の掲載方針とアクセス管理について意見を確認
- 利用状況や同期生の負担を見ながら、認証方式の変更は急がず段階的に判断
- 動画集のDriveプレビューで再生できるか利用者の環境で確認し、必要に応じて提供された要旨を追加

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