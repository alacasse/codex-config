# Changelog

## Unreleased

### Linked config ownership detection

Problem: repo-owned files can be edited through their installed `~/.codex`
symlink while the agent is working in another project, making it easy to miss
the codex-config changelog and git status expectations.

Decision: add `scripts/codex_owner.py` and global instructions for checking
whether a `~/.codex` path resolves to this repo. Repo-owned links now carry a
clear expectation to update `CHANGELOG.md` for meaningful workflow changes and
report this repo's git status.

Expected effect: agents can safely tune linked skills, agents, rules, and
instructions from any project while still treating the edit as codex-config
work.

### Vendor-owned Graphify skill

Problem: `graphify` is vendor-owned and should not be represented as a local
override in this repo's feature manifest.

Decision: remove the local `graphify` feature from `codex-features.json`; the
vendor installer remains responsible for `~/.codex/skills/graphify`.

Expected effect: this repository owns only its explicit linked features, while
vendor-owned skills can manage themselves in the final `~/.codex` directory.

### Versioned feature installer

Problem: `install.sh` was a set of hard-coded symlinks, which made it easy for
the live Codex layout to drift from the repository and hard to add new workflow
features deliberately.

Decision: add a manifest-driven installer. `codex-features.json` now defines
versioned Codex features and their links, while `install.sh` delegates to a
Python installer that supports listing, dry runs, selective installs, conflict
detection, and installed-version state.

Expected effect: new skills, agents, rules, and instruction bundles can be
versioned as features and installed reproducibly without rewriting installer
logic each time.
