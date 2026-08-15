#!/usr/bin/env bash
set -euo pipefail

base_url="https://raw.githubusercontent.com/mameikagou/skill-forge/main/skills/mainline-drift-audit"
skill_dir="${HOME}/.claude/skills/mainline-drift-audit"

mkdir -p "${skill_dir}/agents" "${skill_dir}/scripts"
curl -fsSL "${base_url}/SKILL.md" -o "${skill_dir}/SKILL.md"
curl -fsSL "${base_url}/agents/openai.yaml" -o "${skill_dir}/agents/openai.yaml"
curl -fsSL "${base_url}/scripts/scan_repo.py" -o "${skill_dir}/scripts/scan_repo.py"
chmod +x "${skill_dir}/scripts/scan_repo.py"

test -s "${skill_dir}/SKILL.md"
test -s "${skill_dir}/scripts/scan_repo.py"
echo "mainline-drift-audit installed at ${skill_dir}"
