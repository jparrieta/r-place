#!/usr/bin/env bash
# leadscan.sh DIR: count credential-shaped strings in each case-lead archive (whole or in .partNN).
# A count is not a finding: on 2026-10-02 every hit was an encrypted_content run, an __oailb cookie,
# an OpenAI-Organization/Project id or documentation text. Look at hits with values redacted.
cd "${1:?folder of lead archives}"
for base in $(ls | sed -E 's/\.part[0-9]+$//' | sort -u); do
  n=$(cat "$base"* | zstd -dc 2>/dev/null | grep -acE 'eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}|sk-proj-[A-Za-z0-9_-]{20}|sk-ant-[A-Za-z0-9_-]{20}|"access_token": *"[A-Za-z0-9]|Bearer [A-Za-z0-9._-]{20}')
  printf '%s\t%s\n' "$base" "$n"
done
