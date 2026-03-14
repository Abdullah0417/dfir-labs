#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
import zipfile
from pathlib import Path

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: build_package.py <lab_dir>", file=sys.stderr)
        return 2

    repo_root = Path.cwd()
    lab_dir = repo_root / sys.argv[1]
    manifest_path = lab_dir / "pipeline/manifests/content-manifest.json"
    dist_dir = lab_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    package_prefix = manifest["package_prefix"]
    short_sha = os.environ.get("GITHUB_SHA", "local")[:7]
    zip_path = dist_dir / f"{package_prefix}-{short_sha}.zip"

    to_package: list[Path] = []

    for rel in manifest["deployable_files"]:
        to_package.append(lab_dir / rel)

    for rel in manifest["proof_files"]:
        to_package.append(lab_dir / rel)

    for rel in manifest["proof_directories"]:
        directory = lab_dir / rel
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                to_package.append(path)

    seen = set()
    unique_files = []
    for path in to_package:
        if path in seen:
            continue
        seen.add(path)
        unique_files.append(path)

    missing = [str(p.relative_to(repo_root)) for p in unique_files if not p.exists()]
    if missing:
        print(json.dumps({"missing": missing}, indent=2), file=sys.stderr)
        return 1

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in unique_files:
            arcname = str(path.relative_to(lab_dir))
            zf.write(path, arcname)

    sums_path = dist_dir / "SHA256SUMS.txt"
    with sums_path.open("w", encoding="utf-8") as f:
        for path in unique_files:
            f.write(f"{sha256_file(path)}  {path.relative_to(lab_dir)}\n")
        f.write(f"{sha256_file(zip_path)}  {zip_path.name}\n")

    (dist_dir / "content-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print(f"[OK] Created package: {zip_path}")
    print(f"[OK] Created hashes:  {sums_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())