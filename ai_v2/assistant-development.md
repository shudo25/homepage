# 進行アシスタント開発の要点まとめ

## 1. プロジェクト構成・リファクタリング
- 共通関数を `utils/` サブフォルダに整理
- Assistantクラスを `Assistant.py` に分離
- TTS（CeVIO）や LLM（LangChain）もオブジェクト指向で分離

## 2. 会話エンジン・文脈管理
- LangChainの `ConversationBufferMemory` で会話履歴を自動管理
- Assistantクラスに `save_context`・`load_context` を実装し、会話文脈を `context.json` で保存・復元
- LangChainの新仕様（`messages_to_dict`/`messages_from_dict`）に対応

## 3. TTSサーバ方式
- CeVIOのライセンス制限に配慮し、TTSサーバ（Flask）を独立プロセスで起動
- Assistantクラスの `speak` はTTSサーバ（HTTP経由）にリクエスト送信
- どのUI/プロセスからも安全に発声可能

## 4. WebUI（Flask + Socket.IO）
- チャットUI（送信・直接発声・発声ON/OFF・文脈保存・終了ボタン）
- 文脈保存・復元・サーバ終了をSocket.IOイベントで制御
- サーバ起動・終了時に自動で文脈を保存

## 5. 統合起動
- `main_server.py` でTTSサーバとWebUIサーバをサブプロセス方式で一括起動・終了

## 6. 移植性・運用
- `context.json` をコピーすれば、別マシンでも文脈を引き継いで作業可能
- Copilotチャットの履歴は手動でテキスト保存