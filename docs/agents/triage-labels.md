# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

The two category roles use the existing `bug` and `enhancement` labels.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.

## Repository setup

Check the seven triage roles and five Wayfinder labels without changing GitHub:

```bash
./scripts/setup_github_labels.py --repo alacasse/codex-config
```

After explicit approval for the reported creations, apply only the missing
labels that have repository-approved metadata:

```bash
./scripts/setup_github_labels.py --repo alacasse/codex-config --apply
```

The setup command never edits a same-name label. The existing `bug`,
`enhancement`, `ready-for-agent`, and `wontfix` labels retain their live
metadata.
