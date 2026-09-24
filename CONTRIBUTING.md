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

## How to add an entry

1. Fork the repo and add your entry to the appropriate section of `README.md`.
2. Follow the existing format:

   ```markdown
   - [owner/repo](https://github.com/owner/repo) - One-line description of what it does
     and any notable results. Built by **Discord-handle**.
   ```
3. If the repo was shared by someone other than the owner, add `, shared by @Member`.
4. If you add a new section, add it to the Index at the top.
5. Open a pull request.

Prefer entries that include a concrete, reproducible result (tok/s, context length,
hardware config) — that's what makes this list useful.

If you'd rather not deal with git, just post in the Discord or open an issue.
