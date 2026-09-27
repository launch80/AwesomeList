"""Shared loading helpers for the Launch80 catalog scripts."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
SCHEMAS = ROOT / "schemas"
REPO_SLUG = "launch80/AwesomeList"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_SLUG}/main"
BLOB_BASE = f"https://github.com/{REPO_SLUG}/blob/main"

ID_PATTERN = r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
# e.g. "7.1", ">=7.0,<7.2", "==3.12"
VERSION_RANGE_PATTERN = r"^(?:(?:>=|<=|==|~=|>|<)?[0-9]+(?:\.[0-9]+)*)(?:,(?:>=|<=|==|~=|>|<)?[0-9]+(?:\.[0-9]+)*)*$"


@dataclass
class Catalog:
    vocabulary: dict
    gpu_models: list[dict]
    projects: list[dict]
    recipes: list[dict]
    benchmarks: list[dict]
    paths: list[dict]
    # Source file for each record, keyed by (collection, index) — used in error messages.
    origins: dict = field(default_factory=dict)

    @property
    def projects_by_id(self) -> dict:
        return {p["id"]: p for p in self.projects}

    @property
    def gpus_by_id(self) -> dict:
        return {g["id"]: g for g in self.gpu_models}

    def benchmarks_for(self, project_id: str) -> list[dict]:
        return [b for b in self.benchmarks if b["project"] == project_id]

    def term(self, group: str, key: str) -> str:
        return self.vocabulary.get(group, {}).get(key, key)


def _load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_catalog() -> Catalog:
    origins = {}
    projects, recipes = [], []
    for collection, target in (("projects", projects), ("recipes", recipes)):
        for path in sorted((CATALOG / collection).glob("*.yaml")):
            origins[(collection, len(target))] = path
            target.append(_load_yaml(path))

    benchmarks = []
    bench_path = CATALOG / "benchmarks" / "benchmark-results.jsonl"
    for lineno, line in enumerate(bench_path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            origins[("benchmarks", len(benchmarks))] = f"{bench_path}:{lineno}"
            benchmarks.append(json.loads(line))

    return Catalog(
        vocabulary=_load_yaml(CATALOG / "vocabulary.yaml"),
        gpu_models=_load_yaml(CATALOG / "compatibility" / "gpu-models.yaml"),
        projects=projects,
        recipes=recipes,
        benchmarks=benchmarks,
        paths=_load_yaml(CATALOG / "paths.yaml"),
        origins=origins,
    )


def vocabulary_schema(vocabulary: dict) -> dict:
    """JSON Schema $defs generated from catalog/vocabulary.yaml."""
    defs = {
        "id": {"type": "string", "pattern": ID_PATTERN, "description": "Stable kebab-case record ID."},
        "version_range": {
            "type": "string",
            "pattern": VERSION_RANGE_PATTERN,
            "description": "A version or comma-separated range, e.g. '>=7.0,<7.2'.",
        },
    }
    for group, terms in vocabulary.items():
        defs[group] = {
            "enum": list(terms),
            "description": "; ".join(f"{k}: {v}" for k, v in terms.items()),
        }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"{RAW_BASE}/schemas/vocabulary.schema.json",
        "title": "Launch80 controlled vocabulary",
        "description": "GENERATED from catalog/vocabulary.yaml by scripts/build.py — do not edit.",
        "$defs": defs,
    }
