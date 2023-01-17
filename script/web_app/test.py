'''Fichier de Test des fonctions de l'interface'''
import unittest
from functions import AnalyzeLogs, analyze_error_logs

class FunctionsTestCase(unittest.TestCase):
    """Test case for the functions used in the web app"""

    def test_analyze_logs(self):
        """Test the analyze log"""
        with open('test_log_files/other_vhosts_access.log', encoding="utf-8") as file:
            logs = file.read()
        logs_analyses = AnalyzeLogs(logs)
        for log in logs_analyses:
            if log.name == "/?s=s":
                self.assertEqual(log.numberOfSearchs, 1)
            if log.name == "/?cat=1":
                self.assertEqual(log.numberOfSearchs, 2)
            if log.name == "/?p=1":
                self.assertEqual(log.numberOfSearchs, 4)
            if log.name == "/?s=jfzoiejflz":
                self.assertEqual(log.numberOfSearchs, 1)

    def test_analyze_error_logs(self):
        """Test the function analyze_error_logs"""
        with open('test_log_files/error_test.log', encoding="utf-8") as file:
            logs = file.read()
        warn_list,_,_, crit_list, error_list,_, notice_list, _ = analyze_error_logs(logs)
        self.assertEqual(len(notice_list), 1)
        self.assertEqual(len(error_list), 3)
        self.assertEqual(len(warn_list), 1)
        self.assertEqual(len(crit_list), 1)
