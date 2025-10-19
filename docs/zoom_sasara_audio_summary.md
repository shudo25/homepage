# Zoom・ささらさん・音声認識の現状まとめ

## 状況
- ささらさんの発話（CeVIO→Zoomマイク→あなたへの伝達）は正常に動作している
- ささらさんの聞き取り（Zoomスピーカー→Voicemeeter→Pythonスクリプトでの音声認識）は未解決

## テスト結果
- `test_mic_input.py` では音声が正常に録音・確認できている
- `zoom-agent-sasara.py` では音声認識（聞き取り）が未解決、もしくは認識精度に問題がある

## 今後の検証ポイント
- `zoom-agent-sasara.py` の録音音声（debug_audio_*.wav）が `test_mic_input.py` の録音と同じ品質か比較
- 認識失敗時のエラーメッセージや録音ファイルの内容を確認
- 認識部分のパラメータ（サンプリングレート、duration、phrase_time_limitなど）を `test_mic_input.py` と揃える

## 伝達経路の表現例
- CeVIO: CABLE Input (VB-Audio Virtual Cable)
- Voicemeeter (Stereo Input 1): CABLE Output
- Voicemeeter (Stereo Input 1) [B]: ON
- Zoom（ささら）マイク: Voicemeeter Out B1 (VB-Audio Voicemeeter VAIO)
- Zoom（ささら）スピーカー: Voicemeeter Input (VB-Audio Voicemeeter VAIO)
- Pythonスクリプト: Voicemeeter Out B1 (VB-Audio Voicemeeter VAIO)

## 今後の方針
- 録音ファイルやエラーメッセージを比較・検証し、問題の切り分けを進める
- 必要に応じてパラメータやルーティングを調整

---
このまとめをもとに、別環境でも作業を再開できます。
