# OGP 合成

生成画像（16:9 指定でも実寸は 3:2 になりがち）を 1200×630 に切り、左を暗くして日本語を載せる。

```bash
python3 scripts/compose_og.py <src.png> \
  -o assets/images/alts/og-<slug>.png \
  --title "1行目" \
  --title "2行目" \
  --subtitle "任意の副題"
```

`-o` を省略すると `assets/images/alts/<srcのstem>.png` に書く。採用したら公開パスへコピーする。

```bash
cp assets/images/alts/og-<slug>.png assets/images/og-<slug>.png
```

alts はコミットしない。フォントは `/usr/share/fonts/opentype/noto/NotoSansCJK-*.ttc`（`index=0`）。Pillow が必要（`python3 -c "import PIL"`）。
