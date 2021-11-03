import unittest
import os

from api.utils.storage import Storage

from dotenv import load_dotenv
load_dotenv('test.env')

class TestApi(unittest.TestCase):

    def test_local_list_files(self):
        try:
            files = Storage('local').list()
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertGreater(len(files), 0)
    
    def test_s3_list_files(self):
        try:
            files = Storage('s3').list()
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertGreater(len(files), 0)
    
    def test_local_read_file(self):
        try:
            content = Storage('local').get('test.txt')
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertIsNotNone(content)
    
    def test_s3_read_file(self):
        try:
            content = Storage('s3').get('test.txt')
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertIsNotNone(content)
    
    def test_local_write_file(self):
        try:
            written = Storage('local').put('test2.txt', bytes('this is an another example', 'utf-8'))
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertTrue(written)
    
    def test_s3_write_file(self):
        try:
            written = Storage('s3').put('test2.txt', bytes('this is an another example', 'utf-8'))
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertTrue(written)
    
    def test_local_delete_file(self):
        try:
            deleted = Storage('local').delete('test2.txt')
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertTrue(deleted)
    
    def test_s3_delete_file(self):
        try:
            deleted = Storage('s3').delete('test2.txt')
        except Exception as e:
            print(e)
            self.assertTrue(False)

        self.assertTrue(deleted)

