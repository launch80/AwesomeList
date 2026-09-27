#!/usr/bin/env python3
"""Pick compatible catalog entries for your hardware and goal.

Hard requirements are binary gates: an entry that needs RDNA4, 2+ GPUs, 32 GB VRAM or a
specific OS is never suggested to a reader who lacks it, however good its benchmark numbers.
Survivors are ranked by maturity, verification, fit and setup friction — never by tok/s.

    python scripts/selector.py --gpu r9700 --count 1 --need openai_api
    python scripts/selector.py --arch rdna3 --count 2 --vram 20 --os ubuntu --priority stability
    python scripts/selector.py --gpu v620 --count 4 --json          # machine-readable, for agents
    python scripts/selector.py --list-gpus
"""

from __future__ import annotations

import argparse
import json
import sys

from catalog_lib import BLOB_BASE, load_catalog

MATURITY_SCORE = {"recommended": 1.0, "supported": 0.75, "unverified": 0.4, "experimental": 0.3, "historical": 0.1}
VERIFICATION_SCORE = {"maintainer_verified": 1.0, "community_reproduced": 0.8, "author_reported": 0.5, "unverified": 0.2}
FRICTION = {"beginner": 0.0, "operator": 0.25, "developer": 0.6, "kernel_hacker": 1.0}
# Weights for: stability (maturity + verification), goal fit, recency, setup friction.
PRIORITY_WEIGHTS = {
    "balanced":   {"stability": 1.0, "fit": 1.0, "recency": 0.5, "friction": 0.5},
    "stability":  {"stability": 2.0, "fit": 0.8, "recency": 0.8, "friction": 0.5},
    "simplicity": {"stability": 1.0, "fit": 0.8, "recency": 0.5, "friction": 1.5},
    "throughput": {"stability": 0.6, "fit": 1.5, "recency": 0.5, "friction": 0.2},
}
LINUX_FAMILY = {"linux", "ubuntu"}


def gates(p: dict, profile: dict) -> tuple[list[str], list[str], list[str]]:
    """Return (disqualifiers, reasons it fits, unknowns the reader must confirm)."""
    no, yes, unknown = [], [], []
    hw, sw = p["hardware"], p.get("software", {})

    if hw.get("agnostic"):
        yes.append("Works with any GPU.")
    elif hw.get("architectures"):
        if profile.get("arch") is None:
            unknown.append(f"Requires {', '.join(hw['architectures'])}; your GPU architecture was not given.")
        elif profile["arch"] in hw["architectures"]:
            yes.append(f"Supports {profile['arch']}.")
            if profile.get("gpu") and profile["gpu"] in hw.get("gpu_models", []):
                yes.append(f"Author tested on your exact GPU ({profile['gpu']}).")
        else:
            no.append(f"Requires {', '.join(hw['architectures'])}; you have {profile['arch']}.")
    elif hw.get("vendors"):
        if profile.get("vendor") and profile["vendor"] not in hw["vendors"]:
            no.append(f"Targets {', '.join(hw['vendors'])} GPUs; you have {profile['vendor']}.")
        else:
            unknown.append("Supported GPU architectures are not recorded — check the repository.")
    else:
        unknown.append("Hardware requirements are not recorded — check the repository.")

    count = hw.get("gpu_count") or {}
    if count.get("min", 1) > profile["count"]:
        no.append(f"Needs at least {count['min']} GPUs; you have {profile['count']}.")
    elif count.get("min", 1) > 1:
        yes.append(f"Built for {count['min']}+ GPUs; you have {profile['count']}.")
    if count.get("max") and count["max"] < profile["count"]:
        no.append(f"Supports at most {count['max']} GPUs; you have {profile['count']}.")

    if hw.get("min_vram_gb"):
        if profile.get("vram") is None:
            unknown.append(f"Needs ≥{hw['min_vram_gb']} GB VRAM per GPU; your VRAM was not given.")
        elif profile["vram"] < hw["min_vram_gb"]:
            no.append(f"Needs ≥{hw['min_vram_gb']} GB VRAM per GPU; you have {profile['vram']} GB.")

    missing = [f for f in profile["need"] if f not in p.get("provides", [])]
    if missing:
        no.append(f"Does not provide: {', '.join(missing)}.")
    elif profile["need"]:
        yes.append(f"Provides {', '.join(profile['need'])}.")

    runtimes = sw.get("runtimes", [])
    if profile.get("runtime"):
        if runtimes and profile["runtime"] not in runtimes:
            no.append(f"Uses {', '.join(runtimes)}, not {profile['runtime']}.")
        elif not runtimes:
            unknown.append("Runtime is not recorded.")

    user_os = profile.get("os")
    conflicts = set(p.get("conflicts", []))
    if user_os and f"os:{user_os}" in conflicts:
        no.append(f"Known not to work on {user_os}.")
    elif user_os and sw.get("os"):
        declared = set(sw["os"])
        ok = user_os in declared or (user_os in LINUX_FAMILY and "linux" in declared)
        if not ok:
            no.append(f"Documented for {', '.join(sw['os'])}; you have {user_os}.")
    elif not hw.get("agnostic") and sw.get("runtimes"):
        if user_os == "windows":
            unknown.append("Community ROCm paths are Linux-first; Windows support is not recorded.")
        elif not sw.get("os"):
            unknown.append("Supported OS / ROCm versions are not recorded — check the repository.")

    return no, yes, unknown


def score(p: dict, profile: dict, n_unknown: int, weights: dict, picks: set) -> float:
    ver = p["verification"]
    stability = (MATURITY_SCORE[p["maturity"]] + VERIFICATION_SCORE[ver["level"]]) / 2
    hw = p["hardware"]
    fit = 0.0
    if profile.get("gpu") and profile["gpu"] in hw.get("gpu_models", []):
        fit += 0.4
    if p["id"] in picks:
        fit += 0.4  # a start-here pick for this hardware
    if p.get("evidence"):
        fit += 0.2
    if profile["priority"] == "throughput" and p.get("evidence"):
        fit += 0.3
    recency = 1.0 if ver.get("last_verified") else 0.0
    friction = FRICTION.get(p.get("audience", "developer"), 0.6)
    # Unknown hardware requirements are a bigger risk than an unrecorded OS version.
    hardware_unknown = 0.3 if not hw.get("agnostic") and not hw.get("architectures") else 0.0
    return (
        weights["stability"] * stability + weights["fit"] * fit + weights["recency"] * recency
        - weights["friction"] * friction - 0.1 * n_unknown - hardware_unknown
    )


def confidence(p: dict, n_unknown: int) -> str:
    level = p["verification"]["level"]
    if level in ("maintainer_verified", "community_reproduced") and n_unknown == 0:
        return "high"
    if level == "author_reported" and n_unknown <= 1:
        return "medium"
    return "low"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--gpu", help="GPU model id (see --list-gpus); sets architecture and VRAM")
    parser.add_argument("--arch", help="GPU architecture, e.g. rdna3 (if your GPU is not listed)")
    parser.add_argument("--count", type=int, default=1, help="number of GPUs (default 1)")
    parser.add_argument("--vram", type=float, help="VRAM per GPU in GB (overrides the GPU table)")
    parser.add_argument("--os", help="operating system: ubuntu, linux, proxmox, windows")
    parser.add_argument("--need", action="append", default=[], help="required feature, repeatable (see docs/glossary.md)")
    parser.add_argument("--runtime", help="required runtime: vllm, sglang, llama_cpp, ...")
    parser.add_argument("--priority", choices=PRIORITY_WEIGHTS, default="balanced")
    parser.add_argument("--include-tools", action="store_true", help="also list agent harnesses and unrelated projects")
    parser.add_argument("--top", type=int, default=3, help="how many recommendations to detail")
    parser.add_argument("--show-rejected", action="store_true", help="list entries ruled out and why")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--list-gpus", action="store_true")
    args = parser.parse_args()

    cat = load_catalog()
    vocab = cat.vocabulary
    if args.list_gpus:
        for g in cat.gpu_models:
            print(f"{g['id']:15} {g['name']:42} {g['architecture']:17} {g['vram_gb'] or '?'} GB")
        return 0

    def fail(msg):
        print(f"error: {msg}", file=sys.stderr)
        return 2

    profile = {"gpu": None, "arch": args.arch, "vendor": None, "vram": args.vram, "count": args.count,
               "os": args.os, "need": args.need, "runtime": args.runtime, "priority": args.priority}
    if args.gpu:
        gpu = cat.gpus_by_id.get(args.gpu)
        if not gpu:
            return fail(f"unknown GPU '{args.gpu}'. Run --list-gpus, or pass --arch and --vram.")
        profile.update(gpu=gpu["id"], arch=gpu["architecture"], vendor=gpu["vendor"])
        if profile["vram"] is None:
            profile["vram"] = gpu["vram_gb"]
    if profile["arch"] and profile["arch"] not in vocab["architecture"]:
        return fail(f"unknown architecture '{profile['arch']}'. Choose from: {', '.join(vocab['architecture'])}")
    if profile["arch"] and not profile["vendor"]:
        profile["vendor"] = next((g["vendor"] for g in cat.gpu_models if g["architecture"] == profile["arch"]), None)
    for f in args.need:
        if f not in vocab["feature"]:
            return fail(f"unknown feature '{f}'. Choose from: {', '.join(vocab['feature'])}")
    if args.runtime and args.runtime not in vocab["runtime"]:
        return fail(f"unknown runtime '{args.runtime}'. Choose from: {', '.join(vocab['runtime'])}")
    if args.os and args.os not in vocab["os"]:
        return fail(f"unknown OS '{args.os}'. Choose from: {', '.join(vocab['os'])}")

    blocking = []
    if not profile["arch"]:
        blocking.append("Which GPU do you have? (--gpu or --arch)")
    if profile["vram"] is None:
        blocking.append("How much VRAM per GPU? (--vram)")
    if not args.os:
        blocking.append("Which OS? (--os) — most entries are Linux-only.")

    picks = {
        i for path in cat.paths
        if profile["arch"] in path.get("architectures", []) and path.get("priority", args.priority) == args.priority
        for i in path["start_with"]
    }
    weights = PRIORITY_WEIGHTS[args.priority]
    accepted, rejected = [], []
    for p in cat.projects:
        if not args.include_tools and p["categories"][0] in ("agents", "other"):
            continue
        no, yes, unknown = gates(p, profile)
        if no:
            rejected.append({"id": p["id"], "name": p["name"], "disqualified_by": no})
            continue
        accepted.append({
            "id": p["id"],
            "name": p["name"],
            "outcome": p["tagline"],
            "maturity": p["maturity"],
            "verification_level": p["verification"]["level"],
            "last_verified": p["verification"].get("last_verified"),
            "confidence": confidence(p, len(unknown)),
            "score": round(score(p, profile, len(unknown), weights, picks), 3),
            "why_it_fits": yes,
            "confirm_before_proceeding": unknown,
            "evidence": p.get("evidence", []),
            "card": f"{BLOB_BASE}/docs/projects/{p['id']}.md",
            "repository": p["links"]["repository"],
        })
    accepted.sort(key=lambda r: (-r["score"], r["name"].lower()))

    result = {
        "profile": {k: v for k, v in profile.items() if v not in (None, [])},
        "missing_information": blocking,
        "recommendations": accepted[: args.top],
        "alternatives": accepted[args.top:],
        "rejected": rejected,
        "note": "Ranked by maturity, verification, fit and setup friction — not by benchmark speed. "
                "Most entries are unverified; confirm versions against each repository before installing.",
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    shown = ", ".join(f"{k}={v}" for k, v in result["profile"].items())
    print(f"Profile: {shown}\n")
    for q in blocking:
        print(f"  ? {q}")
    if blocking:
        print()
    if not accepted:
        print("No compatible entries. Re-run with --show-rejected to see why.")
    for i, r in enumerate(result["recommendations"], 1):
        print(f"{i}. {r['name']}  [{r['id']}]")
        print(f"   {r['outcome']}")
        print(f"   maturity: {r['maturity']} · verification: {r['verification_level']} · confidence: {r['confidence']}"
              f" · last verified: {r['last_verified'] or 'never'}")
        for y in r["why_it_fits"]:
            print(f"   + {y}")
        for u in r["confirm_before_proceeding"]:
            print(f"   ? {u}")
        if r["evidence"]:
            print(f"   evidence: {', '.join(r['evidence'])}")
        print(f"   {r['card']}\n")
    if result["alternatives"]:
        print("Also compatible: " + ", ".join(r["id"] for r in result["alternatives"]) + "\n")
    if args.show_rejected and rejected:
        print("Ruled out:")
        for r in rejected:
            print(f"  - {r['id']}: {' '.join(r['disqualified_by'])}")
    elif rejected:
        print(f"{len(rejected)} entries ruled out by hard requirements (--show-rejected to list).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
