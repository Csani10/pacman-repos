#!/usr/bin/env python3
import sys
import json
import os
import subprocess
import shutil
from pathlib import Path

repo_cfg = {}

def info(msg):
    print(f"[INFO] {msg}")

def error(msg):
    print(f"[ERROR] {msg}")

def main():
    global repo_cfg
    argv = sys.argv
    argc = len(argv)

    if argc < 2:
        exit(1)

    with open("repos.json", "r") as f:
        repo_cfg = json.loads(f.read())

    if argv[1] not in repo_cfg:
        exit(1)

    repo_name = argv[1]

    packages = repo_cfg[repo_name]
    not_found_packages = []

    pwd = Path(__file__).resolve().parent

    info(f"Starting build for repo: '{repo_name}'")

    for package in packages:
        if not os.path.exists(f"{package}/"):
            error(f"Cant add '{package}', not found")
            not_found_packages.append(package)
        else:
            info(f"Found package '{package}'")

    for package in not_found_packages:
        packages.remove(package)

    info("Removing old repo, creating new repo")
    if os.path.exists(f"{pwd}/../{repo_name}/"):
        shutil.rmtree(f"{pwd}/../{repo_name}/")    

    dst_dir = Path(f"{pwd}/../{repo_name}/x86_64")
    info("Done creating new repo")

    info("Copying package files")
    pkg_files = []
    for package in packages:
        src_dir = Path(f"{pwd}/{package}/")

        dst_dir.mkdir(parents=True, exist_ok=True)

        for file in src_dir.glob("*.pkg.tar.zst"):
            shutil.copy2(file,dst_dir)
            pkg_files.append(dst_dir / file)
            info(f"Copying {str(file)}")
    info("Done copying package files")

    info("Building repo")
    subprocess.run(
        ["repo-add", f"{repo_name}.db.tar.gz", *map(str, pkg_files)],
        cwd=dst_dir,
        check=True
    )

    os.unlink(f"{pwd}/../{repo_name}/x86_64/{repo_name}.db")
    os.unlink(f"{pwd}/../{repo_name}/x86_64/{repo_name}.files")
    os.rename(f"{pwd}/../{repo_name}/x86_64/{repo_name}.db.tar.gz", f"{pwd}/../{repo_name}/x86_64/{repo_name}.db")
    os.rename(f"{pwd}/../{repo_name}/x86_64/{repo_name}.files.tar.gz", f"{pwd}/../{repo_name}/x86_64/{repo_name}.files")

    info("Done building repo")
    info("All done!")
    exit(0)

if __name__ == "__main__":
    main()
