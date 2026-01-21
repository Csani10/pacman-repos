#!/usr/bin/env python3
import sys
import json
import os
import subprocess
import shutil
from pathlib import Path

repo_cfg = {}

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

    for package in packages:
        if not os.path.exists(f"{package}/"):
            print(f"Cant add '{package}', not found")
            not_found_packages.append(package)

    for package in not_found_packages:
        packages.remove(package)


    if os.path.exists(os.environ["PWD"] + f"/../{repo_name}/"):
        shutil.rmtree(os.environ["PWD"] + f"/../{repo_name}/")    

    for package in packages:
        src_dir = Path(os.environ["PWD"] + f"/{package}/")
        dst_dir = Path(os.environ["PWD"] + f"/../{repo_name}/x86_64")

        dst_dir.mkdir(parents=True, exist_ok=True)

        for file in src_dir.glob("*.pkg.tar.zst"):
            shutil.copy2(file,dst_dir)

    for file in dst_dir.glob("*.pkg.tar.zst"):
        subprocess.run(["repo-add", f"{repo_name}.db.tar.gz", f"{file}"], cwd=dst_dir)

    print("Completed")
    exit(0)

if __name__ == "__main__":
    main()
