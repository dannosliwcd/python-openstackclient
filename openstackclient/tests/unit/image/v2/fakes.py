#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import random
from unittest import mock
import uuid

from openstack.image.v2 import image
from openstack.image.v2 import member
from openstack.image.v2 import task

from openstackclient.tests.unit import fakes
from openstackclient.tests.unit.identity.v3 import fakes as identity_fakes
from openstackclient.tests.unit import utils


class FakeImagev2Client:

    def __init__(self, **kwargs):
        self.images = mock.Mock()
        self.create_image = mock.Mock()
        self.delete_image = mock.Mock()
        self.update_image = mock.Mock()
        self.find_image = mock.Mock()
        self.get_image = mock.Mock()
        self.download_image = mock.Mock()
        self.reactivate_image = mock.Mock()
        self.deactivate_image = mock.Mock()

        self.members = mock.Mock()
        self.add_member = mock.Mock()
        self.remove_member = mock.Mock()
        self.update_member = mock.Mock()

        self.remove_tag = mock.Mock()

        self.tasks = mock.Mock()
        self.get_task = mock.Mock()

        self.auth_token = kwargs['token']
        self.management_url = kwargs['endpoint']
        self.version = 2.0

        self.tasks = mock.Mock()
        self.tasks.resource_class = fakes.FakeResource(None, {})


class TestImagev2(utils.TestCommand):

    def setUp(self):
        super().setUp()

        self.app.client_manager.image = FakeImagev2Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )

        self.app.client_manager.identity = identity_fakes.FakeIdentityv3Client(
            endpoint=fakes.AUTH_URL,
            token=fakes.AUTH_TOKEN,
        )


def create_one_image(attrs=None):
    """Create a fake image.

    :param attrs: A dictionary with all attributes of image
    :type attrs: dict
    :return: A fake Image object.
    :rtype: `openstack.image.v2.image.Image`
    """
    attrs = attrs or {}

    # Set default attribute
    image_info = {
        'id': str(uuid.uuid4()),
        'name': 'image-name' + uuid.uuid4().hex,
        'owner_id': 'image-owner' + uuid.uuid4().hex,
        'is_protected': bool(random.choice([0, 1])),
        'visibility': random.choice(['public', 'private']),
        'tags': [uuid.uuid4().hex for r in range(2)],
    }

    # Overwrite default attributes if there are some attributes set
    image_info.update(attrs)

    return image.Image(**image_info)


def create_images(attrs=None, count=2):
    """Create multiple fake images.

    :param attrs: A dictionary with all attributes of image
    :type attrs: dict
    :param count: The number of images to be faked
    :type count: int
    :return: A list of fake Image objects
    :rtype: list
    """
    images = []
    for n in range(0, count):
        images.append(create_one_image(attrs))

    return images


def create_one_image_member(attrs=None):
    """Create a fake image member.

    :param attrs: A dictionary with all attributes of image member
    :type attrs: dict
    :return: A fake Member object.
    :rtype: `openstack.image.v2.member.Member`
    """
    attrs = attrs or {}

    # Set default attribute
    image_member_info = {
        'member_id': 'member-id-' + uuid.uuid4().hex,
        'image_id': 'image-id-' + uuid.uuid4().hex,
        'status': 'pending',
    }

    # Overwrite default attributes if there are some attributes set
    image_member_info.update(attrs)

    return member.Member(**image_member_info)


def create_one_task(attrs=None):
    """Create a fake task.

    :param attrs: A dictionary with all attributes of task
    :type attrs: dict
    :return: A fake Task object.
    :rtype: `openstack.image.v2.task.Task`
    """
    attrs = attrs or {}

    # Set default attribute
    task_info = {
        'created_at': '2016-06-29T16:13:07Z',
        'expires_at': '2016-07-01T16:13:07Z',
        'id': str(uuid.uuid4()),
        'input': {
            'image_properties': {
                'container_format': 'ovf',
                'disk_format': 'vhd'
            },
            'import_from': 'https://apps.openstack.org/excellent-image',
            'import_from_format': 'qcow2'
        },
        'message': '',
        'owner': str(uuid.uuid4()),
        'result': {
            'image_id': str(uuid.uuid4()),
        },
        'schema': '/v2/schemas/task',
        'status': random.choice(
            [
                'pending',
                'processing',
                'success',
                'failure',
            ]
        ),
        # though not documented, the API only allows 'import'
        # https://github.com/openstack/glance/blob/24.0.0/glance/api/v2/tasks.py#L186-L190
        'type': 'import',
        'updated_at': '2016-06-29T16:13:07Z',
    }

    # Overwrite default attributes if there are some attributes set
    task_info.update(attrs)

    return task.Task(**task_info)


def create_tasks(attrs=None, count=2):
    """Create multiple fake tasks.

    :param attrs: A dictionary with all attributes of Task
    :type attrs: dict
    :param count: The number of tasks to be faked
    :type count: int
    :return: A list of fake Task objects
    :rtype: list
    """
    tasks = []
    for n in range(0, count):
        tasks.append(create_one_task(attrs))

    return tasks
