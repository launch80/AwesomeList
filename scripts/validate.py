#!/usr/bin/env python3
"""Validate every catalog record: schema, controlled vocabulary, IDs and cross-references.

    python scripts/validate.py

Exits non-zero with one line per problem. CI runs this, then `build.py --check`.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from catalog_lib import CATALOG, SCHEMAS, load_catalog, vocabulary_schema


def main() -> int:
    cat = load_catalog()
    errors: list[str] = []

    def err(where, msg):
        errors.append(f"{where}: {msg}")

    # --- vocabulary file shape
    for group, terms in cat.vocabulary.items():
        if not isinstance(terms, dict) or not all(isinstance(v, str) and v for v in terms.values()):
            err("catalog/vocabulary.yaml", f"group '{group}' must map each term to a non-empty definition")

    # --- schema validation (vocabulary schema built in memory so a stale file cannot mask errors)
    vocab = vocabulary_schema(cat.vocabulary)
    resources = [(vocab["$id"], Resource.from_contents(vocab))]
    schemas = {}
    for name in ("project", "recipe", "benchmark", "paths", "gpu-models"):
        schema = json.loads((SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))
        schemas[name] = schema
        resources.append((schema["$id"], Resource.from_contents(schema)))
    registry = Registry().with_resources(resources)

    def check(schema_name, instance, where):
        validator = Draft202012Validator(schemas[schema_name], registry=registry, format_checker=FormatChecker())
        for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
            path = "/".join(str(p) for p in e.absolute_path) or "(root)"
            err(where, f"{path}: {e.message}")

    for i, p in enumerate(cat.projects):
        origin = cat.origins[("projects", i)]
        check("project", p, origin.relative_to(CATALOG.parent))
        if isinstance(p, dict) and p.get("id") != origin.stem:
            err(origin.name, f"file name must match id '{p.get('id')}'")
    for i, r in enumerate(cat.recipes):
        origin = cat.origins[("recipes", i)]
        check("recipe", r, origin.relative_to(CATALOG.parent))
        if isinstance(r, dict) and r.get("id") != origin.stem:
            err(origin.name, f"file name must match id '{r.get('id')}'")
    for i, b in enumerate(cat.benchmarks):
        check("benchmark", b, cat.origins[("benchmarks", i)])
    check("paths", cat.paths, "catalog/paths.yaml")
    check("gpu-models", cat.gpu_models, "catalog/compatibility/gpu-models.yaml")

    if errors:  # cross-reference checks assume well-formed records
        return report(errors)

    # --- unique IDs and repositories
    all_ids = Counter(
        [p["id"] for p in cat.projects] + [r["id"] for r in cat.recipes] + [b["id"] for b in cat.benchmarks]
    )
    for rid, n in all_ids.items():
        if n > 1:
            err("catalog", f"duplicate id '{rid}'")
    for kind, ids in (("gpu model", [g["id"] for g in cat.gpu_models]), ("path", [p["id"] for p in cat.paths])):
        for rid, n in Counter(ids).items():
            if n > 1:
                err("catalog", f"duplicate {kind} id '{rid}'")
    repos = Counter(p["links"]["repository"].rstrip("/").lower() for p in cat.projects)
    for url, n in repos.items():
        if n > 1:
            err("catalog/projects", f"repository listed {n} times: {url} (use categories for cross-listing)")

    # --- cross references
    projects, gpus = cat.projects_by_id, cat.gpus_by_id
    recipes = {r["id"] for r in cat.recipes}
    benches = {b["id"]: b for b in cat.benchmarks}

    for p in cat.projects:
        where = f"catalog/projects/{p['id']}.yaml"
        hw = p["hardware"]
        for ref in p.get("software", {}).get("based_on", []):
            if ref not in projects:
                err(where, f"based_on references unknown project '{ref}'")
            if ref == p["id"]:
                err(where, "based_on references itself")
        for ref in p.get("evidence", []):
            if ref not in benches:
                err(where, f"evidence references unknown benchmark '{ref}'")
            elif benches[ref]["project"] != p["id"]:
                err(where, f"evidence '{ref}' belongs to project '{benches[ref]['project']}'")
        for ref in p.get("recipes", []):
            if ref not in recipes:
                err(where, f"recipes references unknown recipe '{ref}'")
        for g in hw.get("gpu_models", []):
            if g not in gpus:
                err(where, f"unknown gpu model '{g}' (add it to catalog/compatibility/gpu-models.yaml)")
            elif hw.get("architectures") and gpus[g]["architecture"] not in hw["architectures"]:
                err(where, f"gpu model '{g}' is {gpus[g]['architecture']}, not in architectures {hw['architectures']}")
        if hw.get("agnostic") and (hw.get("architectures") or hw.get("gpu_models")):
            err(where, "hardware.agnostic cannot be combined with architectures or gpu_models")
        count = hw.get("gpu_count") or {}
        if count.get("min") and count.get("max") and count["min"] > count["max"]:
            err(where, "hardware.gpu_count.min is greater than max")
        ver = p["verification"]
        if p["maturity"] == "recommended":
            if ver["level"] not in ("community_reproduced", "maintainer_verified"):
                err(where, "maturity 'recommended' requires verification.level community_reproduced or maintainer_verified")
            if not ver.get("last_verified") or not ver.get("tested_by"):
                err(where, "maturity 'recommended' requires verification.last_verified and tested_by")
        if ver["level"] in ("community_reproduced", "maintainer_verified") and not ver.get("tested_by"):
            err(where, f"verification.level '{ver['level']}' requires tested_by")

    for b in cat.benchmarks:
        where = f"benchmark {b['id']}"
        if b["project"] not in projects:
            err(where, f"unknown project '{b['project']}'")
        elif b["id"] not in projects[b["project"]].get("evidence", []):
            err(where, f"project '{b['project']}' does not list this record in evidence")
        if b["hardware"]["gpu_model"] not in gpus:
            err(where, f"unknown gpu model '{b['hardware']['gpu_model']}'")
        if b.get("recipe") and b["recipe"] not in recipes:
            err(where, f"unknown recipe '{b['recipe']}'")
        if b["mode"] == "single_stream" and b.get("workload", {}).get("concurrency", 1) != 1:
            err(where, "single_stream records must have concurrency 1")

    for r in cat.recipes:
        where = f"catalog/recipes/{r['id']}.yaml"
        for ref in r["projects"]:
            if ref not in projects:
                err(where, f"unknown project '{ref}'")
        for alt in r.get("alternatives", []):
            if alt["recommend"] not in recipes | set(projects):
                err(where, f"alternative recommends unknown id '{alt['recommend']}'")
        for ref in r.get("evidence", []):
            if ref not in benches:
                err(where, f"evidence references unknown benchmark '{ref}'")
        for text in _strings(r):
            if re.fullmatch(r"<[^<>]+>", text.strip()):
                err(where, f"unfilled template placeholder: {text.strip()[:60]}")
        step_ids = Counter(s["id"] for s in r["steps"])
        for sid, n in step_ids.items():
            if n > 1:
                err(where, f"duplicate step id '{sid}'")

    for path in cat.paths:
        for ref in path["start_with"] + path.get("then", []):
            if ref not in projects:
                err(f"catalog/paths.yaml#{path['id']}", f"unknown project '{ref}'")

    return report(errors, cat)


def _strings(value):
    """Yield every string nested in a record."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _strings(v)


def report(errors, cat=None) -> int:
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        print(f"\n{len(errors)} problem(s).", file=sys.stderr)
        return 1
    print(
        f"OK: {len(cat.projects)} projects, {len(cat.recipes)} recipes, {len(cat.benchmarks)} benchmarks, "
        f"{len(cat.paths)} paths, {len(cat.gpu_models)} GPU models."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
