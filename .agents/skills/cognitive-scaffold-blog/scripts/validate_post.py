#!/usr/bin/env python3
"""Validate a blog draft or post without requiring Jekyll."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml
from PIL import Image


FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
POST_NAME = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>[a-z0-9][a-z0-9-]*)\.md\Z")
RELATIVE_URL_LINK = re.compile(
    r'\{\{\s*"(?P<path>/\d{4}/\d{2}/\d{2}/[a-z0-9][a-z0-9-]*/)"\s*\|\s*relative_url\s*\}\}'
)
ABS_BLOG_LINK = re.compile(
    r"https://hideshi\.github\.io/blog(?P<path>/(?:20\d{2}/\d{2}/\d{2}/[a-z0-9][a-z0-9-]*)/?)"
)
ABS_MISSING_BLOG = re.compile(
    r"https://hideshi\.github\.io/(?P<path>20\d{2}/\d{2}/\d{2}/[^)\s\"']+)"
)
ROOT_MD_LINK = re.compile(r"\]\(/(?P<path>20\d{2}/\d{2}/\d{2}/[^)]+)\)")
ROOT_HREF = re.compile(r'href="/(?P<path>20\d{2}/\d{2}/\d{2}/[^"]+)"')


def find_repo_root(path: Path) -> Path:
    for candidate in (path.parent, *path.parents):
        if (candidate / "_config.yml").is_file():
            return candidate
    raise ValueError("_config.yml があるリポジトリルートを特定できません")


def date_text(value: object) -> str:
    if isinstance(value, (date, datetime)):
        return value.strftime("%Y-%m-%d")
    return str(value or "")[:10]


def index_posts(posts_dir: Path) -> tuple[set[str], set[str]]:
    slugs: set[str] = set()
    permalinks: set[str] = set()
    if not posts_dir.is_dir():
        return slugs, permalinks
    for post in posts_dir.glob("*.md"):
        name_match = POST_NAME.fullmatch(post.name)
        if not name_match:
            continue
        slug = name_match.group("slug")
        slugs.add(slug)
        y, mo, d = name_match.group("date").split("-")
        permalinks.add(f"/{y}/{mo}/{d}/{slug}/")
    return slugs, permalinks


def normalize_permalink(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if not path.endswith("/"):
        path += "/"
    return path


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return [f"ファイルがありません: {path}"], warnings

    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(text)
    if not match:
        return ["YAML front matter がありません、または閉じられていません"], warnings

    try:
        metadata = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f"front matter の YAML が不正です: {exc}"], warnings

    if not isinstance(metadata, dict):
        return ["front matter はマッピングである必要があります"], warnings

    for key in ("layout", "title", "date", "description", "tags"):
        if metadata.get(key) in (None, "", []):
            errors.append(f"必須項目がありません: {key}")

    if metadata.get("layout") not in (None, "post"):
        warnings.append("記事の layout は通常 post です")
    if metadata.get("description") and not isinstance(metadata["description"], str):
        errors.append("description は文字列にしてください")
    if metadata.get("tags") is not None and not isinstance(metadata["tags"], list):
        errors.append("tags は YAML のリストにしてください")

    repo_root = find_repo_root(path.resolve())
    is_post = path.resolve().parent == repo_root / "_posts"
    is_draft = path.resolve().parent == repo_root / "drafts"
    existing_slugs, existing_permalinks = index_posts(repo_root / "_posts")

    if is_post:
        name_match = POST_NAME.fullmatch(path.name)
        if not name_match:
            errors.append("公開記事名は YYYY-MM-DD-lowercase-slug.md にしてください")
        elif date_text(metadata.get("date")) != name_match.group("date"):
            errors.append("ファイル名の日付と front matter の date が一致しません")
        if metadata.get("draft") is True:
            errors.append("公開記事に draft: true が残っています")
        if not metadata.get("image"):
            errors.append("公開記事には image が必要です")
    elif is_draft and metadata.get("draft") is not True:
        warnings.append("下書きには draft: true を付けると状態が明確です")

    image_meta = metadata.get("image")
    if image_meta:
        if not isinstance(image_meta, dict):
            errors.append("image は path/width/height/alt を持つマッピングにしてください")
        else:
            for key in ("path", "width", "height", "alt"):
                if image_meta.get(key) in (None, ""):
                    errors.append(f"image.{key} がありません")
            image_path_value = image_meta.get("path")
            if isinstance(image_path_value, str):
                image_path = repo_root / image_path_value.lstrip("/")
                if not image_path.is_file():
                    errors.append(f"画像がありません: {image_path_value}")
                else:
                    try:
                        with Image.open(image_path) as image:
                            actual = image.size
                    except Exception as exc:  # Pillow exposes several format errors.
                        errors.append(f"画像を読めません: {image_path_value}: {exc}")
                    else:
                        declared = (image_meta.get("width"), image_meta.get("height"))
                        if actual != (1200, 630):
                            errors.append(f"OGP 実寸は 1200x630 必須です: {actual[0]}x{actual[1]}")
                        if declared != actual:
                            errors.append(f"image.width/height {declared} と実寸 {actual} が一致しません")
                        if is_post and image_path.suffix.lower() not in (".jpg", ".jpeg"):
                            errors.append("公開 OGP は JPEG にしてください")
                        size = image_path.stat().st_size
                        if size > 100 * 1024:
                            warnings.append(f"OGP が 100 KB を超えています: {size / 1024:.1f} KB")

    body = text[match.end() :]
    if body.count("```") % 2:
        errors.append("コードフェンス ``` の数が奇数です")

    # Internal link / baseurl gates.
    # On this site (baseurl=/blog), {% post_url %} has rendered without /blog.
    if "{% post_url" in text or "{%- post_url" in text:
        errors.append(
            "{% post_url %} は使わないでください（/blog が欠ける）。"
            '{{ "/YYYY/MM/DD/slug/" | relative_url }} を使う'
        )

    for m in ABS_MISSING_BLOG.finditer(text):
        errors.append(f"絶対URLに /blog がありません: https://hideshi.github.io/{m.group('path')}")

    for m in ROOT_MD_LINK.finditer(body):
        errors.append(
            f"ルート相対リンクに baseurl がありません（relative_url を使う）: /{m.group('path')}"
        )
    for m in ROOT_HREF.finditer(body):
        errors.append(f"href が /blog なしのルート相対です: /{m.group('path')}")

    if existing_permalinks:
        for m in RELATIVE_URL_LINK.finditer(text):
            permalink = normalize_permalink(m.group("path"))
            if permalink not in existing_permalinks:
                errors.append(f"内部リンク先の記事がありません: {permalink}")

        for m in ABS_BLOG_LINK.finditer(text):
            permalink = normalize_permalink(m.group("path"))
            if permalink not in existing_permalinks:
                errors.append(f"絶対URLの記事がありません: /blog{permalink}")

    related = metadata.get("related")
    if related is not None:
        if not isinstance(related, list):
            errors.append("related は YAML のリストにしてください")
        else:
            for item in related:
                if not isinstance(item, str) or not item:
                    errors.append("related の各要素は slug 文字列にしてください")
                elif existing_slugs and item not in existing_slugs:
                    errors.append(f"related の slug がありません: {item}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="検査する Markdown 記事（省略時は _posts 全件）",
    )
    parser.add_argument(
        "--all-posts",
        action="store_true",
        help="_posts 配下をすべて検査する",
    )
    args = parser.parse_args()

    files = list(args.files)
    if args.all_posts or not files:
        # Default to all posts when no files given, so the gate is easy to run.
        if not files:
            repo = Path.cwd()
            if not (repo / "_config.yml").is_file():
                print("ERROR: リポジトリルートで実行するか、ファイルを指定してください", file=sys.stderr)
                return 2
            files = sorted((repo / "_posts").glob("*.md"))
            if not files:
                print("ERROR: _posts に記事がありません", file=sys.stderr)
                return 2

    failed = False
    for path in files:
        errors, warnings = validate(path)
        print(f"[{path}]")
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARN: {message}")
        if not errors and not warnings:
            print("OK")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
