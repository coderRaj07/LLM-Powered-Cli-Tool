from formbricks.generate import generate
from formbricks.docker import docker_up, docker_down
from formbricks.seed import seed

def handle_formbricks_command(command: str):
    if command == "up":
        docker_up()
    elif command == "down":
        docker_down()
    elif command == "generate":
        generate()
    elif command == "seed":
        seed()
