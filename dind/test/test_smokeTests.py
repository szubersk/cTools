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

    cmd = f"docker run --privileged -d {image}"
    container_id = subprocess.check_output(cmd, shell=True).decode().strip()
    subprocess.check_call(f"docker exec {container_id} true", shell=True)

    yield testinfra.get_host(f"docker://{container_id}")

    subprocess.check_call(f"docker rm -fv {container_id}", shell=True)


def test_pipPackagesAreAvailable(host):
    avail_pkgs = host.pip_package.get_packages()
    assert "tox" in avail_pkgs


def test_executablesAreAvailable(host):
    execs = ["docker", "dockerd"]

    for e in execs:
        assert host.run(f"{e} --version").succeeded


def test_dockerEngineVersion(host):
    res = host.run('docker info -f "{{ .ServerVersion }}"')

    assert res.succeeded
    assert res.stdout.startswith("19.03.8")


def test_canPullImageFromDockerHub(host):
    assert host.run("docker pull -q busybox:latest").succeeded


def test_canSpawnContainerInDefaultNetworkWithNoVolume(host):
    assert host.run("docker pull -q busybox:latest").succeeded
    assert host.run("docker run busybox:latest /bin/echo -n OK").stdout == "OK"


def test_canSpawnContainerInBridgeNetwork(host):
    assert host.run("docker network create net").succeeded

    cmd = "docker run --network net busybox:latest nc -z non-existent-host 53"
    assert host.run(cmd).failed

    cmd = "docker run --network net busybox:latest nc -z 8.8.8.8 53"
    assert host.run(cmd).succeeded


def test_canSpawnContainerWithNamedVolume(host):
    assert host.run("docker volume create vol").succeeded

    cmd = 'docker run -v vol:/vol busybox:latest sh -c "echo OK > /vol/file && cat /vol/file1"'
    assert host.run(cmd).failed

    cmd = 'docker run -v vol:/vol busybox:latest sh -c "echo OK > /vol/file && cat /vol/file"'
    assert host.run(cmd).succeeded
