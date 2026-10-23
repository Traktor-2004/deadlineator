#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")" && pwd)"
cd "$project_root"

if [[ "$#" -ne 1 ]]; then
  printf 'Usage: bash ci-verify.sh build|test\n' >&2
  exit 2
fi
mode="$1"
python_exe="$(cygpath -u "$LOCALAPPDATA/Programs/Python/Python312/python.exe")"
archive="$project_root/deadlineator-source.zip"

if [[ ! -x "$python_exe" ]]; then
  printf 'Python 3.12 was not found: %s\n' "$python_exe" >&2
  exit 1
fi
if [[ ! -f "$archive" ]]; then
  printf 'Source archive was not found: %s\n' "$archive" >&2
  exit 1
fi

printf 'Mode: %s\n' "$mode"
printf 'Python: %s\n' "$python_exe"
"$python_exe" -c 'import sys,zipfile; a,p=sys.argv[1:3]; z=zipfile.ZipFile(a); [z.extract(n,p) for n in z.namelist() if n.startswith(("data/","scripts/","src/","tests/"))]' "$archive" "$project_root"

case "$mode" in
  build)
    "$python_exe" --version
    "$python_exe" -m compileall -q src tests scripts
    printf 'Compilation passed.\n'
    ;;
  test)
    "$python_exe" -m unittest discover -s tests -v
    printf 'Unit tests passed.\n'
    ;;
  *)
    printf 'Unsupported mode: %s\n' "$mode" >&2
    exit 2
    ;;
esac


