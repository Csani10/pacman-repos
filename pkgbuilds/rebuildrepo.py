#!/usr/bin/env python3
import sys
import json
import os

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

    packages = repo_cfg[argv[1]]

    for package in packages:
        if not os.path.exists(f"{package}/"):
            print(f"Cant add '{package}', not found")
            packages.remove(package)

    print(packages)

if __name__ == "__main__":
    main()
