import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCKER_DIR = ROOT_DIR / "formbricks-quickstart"

def run(cmd: list[str]):
    print(">>", " ".join(cmd))
    result = subprocess.run(cmd, cwd=DOCKER_DIR)
    if result.returncode != 0:
        sys.exit(result.returncode)

def docker_up():
    print("Starting Formbricks...")
    run(["docker", "compose", "up", "-d"])
    print("Formbricks is running at http://localhost:3000")

def docker_down():
    print("Stopping Formbricks...")
    run(["docker", "compose", "down"])
    print("Formbricks stopped")
