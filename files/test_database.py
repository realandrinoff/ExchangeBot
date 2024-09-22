import unittest
import os
from database import LanguageDatabase

class TestLanguageDatabase(unittest.TestCase):
    def setUp(self):
        self.db = LanguageDatabase("test.db")

    def tearDown(self):
        self.db.close()

        os.remove("test.db")

    def test_get_user_language(self):
        self.db.set_user_language(1, 'eng')

        lang = self.db.get_user_language(1)
        self.assertEqual(lang, 'eng')

    def test_update_existing_language(self):
        self.db.set_user_language(2, 'eng')
        self.db.set_user_language(2, 'kar')

        lang = self.db.get_user_language(2)
        self.assertEqual(lang, 'kar')

    def test_client_list(self):
        self.db.set_user_language(4, 'kar')
        self.db.set_user_language(1, 'eng')
        self.db.set_user_language(2, 'rus')
        self.db.set_user_language(3, 'ukr')

        clients = self.db.client_list()

        self.assertEqual(clients, [1, 2, 3, 4])

    def test_add_multiple_users(self):
        self.db.set_user_language(10, 'eng')
        self.db.set_user_language(20, 'ukr')

        lang1, lang2 = self.db.get_user_language(10), self.db.get_user_language(20)

        self.assertEqual(lang1, 'eng')
        self.assertEqual(lang2, 'ukr')

if __name__ == '__main__':
    unittest.main()
