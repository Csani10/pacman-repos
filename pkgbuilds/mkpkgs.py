#!/usr/bin/env python3
from pathlib import Path
import subprocess

def info(msg):
    print(f"[INFO] {msg}")

def error(msg):
    print(f"[ERROR] {msg}")

def main():
    info("Making all packages...")
    pwd = Path(__file__).resolve().parent
    
    for entry in pwd.iterdir():
        if not entry.is_dir(): continue
        info(f"Making '{entry.name}'...")
        retval = subprocess.run(["makepkg", "-f"], cwd=entry)
        if not retval.returncode == 0:
            error(f"Failed to build '{entry.name}', exited with: {retval}")
        else:
            info(f"Done building '{entry.name}'")

    info("Done building everything!")

if __name__ == "__main__":
    main()
