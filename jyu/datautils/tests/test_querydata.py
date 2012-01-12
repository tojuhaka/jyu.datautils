# -*- coding: utf-8 -*-
import datetime
import unittest
from jyu.datautils.querydata import KeyGenerator 
from jyu.datautils.tests.query_test_data import test_result, test_result2
from jyu.datautils.persist import to_persistent, to_normal
import persistent

class DummyTutkaQueryObj(object):
    def __init__(self):
        self.query = {}
        self.query['section'] = 'julkaisut'
        self.query['tutka_type'] = 'Studysubject'
        self.query['date_start'] = datetime.date(2011, 1, 1)
        self.query['date_end'] = datetime.date(2012, 1, 1)
        self.query['atk_username'] = None
        self.query['organization'] = 'jyu_6'
        self.query['studysubject'] = None

        self.query2 = {}
        self.query2['section'] = 'esitykset'
        self.query2['tutka_type'] = 'Studysubject'
        self.query2['date_start'] = datetime.date(2011, 1, 1)
        self.query2['date_end'] = datetime.date(2012, 1, 1)
        self.query2['atk_username'] = None
        self.query2['organization'] = 'jyu_6'
        self.query2['studysubject'] = None
        
        self.query4 = {}
        self.query4['section'] = 'esitykset'
        self.query4['tutka_type'] = 'Studysubject'
        self.query4['date_start'] = datetime.date(2011, 1, 1)
        self.query4['date_end'] = datetime.date(2012, 1, 1)
        self.query4['atk_username'] = None
        self.query4['organization'] = 'jyu_8'
        self.query4['studysubject'] = None

        self.query3 = {}
        self.query3['section'] = 'esitykset'
        self.query3['tutka_type'] = 'Researcher'
        self.query3['date_start'] = datetime.date(2011, 1, 1)
        self.query3['date_end'] = None
        self.query3['atk_username'] = None
        self.query3['organization'] = 'jyu_20'
        self.query3['studysubject'] = None

class QueryDataTest(unittest.TestCase):

    def setUp(self):
        obj = DummyTutkaQueryObj()
        self.obj = obj
        self.first_query = obj.query
        self.second_query = obj.query2
        self.third_query = obj.query3

        self.recur_test_query = {
            'asdf': ['äöesd', 'AsÄlä'],
                'olololol': {'asdfg': 'päsdfö', 'äes': 'päsähti',  'däcti': 
                    {'testiä': 'testip'}
                },
            'testi': 'yeah'
        }

        self.test_result = test_result
        self.test_result2 = test_result2

        self.first_query_key = KeyGenerator(self.first_query).generate()
        self.second_query_key = KeyGenerator(self.second_query).generate()
        self.test_result_key = KeyGenerator(self.test_result).generate()
        self.test_result2_key = KeyGenerator(self.test_result2).generate()

    def test_key_change(self):
        result_key = KeyGenerator(self.recur_test_query).generate()
        self.recur_test_query['asdf']['olololol']['asdfg'] = ['s', 'v', 'k']

        changed_result_key = KeyGenerator(self.recur_test_query).generate()
        self.assertNotEquals(changed_result_key, result_key)

    def test_key_generate_special(self):
        # Test special characters
        key = KeyGenerator("jyu_30").generate()
        key2 = KeyGenerator("jyu_31").generate()
        self.assertNotEquals(key, key2)

    def test_key_generate_dif(self):
        self.assertNotEquals(self.first_query_key, self.second_query_key, "Different queries will have different keys")
        self.assertNotEquals(self.test_result_key, self.test_result2_key, "Different queries will have different keys")
        #additional test
        obj = DummyTutkaQueryObj()

        key = KeyGenerator(obj.query4).generate()
        key2 = KeyGenerator(obj.query2).generate()
        self.assertNotEquals(key, key2, "Different queries will have different keys")
        

    def test_key_generate_equal(self):
        self.assertTrue(KeyGenerator(self.second_query).generate() == KeyGenerator(self.second_query).generate(),"Similar queries will have similar keys")
        self.assertTrue(KeyGenerator(self.third_query).generate() == KeyGenerator(self.third_query).generate(),"Similar queries will have similar keys ")
        self.assertTrue(KeyGenerator(self.first_query).generate() == KeyGenerator(self.first_query).generate(), "Similar queries will have similar keys")

    def test_key_generate_recur(self):
        self.assertTrue(type(KeyGenerator(self.recur_test_query).generate()) == type('asd'))


    def test_keygenerator_final(self):
        key = KeyGenerator(self.obj.query3).generate()
        key2 = KeyGenerator(self.obj.query3).generate()
        key3 = KeyGenerator(self.obj.query3).generate()
        key4 = KeyGenerator(self.obj.query3).generate()

        self.assertEquals(key, key2)
        self.assertEquals(key, key3)
        self.assertEquals(key, key4)
        self.assertEquals(key2, key2)
        self.assertEquals(key2, key3)
        self.assertEquals(key2, key4)


    def test_persistent_converter(self):
        data = to_persistent(self.recur_test_query)
        self.is_persistent(data) 

        normal_data = to_normal(data)
        self.is_normal(normal_data)
   
    # METHODS FOR RECURSIVE TESTING
    def is_persistent(self, data):
        # For recursive testing
        if not isinstance(data, persistent.Persistent):
            if type(data) == list:
                self.assertEquals(1,2, "list should be persistent")
            if type(data) == dict:
                self.assertEquals(1,2, "dict should be persistent")

        if isinstance(data, persistent.Persistent):
            try:
                _list = data.values()
            except AttributeError:
                _list = data

            for item in _list:
                self.is_persistent(item)
    
    def is_normal(self, data):
        # For recursive testing
        if not isinstance(data, list) or not isinstance(data, dict):
            if isinstance(data, persistent.Persistent):
                self.assertEquals(1,2, "list should be persistent")

        if isinstance(data, list) or isinstance(data, dict):
            try:
                _list = data.values()
            except AttributeError:
                _list = data

            for item in _list:
                self.is_normal(item)



