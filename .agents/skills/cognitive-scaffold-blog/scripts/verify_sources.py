#!/usr/bin/env python3
"""Validate a per-article source and claim evidence pack."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml


CLASSES = {"source-fact", "source-hypothesis", "author-inference", "coined-term", "recommendation"}
STATUSES = {"verified", "qualified", "unsupported", "pending"}
NO_SOURCE = {"", "-", "—", "none", "n/a"}
TABLE_HEADER = ["id", "draft claim", "source", "locator", "class", "status", "notes"]


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def load_claims(path: Path) -> tuple[list[list[str]], list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return [], [f"claims.md がありません: {path}"]

    lines = path.read_text(encoding="utf-8").splitlines()
    header_index = None
    for index, line in enumerate(lines):
        if line.lstrip().startswith("|") and [c.lower() for c in split_row(line)] == TABLE_HEADER:
            header_index = index
            break
    if header_index is None:
        return [], ["claims.md に所定の7列ヘッダーがありません"]
    if header_index + 1 >= len(lines) or not is_separator(split_row(lines[header_index + 1])):
        errors.append("claims.md のヘッダー直後に区切り行がありません")

    rows: list[list[str]] = []
    for line in lines[header_index + 2 :]:
        if not line.lstrip().startswith("|"):
            if rows:
                break
            continue
        cells = split_row(line)
        if len(cells) != 7:
            errors.append(f"claims.md の列数が7ではありません: {line}")
        else:
            rows.append(cells)
    if not rows:
        errors.append("claims.md に主張がありません")
    return rows, errors


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_repo_root(path: Path) -> Path | None:
    for candidate in (path, *path.parents):
        if (candidate / "_config.yml").is_file():
            return candidate
    return None


def validate(pack: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    source_file = pack / "sources.yaml"
    if not source_file.is_file():
        return [f"sources.yaml がありません: {source_file}"], warnings

    try:
        data = yaml.safe_load(source_file.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"sources.yaml が不正です: {exc}"], warnings
    if not isinstance(data, dict):
        return ["sources.yaml はマッピングである必要があります"], warnings
    if data.get("version") != 1:
        errors.append("version は 1 にしてください")
    article_value = data.get("article")
    if not article_value:
        errors.append("article がありません")
    else:
        repo_root = find_repo_root(pack.resolve())
        if repo_root is None:
            warnings.append("article の存在確認に必要なリポジトリルートを特定できません")
        else:
            article = (repo_root / str(article_value)).resolve()
            try:
                article.relative_to(repo_root.resolve())
            except ValueError:
                errors.append("article はリポジトリ内を指してください")
            else:
                if not article.is_file():
                    errors.append(f"article がありません: {article_value}")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        return errors + ["sources は1件以上のリストにしてください"], warnings

    source_ids: set[str] = set()
    for index, source in enumerate(sources, start=1):
        label = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{label} はマッピングである必要があります")
            continue
        for key in ("id", "type", "title", "canonical_url", "retrieved_at"):
            if source.get(key) in (None, ""):
                errors.append(f"{label}.{key} がありません")
        source_id = str(source.get("id", ""))
        if source_id and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", source_id):
            errors.append(f"{label}.id は小文字英数字とハイフンにしてください")
        if source_id in source_ids:
            errors.append(f"source id が重複しています: {source_id}")
        source_ids.add(source_id)
        parsed = urlparse(str(source.get("canonical_url", "")))
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"{label}.canonical_url は http(s) の正規 URL にしてください")

        snapshot_value = source.get("local_snapshot")
        expected_hash = str(source.get("sha256", "")).lower()
        if snapshot_value:
            snapshot = (pack / str(snapshot_value)).resolve()
            try:
                snapshot.relative_to(pack.resolve())
            except ValueError:
                errors.append(f"{label}.local_snapshot は証拠パック内を指してください")
            else:
                if not snapshot.is_file():
                    errors.append(f"snapshot がありません: {snapshot_value}")
                elif not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                    errors.append(f"{label}.sha256 は64桁の16進数で指定してください")
                elif sha256(snapshot) != expected_hash:
                    errors.append(f"snapshot の SHA-256 が一致しません: {snapshot_value}")
        elif expected_hash:
            warnings.append(f"{label} は sha256 があるのに local_snapshot がありません")
        if str(source.get("license", "")).lower() in {"", "unknown"} and snapshot_value:
            warnings.append(f"{label} の再配布可否を確認してください")

    rows, claim_errors = load_claims(pack / "claims.md")
    errors.extend(claim_errors)
    claim_ids: set[str] = set()
    for row in rows:
        claim_id, claim, source_id, locator, claim_class, status, _notes = row
        if not claim_id:
            errors.append("空の claim ID があります")
        elif not re.fullmatch(r"C\d{3,}", claim_id):
            errors.append(f"claim ID は C と3桁以上の数字にしてください: {claim_id}")
        elif claim_id in claim_ids:
            errors.append(f"claim ID が重複しています: {claim_id}")
        claim_ids.add(claim_id)
        if not claim:
            errors.append(f"{claim_id}: Draft claim が空です")
        if claim_class not in CLASSES:
            errors.append(f"{claim_id}: Class が不正です: {claim_class}")
        if status not in STATUSES:
            errors.append(f"{claim_id}: Status が不正です: {status}")

        normalized_source = source_id.lower()
        needs_source = claim_class in {"source-fact", "source-hypothesis"}
        if source_id not in source_ids and normalized_source not in NO_SOURCE:
            errors.append(f"{claim_id}: 未登録の Source です: {source_id}")
        if needs_source and normalized_source in NO_SOURCE:
            errors.append(f"{claim_id}: {claim_class} には Source が必要です")
        if needs_source and locator.lower() in NO_SOURCE:
            errors.append(f"{claim_id}: {claim_class} には Locator が必要です")
        if status == "verified" and needs_source and source_id not in source_ids:
            errors.append(f"{claim_id}: verified ですが有効な Source がありません")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path, help="research/<slug> ディレクトリ")
    args = parser.parse_args()
    errors, warnings = validate(args.pack)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")
    if not errors and not warnings:
        print("OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
