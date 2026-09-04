# OGP 画像

## 仕様

- 公開画像は 1200×630 の JPEG、品質 85 前後、目安 100 KB 以下。
- 暗い炭色 `#161513`、生成り `#f3efe6`、水色 `#8ec4e0` を基本にした平面の図版・印刷ポスター調。
- サイト名とタイトルは左上から左中、記事の中心的な関係を示す図を右側に置く。
- X モバイルのタイトルバーを避けるため、下 20%（約 126 px）には意味上必要な要素を置かず、背景または床だけにする。
- 3D の木材、真鍮、発光ケーブルなど、記事より画風が先に立つ装飾を避ける。

## 作成手順

1. 対象記事の front matter から title と description を原文で読む。
2. 画像生成プロンプトへ title、description、画風、右側の図の意味、下端の安全域を含める。会話の要約や slug だけを根拠にしない。
3. 生成した背景を `scripts/compose_og.py` で 1200×630 に切り出し、日本語タイトルを重ねる。
4. JPEG へ変換し、サイズ、容量、下端の安全域を目視確認する。
5. `assets/images/og-<slug>.jpg` に置き、front matter と一致させる。

```bash
python3 scripts/compose_og.py <src.png> \
  -o assets/images/alts/og-<slug>.png \
  --title "1行目" \
  --title "2行目" \
  --subtitle "任意の副題"

python3 - <<'PY'
from pathlib import Path
from PIL import Image
src = Path("assets/images/alts/og-<slug>.png")
image = Image.open(src).convert("RGB")
image.save("assets/images/og-<slug>.jpg", "JPEG", quality=85, optimize=True)
PY
```

`assets/images/alts/` の候補は commit しない。画像生成や編集が利用可能な環境では、その環境の画像生成機能を使う。既存画像を編集する前に元画像を確認する。
