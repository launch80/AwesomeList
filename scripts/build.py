#!/usr/bin/env python3
"""Generate every derived view from the structured catalog.

    python scripts/build.py          # write generated files
    python scripts/build.py --check  # exit 1 if any generated file is stale (used in CI)

Outputs: README.md, catalog.json, llms.txt, llms-full.txt, schemas/vocabulary.schema.json,
docs/glossary.md, docs/benchmarks.md, docs/projects/*.md, docs/hardware/*.md.
Output is deterministic (no timestamps) so --check can compare byte-for-byte.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from urllib.parse import urlparse

from catalog_lib import BLOB_BASE, RAW_BASE, ROOT, Catalog, load_catalog, vocabulary_schema

ARCH_LABELS = {
    "rdna2": "RDNA2", "rdna3": "RDNA3", "rdna3_5": "RDNA3.5", "rdna4": "RDNA4",
    "cdna": "CDNA", "cdna2": "CDNA2", "cdna3": "CDNA3",
    "intel_arc": "Intel Arc", "nvidia_blackwell": "NVIDIA Blackwell",
}
RUNTIME_LABELS = {
    "vllm": "vLLM", "sglang": "SGLang", "llama_cpp": "llama.cpp", "tgi": "TGI",
    "ollama": "Ollama", "custom_engine": "custom engine", "diffusion": "diffusion",
}
# Hardware landing pages / Inference Servers subsections, in display order.
HARDWARE_GROUPS = [
    ("rdna4", "Radeon AI PRO R9700 / RX 9070 — RDNA4 (gfx1201)", ["rdna4"]),
    ("rdna3", "Radeon RX 7900 — RDNA3 (gfx1100)", ["rdna3"]),
    ("rdna2", "Radeon Pro V620 — RDNA2 (gfx1030) and Strix APUs", ["rdna2", "rdna3_5"]),
    ("cdna", "Instinct MI210 / MI100 / MI250X — CDNA datacenter", ["cdna", "cdna2", "cdna3"]),
    ("intel-arc", "Intel Arc", ["intel_arc"]),
    ("nvidia", "NVIDIA Blackwell", ["nvidia_blackwell"]),
]
MATURITY_ORDER = ["recommended", "supported", "experimental", "historical", "unverified"]
# Fields that make a benchmark reproducible; the completeness column counts how many are present.
BENCH_KEY_FIELDS = [
    ("hardware", "gpu_count"), ("hardware", "interconnect"), ("hardware", "host_cpu"),
    ("platform", "os"), ("platform", "kernel"), ("platform", "rocm"),
    ("runtime", "version"), ("runtime", "commit"), ("model", "artifact"), ("model", "quantization"),
    ("workload", "context_length"), ("workload", "prompt_tokens"), ("workload", "output_tokens"),
    ("workload", "concurrency"), (None, "command"), (None, "measured_on"),
]
UNKNOWN = "_not yet documented_"


# ---------------------------------------------------------------- helpers

def arch_list(archs) -> str:
    return ", ".join(ARCH_LABELS.get(a, a) for a in archs or [])


def runtime_list(runtimes) -> str:
    return ", ".join(RUNTIME_LABELS.get(r, r) for r in runtimes or [])


def gpu_count_label(hw: dict) -> str:
    count = hw.get("gpu_count") or {}
    lo, hi = count.get("min"), count.get("max")
    if lo and hi:
        return f"{lo}–{hi} GPUs" if lo != hi else f"{lo} GPU{'s' if lo > 1 else ''}"
    if lo and lo > 1:
        return f"{lo}+ GPUs"
    return ""


def people_line(p: dict) -> str:
    people = p["people"]
    line = "Built by " + ", ".join(f"**{b}**" for b in people["builders"])
    if people.get("shared_by"):
        line += ", shared by " + ", ".join(f"@{s}" for s in people["shared_by"])
    return line


def anchor(text: str) -> str:
    """GitHub heading anchor."""
    text = re.sub(r"[^\w\- ]", "", text.strip().lower())
    return text.replace(" ", "-")


def card_path(pid: str) -> str:
    return f"docs/projects/{pid}.md"


def bench_completeness(b: dict) -> str:
    have = sum(1 for sect, key in BENCH_KEY_FIELDS if (b.get(sect) or {}).get(key) if sect) + sum(
        1 for sect, key in BENCH_KEY_FIELDS if sect is None and b.get(key)
    )
    return f"{have}/{len(BENCH_KEY_FIELDS)}"


def fmt_num(v, approx=False) -> str:
    s = f"{v:,.0f}" if isinstance(v, (int, float)) else str(v)
    return f"~{s}" if approx else s


def fmt_ctx(n) -> str:
    if not n:
        return "not reported"
    return f"{round(n / 1024)}K" if n % 1024 == 0 else f"{round(n / 1000)}K"


def sort_projects(projects, paths=()):
    """Maturity first, then start-here picks, then alphabetical — never by benchmark numbers."""
    picks = {i for path in paths for i in path["start_with"]}
    return sorted(
        projects,
        key=lambda p: (MATURITY_ORDER.index(p["maturity"]), p["id"] not in picks, p["name"].lower()),
    )


def hardware_group(p: dict):
    archs = p["hardware"].get("architectures") or []
    for gid, _, members in HARDWARE_GROUPS:
        if archs and archs[0] in members:
            return gid
    return None


# ---------------------------------------------------------------- README

def render_start_here(cat: Catalog, paths: list[dict], cards: str = "docs/projects/") -> str:
    by_id = cat.projects_by_id
    rows = ["| I want to… | Hardware | Start with | Then look at | Typical reader |", "|---|---|---|---|---|"]
    for path in paths:
        start = " · ".join(f"[{by_id[i]['name']}]({cards}{i}.md)" for i in path["start_with"])
        then = " · ".join(f"[{by_id[i]['name']}]({cards}{i}.md)" for i in path.get("then", [])) or "—"
        note = f"<br><sub>{path['why']}"
        if path.get("caveat"):
            note += f" ⚠️ {path['caveat']}"
        note += "</sub>"
        rows.append(f"| **{path['i_want_to']}**{note} | {path['hardware']} | {start} | {then} | {path['typical_reader']} |")
    return "\n".join(rows)


def render_entry(cat: Catalog, p: dict, cards: str = "docs/projects/") -> str:
    hw = p["hardware"]
    meta = [f"`{p['maturity']}`"]
    if hw.get("agnostic"):
        meta.append("any hardware")
    elif hw.get("architectures"):
        meta.append(arch_list(hw["architectures"]))
    if gpu_count_label(hw):
        meta.append(gpu_count_label(hw))
    if p.get("software", {}).get("runtimes"):
        meta.append(runtime_list(p["software"]["runtimes"]))
    if p.get("evidence"):
        meta.append(f"{len(p['evidence'])} benchmark record{'s' if len(p['evidence']) > 1 else ''}")
    meta.append(f"[card →]({cards}{p['id']}.md)")
    return (
        f"- **[{p['name']}]({p['links']['repository']})** — {p['tagline']} {people_line(p)}.<br>\n"
        f"  {' · '.join(meta)}"
    )


def render_directory(cat: Catalog) -> tuple[str, str]:
    sections, index = [], []
    for cat_key, title in cat.vocabulary["category"].items():
        primary = [p for p in cat.projects if p["categories"][0] == cat_key]
        secondary = [p for p in cat.projects if cat_key in p["categories"][1:]]
        if not primary and not secondary:
            continue
        index.append(f"[{title}](#{anchor(title)})")
        out = [f"### {title}", ""]
        if cat_key == "inference_servers":
            grouped = defaultdict(list)
            for p in primary:
                grouped[hardware_group(p)].append(p)
            for gid, heading, _ in HARDWARE_GROUPS:
                if grouped.get(gid):
                    out += [f"#### {heading}", ""]
                    out += [render_entry(cat, p) for p in sort_projects(grouped[gid], cat.paths)]
                    out.append("")
        else:
            out += [render_entry(cat, p) for p in sort_projects(primary, cat.paths)]
            out.append("")
        if secondary:
            links = " · ".join(f"[{p['name']}]({card_path(p['id'])})" for p in sort_projects(secondary))
            out += [f"*Also relevant here:* {links}", ""]
        sections.append("\n".join(out))

    codeberg = [p for p in cat.projects if urlparse(p["links"]["repository"]).hostname == "codeberg.org"]
    mirrored = [p for p in cat.projects if any("codeberg.org" in m for m in p["links"].get("mirrors", []))]
    if codeberg or mirrored:
        title = "Hosted on Codeberg"
        index.append(f"[{title}](#{anchor(title)})")
        lines = [f"### {title}", "", "Much of the Launch80 stack lives on Codeberg rather than GitHub:", ""]
        lines += [f"- [{p['name']}]({p['links']['repository']}) — [card]({card_path(p['id'])})" for p in codeberg]
        for p in mirrored:
            mirror = next(m for m in p["links"]["mirrors"] if "codeberg.org" in m)
            lines.append(f"- [{urlparse(mirror).path.strip('/')}]({mirror}) — Codeberg mirror of [{p['name']}]({card_path(p['id'])})")
        sections.append("\n".join(lines) + "\n")
    return " ⁕ ".join(index), "\n".join(sections).rstrip() + "\n"


def render_readme(cat: Catalog) -> str:
    template = (ROOT / "docs" / "templates" / "README.md.tmpl").read_text(encoding="utf-8")
    index, directory = render_directory(cat)
    legend = "\n".join(f"- `{k}` — {v}" for k, v in cat.vocabulary["maturity"].items())
    counts = defaultdict(int)
    for p in cat.projects:
        counts[p["maturity"]] += 1
    legend += "\n\nCurrently: " + ", ".join(f"{counts[m]} {m}" for m in MATURITY_ORDER if counts[m]) + "."
    hw_pages = " ⁕ ".join(
        f"[{heading.split(' — ')[0]}](docs/hardware/{gid}.md)"
        for gid, heading, members in HARDWARE_GROUPS
        if any(set(p["hardware"].get("architectures") or []) & set(members) for p in cat.projects)
    )
    replacements = {
        "start_here": render_start_here(cat, cat.paths),
        "maturity_legend": legend,
        "index": index,
        "directory": directory.rstrip(),
        "hardware_pages": hw_pages,
    }
    for key, value in replacements.items():
        template = template.replace(f"<!-- {key} -->", value)
    return template


# ---------------------------------------------------------------- cards

def render_card(cat: Catalog, p: dict) -> str:
    gpus = cat.gpus_by_id
    hw, sw, sup, ver = p["hardware"], p.get("software", {}), p.get("supports", {}), p["verification"]

    if hw.get("agnostic"):
        hardware = "Any (not GPU-specific)"
    elif hw.get("architectures") or hw.get("gpu_models"):
        parts = []
        if hw.get("architectures"):
            gfx = sorted({g["gfx_target"] for g in cat.gpu_models if g["architecture"] in hw["architectures"] and g.get("gfx_target")})
            parts.append(arch_list(hw["architectures"]) + (f" ({', '.join(gfx)})" if gfx else ""))
        if hw.get("gpu_models"):
            parts.append("tested on " + ", ".join(gpus[g]["name"] for g in hw["gpu_models"]))
        if gpu_count_label(hw):
            parts.append(gpu_count_label(hw) + " required")
        if hw.get("min_vram_gb"):
            parts.append(f"≥{hw['min_vram_gb']} GB VRAM per GPU")
        hardware = "; ".join(parts)
    else:
        hardware = ", ".join(v.upper() for v in hw.get("vendors", [])) + " — architectures " + UNKNOWN

    software = []
    if sw.get("os"):
        software.append(", ".join(sw["os"]) + (" " + ", ".join(sw["os_versions"]) if sw.get("os_versions") else ""))
    if sw.get("rocm"):
        software.append(f"ROCm {sw['rocm']}")
    if sw.get("python"):
        software.append(f"Python {sw['python']}")
    if sw.get("container"):
        software.append("Docker")
    if sw.get("stack_notes"):
        software.append(sw["stack_notes"])

    not_for = list(p.get("not_suitable_for", []))
    if hw.get("architectures") and not hw.get("agnostic"):
        others = [ARCH_LABELS[a] for a in cat.vocabulary["architecture"] if a not in hw["architectures"]]
        not_for.append("GPUs outside " + arch_list(hw["architectures"]) + f" (e.g. {', '.join(others[:3])})")
    if (hw.get("gpu_count") or {}).get("min", 1) > 1:
        not_for.append(f"Fewer than {hw['gpu_count']['min']} GPUs")

    status = f"`{p['maturity']}` — {cat.term('maturity', p['maturity'])}"
    rows = [
        ("Status", status),
        ("Verification", f"`{ver['level']}` — {cat.term('verification_level', ver['level'])}"),
        ("Kind", cat.term("kind", p["kind"])),
        ("Hardware", hardware),
        ("Software", "; ".join(software) or UNKNOWN),
        ("Runtime", runtime_list(sw.get("runtimes")) or "—"),
        ("Models tested", ", ".join(sup.get("models", [])) or UNKNOWN),
        ("Quantization", ", ".join(sup.get("quantizations", [])) or "—"),
        ("Provides", ", ".join(f"`{f}`" for f in p.get("provides", [])) or "—"),
        ("Topology", ", ".join(sup.get("topologies", [])) or "—"),
        ("Not suitable for", "; ".join(not_for) or "—"),
        ("Audience", f"`{p['audience']}` — {cat.term('audience', p['audience'])}" if p.get("audience") else "—"),
        ("Last verified", ver.get("last_verified", "never") + (f" by {', '.join(ver['tested_by'])}" if ver.get("tested_by") else "")),
        ("Last commit checked", ver.get("last_commit_checked", "—")),
        ("Listed since", ver.get("listed_since", "—")),
    ]
    by_id = cat.projects_by_id
    out = [
        f"<!-- GENERATED from catalog/projects/{p['id']}.yaml by scripts/build.py — do not edit. -->",
        "",
        f"# {p['name']}",
        "",
        f"**{p['tagline']}**",
        "",
        f"**Use it if:** {p['use_it_if']}",
        "",
        "| Field | Value |",
        "|---|---|",
        *[f"| {k} | {v} |" for k, v in rows],
        "",
        f"{people_line(p)}" + (f" · Contributors: {', '.join(p['people']['contributors'])}" if p["people"].get("contributors") else "") + ".",
        "",
    ]
    if p.get("description"):
        out += [p["description"], ""]
    if sw.get("based_on"):
        out += ["**Builds on:** " + " · ".join(f"[{by_id[b]['name']}]({b}.md)" for b in sw["based_on"]), ""]
    derived = [q for q in cat.projects if p["id"] in q.get("software", {}).get("based_on", [])]
    if derived:
        out += ["**Built on by:** " + " · ".join(f"[{q['name']}]({q['id']}.md)" for q in sort_projects(derived)), ""]
    if hw.get("host_notes"):
        out += [f"**Host:** {hw['host_notes']}", ""]
    out += ["**Quick start:**", ""]
    if p.get("quick_start"):
        out += ["```sh", p["quick_start"], "```", ""]
    else:
        out += [f"Follow the [repository README]({p['links'].get('setup_guide', p['links']['repository'])}) — no pinned commands recorded yet.", ""]
    out += ["**Known issues:** " + ("" if p.get("known_issues") else "none recorded."), ""]
    out += [f"- {i}" for i in p.get("known_issues", [])]
    if p.get("known_issues"):
        out.append("")
    if p.get("notes"):
        out += [f"**Notes:** {p['notes']}", ""]

    out += ["## Evidence", ""]
    benches = cat.benchmarks_for(p["id"])
    if benches:
        out += [bench_table(cat, benches, link_projects=False, prefix="../"), ""]
    else:
        out += ["No benchmark records yet. Run [BetterBench](betterbench.md) and submit the result.", ""]

    recipes = [r for r in cat.recipes if p["id"] in r["projects"]]
    if recipes:
        out += ["## Recipes", ""] + [f"- `{r['id']}` — {r['title']} (`{r['maturity']}`)" for r in recipes] + [""]

    links = [f"[Repository]({p['links']['repository']})"]
    for key, label in (("setup_guide", "Setup guide"), ("docker_image", "Docker image"), ("writeup", "Write-up"), ("discussion", "Discussion")):
        if p["links"].get(key):
            links.append(f"[{label}]({p['links'][key]})")
    links += [f"[Mirror]({m})" for m in p["links"].get("mirrors", [])]
    links.append(f"[Record](../../catalog/projects/{p['id']}.yaml)")
    out += ["## Links", "", " · ".join(links), ""]
    return "\n".join(out)


# ---------------------------------------------------------------- benchmarks

def bench_table(cat: Catalog, benches: list[dict], link_projects=True, prefix="", metric=None) -> str:
    gpus, by_id = cat.gpus_by_id, cat.projects_by_id
    header = ["GPUs", "Model", "Quant", "Context", "Concurrency", "Decode tok/s", "Prefill tok/s", "Runtime", "Mode", "Fields reported", "Source"]
    if metric == "decode":
        header.remove("Prefill tok/s")
    if metric == "prefill":
        header.remove("Decode tok/s")
    if link_projects:
        header.insert(0, "Project")
    rows = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for b in sorted(benches, key=lambda b: (b["hardware"]["gpu_model"], b["project"], b["id"])):
        m, hw, wl, rt = b["metrics"], b["hardware"], b.get("workload", {}), b.get("runtime", {})
        approx = m.get("approximate", False)
        decode = fmt_num(m["decode_tok_s"], approx) if "decode_tok_s" in m else "—"
        if m.get("statistic") in ("median", "peak") and "decode_tok_s" in m:
            decode += f" ({m['statistic']})"
        src = b["source"]
        source = f"[{src['type']}]({src['url']})" if src.get("url") else src["type"]
        row = {
            "Project": f"[{by_id[b['project']]['name']}]({prefix}projects/{b['project']}.md)",
            "GPUs": (f"{hw['gpu_count']}× " if hw.get("gpu_count") else "")
            + gpus[hw["gpu_model"]]["name"]
            + ("" if hw.get("gpu_count") else " (count not reported)")
            + (" (P2P)" if hw.get("p2p") else ""),
            "Model": b["model"]["name"],
            "Quant": b["model"].get("quantization", "—"),
            "Context": fmt_ctx(wl.get("context_length")),
            "Concurrency": str(wl["concurrency"]) if wl.get("concurrency") else "not reported",
            "Decode tok/s": decode,
            "Prefill tok/s": fmt_num(m["prefill_tok_s"], approx) if "prefill_tok_s" in m else "—",
            "Runtime": " ".join(filter(None, [RUNTIME_LABELS.get(rt.get("name"), rt.get("name")), rt.get("version"), rt.get("speculative")])) or "not reported",
            "Mode": b["mode"],
            "Fields reported": bench_completeness(b),
            "Source": source,
        }
        rows.append("| " + " | ".join(row[h] for h in header) + " |")
    return "\n".join(rows)


def render_benchmarks(cat: Catalog) -> str:
    single = [b for b in cat.benchmarks if b["mode"] == "single_stream" and "decode_tok_s" in b["metrics"]]
    batched = [b for b in cat.benchmarks if b["mode"] == "batched" and "decode_tok_s" in b["metrics"]]
    unknown = [b for b in cat.benchmarks if b["mode"] == "not_reported" and "decode_tok_s" in b["metrics"]]
    prefill = [b for b in cat.benchmarks if "prefill_tok_s" in b["metrics"]]
    fields = ", ".join(f"`{s + '.' if s else ''}{k}`" for s, k in BENCH_KEY_FIELDS)

    def section(title, intro, rows, metric):
        body = bench_table(cat, rows, metric=metric) if rows else "_No records yet._"
        return f"## {title}\n\n{intro}\n\n{body}\n"

    return "\n".join([
        "<!-- GENERATED from catalog/benchmarks/benchmark-results.jsonl by scripts/build.py — do not edit. -->",
        "",
        "# Benchmarks",
        "",
        "Author-reported numbers, normalized. Tables are sorted by hardware, **not** by speed: a number is",
        "only comparable to another measured with the same mode, context, prompt/output length and",
        "concurrency. **Fields reported** counts how many of the key workload fields the source stated",
        f"({fields}).",
        "",
        "Raw data: [`catalog/benchmarks/benchmark-results.jsonl`](../catalog/benchmarks/benchmark-results.jsonl) ·",
        "schema: [`schemas/benchmark.schema.json`](../schemas/benchmark.schema.json).",
        "",
        section("Decode — single stream", "One request at a time: what a single user feels.", single, "decode"),
        section("Decode — batched (aggregate)", "Total decode throughput across concurrent requests.", batched, "decode"),
        section("Prefill", "Prompt-processing speed. Mode is shown per row.", prefill, "prefill"),
        section(
            "Decode — concurrency not reported",
            "The source did not say whether this was one stream or many. Do not compare these with the tables above; "
            "if you can reproduce one with BetterBench, submit a record with `mode` set.",
            unknown, "decode",
        ).rstrip(),
        "",
    ])


# ---------------------------------------------------------------- hardware pages

def render_hardware_page(cat: Catalog, gid: str, heading: str, members: list[str]) -> str:
    projects = [p for p in cat.projects if set(p["hardware"].get("architectures") or []) & set(members)]
    gpus = [g for g in cat.gpu_models if g["architecture"] in members]
    benches = [b for b in cat.benchmarks if cat.gpus_by_id[b["hardware"]["gpu_model"]]["architecture"] in members]
    paths = [path for path in cat.paths if set(path.get("architectures", [])) & set(members)]
    out = [
        "<!-- GENERATED by scripts/build.py — do not edit. -->",
        "",
        f"# {heading}",
        "",
        "GPUs: " + ", ".join(
            f"{g['name']}" + (f" ({g['vram_gb']} GB)" if g.get("vram_gb") else "") + (f" `{g['gfx_target']}`" if g.get("gfx_target") else "")
            for g in gpus
        ),
        "",
        f"Selector: `python scripts/selector.py --gpu {gpus[0]['id']} --count 1`",
        "",
    ]
    if paths:
        out += ["## Start here", "", render_start_here(cat, paths, cards="../projects/"), ""]
    out += ["## Projects", ""]
    out += [render_entry(cat, p, cards="../projects/") for p in sort_projects(projects, cat.paths)]
    out.append("")
    if benches:
        out += ["## Reported benchmarks", "", "Mixed modes — check the Mode column before comparing. See [all benchmarks](../benchmarks.md).", "", bench_table(cat, benches, prefix="../"), ""]
    agnostic = [p for p in cat.projects if p["hardware"].get("agnostic") and "benchmarking" in p.get("provides", [])]
    if agnostic:
        out += ["## Works with any hardware", "", " · ".join(f"[{p['name']}](../projects/{p['id']}.md)" for p in agnostic), ""]
    return "\n".join(out)


# ---------------------------------------------------------------- glossary

def render_glossary(cat: Catalog) -> str:
    out = [
        "<!-- GENERATED from catalog/vocabulary.yaml by scripts/build.py — do not edit. -->",
        "",
        "# Glossary",
        "",
        "Canonical terms used in every catalog record. The schemas reject anything not listed here, so",
        "`rdna4`, never `RDNA 4` or `gfx1201`. To add a term, edit `catalog/vocabulary.yaml`.",
        "",
    ]
    for group, terms in cat.vocabulary.items():
        out += [f"## `{group}`", "", "| Term | Meaning |", "|---|---|"]
        out += [f"| `{k}` | {v} |" for k, v in terms.items()]
        out.append("")
    out += ["## GPU models", "", "| ID | Name | Architecture | gfx | VRAM (GB) |", "|---|---|---|---|---|"]
    out += [
        f"| `{g['id']}` | {g['name']} | `{g['architecture']}` | {g.get('gfx_target') or '—'} | {g.get('vram_gb') or '—'} |"
        for g in cat.gpu_models
    ]
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- machine-readable

def render_catalog_json(cat: Catalog) -> str:
    def with_links(p):
        return {
            **p,
            "_card_url": f"{BLOB_BASE}/{card_path(p['id'])}",
            "_record_url": f"{RAW_BASE}/catalog/projects/{p['id']}.yaml",
        }

    data = {
        "name": "Awesome Launch80 List",
        "description": "Community-owned inference repos from the Launch80 Discord, as structured records.",
        "schema_version": 1,
        "schemas": {
            name: f"{RAW_BASE}/schemas/{name}.schema.json"
            for name in ("project", "recipe", "benchmark", "paths", "gpu-models", "vocabulary")
        },
        "guidance": (
            "Hard requirements (hardware.architectures, hardware.gpu_count.min, hardware.min_vram_gb, "
            "software.os, conflicts) are binary gates: never recommend a record whose gates the user fails. "
            "Rank the rest by maturity and verification.level, not by the largest tok/s number. "
            "Cite record IDs and state verification.level. A missing field means unknown, not unsupported."
        ),
        "vocabulary": cat.vocabulary,
        "gpu_models": cat.gpu_models,
        "paths": cat.paths,
        "projects": [with_links(p) for p in sorted(cat.projects, key=lambda p: p["id"])],
        "recipes": sorted(cat.recipes, key=lambda r: r["id"]),
        "benchmarks": sorted(cat.benchmarks, key=lambda b: b["id"]),
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def render_llms_txt(cat: Catalog) -> str:
    by_id = cat.projects_by_id
    out = [
        "# Awesome Launch80 List",
        "",
        "> Structured catalog of community-owned LLM inference repos (vLLM/Radiance, SGLang, llama.cpp forks,",
        "> kernels, launchers, multi-GPU setups, benchmarks) from the Launch80 Discord, focused on AMD ROCm",
        "> GPUs (RDNA2/3/4, CDNA) plus a few Intel Arc and NVIDIA entries.",
        "",
        "Rules for agents: treat hardware.architectures, hardware.gpu_count.min, hardware.min_vram_gb and",
        "software.os as hard gates. Rank by maturity and verification.level, never by the highest tok/s.",
        "A missing field means unknown. Most records are `unverified` (author-reported); say so.",
        "Cite record IDs. Ask the user for GPU model, GPU count, VRAM and OS if they are missing.",
        "",
        "## Machine-readable data",
        "",
        f"- [catalog.json]({RAW_BASE}/catalog.json): every project, benchmark, start-here path, GPU model and vocabulary term",
        f"- [llms-full.txt]({RAW_BASE}/llms-full.txt): the full catalog as compact text",
        f"- [benchmark-results.jsonl]({RAW_BASE}/catalog/benchmarks/benchmark-results.jsonl): normalized benchmark records",
        f"- [project.schema.json]({RAW_BASE}/schemas/project.schema.json): project record schema",
        f"- [benchmark.schema.json]({RAW_BASE}/schemas/benchmark.schema.json): benchmark record schema",
        f"- [recipe.schema.json]({RAW_BASE}/schemas/recipe.schema.json): deployment recipe schema",
        f"- [vocabulary.schema.json]({RAW_BASE}/schemas/vocabulary.schema.json): controlled vocabulary enums",
        "",
        "## Start here",
        "",
    ]
    for path in cat.paths:
        picks = ", ".join(path["start_with"])
        out.append(f"- [{path['i_want_to']}]({BLOB_BASE}/{card_path(path['start_with'][0])}): start with {picks} ({path['hardware']})")
    out += [
        "",
        "## Docs",
        "",
        f"- [Glossary]({BLOB_BASE}/docs/glossary.md): canonical terms for architectures, runtimes, quantizations, maturity",
        f"- [Benchmarks]({BLOB_BASE}/docs/benchmarks.md): normalized tables split by single-stream, batched and prefill",
        f"- [Selector]({BLOB_BASE}/scripts/selector.py): `python scripts/selector.py --gpu r9700 --count 1 --need openai_api --json`",
        f"- [Contributing]({BLOB_BASE}/CONTRIBUTING.md): how records are added and verified",
        "",
        "## Optional",
        "",
    ]
    for p in sorted(cat.projects, key=lambda p: p["id"]):
        out.append(f"- [{p['id']}]({BLOB_BASE}/{card_path(p['id'])}): {p['tagline']}")
    out.append("")
    assert all(i in by_id for path in cat.paths for i in path["start_with"])
    return "\n".join(out)


def render_llms_full(cat: Catalog) -> str:
    out = [
        "# Awesome Launch80 List — full catalog",
        "",
        "Generated from catalog/. Fields absent from a record are unknown. Hard gates: architectures,",
        "gpu_count_min, min_vram_gb, os. Maturity/verification describe how much to trust each entry.",
        "",
    ]
    for p in sorted(cat.projects, key=lambda p: p["id"]):
        hw, sw, sup = p["hardware"], p.get("software", {}), p.get("supports", {})
        lines = [
            f"## {p['id']}",
            f"name: {p['name']}",
            f"outcome: {p['tagline']}",
            f"use_it_if: {p['use_it_if']}",
            f"kind: {p['kind']} | maturity: {p['maturity']} | verification: {p['verification']['level']}"
            + (f" | last_verified: {p['verification']['last_verified']}" if p["verification"].get("last_verified") else ""),
            "hardware: " + ("any" if hw.get("agnostic") else ", ".join(hw.get("architectures", [])) or "unknown")
            + (f" | gpu_models: {', '.join(hw['gpu_models'])}" if hw.get("gpu_models") else "")
            + (f" | gpu_count_min: {hw['gpu_count']['min']}" if (hw.get("gpu_count") or {}).get("min") else "")
            + (f" | min_vram_gb: {hw['min_vram_gb']}" if hw.get("min_vram_gb") else ""),
        ]
        if sw:
            lines.append("software: " + " | ".join(
                f"{k}: {', '.join(v) if isinstance(v, list) else v}" for k, v in sw.items()
            ))
        if p.get("provides"):
            lines.append(f"provides: {', '.join(p['provides'])}")
        if sup:
            lines.append("supports: " + " | ".join(f"{k}: {', '.join(v)}" for k, v in sup.items()))
        for key in ("not_suitable_for", "conflicts", "known_issues"):
            if p.get(key):
                lines.append(f"{key}: {'; '.join(p[key])}")
        if p.get("quick_start"):
            lines.append(f"quick_start: {p['quick_start']}")
        if p.get("evidence"):
            lines.append(f"evidence: {', '.join(p['evidence'])}")
        lines.append(f"repository: {p['links']['repository']}")
        people = p["people"]
        lines.append("builders: " + ", ".join(people["builders"]) + (f" | shared_by: {', '.join(people['shared_by'])}" if people.get("shared_by") else ""))
        if p.get("notes"):
            lines.append(f"notes: {p['notes']}")
        out += lines + [""]

    out += ["# Benchmarks", "", "mode=not_reported means concurrency is unknown; do not compare across modes.", ""]
    for b in sorted(cat.benchmarks, key=lambda b: b["id"]):
        out.append(f"- {b['id']}: " + json.dumps({k: v for k, v in b.items() if k != "id"}, ensure_ascii=False, separators=(",", ":")))
    out += ["", "# Start-here paths", ""]
    for path in cat.paths:
        out.append(f"- {path['id']}: {path['i_want_to']} ({path['hardware']}) -> start_with={','.join(path['start_with'])}"
                   + (f" then={','.join(path['then'])}" if path.get("then") else "") + f". why: {path['why']}"
                   + (f" caveat: {path['caveat']}" if path.get("caveat") else ""))
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------- main

def render_all(cat: Catalog) -> dict:
    files = {
        "README.md": render_readme(cat),
        "catalog.json": render_catalog_json(cat),
        "llms.txt": render_llms_txt(cat),
        "llms-full.txt": render_llms_full(cat),
        "schemas/vocabulary.schema.json": json.dumps(vocabulary_schema(cat.vocabulary), indent=2, ensure_ascii=False) + "\n",
        "docs/glossary.md": render_glossary(cat),
        "docs/benchmarks.md": render_benchmarks(cat),
    }
    for p in cat.projects:
        files[card_path(p["id"])] = render_card(cat, p)
    for gid, heading, members in HARDWARE_GROUPS:
        if any(set(p["hardware"].get("architectures") or []) & set(members) for p in cat.projects):
            files[f"docs/hardware/{gid}.md"] = render_hardware_page(cat, gid, heading, members)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail if generated files are out of date")
    args = parser.parse_args()

    files = render_all(load_catalog())
    # Generated directories are owned entirely by this script; anything else in them is stale.
    owned = {str(p.relative_to(ROOT)) for d in ("docs/projects", "docs/hardware") for p in (ROOT / d).glob("*.md")}
    stale_extra = sorted(owned - set(files))

    if args.check:
        stale = [rel for rel, text in files.items() if not (ROOT / rel).exists() or (ROOT / rel).read_text(encoding="utf-8") != text]
        for rel in stale + stale_extra:
            print(f"out of date: {rel}", file=sys.stderr)
        if stale or stale_extra:
            print("Run `python scripts/build.py` and commit the result.", file=sys.stderr)
            return 1
        print(f"{len(files)} generated files up to date.")
        return 0

    for rel, text in files.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    for rel in stale_extra:
        (ROOT / rel).unlink()
        print(f"removed {rel}")
    print(f"wrote {len(files)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
