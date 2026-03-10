#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="${1:-external/clone_first}"
DRY_RUN="${DRY_RUN:-0}"

REPOS=(
  "https://github.com/IfcOpenShell/IfcOpenShell.git"
  "https://github.com/mozman/ezdxf.git"
  "https://github.com/blender/blender.git"
  "https://github.com/FreeCAD/FreeCAD.git"
)

mkdir -p "${TARGET_DIR}"

echo "[info] clone-first bootstrap başladı"
echo "[info] hedef klasör: ${TARGET_DIR}"
echo "[info] dry-run: ${DRY_RUN}"

for repo in "${REPOS[@]}"; do
  name="$(basename "${repo}" .git)"
  dest="${TARGET_DIR}/${name}"

  if [[ -d "${dest}/.git" ]]; then
    echo "[skip] ${name} zaten mevcut, güncelleniyor"
    if [[ "${DRY_RUN}" == "1" ]]; then
      echo "[dry-run] git -C ${dest} fetch --all --tags --prune"
    else
      git -C "${dest}" fetch --all --tags --prune
    fi
    continue
  fi

  echo "[clone] ${repo}"
  if [[ "${DRY_RUN}" == "1" ]]; then
    echo "[dry-run] git clone --depth 1 ${repo} ${dest}"
  else
    git clone --depth 1 "${repo}" "${dest}"
  fi
done

echo "[ok] clone-first bootstrap tamamlandı"
