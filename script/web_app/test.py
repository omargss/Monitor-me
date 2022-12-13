'''Fichier de Test des fonctions de l'interface'''
import unittest
from functions import *
from connection import client


class FunctionsTestCase(unittest.TestCase):
    """Test case for the functions used in the web app"""
    def test_get_memory(self):
        """Test for the get_memory function"""
        self.assertNotEqual(get_memory(client), 0)

    def test_get_process(self):
        """Test for the get_process_infos function"""
        process_list = get_process_infos(client)
        for process in process_list:
            self.assertNotEqual(process.user, '')
            self.assertNotEqual(process.memory, 0)
            self.assertNotEqual(process.start_time, '')
            self.assertNotEqual(process.command, '')
            self.assertNotEqual(process.pid, 0)

    def test_analyze_logs(self):
        """Test the analyze log"""
        with open('other_vhosts_access.log') as f:
            logs = f.read()
        logsAnalyses = AnalyzeLogs(logs)
        for log in logsAnalyses:
            if(log.name == "/?s=s"):
                self.assertEqual(log.numberOfSearchs,1)
            if(log.name == "/?cat=1"):
                self.assertEqual(log.numberOfSearchs,2)
            if(log.name == "/?p=1"):
                self.assertEqual(log.numberOfSearchs,4)
            if(log.name == "/?s=jfzoiejflz"):
                self.assertEqual(log.numberOfSearchs,1)
