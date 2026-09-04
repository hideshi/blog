# Claim review

| ID | Draft claim | Source | Locator | Class | Status | Notes |
|---|---|---|---|---|---|---|
| C001 | Scholarly Agent Skills はソフトウェア開発の品質規範を論文執筆へ移植したオープンソースツール集である | hideshi-scholarly-agent-skills-repo | README.md | source-fact | verified | リポジトリの明記された目的および設計思想と一致 |
| C002 | 2026年8月27日時点で日本語版と英語版にそれぞれ23スキルが存在する | hideshi-scholarly-agent-skills-repo | skills/ja, skills/en (commit f5391e9) | source-fact | verified | 本文執筆時点のリポジトリ構成 |
| C003 | 25本のPythonスクリプトと23のテストモジュールがあり、ローカル検証で157件のユニットテストが通過した | hideshi-scholarly-agent-skills-repo | tests/ (commit f5391e9) | author-inference | qualified | 執筆時点の著者のローカル回帰テスト結果。将来の成果の正しさを保証するものではないと留保あり |
| C004 | Thesis-Driven Development はDDD、TDD、仕様ギャップ分析、不変条件監査を研究工程に読み替える | hideshi-scholarly-agent-skills-repo | README.md および各スキル定義 | source-fact | verified | 本文の表とスキルカタログの対応関係と一致 |
| C005 | Scholarly Agent Skills はMIT Licenseで公開されている | hideshi-scholarly-agent-skills-repo | LICENSE | source-fact | verified | リポジトリのライセンス表記と一致 |
| C006 | Scholarly Agent Skills は論文の正確性、網羅性、学術倫理、査読通過を保証しない | hideshi-scholarly-agent-skills-repo | DISCLAIMER.md | source-fact | verified | 免責条項と一致 |
| C007 | 低い層の認知負荷を外部化しつつ主張の強さ・採否・最終責任を人間に残す分業 | ogoshi-2026-cognitive-scaffolding | 論文要約および第3章 | source-fact | verified | 著者の Zenodo 論文の主旨と一致 |
| C008 | 外部資源の使用の有無ではなく、出力を検証・統合し使用に責任を持てるかを問う | ogoshi-2026-cognitive-pluralism | 論文要約および第4章 | source-fact | verified | 著者の Zenodo 論文の主旨と一致 |
| C009 | 人間が根拠を示し誤りを検出・訂正し採否を決定できる範囲を外部化の境界とする | ogoshi-2026-answerability-boundary | 論文要約および第2章 | source-fact | verified | 著者の Zenodo 論文の主旨と一致 |
| C010 | 単一のプロンプトではなく、入力を管理し出力を検査し採否と証拠を残す工程設計が重要である | — | — | recommendation | qualified | ソフトウェア工学の手法を研究・認知作業へ適用する実務的提言 |
