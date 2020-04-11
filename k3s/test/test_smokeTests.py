import json
import pytest
import subprocess
import sys
import testinfra


@pytest.fixture(scope="session")
def host(request):
    with open(f"{sys.path[0]}/../image.pkrvars.json") as f:
        j = json.load(f)
        image = f"{j['targetImage']}:{j['targetTag']}"

    cmd = f"docker run -i --privileged -p 6443:6443 -d {image}"
    container_id = subprocess.check_output(cmd, shell=True).decode().strip()
    subprocess.check_call(f"docker exec {container_id} true", shell=True)

    yield testinfra.get_host(f"docker://{container_id}")

    subprocess.check_output(f"docker rm -fv {container_id}", shell=True)


def test_canEcho(host):
    assert host.run("/bin/echo OK").succeeded
