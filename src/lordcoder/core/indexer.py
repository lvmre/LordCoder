"""Lightweight file indexing and selection."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

from ..models import FileIndexEntry

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".toml",
    ".json",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".html",
    ".css",
    ".sh",
}


def _should_ignore(path: Path, project_root: Path, ignore_names: Iterable[str]) -> bool:
    ignore_set = set(ignore_names)
    relative_parts = path.relative_to(project_root).parts
    return any(part in ignore_set for part in relative_parts)


def build_index(project_root: Path, ignore_names: Iterable[str]) -> List[FileIndexEntry]:
    """Index text-like files under the project root."""
    entries: List[FileIndexEntry] = []
    for path in project_root.rglob("*"):
        if not path.is_file():
            continue
        if _should_ignore(path, project_root, ignore_names):
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        stat = path.stat()
        entries.append(
            FileIndexEntry(
                path=str(path.relative_to(project_root)),
                size=stat.st_size,
                modified_time=stat.st_mtime,
            )
        )
    return sorted(entries, key=lambda entry: entry.path)


def select_relevant_files(entries: List[FileIndexEntry], objective: str, max_files: int) -> List[FileIndexEntry]:
    """Select files whose names best match the objective."""
    keywords = [token for token in re.split(r"[^a-zA-Z0-9]+", objective.lower()) if token]
    scored: List[FileIndexEntry] = []
    for entry in entries:
        score = 0
        haystack = entry.path.lower()
        for keyword in keywords:
            if keyword in haystack:
                score += 3
            if haystack.endswith(keyword):
                score += 2
        scored.append(
            FileIndexEntry(
                path=entry.path,
                size=entry.size,
                modified_time=entry.modified_time,
                score=score,
            )
        )

    ranked = sorted(scored, key=lambda item: (-item.score, item.path))
    chosen = [entry for entry in ranked if entry.score > 0][:max_files]
    if chosen:
        return chosen
    return ranked[:max_files]
