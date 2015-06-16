"""Freezer restore.py related tests

Copyright 2014 Hewlett-Packard

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This product includes cryptographic software written by Eric Young
(eay@cryptsoft.com). This product includes software written by Tim
Hudson (tjh@cryptsoft.com).
========================================================================

"""

from commons import *
from freezer.restore import (
    restore_fs, restore_fs_sort_obj, RestoreOs)
from freezer import swift
import freezer
import logging
import pytest


class TestRestore:

    def test_restore_fs(self, monkeypatch):

        backup_opt = BackupOpt1()
        fakelogging = FakeLogging()

        monkeypatch.setattr(logging, 'critical', fakelogging.critical)
        monkeypatch.setattr(logging, 'warning', fakelogging.warning)
        monkeypatch.setattr(logging, 'exception', fakelogging.exception)
        monkeypatch.setattr(logging, 'error', fakelogging.error)
        monkeypatch.setattr(
            freezer.restore, 'restore_fs_sort_obj', fake_restore_fs_sort_obj)
        assert restore_fs(backup_opt) is None

        backup_opt = BackupOpt1()
        backup_opt.container = None
        pytest.raises(Exception, restore_fs, backup_opt)

        backup_opt = BackupOpt1()
        backup_opt.restore_from_date = None
        assert restore_fs(backup_opt) is None

    def test_restore_fs_sort_obj(self, monkeypatch):

        fakelogging = FakeLogging()
        # TEST 1
        backup_opt = BackupOpt1()
        fakemultiprocessing = FakeMultiProcessing()
        monkeypatch.setattr(logging, 'critical', fakelogging.critical)
        monkeypatch.setattr(logging, 'warning', fakelogging.warning)
        monkeypatch.setattr(logging, 'exception', fakelogging.exception)
        monkeypatch.setattr(logging, 'error', fakelogging.error)
        monkeypatch.setattr(multiprocessing, 'Process', fakemultiprocessing.Process)
        assert restore_fs_sort_obj(backup_opt) is None

        # TEST 2
        backup_opt = BackupOpt1()
        backup_opt.backup_name = 'abcdtest'
        monkeypatch.setattr(multiprocessing, 'Process', fakemultiprocessing.Process)
        pytest.raises(Exception, restore_fs_sort_obj, backup_opt)

        # TEST 3
        backup_opt = BackupOpt1()
        fakemultiprocessing = FakeMultiProcessing1()
        monkeypatch.setattr(multiprocessing, 'Process', fakemultiprocessing.Process)
        pytest.raises(Exception, restore_fs_sort_obj, backup_opt)

    def test_restore_cinder_by_glance(self):
        backup_opt = BackupOpt1()
        ros = RestoreOs(backup_opt.client_manager, backup_opt.container)
        ros.restore_cinder_by_glance(backup_opt.restore_from_date, 34)

    def test_restore_cinder(self):
        backup_opt = BackupOpt1()
        ros = RestoreOs(backup_opt.client_manager, backup_opt.container)
        ros.restore_cinder(backup_opt.restore_from_date, 34)


    def test_restore_nova(self):
        backup_opt = BackupOpt1()
        ros = RestoreOs(backup_opt.client_manager, backup_opt.container)
        ros.restore_nova(backup_opt.restore_from_date, 34)


