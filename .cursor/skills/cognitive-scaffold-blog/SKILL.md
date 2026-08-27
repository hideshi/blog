---
name: cognitive-scaffold-blog
description: >-
  ブログ「認知の足場」(hideshi.github.io/blog) の執筆・画像・公開手順。
  Jekyll / GitHub Pages、drafts から _posts への公開、1200x630 の平面 OGP、
  X カード、sitemap / 検索向けメタ、github-personal の Git 身元を扱う。
  記事執筆、下書き、OGP、テーマ、公開、SEO、コミット、X プレビューのときに使う。
---

# 認知の足場 — ブログ運用

Jekyll プロジェクトサイト。公開 URL は `https://hideshi.github.io/blog/`（`baseurl: /blog`）。

## 名義と文体

- サイト名は **認知の足場**。実名（小越 秀 など）を title / author / 本文 / about に出さない。
- `_config.yml` の `author.name` と `social.name` もサイト名。実名は入れない。
- 連絡先は X `@hdsh0428`。GitHub は `hideshi`。
- 軸は AI駆動開発・ソフトウェア設計を、認知作業の外部化と答え責任から書くこと。
- 専門家ぶらない。仮説と限界を書く。ツールやゲートの通過を正しさの保証にしない。
- 研究論文への言及は DOI を使う（about.md の3本）。

## Git

- remote: `git@github-personal:hideshi/blog.git`
- このリポジトリの local `user.email` は `hideshi.ogoshi@gmail.com`。会社メアド `ogoshi@y-n-s.co.jp` は使わない。
- `git add` / `git commit` は「コミットして」と明示されたときだけ。push も明示時だけ。
- コミットしない: `drafts/`、`assets/images/alts/`、生データ。

## ディレクトリ

| パス | 役割 |
|---|---|
| `_posts/` | 公開記事。Jekyll が拾う |
| `drafts/` | 非公開。`_config.yml` の exclude 済み |
| `_layouts/` | `home` / `page` / `post`（theme の `default` を包む） |
| `_layouts/default.html` | `{% seo %}` の直後に `{% feed_meta %}`。記事・about のサイト名は `h1` にしない |
| `_layouts/post.html` | 本文のあと「同じ軸の記事」（自記事以外、最大5件） |
| `assets/css/style.scss` | Minimal の上に暗い配色 |
| `assets/images/` | 公開 OGP。ファイル名は記事 slug |
| `_includes/head-twitter.html` | `name="twitter:image"`（jekyll-seo-tag の `property` 不足を補う） |
| `_includes/head-custom.html` | GA4 gtag |
| `robots.txt` | クローラ許可と `Sitemap:` |

## 公開フロー

1. `drafts/YYYY-MM-DD-slug.md` で書く。front matter に `draft: true` を付けてよい。
2. 公開前に OGP（1200×630）を作り、`assets/images/og-<slug>.png` へ置く。
3. `_posts/` へ移し、`draft: true` を外す。`image:` を付ける。関連記事リストは `post.html` が出すので、本文末に同じ一覧を重複させない。本文中の接続は残してよい。
4. ユーザー承認後に commit。Pages 反映は push 後。
5. X は初回クロールをキャッシュする。画像追加後は URL を付け直すか `?v=2` を付ける。

## 記事 front matter

既存記事に合わせる:

```yaml
---
layout: post
title: "..."
date: YYYY-MM-DD
description: "120字前後。検索と X 用。"
image:
  path: /assets/images/og-<slug>.png
  width: 1200
  height: 630
  alt: 図が何を表すかを一文で。
tags:
  - ...
---
```

`post.html` が `page.image` をタイトル直下に出す。本文へ同じ画像を重複挿入しない。

## 検索・SEO

土台は `jekyll-seo-tag` / `jekyll-feed` / `jekyll-sitemap`。プラグインを外さない。タグ一覧ページは作らない（薄いページが増える）。

守ること:

- `index.md` の `title` は **認知の足場**（サイト名と同じ）。`記事` にすると `<title>` が「記事 | 認知の足場」になる。一覧見出しは `list_title: 新着記事`。
- 各記事に固有の `description`（120字前後）と OGP。about にも `description` を付ける。
- 記事ページの H1 は本文タイトルだけ。左カラムのサイト名は `p.site-title`。トップだけサイト名を `h1` にする。
- `robots.txt` の Sitemap は `https://hideshi.github.io/blog/sitemap.xml`。
- 公開後、Search Console のプロパティ `https://hideshi.github.io/blog/` へ sitemap を送る作業は利用者が行う（エージェントはアカウントを持たない）。

やらないこと: description のキーワード詰め、見出しへの検索語の無理な挿入、AMP。

## OGP 画像

読める図にする。3D の木・真鍮・発光ケーブルは使わない（AI っぽく、比喩が読めない）。

採用した画風:

- 暗い炭色地 `#161513`、生成り `#f3efe6`、水色枠 `#8ec4e0`
- 平面の枠と生成り色の「原稿」矩形。印刷ポスター／図版
- 左に「認知の足場」＋タイトル（Noto Sans CJK）。右に比喩
- 比喩は一目で読めること（ゲートを通る原稿、枠に収まる1枚 など）
- 書き出しサイズ **1200×630**。`article img { height: auto }` があるので HTML の `height="630"` を固定表示にしない

タイトル重ねは `python3 scripts/compose_og.py`。使い方は [og-compose.md](og-compose.md)。

## Pages

`.github/workflows/pages.yml` が HEAD 以外の SHA を公開しない。ブランチからの自動 build と Actions が併走することがある。公開面が古い／白いときは、まず最新 SHA のデプロイか、古い run の上書きを疑う。
