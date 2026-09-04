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


def find_repo_root(path: Path) -> Path:
    for candidate in (path.parent, *path.parents):
        if (candidate / "_config.yml").is_file():
            return candidate
    raise ValueError("_config.yml があるリポジトリルートを特定できません")


def date_text(value: object) -> str:
    if isinstance(value, (date, datetime)):
        return value.strftime("%Y-%m-%d")
    return str(value or "")[:10]


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

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="検査する Markdown 記事")
    args = parser.parse_args()

    failed = False
    for path in args.files:
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
