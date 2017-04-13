#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testnatashas_demo_runModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_natashas_demo_run_model(self):
        from qube.src.models.natashas_demo_run import natashas_demo_run
        natashas_demo_run_data = natashas_demo_run(name='testname')
        natashas_demo_run_data.tenantId = "23432523452345"
        natashas_demo_run_data.orgId = "987656789765670"
        natashas_demo_run_data.createdBy = "1009009009988"
        natashas_demo_run_data.modifiedBy = "1009009009988"
        natashas_demo_run_data.createDate = str(int(time.time()))
        natashas_demo_run_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            natashas_demo_run_data.save()
            self.assertIsNotNone(natashas_demo_run_data.mongo_id)
            natashas_demo_run_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
