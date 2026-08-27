# OGP 合成

絵を起こす前に、記事 front matter の `title` と `description` を読む。画像生成プロンプトへ両方を原文で入れる。本文やチャット要約だけを根拠にしない。

GenerateImage の `description` には、画風・title・description に加えて **下端の安全域** を入れる。X モバイルのカードは画像下端に半透明バーでページタイトルを重ねるため、比喩・アイコン・原稿を下 20% に置くと隠れる。1200×630 なら下約 126px は炭色の余白だけ。`compose_og.py` の切り出しはソース下端を残しがちなので、生成段階で空けないとカードで欠ける。2026-08-27「読みさえできれば」で下段の原稿アイコンが半分隠れた。

生成画像（16:9 指定でも実寸は 3:2 になりがち）を 1200×630 に切り、左を暗くして日本語を載せる。

```bash
python3 scripts/compose_og.py <src.png> \
  -o assets/images/alts/og-<slug>.png \
  --title "1行目" \
  --title "2行目" \
  --subtitle "任意の副題"
```

`-o` を省略すると `assets/images/alts/<srcのstem>.png` に書く。採用したら JPEG にして公開パスへ置く（X カード用。PNG のまま 700KB 級だと画像だけ欠けることがある）。

```bash
python3 - <<'PY'
from pathlib import Path
from PIL import Image
src = Path("assets/images/alts/og-<slug>.png")
im = Image.open(src).convert("RGB")
im.save("assets/images/og-<slug>.jpg", "JPEG", quality=85, optimize=True)
PY
```

front matter の `image.path` は `/assets/images/og-<slug>.jpg`。alts はコミットしない。フォントは `/usr/share/fonts/opentype/noto/NotoSansCJK-*.ttc`（`index=0`）。Pillow が必要（`python3 -c "import PIL"`）。
