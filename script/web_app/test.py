'''Fichier de Test des fonctions de l'interface'''
import unittest
from functions import get_memory, getProcessInfos
from connection import client


class FunctionsTestCase(unittest.TestCase):
    """Test case for the functions used in the web app"""
    def test_get_memory(self):
        """Test for the get_memory function"""
        self.assertNotEqual(get_memory(client), 0)

    def test_get_process(self):
        """Test for the get_process_infos function"""
        process_list = getProcessInfos(client)
        for process in process_list:
            self.assertNotEqual(process.user, '')
            self.assertNotEqual(process.memory, 0)
            self.assertNotEqual(process.start_time, '')
            self.assertNotEqual(process.command, '')
            self.assertNotEqual(process.pid, 0)
