# Zoom × さとうささら 音声認識・応答テスト環境まとめ
# ※ 本テスト環境は Voicemeeter Potato（複数仮想入力対応版）を使用しています。

## テスト構成の概要

**2台のPCを使用**
  - **PC1（あなた）**: Zoom会議を主催・参加（通常のアカウント）
  - **PC2（ささら）**: Zoomに「さとうささら」アカウントで参加
    - マイク: 仮想マイク（Voicemeeter Out B1等、CeVIOの出力が流れる）
    - スピーカー: 仮想スピーカーまたは物理スピーカー（Zoomからの音声をPythonで認識）
    - カメラ: OBS Studioの仮想カメラ（「さとうささら」シーンを定義し、Zoomで選択）

> ※OBS Studioで「さとうささら」シーンを作成し、仮想カメラを有効化することで、Zoom画面上で「ささら」としての視覚的識別が容易になります。音声認識・応答には直接関係しませんが、テストや実運用時の利便性向上のための設定です。

## 主要スクリプト

- `zoom-agent-sasara.py`
  - Zoom経由の音声を仮想マイクから認識（Google音声認識API）
  - OpenAI (ChatGPT) で応答生成
  - CeVIO「さとうささら」で音声合成しZoomへ返す
  - 会話履歴を維持し文脈を保った応答
  - 録音音声はデバッグ用に保存

- `voicemeeter_configuration.py`
  - 上記構成の物理・仮想デバイス間の音声ルーティングを図示

## テストの流れ

1. PC1でZoom会議を開始し、PC2（ささら）もZoomに参加
2. PC2で`zoom-agent-sasara.py`を起動
3. PC1からZoom経由で話しかける
4. PC2が音声認識→ChatGPT応答→CeVIO発声→Zoomマイク出力
5. PC1で「ささら」の自動応答を確認

## 注意点
- 仮想マイク・スピーカーのデバイスインデックスは環境に合わせて設定
- CeVIO・Voicemeeter・Zoomの音声入出力設定を正しく行う
- 音声認識失敗時は「うまく聞き取れませんでした」と発話

---

このMarkdownはテスト環境の現状理解・再現のための記録です。

---

## 音声ルーティング成立条件（ノード名対応）

### 「ささらの発話」

（CeVIO → SasaraMic → Zoom → あなたのスピーカー）

**成功条件（実際に動作した設定例）**
- CeVIO AI の「ツール → オプション → オーディオデバイス」を「Voicemeeter AUX Input」に設定
- ささら Zoom のマイク設定（SasaraMic）を「Voicemeeter Out B2」に設定


**B2 を選ぶ理由（Voicemeeter Potatoの仕様）**

- **B1** … Voicemeeter Input（メイン）と連動（PC全体の標準的な音声出力。多くのアプリやシステム音がここに集まる）
- **B2** … Voicemeeter AUX Inputと連動（AUX Input専用の出口。特定アプリの音だけを分離して出力できる）
- **B3** … Voicemeeter VAIO3 Inputと連動（追加用途。必要に応じて使い分け可能）

→ **B2を使うことで、AUX INPUT（CeVIOの発話）だけをZoomマイクに流し、他のPC音が混ざるのを防げる**

**その他の成立条件**
- あなた側のZoomスピーカー（UserSpk）が正常に音声を再生できること
- OBS Studioの映像出力は音声ルーティングに影響しない

### 「ささらの聞き取り」
（あなたのマイク → Zoom → SasaraSpk → Voicemeeter → Pythonスクリプト）


**成功条件（実際に動作した設定例）**
- PC2（ささら）のZoomスピーカーを「Voicemeeter VAIO3 Input」に設定
- VoicemeeterのVAIO3ストリップで「B3」ボタンをONにする（B3バスに音声が流れる）
- PythonスクリプトのVIRTUAL_MIC_INDEXを「Voicemeeter Out B3」に対応する番号（例: 5）に設定
  （デバイス一覧で「Voicemeeter Out B3 (VB-Audio Voicemeeter VAIO)」を選択）
- これにより、PC1の声がZoom経由でPC2のPythonスクリプトに正しく届き、認識できる

**その他の成立条件**
- あなたの発話がZoom経由でSasaraSpk（Zoomスピーカー）に届くこと
- Zoomのスピーカー設定が「Voicemeeter Input」等、SasaraSpkに対応していること
- VoicemeeterでSasaraSpkの出力がPythonスクリプト（Micデバイス）に正しくルーティングされていること
- PythonスクリプトのMicデバイスインデックス（VIRTUAL_MIC_INDEX）がSasaraSpkに対応していること
- CeVIOの設定はこの経路には影響しない

---

現状：
- 「ささらの発話」…OK（CeVIO→Zoomマイク→あなたへの音声伝達は正常）
- 「ささらの聞き取り」…課題あり（Zoomスピーカー→Voicemeeter→Python音声認識に問題）
