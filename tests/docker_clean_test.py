import io
import os
import sys
import unittest
import docker_clean
from contextlib import redirect_stdout
from click.testing import CliRunner
from docker.errors import NotFound
from docker import client
DOCKER_CLIENT = client.from_env()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR + '/../')


class DockerCleanTest(unittest.TestCase):
    def test_remove_containers_empty(self):
        clean_cts()

        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_containers(True)
        res = fake_file.getvalue()
        self.assertEqual('No exited container to remove', res.strip())

    def test_remove_containers_pretend(self):
        clean_cts()
        clean_images()

        DOCKER_CLIENT.containers.run('hello-world', remove=False)
        num_containers = len(DOCKER_CLIENT.containers.list(all=True))
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_containers(False)
        res = fake_file.getvalue()
        self.assertEqual("--force is not set so I won't do anything", res.strip())
        self.assertEqual(num_containers, len(DOCKER_CLIENT.containers.list(all=True)))

    def test_remove_containers(self):
        clean_cts()
        clean_images()

        DOCKER_CLIENT.containers.run('hello-world', remove=False)
        num_containers = len(DOCKER_CLIENT.containers.list(all=True))
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_containers(True)
        res = fake_file.getvalue()
        self.assertEqual("Removed 1 exited container(s), saved", res[:38].strip())
        self.assertEqual((num_containers - 1), len(DOCKER_CLIENT.containers.list(all=True)))

    def test_remove_images_empty(self):
        clean_cts()
        clean_images()

        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_images(True)
        res = fake_file.getvalue()
        self.assertEqual('No image to remove', res.strip())

    def test_remove_images_pretend(self):
        clean_cts()
        clean_images()

        DOCKER_CLIENT.containers.run('hello-world', remove=True)
        num_images = len(DOCKER_CLIENT.images.list(all=True))
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_images(False)
        res = fake_file.getvalue()
        self.assertEqual("--force is not set so I won't do anything", res.strip())
        self.assertEqual(num_images, len(DOCKER_CLIENT.images.list(all=True)))

    def test_remove_images(self):
        clean_cts()
        clean_images()

        DOCKER_CLIENT.containers.run('hello-world', remove=True)
        num_images = len(DOCKER_CLIENT.images.list(all=True))
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_images(True)
        res = fake_file.getvalue()
        self.assertEqual((num_images - 1), len(DOCKER_CLIENT.images.list(all=True)))
        self.assertEqual("Removed", res[:9].strip())

    def test_remove_networks_empty(self):
        clean_cts()
        DOCKER_CLIENT.networks.prune()

        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_networks(True)
        res = fake_file.getvalue()
        self.assertEqual('No network to remove', res.strip())

    def test_remove_networks_pretend(self):
        DOCKER_CLIENT.networks.prune()
        DOCKER_CLIENT.networks.create('network_pytest')

        num_networks = len(DOCKER_CLIENT.networks.list())
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_networks(False)
        res = fake_file.getvalue()
        self.assertEqual("--force is not set so I won't do anything", res.strip())
        self.assertEqual(num_networks, len(DOCKER_CLIENT.networks.list()))

    def test_remove_networks(self):
        DOCKER_CLIENT.networks.prune()
        DOCKER_CLIENT.networks.create('network_pytest')

        num_networks = len(DOCKER_CLIENT.networks.list())
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_networks(True)
        res = fake_file.getvalue()
        self.assertEqual("Removed 1 network(s)", res.strip())
        self.assertEqual((num_networks - 1), len(DOCKER_CLIENT.networks.list()))

    def test_remove_volumes_empty(self):
        clean_cts()
        DOCKER_CLIENT.volumes.prune()

        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_volumes(True)
        res = fake_file.getvalue()
        self.assertEqual('No volume to remove', res.strip())

    def test_remove_volumes_pretend(self):
        DOCKER_CLIENT.volumes.prune()
        DOCKER_CLIENT.volumes.create('test123')

        num_volumes = len(DOCKER_CLIENT.volumes.list())
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_volumes(False)
        res = fake_file.getvalue()
        self.assertEqual("--force is not set so I won't do anything", res.strip())
        self.assertEqual(num_volumes, len(DOCKER_CLIENT.volumes.list()))

    def test_remove_volumes(self):
        DOCKER_CLIENT.volumes.prune()
        DOCKER_CLIENT.volumes.create('test123')
        num_volumes = len(DOCKER_CLIENT.volumes.list())
        fake_file = io.StringIO()
        with redirect_stdout(fake_file):
            docker_clean.remove_volumes(True)
        res = fake_file.getvalue()
        self.assertEqual("Removed 1 volume(s), saved", res[:28].strip())
        self.assertEqual((num_volumes - 1), len(DOCKER_CLIENT.volumes.list()))

    def test_no_arg(self):
        result = CliRunner().invoke(docker_clean.clean)
        self.assertEqual(0, result.exit_code)
        regex = r'.*Cleaning Docker stopped containers.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused images.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused volumes.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused networks.*'
        self.assertRegex(result.output, regex)

    def test_bad_arg(self):
        result = CliRunner().invoke(docker_clean.clean, ['hello-world'])
        self.assertEqual(2, result.exit_code)
        self.assertRegex(result.output, r'Usage: docker-clean \[OPTIONS\].*')

    def test_full_clean(self):
        # Remove data that could create conflicts
        # Stop all containers
        clean_cts()
        # Remove all networks
        DOCKER_CLIENT.networks.prune()
        # Remove all volumes
        DOCKER_CLIENT.volumes.prune()
        # Remove all images
        clean_images()

        # Standard info
        num_default_nets = len(DOCKER_CLIENT.networks.list())
        num_default_cts = len(DOCKER_CLIENT.containers.list(all=True))
        num_default_images = len(DOCKER_CLIENT.images.list(all=True))
        num_default_vols = len(DOCKER_CLIENT.volumes.list())

        # Start specific networks
        DOCKER_CLIENT.networks.create('test_delete')
        net_pytest = DOCKER_CLIENT.networks.create('network_pytest')
        nets = DOCKER_CLIENT.networks.list()
        # 5 because by default I have already 3
        self.assertIs(len(nets), (2 + num_default_nets))

        # We should have volumes also stored
        DOCKER_CLIENT.volumes.create('hello')
        self.assertIs(len(DOCKER_CLIENT.volumes.list()), (1 + num_default_vols))

        # Create 2 ct that'll be off but present
        # don't remove the first
        DOCKER_CLIENT.containers.run('alpine:latest', name='hello_world_test')
        ct_test = DOCKER_CLIENT.containers.run('edyan/adminer:latest',
                                                     remove=False, detach=True, name='ct_test')

        net_pytest.connect(ct_test)

        # Make sure we have two new image : hello-world + adminer
        num_images = len(DOCKER_CLIENT.images.list(all=True))
        self.assertIs(num_images, (2 + num_default_images))

        # Make sure we have two new containers
        cts = DOCKER_CLIENT.containers.list(all=True)
        self.assertIs(len(cts), (2 + num_default_cts))

        # CLEAN
        result = CliRunner().invoke(docker_clean.clean, ['--force'])
        self.assertEqual(0, result.exit_code)
        regex = r'.*Cleaning Docker stopped containers.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Removed 1 exited container\(s\), saved 0 bytes.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused images.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Removed [0-9]+ images\(s\).*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused volumes.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Removed 1 volume\(s\), saved 0 bytes.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused networks.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Removed 1 network\(s\).*'
        self.assertRegex(result.output, regex)

        # Make sure it has been cleaned
        # Except ct_test that is running so : 1 image, 1 network, 1 container
        self.assertIs(len(DOCKER_CLIENT.networks.list()), num_default_nets + 1)
        self.assertIs(len(DOCKER_CLIENT.volumes.list()), num_default_vols)
        self.assertIs(len(DOCKER_CLIENT.images.list(all=True)), num_default_images + 1)
        self.assertIs(len(DOCKER_CLIENT.networks.list()), num_default_nets + 1)

        ct_test.stop()

        # Stop adminer and clean again
        result = CliRunner().invoke(docker_clean.clean, ['--force'])
        self.assertEqual(0, result.exit_code, 'Error: {}'.format(result.output))
        regex = r'.*Cleaning Docker stopped containers.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Removed 1 exited container\(s\), saved 0 bytes.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused images.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Removed [0-9]+ images\(s\).*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused volumes.*'
        self.assertRegex(result.output, regex)
        regex = r'.*No volume to remove*'
        self.assertRegex(result.output, regex)
        regex = r'.*Cleaning Docker unused networks.*'
        self.assertRegex(result.output, regex)
        regex = r'.*Removed 1 network\(s\).*'
        self.assertRegex(result.output, regex)

        # Make sure it has been cleaned
        # Except ct_test so : 1 image, 1 network, 1 container
        self.assertIs(len(DOCKER_CLIENT.networks.list()), num_default_nets)
        self.assertIs(len(DOCKER_CLIENT.volumes.list()), num_default_vols)
        self.assertIs(len(DOCKER_CLIENT.images.list(all=True)), num_default_images)
        self.assertIs(len(DOCKER_CLIENT.networks.list()), num_default_nets)


def clean_cts():
    cts = DOCKER_CLIENT.containers.list(all=True)
    for ct in cts:
        try:
            ct.stop()
            ct.remove(v=True, force=True)
        except NotFound:
            pass


def clean_images():
    images = DOCKER_CLIENT.images.list(all=True)
    for image in images:
        try:
            DOCKER_CLIENT.images.remove(image.id, force=True)
        except NotFound:
            pass


if __name__ == "__main__":
    unittest.main()
