---
name: cognitive-scaffold-blog
description: >-
  ブログ「認知の足場」(hideshi.github.io/blog) の執筆・画像・公開手順。
  Jekyll / GitHub Pages、drafts から _posts への公開、1200x630 の平面 OGP、
  X カード、sitemap / 検索向けメタ、github-personal の Git 身元を扱う。
  記事執筆、下書き、OGP、テーマ、公開、SEO、コミット、X 投稿文面のときに使う。
  公開3本から抽出した草稿の型（便利さのずらし、対応関係、限界、答え責任）を扱う。
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

## 草稿の考え方

公開3本（言語選択、Scholarly Agent Skills、読みさえできれば）から抽出した型。毎回同じ導入素材（日常比喩や対応表）にする必要はない。骨格は共有する。

背骨: 観察された楽さ → 負担の置き場が移ったと見る → 対応関係を示す → その読みの限界を書く → 論文3本の枠（外部化と答え責任）へ接続 → 条件付きで閉じる。

「AIで楽になる」で始め、「だから人間は不要」では終わらない。残るのは採否・検証・答えられること。

手順:

1. ありがちな結論を先に置き、ずらす。導入の数段落で問い、仮説、やりすぎない範囲を出す。
2. 専門性を先に下げる。優位の断定、プロンプト集、怠けの推奨、ゲート通過＝正しさ、は書かない。仮説・存在例・実務家の整理にする。
3. 消えた負担と残った負担を対にする。覚える／手で書く／一回の生成 → 検証・レビュー・採否・工程。楽になった、とは言わない。
4. 対応関係を表か箇条書きで固定する。読者が「似ている」を自分で埋めなくて済むようにする。
5. 比喩・読み替えの効く範囲を、効かない範囲より先に切る。個人の好み≠組織標準、試しやすさ≠本番責任、閉じた辞書≠AIの出力、など。
6. 論文は証明ではなく、残る線引きの語彙として DOI で出す。「論文が実証した」とは書かない。
7. 終わりは標語ではなく条件。足場になるのは、読める／検証できる／採否を引き受けられるとき。そうでなければ増幅器になる。

title はずらしが一文で見える形（なぜ〜か、〜する前に、〜に似ている）。description は便利さだけにせず、ずらしを同じ120字に入れる。

**増幅器**: AI活用の一般的な用法では、人間の能力を拡張する肯定語になりやすい。本ブログの「読みさえできれば」では「誤りの増幅器」であり、条件を欠いた外部化の帰結として否定的に使っている。単独の「増幅器」を悪語として使わない。否定するときは「誤りの〜」など何を増幅するかを付ける。

種: 増幅器の両義。公開: `_posts/2026-08-27-what-the-amplifier-amplifies.md`。

## Git

- remote: `git@github-personal:hideshi/blog.git`
- このリポジトリの local `user.email` は `hideshi.ogoshi@gmail.com`。会社メアド `ogoshi@y-n-s.co.jp` は使わない。
- `git add` / `git commit` は「コミットして」と明示されたときだけ。push も明示時だけ。
- コミットしない: `drafts/`、`assets/images/alts/`、生データ。`alts/` は `.gitignore` 済み。

## ディレクトリ

| パス | 役割 |
|---|---|
| `_posts/` | 公開記事。Jekyll が拾う |
| `drafts/` | 非公開。`_config.yml` の exclude 済み |
| `_layouts/` | `home` / `page` / `post`（theme の `default` を包む） |
| `_layouts/default.html` | `{% seo %}` → `{% feed_meta %}` → `head-twitter.html`。`name="twitter:image"` は SEO の `property` より後。記事・about のサイト名は `h1` にしない |
| `_layouts/post.html` | 本文のあと「同じ軸の記事」（自記事以外、最大5件） |
| `assets/css/style.scss` | Minimal の上に暗い配色 |
| `assets/images/` | 公開 OGP。ファイル名は記事 slug |
| `_includes/head-twitter.html` | `name="twitter:card"` と `name="twitter:image"`。画像 URL にクエリを付けない |
| `_includes/head-custom.html` | GA4 gtag |
| `robots.txt` | クローラ許可と `Sitemap:` |

## 公開フロー

1. `drafts/YYYY-MM-DD-slug.md` で書く。front matter に `draft: true` を付けてよい。
2. 公開前に OGP（1200×630 の JPEG、目安 100KB 以下）を作り、`assets/images/og-<slug>.jpg` へ置く。`image.path` も `.jpg`。
3. `_posts/` へ移し、`draft: true` を外す。`image:` を付ける。関連記事リストは `post.html` が出すので、本文末に同じ一覧を重複させない。本文中の接続は残してよい。
4. ユーザー承認後に commit。Pages 反映は push 後。
5. X 文面を出す（下記「X 投稿」）。初回は正規 URL（末尾 `/`、クエリなし）。カードが古い／欠けたあとの**新しい共有**だけ `?v=2`。投稿済みポストのカードは更新されない。

## X 投稿

カードに title と OGP が出る。ポスト本文にタイトルを重ねない。description の復唱だけにもしない。ずらしを2〜3文で書き、末尾に正規 URL を1つ置く。

型:

```
記事を書きました。
<ずらし。便利さの片側だけにしない。増幅器を悪語にするなら「誤りの〜」と何が増えるかを付ける>
<空行>
<https://hideshi.github.io/blog/YYYY/MM/DD/slug/>
```

- 280 字以内（CJK は2、URL は t.co で23）
- ハッシュタグは付けない（カードと本文が重複しやすい）
- 初回の URL は `https://hideshi.github.io/blog/YYYY/MM/DD/slug/`（末尾 `/`、`?v=` なし）
- 下書きの灰色箱だけでは失敗と決めない。title/description だけ出て新聞アイコンのまま投稿したら、カードは画像なしで固定される
- `twitter:image` にビルド SHA などのクエリを付けない。jekyll-seo-tag は `property="twitter:image"` を出すので、`head-twitter.html` は `{% seo %}` の**後**に置く
- カードの再取得は**ページ URL** の `?v=2`。画像 URL 側にクエリを足さない
- 画像なしで一度出してしまった投稿は、Pages で新 JPEG が 200 になってから削除し、`...?v=2` で出し直す。同じ URL の再投稿ではカードは変わらない
- 2026-08-27 増幅器記事: SHA 付き `twitter:image` と 700KB PNG で画像だけ欠けた。クエリを外し JPEG（約 60KB）にして `?v=2` で出し直すと出た
- X モバイルのカードは、OGP 画像の下端に半透明バーでページタイトルを重ねる。比喩やアイコンを下端に置くと隠れる（「OGP 画像」の安全域）

## 記事 front matter

既存記事に合わせる:

```yaml
---
layout: post
title: "..."
date: YYYY-MM-DD
description: "120字前後。検索と X 用。"
image:
  path: /assets/images/og-<slug>.jpg
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

生成前に、対象記事の front matter から **`title` と `description` を Read** する。slug・会話の要約・本文だけを入力にして図を起こさない。

GenerateImage の `description` には、画風指定に加えて **title と description を原文のまま含める**。右の比喩は、その2つを読んだ人にも通じるものにする。本文は補助（表のセルや固有の挿話を主モチーフにしない）。重ねる日本語は `title`（必要なら `description` 由来の subtitle）。

読める図にする。3D の木・真鍮・発光ケーブルは使わない（AI っぽく、比喩が読めない）。

**X カードの下端バー（必須）**: モバイルのサマリーカードは、画像の下端に半透明の暗いバーを重ね、そこにページタイトルを白字で出す。下端の図は欠ける。GenerateImage の `description` に、下側の安全域を原文で含める。

- 1200×630 のうち、**下から約 20%（およそ 126px、y 504–630）は比喩の本体を置かない**。炭色の余白・床だけにする
- 置いてはいけないもの: 原稿アイコンの列、枠に入る1枚、ゲート、採否の対象など、図の読みに必要な要素
- サイト名とタイトルは左上〜左中（`compose_og.py` が載せる）。下端バーと重ならない
- 2026-08-27「読みさえできれば」: 下段の原稿アイコンが、X モバイルのタイトルバーで半分隠れた

採用した画風:

- 暗い炭色地 `#161513`、生成り `#f3efe6`、水色枠 `#8ec4e0`
- 平面の枠と生成り色の「原稿」矩形。印刷ポスター／図版
- 左に「認知の足場」＋タイトル（Noto Sans CJK）。右に比喩
- 比喩は一目で読めること（ゲートを通る原稿、枠に収まる1枚 など）。比喩は画面の中〜上に置く
- 書き出しサイズ **1200×630**。`article img { height: auto }` があるので HTML の `height="630"` を固定表示にしない
- 公開ファイルは **JPEG**（品質 85 前後、目安 100KB 以下）。X は 700KB 級 PNG だと画像だけ欠けることがある。合成の PNG は `alts/` に残してよい

タイトル重ねは `python3 scripts/compose_og.py`。使い方は [og-compose.md](og-compose.md)。

## Pages

`.github/workflows/pages.yml` が HEAD 以外の SHA を公開しない。ブランチからの自動 build と Actions が併走することがある。公開面が古い／白いときは、まず最新 SHA のデプロイか、古い run の上書きを疑う。
