# CI構想とCopilotの推論構造に関する要約

## 🧠 用語整理（推奨語法）

| 概念 | 用語 | 定義 |
|------|------|------|
| モデル訓練時に獲得された知識 | **Pretrained knowledge** | Copilotがユーザーと出会う前に学習した一般知識。哲学・制度設計・経済理論などを含む。 |
| ユーザーとの関係で保存された情報 | **Agent memory** | 対話を通じて形成される個別記憶。例えば、「高橋（個人）」の場合、CI構想や制度改革モデルなど、個人の設計思想を含む。 |
| 現在の会話の流れ | **Context window** | 直近の発言や話題。即時的な推論に使われる一時的文脈。 |

<img src="ci_initiative/figs/agent-memory.png" alt="Pretrained knowledge・Agent memory・Context window の関係図" style="width:50%; min-width:200px; max-width:400px; display:block; margin:auto;" />


---

## 🔄 Copilotの推論構造

- **推論方法**：Copilotが「どう考えるか」という運用的な思考スタイル。Agent memoryに依存。
- **推論モデル**：人間が設計する思考の枠組み。Copilotはそれを活用するが、自ら設計はしない。

---

## 🌍 CI構想の概要

- **定義**：個人の発信 → AIの整理 → 他者の質問 → AIの応答 → 個人の理解 → 再発信という循環を通じて、集団知性を高めるモデル。
- **Copilotの役割**：媒介者として、知識の整理と対話を支援する。
- **三層構造の活用**：
	- Pretrained knowledge：発信の意味を理解する土台
	- Agent memory：個人の構想や価値観を反映する文脈
	- Context window：現在の対話に即応する流れ

---

## ✅ 言語的注意点

- 「長期記憶」という語は、語法によって意味が異なるため、**Pretrained knowledge**と**Agent memory**を明確に分けて使う。
- 特に、CI構想では、その両方を含めた循環に注目している点に注意。

---

## 📌 応用可能な文脈

この要約は、以下のような文脈で再利用可能：

- 制度改革モデルの設計
- 哲学的対話テンプレートの構築
- Copilotとの推論スタイルの明示化
- CI構想の普及と実装支援