#!/usr/bin/env bash
# Functional smoke test for .github/scripts/create-issues.sh.
#
# Stubs the `gh` CLI so no network call is made, then asserts:
#   1. the script is syntactically valid
#   2. it creates exactly the expected set of issues, with Module B covered
#   3. every issue body links to the published site, not to a source file
#   4. a second run is idempotent — the dedup guard skips everything
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

state="$work/created.txt"
calls="$work/calls.txt"
: >"$state"
: >"$calls"

# ─── gh stub ──────────────────────────────────────────────────────────────────
cat >"$work/gh" <<'STUB'
#!/usr/bin/env bash
set -euo pipefail
echo "$*" >>"$CALLS"
if [ "${1:-}" = "issue" ] && [ "${2:-}" = "list" ]; then
  # The caller's --jq is: [.[] | select(.title == "TITLE")] | length
  jq_expr=""
  while [ $# -gt 0 ]; do
    if [ "$1" = "--jq" ]; then jq_expr="$2"; fi
    shift
  done
  title="${jq_expr#*.title == \"}"
  title="${title%%\"*}"
  # awk, not `grep -Fx`: Cygwin's grep fails an exact-line match on a line
  # starting with a 4-byte emoji, which would fake a dedup failure. The real
  # `gh --jq` does a byte-exact jq string comparison.
  awk -v t="$title" '$0 == t { n++ } END { print n + 0 }' "$STATE"
  exit 0
fi
if [ "${1:-}" = "issue" ] && [ "${2:-}" = "create" ]; then
  title=""
  body=""
  while [ $# -gt 0 ]; do
    case "$1" in
      --title) title="$2" ;;
      --body)  body="$2" ;;
    esac
    shift
  done
  printf '%s\n' "$title" >>"$STATE"
  printf '%s\n' "$body" >>"$BODIES"
  exit 0
fi
exit 0
STUB
chmod +x "$work/gh"

export PATH="$work:$PATH"
export STATE="$state" CALLS="$calls" BODIES="$work/bodies.txt"
: >"$BODIES"
export GH_TOKEN=stub CYCLE_LABEL="audit-2026" MILESTONE="Audit 2026"
export REPO="NikoMix/specialization-hybrid-cloud-azure-hci"

script="$repo_root/.github/scripts/create-issues.sh"

echo "== 1. syntax =="
bash -n "$script"
echo "   OK"

echo "== 2. first run =="
bash "$script" >"$work/run1.log"
created=$(wc -l <"$state")
echo "   created: $created"

module_b=$(awk '/^B\./ { n++ } END { print n + 0 }' "$state")
module_a=$(awk '/^A\./ { n++ } END { print n + 0 }' "$state")
echo "   module A: $module_a   module B: $module_b"

fail=0
[ "$created" -eq 14 ] || { echo "   FAIL expected 14 issues, got $created"; fail=1; }
[ "$module_a" -eq 7 ] || { echo "   FAIL expected 7 Module A issues, got $module_a"; fail=1; }
[ "$module_b" -eq 6 ] || { echo "   FAIL expected 6 Module B issues, got $module_b"; fail=1; }

echo "== 3. issue bodies =="
site_links=$(grep -ci 'https://nikomix.github.io/specialization-hybrid-cloud-azure-hci/docs/' "$BODIES" || true)
stale=$(grep -c 'src/content/docs\|\.mdx\|\$SITE_URL' "$BODIES" || true)
echo "   published-site links: $site_links   stale source links: $stale"
[ "$site_links" -ge 14 ] || { echo "   FAIL expected >=14 site links, got $site_links"; fail=1; }
[ "$stale" -eq 0 ] || { echo "   FAIL $stale unexpanded or stale doc link(s)"; fail=1; }

echo "== 4. idempotency (second run) =="
before=$(wc -l <"$state")
bash "$script" >"$work/run2.log"
after=$(wc -l <"$state")
skipped=$(grep -c '^⏭' "$work/run2.log" || true)
echo "   issues before: $before  after: $after  skipped: $skipped"
[ "$before" -eq "$after" ] || { echo "   FAIL second run created $((after - before)) duplicate(s)"; fail=1; }
[ "$skipped" -eq 14 ] || { echo "   FAIL expected 14 skips, got $skipped"; fail=1; }

echo
if [ "$fail" -eq 0 ]; then
  echo "PASS: create-issues.sh creates 14 issues (7 Module A, 6 Module B, 1 gate) and is idempotent."
else
  echo "FAIL"
fi
printf '\nTitles created:\n'
sed 's/^/  /' "$state"
exit "$fail"
