#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['NATASHAS_DEMO_RUN_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['NATASHAS_DEMO_RUN_MONGOALCHEMY_SERVER'] = ''
    os.environ['NATASHAS_DEMO_RUN_MONGOALCHEMY_PORT'] = ''
    os.environ['NATASHAS_DEMO_RUN_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.natashas_demo_run import natashas_demo_run
    from qube.src.services.natashas_demo_runservice import natashas_demo_runService
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, natashas_demo_runServiceError


class Testnatashas_demo_runService(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.natashas_demo_runService = natashas_demo_runService(context)
        self.natashas_demo_run_api_model = self.createTestModelData()
        self.natashas_demo_run_data = self.setupDatabaseRecords(self.natashas_demo_run_api_model)
        self.natashas_demo_run_someoneelses = \
            self.setupDatabaseRecords(self.natashas_demo_run_api_model)
        self.natashas_demo_run_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.natashas_demo_run_someoneelses.save()
        self.natashas_demo_run_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.natashas_demo_run_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.natashas_demo_run_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, natashas_demo_run_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            natashas_demo_run_data = natashas_demo_run(name='test_record')
            for key in natashas_demo_run_api_model:
                natashas_demo_run_data.__setattr__(key, natashas_demo_run_api_model[key])

            natashas_demo_run_data.description = 'my short description'
            natashas_demo_run_data.tenantId = "23432523452345"
            natashas_demo_run_data.orgId = "987656789765670"
            natashas_demo_run_data.createdBy = "1009009009988"
            natashas_demo_run_data.modifiedBy = "1009009009988"
            natashas_demo_run_data.createDate = str(int(time.time()))
            natashas_demo_run_data.modifiedDate = str(int(time.time()))
            natashas_demo_run_data.save()
            return natashas_demo_run_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_natashas_demo_run(self, *args, **kwargs):
        result = self.natashas_demo_runService.save(self.natashas_demo_run_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.natashas_demo_run_api_model['name'])
        natashas_demo_run.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_natashas_demo_run(self, *args, **kwargs):
        self.natashas_demo_run_api_model['name'] = 'modified for put'
        id_to_find = str(self.natashas_demo_run_data.mongo_id)
        result = self.natashas_demo_runService.update(
            self.natashas_demo_run_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.natashas_demo_run_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_natashas_demo_run_description(self, *args, **kwargs):
        self.natashas_demo_run_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.natashas_demo_run_data.mongo_id)
        result = self.natashas_demo_runService.update(
            self.natashas_demo_run_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.natashas_demo_run_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_natashas_demo_run_item(self, *args, **kwargs):
        id_to_find = str(self.natashas_demo_run_data.mongo_id)
        result = self.natashas_demo_runService.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_natashas_demo_run_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(natashas_demo_runServiceError):
            self.natashas_demo_runService.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_natashas_demo_run_list(self, *args, **kwargs):
        result_collection = self.natashas_demo_runService.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.natashas_demo_run_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.natashas_demo_run_data.mongo_id)
        with self.assertRaises(natashas_demo_runServiceError) as ex:
            self.natashas_demo_runService.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.natashas_demo_run_data.mongo_id)
        self.natashas_demo_runService.auth_context.is_system_user = True
        self.natashas_demo_runService.delete(id_to_delete)
        with self.assertRaises(natashas_demo_runServiceError) as ex:
            self.natashas_demo_runService.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.natashas_demo_runService.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.natashas_demo_run_someoneelses.mongo_id)
        with self.assertRaises(natashas_demo_runServiceError):
            self.natashas_demo_runService.delete(id_to_delete)
