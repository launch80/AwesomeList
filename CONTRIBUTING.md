# Contributing

This list indexes open-source work built by Launch80 community members and shared in the
[Launch80 Discord](https://discord.gg/launch80) to help others make progress.

## What belongs here

- Repos **you own** (or that another Launch80 community member owns) that were shared in the
  Discord server, e.g.:
  - inference engine forks, kernels, and patches (vLLM / Radiance / llama.cpp / SGLang / AITER ...)
  - launcher scripts, deployment recipes, and multi-GPU platform guides
  - benchmarks, evals, monitoring, and dev tooling
  - agent harnesses and anything else that helps the community
- Not here: upstream projects that aren't community-owned (vLLM, llama.cpp, ROCm, etc.),
  or commercial links.

If you'd rather not deal with git, post in the Discord or open an
[Add a project](https://github.com/launch80/AwesomeList/issues/new?template=new-entry.yml) issue.

## How the repo works

`catalog/` is the source of truth. `README.md`, `catalog.json`, `llms.txt`, `llms-full.txt`,
`docs/projects/`, `docs/hardware/`, `docs/benchmarks.md` and `docs/glossary.md` are **generated**.
Don't edit them by hand; CI fails if they drift from the catalog. The README's fixed prose
(intro, section text) lives in `docs/templates/README.md.tmpl`, and the Agent quickstart prompt
lives in `prompts/agent-quickstart.md`. Rebuild after editing either one.

```
catalog/
  projects/<id>.yaml                  one record per repo          → schemas/project.schema.json
  recipes/<id>.yaml                   reproducible deployment path → schemas/recipe.schema.json
  benchmarks/benchmark-results.jsonl  one measured result per line → schemas/benchmark.schema.json
  compatibility/gpu-models.yaml       GPU → architecture, gfx, VRAM
  paths.yaml                          README "Start here" rows
  vocabulary.yaml                     controlled terms (see docs/glossary.md)
```

## Add a project

1. Copy an existing record in `catalog/projects/` that's similar to yours, and rename it `<id>.yaml`.
   The `id` is kebab-case, stable, and must match the file name.
2. Fill in what you **know**. Leave out anything you don't know. A missing field reads as
   "not yet documented", which is far better than a guess.
   - `tagline`: one line that says what someone gets from it.
   - `use_it_if`: who it's for, starting with "You…".
   - `hardware.architectures` and `hardware.gpu_count.min` are **hard gates**. The selector never
     shows your entry to someone who fails them, so set them accurately.
   - Use only terms from [`docs/glossary.md`](docs/glossary.md). Need a new one? Add it to
     `catalog/vocabulary.yaml` in the same PR.
3. New maturity is `unverified` (or `experimental` for a WIP/proof of concept). Only maintainers
   set `supported` or `recommended`. `recommended` also requires a reproduction on record.
4. Run:

   ```sh
   pip install -r requirements.txt
   python scripts/validate.py
   python scripts/build.py
   ```

5. Commit the record **and** the regenerated files, then open a pull request.

## Add a benchmark result

Append one JSON line to `catalog/benchmarks/benchmark-results.jsonl` and add its `id` to the
project's `evidence` list. Report as much of the workload as you can: exact model artifact,
quantization, context length, prompt/output tokens, concurrency, versions, the command, and the
date. Set `mode` to `single_stream` or `batched`. Use `not_reported` only if the source didn't say,
because those rows are kept apart from the comparable tables. [BetterBench](https://github.com/GGZ14/BetterBench)
is the preferred tool.

## Add a recipe

Copy [`docs/recipe-template.yaml`](docs/recipe-template.yaml) to `catalog/recipes/<id>.yaml`.
Recipes are narrow and exact: one hardware/OS/runtime/model combination, with pinned versions and
the commands you actually ran. `verification.tested_by` and `last_verified` are required.

## Verify someone else's entry

File a [reproduction report](https://github.com/launch80/AwesomeList/issues/new?template=reproduction-report.yml).
A maintainer records it in the entry's `verification` block (`community_reproduced`, `tested_by`,
`last_verified`, `last_commit_checked`). Entries are promoted on reproducibility, not stars.

## Maturity labels

| Label | Meaning |
|---|---|
| `recommended` | Repeatable setup, recently reproduced, clear docs. Maintainer-set. |
| `supported` | Active and supported by its author, but environment-sensitive or narrow. |
| `experimental` | Promising proof of concept; expect manual debugging. |
| `historical` | Useful reference, no longer the suggested default. |
| `unverified` | Submitted, not yet reproduced by anyone else. |
