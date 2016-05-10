# (C) Copyright 2016 Hewlett Packard Enterprise Development Company LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import os
import shutil

import datetime
import subprocess

from freezer.tests.freezer_tempest_plugin.tests.api import base
from tempest import test


class TestFreezerSwiftBackup(base.BaseFreezerTest):

    def __init__(self, *args, **kwargs):

        super(TestFreezerSwiftBackup, self).__init__(*args, **kwargs)

    def setUp(self):

        super(TestFreezerSwiftBackup, self).setUp()

        now_in_secs = datetime.datetime.now().strftime("%s")

        self.backup_source_dir = ("/tmp/freezer-test-backup-source/"
                             + now_in_secs)
        self.backup_source_sub_dir = self.backup_source_dir + "/subdir"

        self.restore_target_dir = (
            "/tmp/freezer-test-backup-restore/"
            + now_in_secs)

        self.freezer_container_name = 'freezer-test-container-0'
        self.freezer_backup_name = 'freezer-test-backup-swift-0'

        shutil.rmtree(self.backup_source_dir, True)
        os.makedirs(self.backup_source_dir)
        open(self.backup_source_dir + "/a", 'w').close()
        open(self.backup_source_dir + "/b", 'w').close()
        open(self.backup_source_dir + "/c", 'w').close()

        os.makedirs(self.backup_source_sub_dir)
        open(self.backup_source_sub_dir + "/x", 'w').close()
        open(self.backup_source_sub_dir + "/y", 'w').close()
        open(self.backup_source_sub_dir + "/z", 'w').close()

        shutil.rmtree(self.restore_target_dir, True)
        os.makedirs(self.restore_target_dir)

        self.environ = super(TestFreezerSwiftBackup, self).get_environ()

    def tearDown(self):

        super(TestFreezerSwiftBackup, self).tearDown()

        shutil.rmtree(self.backup_source_dir, True)
        shutil.rmtree(self.restore_target_dir, True)


    @test.attr(type="gate")
    def test_freezer_swift_backup(self):

        backup_args = ['freezer-agent',
                       '--path-to-backup',
                       self.backup_source_dir,
                       '--container',
                       self.freezer_container_name,
                       '--backup-name',
                       self.freezer_backup_name]

        output = subprocess.check_output(backup_args,
                                         stderr=subprocess.STDOUT,
                                         env=self.environ, shell=False)

        restore_args = ['freezer-agent',
                        '--action',
                        'restore',
                        '--restore-abs-path',
                        self.restore_target_dir,
                        '--container',
                        self.freezer_container_name,
                        '--backup-name',
                        self.freezer_backup_name,
                        '--storage',
                        'swift']

        output = subprocess.check_output(restore_args,
                                         stderr=subprocess.STDOUT,
                                         env=self.environ, shell=False)

        diff_args = ['diff',
                     '-r',
                     '-q',
                     self.backup_source_dir,
                     self.restore_target_dir]

        diff_rc = subprocess.call(diff_args,
                                  shell=False)

        self.assertEqual(0, diff_rc, "Test backup to swift and restore")