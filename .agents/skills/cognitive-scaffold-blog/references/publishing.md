# Jekyll・公開準備

## ディレクトリと権限

- `_posts/`: 公開記事
- `drafts/`: 非公開の記事下書き（本文候補）だけ。Git に追加しない
- `reviews/`: 外部モデル等によるレビューメモ。Git に追加しない
- `scratch/`: `.bak` やツールの raw 出力など一時物。Git に追加しない
- `social/`: X・note など共有用の文案。Git に追加しない
- `assets/images/`: 公開 OGP
- `assets/images/alts/`: 画像生成・合成の候補。Git に追加しない
- `research/`: 原典メタデータと主張表。Jekyll の公開対象から除外する

Git remote は `git@github-personal:hideshi/blog.git`。このリポジトリの local `user.email` は `hideshi.ogoshi@gmail.com` とし、会社メールを使わない。`git add`、commit、push は、それぞれユーザーが明示した場合だけ行う。

## front matter

```yaml
---
layout: post
title: "..."
date: YYYY-MM-DD
description: "120字前後。本文なしでも問いと論点が分かる文章。"
image:
  path: /assets/images/og-<slug>.jpg
  width: 1200
  height: 630
  alt: 図が何を表すかを一文で。
tags:
  - ...
related:
  - other-post-slug
---
```

- `_posts/YYYY-MM-DD-slug.md` の日付と front matter の日付を一致させる。
- `drafts/` 下のファイル名は日付を入れず `slug.md` とする（作成日＝公開日とは限らないため）。公開時に `_posts/YYYY-MM-DD-slug.md` へ移動して公開日付を付与する。
- 公開記事から `draft: true` を外す。
- `image.path` は存在する 1200×630 の JPEG にする。
- `_layouts/post.html` が画像と関連記事を出すため、本文へ同じ OGP や関連記事一覧を重複挿入しない。
- 各記事に固有の title、description、alt を付ける。
- `related` は他記事の **slug**（ファイル名の日付以降、拡張子なし）のリスト。新しい順やタグ一致の自動列挙は使わない。空なら「同じ軸の記事」節は出さない。

## 同じ軸の記事（related）

公開準備のとき、執筆エージェントが既存 `_posts/` を見て候補を提案し、妥当なら front matter の `related` へ挿入する（ユーザーが明示的に別リストを指定していればそれに従う）。

照合の観点（すべて機械タグではなく内容）:

1. **問い**: 同じずれ・同じ設計判断を別角度から扱っているか
2. **用語・操作点**: 足場／再利用手順／正本／答え責任など、本稿の核と接続するか（タグ一致だけでは足りない）
3. **読者の次の一歩**: 本稿の直後に読むと納得が増すか

手順:

1. 本稿の中心命題を一文で置く。
2. 既存記事の title・description・見出しを眺め、上記3点で最大5件まで候補を上げ、各1行の理由を添える。
3. 弱い候補は載せない（件数を埋めない）。0件なら `related` 自体を省略する。
4. 採用した slug を front matter の `related` に書き、本文末へ手書き一覧を重複させない。
5. 公開報告に、選んだ slug と短い理由を残す。

## 準備手順

1. 対象ファイルと現在の `git status` を確認する。
2. front matter、見出し、コードフェンス、内部リンク、画像パスを検査する。title／description と本文の着地（おわりに・後半の核）が同じ話か照合する。
3. 「同じ軸の記事」について既存 `_posts/` から候補を提案し、採用分を `related` へ挿入する（上節）。ユーザー指定があればそれを優先する。
4. 原典を使う記事は証拠パックを検査する。
5. OGP を作成し、実寸と容量を確認する。
6. `drafts/slug.md` から `_posts/YYYY-MM-DD-slug.md` へ移動した場合は、公開日付をファイル名と front matter に反映し、`draft: true` を外して元の `drafts/` 下のファイルを削除する（重複・二重管理の防止）。
7. `validate_post.py` を実行する。
8. 保存後のファイルを読み直し、差分を示す。

```bash
python3 .agents/skills/cognitive-scaffold-blog/scripts/validate_post.py _posts/YYYY-MM-DD-slug.md
```

Ruby/Jekyll を実行できる環境ならビルドも確認する。実行できなければ、未実施であることを報告する。


## 内部リンク（baseurl）

このサイトは `baseurl: /blog` なので、記事間リンクは必ず `/blog` 付きになる書き方にする。

- **使う**: `{{ "/YYYY/MM/DD/slug/" | relative_url }}`、または `https://hideshi.github.io/blog/YYYY/MM/DD/slug/`
- **使わない**: `{% post_url YYYY-MM-DD-slug %}`（GitHub Pages 上で `/blog` が欠ける事例あり）、`https://hideshi.github.io/YYYY/...`、`]/YYYY/...` のルート相対

公開前ゲート:

```bash
python3 .agents/skills/cognitive-scaffold-blog/scripts/validate_post.py _posts/YYYY-MM-DD-slug.md
# または全件
python3 .agents/skills/cognitive-scaffold-blog/scripts/validate_post.py --all-posts
```

`validate_post.py` は `{% post_url %}`、`/blog` 欠落の絶対URL、存在しない permalink / related slug を ERROR にする。

## SEO と Pages

- `jekyll-seo-tag`、`jekyll-feed`、`jekyll-sitemap` を外さない。
- 記事ページの H1 は本文タイトルだけにする。
- description へ検索語を不自然に詰め込まない。
- `robots.txt` の Sitemap は `https://hideshi.github.io/blog/sitemap.xml`。
- Pages への反映は push と deploy の完了後である。ローカル保存や commit を「公開」と呼ばない。
- 公開面が古い場合は、公開対象 SHA、Actions の競合、画像 URL の到達性を確認する。
