# -*- coding: utf-8 -*-

import datetime
import pytest
import io

import UDIdriver


class FakeDriver(object):
    def __init__(self, cfg):
        self.cfg = cfg
        self.first_apt = datetime.datetime(2019, 3, 7)

    def run(self):
        return self.cfg['wait_if_earlier_than'] < self.first_apt


def test_config():
    cfg = io.StringIO(u'''{
    "username": "someone@somewhere.com",
    "password": "hunter2",
    "wait_if_earlier_than": "2019-02-03"
}''')

    assert not UDIdriver.main(FakeDriver, cfg)
