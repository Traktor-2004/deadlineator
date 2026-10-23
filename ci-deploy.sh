#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")" && pwd)"
cd "$project_root"
python_exe="$(cygpath -u "$LOCALAPPDATA/Programs/Python/Python312/python.exe")"
archive="$project_root/deadlineator-source.zip"
release_parent='/d/учёба/Программная инженерия/deploy/releases'

if [[ ! -x "$python_exe" ]]; then
  printf 'Python 3.12 was not found: %s\n' "$python_exe" >&2
  exit 1
fi
if [[ ! -f "$archive" ]]; then
  printf 'Source archive was not found: %s\n' "$archive" >&2
  exit 1
fi

"$python_exe" -c 'import sys,zipfile; a,p=sys.argv[1:3]; z=zipfile.ZipFile(a); [z.extract(n,p) for n in z.namelist() if n.startswith(("data/","scripts/","src/","tests/"))]' "$archive" "$project_root"
release_path="$release_parent/release-$(date +%Y%m%d-%H%M%S)-$$"
mkdir -p "$release_path/data" "$release_path/scripts"
cp -R "$project_root/src" "$release_path/"
cp "$project_root/data/demo_tasks.json" "$release_path/data/"
cp "$project_root/scripts/seed_demo_data.py" "$release_path/scripts/"
cp "$project_root/README.md" "$release_path/"
for required in \
  "$release_path/src/server.py" \
  "$release_path/src/static/index.html" \
  "$release_path/data/demo_tasks.json" \
  "$release_path/scripts/seed_demo_data.py"
do
  if [[ ! -f "$required" ]]; then
    printf 'Release is incomplete; missing %s\n' "$required" >&2
    exit 1
  fi
done

printf 'Local release prepared: %s\n' "$release_path"


