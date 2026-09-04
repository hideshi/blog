# Jekyll・公開準備

## ディレクトリと権限

- `_posts/`: 公開記事
- `drafts/`: 非公開下書き。Git に追加しない
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
---
```

- `_posts/YYYY-MM-DD-slug.md` の日付と front matter の日付を一致させる。
- 公開記事から `draft: true` を外す。
- `image.path` は存在する 1200×630 の JPEG にする。
- `_layouts/post.html` が画像と関連記事を出すため、本文へ同じ OGP や関連記事一覧を重複挿入しない。
- 各記事に固有の title、description、alt を付ける。

## 準備手順

1. 対象ファイルと現在の `git status` を確認する。
2. front matter、見出し、コードフェンス、内部リンク、画像パスを検査する。
3. 原典を使う記事は証拠パックを検査する。
4. OGP を作成し、実寸と容量を確認する。
5. `validate_post.py` を実行する。
6. 保存後のファイルを読み直し、差分を示す。

```bash
python3 .agents/skills/cognitive-scaffold-blog/scripts/validate_post.py _posts/YYYY-MM-DD-slug.md
```

Ruby/Jekyll を実行できる環境ならビルドも確認する。実行できなければ、未実施であることを報告する。

## SEO と Pages

- `jekyll-seo-tag`、`jekyll-feed`、`jekyll-sitemap` を外さない。
- 記事ページの H1 は本文タイトルだけにする。
- description へ検索語を不自然に詰め込まない。
- `robots.txt` の Sitemap は `https://hideshi.github.io/blog/sitemap.xml`。
- Pages への反映は push と deploy の完了後である。ローカル保存や commit を「公開」と呼ばない。
- 公開面が古い場合は、公開対象 SHA、Actions の競合、画像 URL の到達性を確認する。
