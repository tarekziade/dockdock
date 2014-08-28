import docker
import random

# see https://docs.docker.com/examples/running_ssh_service/


class Docker(object):

    def __init__(self, host='tcp://192.168.59.103:2375'):
        self.c = docker.Client(host)
        self.name = self.image = None

    def _build(self):
        self.image = 'sshd-%d' % random.randint(1, 9999)
        self.c.build('.', tag=self.image)

    def _create_container(self):
        """creates a container with an ssh service
        """
        name = 'loads_%d' % random.randint(1, 9999)
        container = self.c.create_container(self.image, name=name)
        id = container['Id']
        self.c.start(container=id, publish_all_ports=True)
        self.name = name
        return name, self.c.port(name, 22)[0]['HostPort']

    def start(self):
        self._build()
        return self._create_container()

    def stop(self):
        self.c.stop(self.name)
        self.c.remove_container(self.name)
        self.c.remove_image(self.image)



d = Docker()
print d.start()
d.stop()

