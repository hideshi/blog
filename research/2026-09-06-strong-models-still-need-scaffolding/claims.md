# Claims verification

| ID | Draft claim | Source | Locator | Class | Status | Notes |
|---|---|---|---|---|---|---|
| C001 | GPT-6 Astraはコード、ブラウザ、業務ソフトウェアをまたぐ複数段階のワークフローに強い | openai-gpt-6-astra-model-guidance | Introduction | source-fact | verified | 公式文書の説明と一致 |
| C002 | Astraは従来モデルより指示追従が強く、SkillsやAGENTS.mdの指示へ敏感なため監査が推奨される | openai-gpt-6-astra-model-guidance | Prompting best practices > Instruction following | source-fact | verified | 曖昧・競合指示が停止やブロックにつながり得るとの留保を本文へ反映 |
| C003 | GPT-5.6 Solは複雑な専門作業向けで、Skills、MCP、Tool search、File searchをサポートする | openai-gpt-5-6-sol-model | 冒頭およびTools | source-fact | verified | 公式モデルページと一致 |
| C004 | CodexではAGENTS.md、Skills、MCPがそれぞれ永続指示、再利用可能なワークフロー、外部接続を担い、相互補完する | openai-codex-customization | 冒頭、AGENTSガイダンス、スキル、MCP | source-fact | verified | 公式カスタマイズ文書と一致 |
| C005 | cc-sddは仕様を巨大な命令書ではなくシステムの各部分が守る約束事と捉え、その範囲内では実装方法をエージェントが選べるとする | cc-sdd-philosophy | The short version、Specification vs Design | source-fact | verified | contractとfree exploration spaceの意味を一般向けの語で本文へ記載 |
| C006 | cc-sddのtasks.mdは成果物を実装可能な単位へ分解し、並列化可能な波を示す | cc-sdd-spec-driven-workflow | Long-Running Autonomy Depends on the Spec Harness、Lifecycle Overview > Task Planning | source-fact | verified | P0、P1等の具体表記は本文では省略 |
| C007 | Zenn記事のTypeScript事例ではレビュー用コンテキストが9,272〜142,188トークンから約70トークンになった | helloworld-knowledge-graph-2026 | 実測データ > トークン削減 | source-fact | qualified | 単一プロジェクトの報告であり一般ベンチマークではないと本文で限定 |
| C008 | 同事例では意味検索、間接依存の追跡、LSPによる定義・実装位置の取得を報告している | helloworld-knowledge-graph-2026 | 実測データ > 意味検索、影響範囲、型確定 | source-fact | verified | 記事内の実測として記述 |
| C009 | Zenn記事ではルーティングルールのもとで、ツール名を指定しない9種類の質問が意図したツールへ振り分けられた | helloworld-knowledge-graph-2026 | 実測データ > ルーティング | source-fact | qualified | 著者の2リポジトリでの報告。Astra／Solの検証ではない |
| C010 | Zenn記事は古いグラフが誤情報の原因になると注意している | helloworld-knowledge-graph-2026 | 使い方 > グラフを最新に保つ | source-fact | verified | 更新方法がツールごとに異なる点も確認 |
| C011 | 同記事のセキュリティスキャンでは仕込んだSQLインジェクション、秘密鍵、evalを検出できなかった | helloworld-knowledge-graph-2026 | 実測データ > ルーティング直後のセキュリティ検証 | source-fact | verified | ツール選択と検出能力を区別する例として使用 |
| C012 | 検索基盤はAstraにもSolにも効果が見込め、Solの相対改善幅が大きい可能性がある | — | — | author-inference | qualified | Astra／Solの直接比較データも筆者自身による比較実験もなく、本文で筆者の推論と明示 |
| C013 | Astra向けの棚卸しでは要件・変更範囲・完了条件を残し、重複指示や実装の細かな操作指定を減らすべきである | — | — | recommendation | qualified | OpenAIの監査推奨と、仕様で守る条件と実装判断を分ける一般原則から導く実務提案。cc-sddは具体例として参照 |
| C014 | 検索基盤はrgとLSPから始め、観測した探索上の問題に応じて意味検索や依存グラフを追加すべきである | — | — | recommendation | qualified | 導入・更新コストを踏まえた段階的導入案 |
| C015 | CodexはSkillのメタデータを先に参照し、選択後にSKILL.md、必要に応じてリファレンスやスクリプトを利用する | openai-codex-customization | スキル > 段階的開示 | source-fact | verified | 多数のSkillが直ちに全文コンテキスト化されるわけではないことの根拠 |
| C016 | 多数のSkillは個数ではなく、AIに任せる作業、呼び出される条件、成果物、検証方法の重複で棚卸しすべきである | — | — | recommendation | qualified | OpenAIの段階的開示とAstraの指示感度を踏まえた分類・運用案 |
| C017 | Skillは専門領域の知能を追加するというより、現場で必要な確認事項と、人が判断すべき場面を再利用可能にする | — | — | author-inference | qualified | 本稿におけるSkillの機能的な読み替え |
| C018 | 既存のSkill、仕様と検証の仕組み、検索基盤は、代表作業とファイル上の根拠を使い、点検と修正を分けて改善すべきである | — | — | recommendation | qualified | 付録の実務用プロンプトとして具体化。困りごとが不明な場合は根拠のある候補と確認方法を出し、削減数ではなく成果と失敗の変化を評価する |
| C019 | ナデラは「トークン資本」を、企業が構築し所有するAI能力として説明している | nadella-frontier-ecosystem-2026 | 「Every company is going to have to build」から始まる段落 | source-hypothesis | qualified | 本人による経営上の概念。確立した会計用語や実証結果としては扱わない。Xは取得時に直接閲覧できず、同一投稿IDの転載と複数報道で本文を照合 |
| C020 | ナデラはトークン資本の具体例として、文脈、Skill、モデルの重みを挙げ、自社で所有・管理し、改善を重ねる仕組みを求めている | possible-nadella-token-capital-2026 | Transcript、SATYA発言、段落134–137 | source-hypothesis | verified | 本人への対談全文で文脈と限定を確認 |
| C021 | 仕様、Skill、評価基準、検索できる社内知識は、モデルをアップグレードまたは廉価なモデルへ切り替えても残る組織固有のAI活用力と捉えられる | — | — | author-inference | qualified | C019・C020のtoken capitalを本稿の対象へ当てはめた筆者の読み替え。技術的効果の証明ではないと本文で限定 |
| C022 | Astra向けの棚卸しで成果物、変更範囲、完了条件、検証方法を残し、環境固有の部分を分離したSkillの中核は、低コストモデルでも再利用しやすい | — | — | author-inference | qualified | 筆者自身によるモデル間比較は未実施で、モデル間・実行環境間の完全互換を意味しない。切り替え先で取りこぼした判断点は代表タスクの結果に基づいて戻すという条件を本文で明記 |
| C023 | GPT-6 AstraはGPT-5.6 Solなどの従来モデルより高い知能と能力を持つとOpenAIが説明している | openai-gpt-6-astra-model-guidance | Prompting best practices 冒頭 | source-fact | verified | 公式文書の「more intelligent and capable than prior models like GPT-5.6 Sol」に対応 |
| C024 | KiroのFeature Specsには要件先行と設計先行の二つの流れがあり、案件に応じて選べる | kiro-feature-specs | Workflow Variants | source-fact | verified | 特定の工程順を仕様駆動開発全体の定義にしない根拠として使用 |
| C025 | cc-sddはKiroに着想を得て、複数のAIコーディング環境へ仕様駆動の流れを展開するOSS実装である | cc-sdd-readme | 冒頭、Kiro-inspiredおよびSupported Agents | source-fact | verified | cc-sddを仕様駆動開発全体の代表ではなく一実装として位置づける |
| C026 | 本稿では仕様駆動開発を、実装で守る条件と判断の根拠を、確認・更新できる成果物として残す進め方と広く捉える | — | — | author-inference | qualified | 業界全体の標準定義ではなく、本稿の議論に必要な操作上の捉え方として明示 |
| C027 | 本稿は筆者自身によるAstraと複数の低コストモデルの比較実験ではなく、Skillの再利用性と検索基盤のモデル間効果は未検証である | — | — | author-inference | verified | 記事の根拠範囲を示す注記。同じ成果が得られると一般化していないことを本文に明記 |
