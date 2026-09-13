# 主張と原典の対応

本稿は移行評価の設計を提案する記事。特定モデルの比較、各フレームワークの接続、評価ケースの実行は行っていない。本文のケースとひな型は設計例であり、観測結果ではない。前稿のモデル性能に関する記述を本稿の証拠として再利用していない。

| ID | Draft claim | Source | Locator | Class | Status | Notes |
|---|---|---|---|---|---|---|
| C001 | Agent SkillsはSKILL.mdと任意のスクリプトや資料の構成を定める | agent-skills-spec | Directory structure; Optional directories | source-fact | verified | ファイル形式と構成の説明に限定。 |
| C002 | compatibilityは環境要件を示し、allowed-tools対応は実装で異なる | agent-skills-spec | compatibility field; allowed-tools field | source-fact | verified | allowed-toolsは実験的機能。対応が統一済みとはしない。 |
| C003 | 形式を受け入れられることから実行品質は導けない | agent-skills-spec | SKILL.md format; Body content | author-inference | qualified | 形式規定を行動保証として扱わないという筆者の整理。 |
| C004 | Anthropicは利用予定の全モデルでのSkillテストを勧める | anthropic-skill-practices | Test with all models you plan to use | source-fact | verified | 説明量の差を含む。Claude向け指針であり他社互換性の実験ではない。 |
| C005 | スキルとハーネスの範囲を本文のように置く | - | 誤解、遂行の失敗、環境の不一致を分ける | coined-term | qualified | 本稿内の用語の範囲。新語や統一標準の主張ではない。 |
| C006 | 指示解釈・遂行・環境を原因候補として分ける | - | 誤解、遂行の失敗、環境の不一致を分ける | recommendation | qualified | 出力だけで原因を確定できないと留保。 |
| C007 | 旧ログを要件と照合し成果と必要な前後関係を評価する | - | 旧モデルの成功ログから、合否基準を取り出す | recommendation | qualified | ブログの評価ケースは未実施の設計例。 |
| C008 | モデルだけの比較と実行環境全体の比較を分け、初期状態を揃える | - | 比較するのは、モデルだけか、実行環境も含むのか | recommendation | qualified | 固定資料の評価と実接続の評価を区別。設定値の同一性を公平性の保証にしない。 |
| C009 | 最終回答・操作履歴・成果物を突き合わせる | - | 最終回答、実行記録、成果物を突き合わせる | recommendation | qualified | 最終差分は途中の書き込みを証明しない。機械検査と人・LLMの判断の限界を明示。 |
| C010 | Promptfooのcustom providerはJS/TSで独自の処理を接続できる | promptfoo-custom-provider | Javascript Provider introduction; Provider Interface | source-fact | verified | 接続可能性の紹介。ブログエージェントの動作確認済みとはしない。 |
| C011 | 実エージェントを接続して操作記録等を評価へ渡す構成が考えられる | promptfoo-custom-provider | Provider Interface | author-inference | qualified | 筆者の構成案。標準で全証拠が自動収集されるとは述べない。 |
| C012 | TaskCompletionMetricは実行トレースを用いLLMで達成度を評価する | deepeval-task-completion | Usage; How Is It Calculated; FAQs | source-fact | verified | 最終状態の独立した検証や正しさの保証ではない。 |
| C013 | 複数回実行、重大条件の事前設定、調整に使わないケースでの再確認を行う | - | 読者の仕事に置き換えるための評価ケース | recommendation | qualified | 統計的な信頼水準や全モデルへの一般化は主張しない。 |
| C014 | 入力・評価基準・失敗例も移行可能な資産として残す | - | 次のモデルへ、何を残すか | recommendation | qualified | 本稿の中心的提案。効果量を実証したものではない。 |
