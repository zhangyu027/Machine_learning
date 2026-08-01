#!/usr/bin/env bash
set -euo pipefail

TARGET="$HOME/projects/Machine_learning/11_enterprise_data_platform_architecture"
PARENT="$(dirname "$TARGET")"
SOURCE="$(cd "$(dirname "$0")" && pwd)/11_enterprise_data_platform_architecture"
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP="${TARGET}_backup_${STAMP}"

mkdir -p "$PARENT"
cd "$PARENT"

if [[ -d "$TARGET" ]]; then
  echo "Backing up existing folder to: $BACKUP"
  mv "$TARGET" "$BACKUP"
fi

cp -R "$SOURCE" "$TARGET"

# Remove common macOS quarantine and ACL metadata without changing the path.
xattr -dr com.apple.quarantine "$TARGET" 2>/dev/null || true
chmod -R u+rwX "$TARGET"

cd "$TARGET"
python3 - <<'PY'
import os
print("Current directory access OK:", os.getcwd())
PY

echo
echo "Installed at: $TARGET"
echo "Next commands:"
echo "  cd \"$TARGET\""
echo "  python3.11 -m venv .venv"
echo "  source .venv/bin/activate"
echo "  python -m pip install --upgrade pip"
echo "  python -m pip install -e reference_implementation"
echo "  pytest -q"
echo "  python -m enterprise_data_platform.pipeline"
