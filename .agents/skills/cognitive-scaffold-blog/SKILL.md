---
name: cognitive-scaffold-blog
description: >-
  ブログ「認知の足場」の記事を起草、レビュー、改稿、原典検証、公開準備する。
  記事執筆、ハルシネーション検証、Jekyll front matter、OGP、SEO、公開手順、
  X投稿文を扱う。このブログ以外の一般的なMarkdown編集には使わない。
---

# 認知の足場 — 記事制作

Jekyll プロジェクトサイト。公開 URL は `https://hideshi.github.io/blog/`。

## 守ること

- サイト名と公開上の著者名は「認知の足場」。実名を title、author、本文、about に出さない。
- 連絡先は X `@hdsh0428`、GitHub の運用名は `hideshi`。
- 仮説、観察、原典の主張、筆者の推論を混同しない。ツールや検査の通過を正しさの保証にしない。
- サイトの主題である「認知作業の外部化と答え責任」は有効な視点として使い、各記事へ機械的に押し込まない。
- 外部への投稿、コミット、push、公開状態への変更は、ユーザーが明示した場合だけ行う。

## 最初に作業モードを決める

- **レビュー**: 原則として読み取り専用。重要度順に根拠付きで指摘し、依頼がなければ本文を変更しない。
- **起草・改稿・適用**: ファイルを編集し、保存後に読み直す。`drafts/` 下のファイル名は日付を入れず `slug.md` とする（作成日＝公開日ではないため）。最終報告に保存先と Git 状態を含める。
- **公開準備**: front matter、OGP、リンク、検査を整える。`drafts/slug.md` から `_posts/YYYY-MM-DD-slug.md` への移動は明示依頼時だけ。
- **公開**: commit と push はそれぞれ明示依頼時だけ。準備完了を公開済みと表現しない。

「未保存」は区別する。エディタ上だけの未保存内容は観測できない。ディスク上の保存済み、Git の未追跡、Git の変更済み、commit 済みを `git status` などで確認して伝える。

## 必要な手順を読む

- 構成、文体、比喩、具体例のレビューや執筆: [references/editorial.md](references/editorial.md)
- 外部資料、固有名詞、引用、技術概念、数値、ファクトチェック: [references/source-verification.md](references/source-verification.md)
- front matter、SEO、draft、Git、Pages: [references/publishing.md](references/publishing.md)
- OGP の生成・合成: [references/ogp.md](references/ogp.md)
- X 投稿文、記事から切り出す発見・具体例・問い: [references/social.md](references/social.md)

複数に該当すれば必要なものだけ組み合わせる。外部資料に依存する記事や、ハルシネーション検証を求められたレビューでは、`source-verification.md` を必ず先に読む。

## 原典を扱う記事の基本フロー

1. 記事の中心的な主張と、その根拠になる原典を特定する。
2. `research/<slug>/sources.yaml` と `claims.md` を作成または更新する。
3. 原典そのものを確認し、主張、推論、造語を分類する。検索結果の抜粋や二次要約だけで確定しない。
4. 記事を修正し、証拠パックと本文の対応を再確認する。
5. `verify_sources.py` と `validate_post.py` を実行する。これらは形式と追跡可能性の検査であり、事実の正しさを自動保証しない。

```bash
python3 .agents/skills/cognitive-scaffold-blog/scripts/verify_sources.py research/<slug>
python3 .agents/skills/cognitive-scaffold-blog/scripts/validate_post.py <article.md>
```

## 完了報告

変更したファイル、行った検証、残る未確認事項を短く示す。原典未確認、到達不能、日付不明、解釈に幅がある事項は隠さず明記する。

## このスキルを直すとき

往復の気づきをスキルへ戻すときは、**次の記事でも使う手順の型だけ**を書く。今回の記事の語彙、構図、読者設定、固有の比喩、特定の企業例、特定の節タイトルは入れない。

- 入れるもの: 照合のタイミング、置き場、確認の順番、失敗しやすいパターンの一般名
- 入れないもの: その記事で効いたモチーフや言い回しを既定化する文（OGP の定番図、読者向け語彙の固定リスト、発見の順番の中身など）
- 追記したあと、「別の題材の記事でもこの一文がそのまま正しいか」を一度読み返す。当てはまらないなら例を削るか、「〜の場合」に落とす
- 既存の節と矛盾する新ルールを足す前に、どちらが本則かを決め、古い方を更新する（定義を増やす／言い換えを優先する、など）
- スキル変更の commit は、記事本文と同様、ユーザーが明示したときだけ行う

