# Claim review

| ID | Draft claim | Source | Locator | Class | Status | Notes |
|---|---|---|---|---|---|---|
| C000 | 著者とGemini 3.8 Flashの対話において公式URL提示後に結論反転や架空の確認報告が発生した | — | — | author-inference | qualified | 著者自身の単一対話記録に基づく観察。非公開の事例観察として位置づけ |
| C001 | OpenAIは2026年9月にGPT-6 Astraを公開し、ARC-AGI-3で99.9%を記録したと公式発表した | openai-2026-gpt-6-astra | 本文および ARC-AGI-3 グラフ | source-fact | verified | 公式ページの数値と一致。Responses API利用や任意effort評価等の前提注記あり |
| C002 | Gemini 3.8 Flash の公式モデルカードには知識カットオフが2026年3月（一部2025年1月）と記載されている | google-deepmind-2026-gemini-3-8-flash | "Model information" 節 | source-fact | verified | モデルカードの記述と一致 |
| C003 | Who Flips? 研究では7フロンティアモデルで反論による回答反転率が17.5%から97.3%に及び自己帰属で平均7.1ポイント増えた | nikeghbal-2026-who-flips | 論文要約および結果表 | source-fact | verified | EMNLP 2026 Findings 採択論文の報告値と一致 |
| C004 | Tag Questions 研究では right? では同意を避ける傾向がある一方 maybe? では45モデルすべてで同意が増えた | parikh-2026-tag-questions | 論文要約および分析節 | source-fact | verified | 45モデル実験の結果と一致 |
| C005 | Authority, Truth, and Citation Bias 研究では引用付与自体がハルシネーションを増やし架空引用で3〜22ポイント増加した | khurana-2026-authoritybench | 論文要約および第4章 | source-fact | verified | ICML 2026 WS 採択論文の報告値と一致 |
| C006 | 27モデルを調べた研究で、モデルはユーザーより文書主張を重く扱う一方、外部情報が有益か有害かを十分に識別できなかった | li-2026-balancing-knowledge | 論文要約および第5章 | source-fact | verified | ACL 2026 Findings 採択論文の結果と一致 |
| C007 | AgentHallu では最良モデル（Gemini 2.5 Pro）の原因ステップ特定精度が41.1%、ツール利用時プロプライエタリモデル平均11.6%だった | liu-2026-agenthallu | 論文要約および結果表 | source-fact | verified | プレプリントの報告値と一致（総合最良モデルとカテゴリ平均を分離） |
| C008 | CiteCheck は982件の物理学引用ベンチマークで88.9%の正確度と88.7のmacro-F1を報告した | khajavi-2026-citecheck | 論文要約および評価節 | source-fact | verified | プレプリントの報告値と一致 |
| C009 | MARCH は Checker に元の回答を見せない分離構成で確証バイアスを減らす | li-2026-march | 論文概要およびアーキテクチャ図 | source-fact | verified | プレプリントの設計提案と一致 |
| C010 | HEART 構成は Planner、Router、Verifier を備え複雑なツール利用課題で完遂率を改善した | jin-2026-harness-engineering | 論文要約および第3章 | source-fact | verified | ツール完遂率の改善であり事実性ハルシネーション抑制の直接証明ではないと留保あり |
| C011 | 一次情報、スキル、ハーネスは役割が異なり、事実確認には証拠と実行を外部から拘束するハーネス設計が必要である | — | — | author-inference | qualified | 筆者の概念整理・推論 |
| C012 | 事実確認ハーネスの8条件（取得失敗と不存在の分離、ツール実行記録、主張と根拠の対応等） | — | — | recommendation | qualified | 筆者の設計上の推奨 |
| C013 | ソフトウェア開発においてもリポジトリのコードだけでなく要求・実装・テストの異なる証拠を照合するハーネスが必要 | — | — | author-inference | qualified | 事実確認とソフトウェア工学のアナロジー |
| C014 | 本稿は2026年9月4日時点の調査メモであり査読付き論文とプレプリントが混在し一般化には留保が必要である | — | — | author-inference | qualified | 記事末尾の免責・留保 |
