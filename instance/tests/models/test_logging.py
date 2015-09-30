# -*- coding: utf-8 -*-
#
# OpenCraft -- tools to aid developing and hosting free software projects
# Copyright (C) 2015 OpenCraft <xavier@opencraft.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Logger models & mixins - Tests
"""

# Imports #####################################################################

from freezegun import freeze_time

from instance.tests.base import TestCase
from instance.tests.models.factories.instance import OpenEdXInstanceFactory
from instance.tests.models.factories.server import OpenStackServerFactory


# Tests #######################################################################

# Factory boy doesn't properly support pylint+django
#pylint: disable=no-member

class LoggerInstanceMixinTestCase(TestCase):
    """
    Test cases for LoggerInstanceMixin
    """
    def test_log(self):
        """
        Check `log` output for combination of instance & server logs
        """
        instance = OpenEdXInstanceFactory()
        server = OpenStackServerFactory(instance=instance)

        with freeze_time("2015-08-05 18:07:00"):
            instance.log('info', 'Line #1, on instance')

        with freeze_time("2015-08-05 18:07:01"):
            server.log('info', 'Line #2, on server')

        with freeze_time("2015-08-05 18:07:02"):
            instance.log('debug', 'Line #3, on instance (debug, not published by default)')

        with freeze_time("2015-08-05 18:07:03"):
            instance.log('info', 'Line #4, on instance')

        with freeze_time("2015-08-05 18:07:04"):
            instance.log('warn', 'Line #5, on instance (warn)')

        with freeze_time("2015-08-05 18:07:05"):
            server.log('info', 'Line #6, on server')

        with freeze_time("2015-08-05 18:07:06"):
            server.log('exception', 'Line #7, on server (exception)')

        self.assertEqual(instance.log_entries, [
            "2015-08-05 18:07:00 [info] Line #1, on instance",
            "2015-08-05 18:07:01 [info] Line #2, on server",
            "2015-08-05 18:07:03 [info] Line #4, on instance",
            "2015-08-05 18:07:04 [warn] Line #5, on instance (warn)",
            "2015-08-05 18:07:05 [info] Line #6, on server",
            "2015-08-05 18:07:06 [exception] Line #7, on server (exception)"])
