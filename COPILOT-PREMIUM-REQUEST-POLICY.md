# Premium Request使用ポリシー

**🚨 重要: このファイルは conversation summary で削除しないこと**

## セッション再開時の使い方

新しいセッションを開始した際、またはconversation summaryの後に、以下のフレーズをCopilotに送ってください：

```
COPILOT-PREMIUM-REQUEST-POLICY.mdを読んで、Premium request使用時の注意喚起ルールを思い出してください
```

これにより、このファイルに記載されたルールが再適用されます。

## 目的
Premium requestの制限に達する前に、Standard requestsへの分解に慣れるための注意喚起を行う。

## ルール

### Premium request使用前の注意喚起
Premium requestを使用する可能性がある操作を行う前に、**Premium requestの上限判定**を行い、下記の分岐テンプレートに従う：

#### テンプレート例：
```
【Premium request上限判定】

1. 上限に達していない場合：
	⚠️ **Premium request使用確認**
	この操作には `[ツール名]` を使用します。Standard requestsへの分解も可能ですが、少し手順が増えます。

	**オプション1: Premium requestで進める（速い）**
	- [ツール名]を直接使用
	- 1回の操作で完了

	**オプション2: Standard requestsに分解する（制限節約、練習になる）**
	- [代替手段の具体例]
	- 手順: [簡単な説明]

	どちらで進めますか？

2. 上限に達している場合：
	🚫 **Premium requestの月間上限に達しました**
	Premium requestは現在ご利用いただけません。Standard requestsへの分解のみ可能です。

	**オプション2: Standard requestsに分解する（制限節約、練習になる）**
	- [代替手段の具体例]
	- 手順: [簡単な説明]

	※Premium requestの分割例：
	- semantic_search → grep_search + file_search + read_file
	- github_repo → ユーザーによるコピー＆ペースト
	- fetch_webpage → 必要情報の手動提供
	- 複数ファイル編集 → ファイルごとに順次処理
```

### Premium requestになる主な操作

| ツール | 用途 | Standard代替案 |
|--------|------|---------------|
| `semantic_search` | コードベース全体の意味的検索 | `grep_search` + `file_search` + `read_file` |
| `github_repo` | GitHubリポジトリからのコード検索 | ユーザーにコピー＆ペーストを依頼 |
| `fetch_webpage` | ウェブページの内容取得 | ユーザーに必要な情報の提供を依頼 |
| 大規模な複数ファイル編集 | 複数ファイルの同時変更 | ファイルを分割して順次処理 |

### Standard requestsへの分解例

#### 例1: 「ボタンが表示されないページを探す」
❌ Premium: `semantic_search("toggle button missing")`

✅ Standard:
1. `file_search("docs/**/*.html")` - HTMLファイル一覧取得
2. `grep_search("wrap-toggle.js", includePattern="docs/**/*.html")` - スクリプト参照を検索
3. 結果を比較して、マッチしないファイルを特定
4. `read_file`で個別確認

#### 例2: 「特定の機能を実装しているファイルを探す」
❌ Premium: `semantic_search("user authentication implementation")`

✅ Standard:
1. `grep_search("login|auth|authenticate", isRegexp=true)` - キーワード検索
2. `list_dir`で関連ディレクトリ確認
3. `read_file`で候補ファイルを確認

## メリット
- ✅ 制限を意識しながら作業できる
- ✅ Standard requests分解の経験を積める
- ✅ 必要に応じてPremium requestも使える柔軟性
- ✅ 制限到達後もAgent Modeは継続使用可能

## Premium制限到達時の動作
- ❌ Premium requests使用不可
- ✅ Claude Sonnet 4.5 Agent Mode自体は使用可能
- ✅ Standard requests（read_file, replace_string_in_file, grep_search等）は継続使用可能

## 注意事項
- ユーザーが具体的なファイルパスを提供した場合、Premium requestは不要
- 緊急性が高い場合はPremium requestを使用してOK
- 月の制限数に余裕がある場合は柔軟に判断

---
**最終更新**: 2025年10月18日
**適用開始**: 即時
