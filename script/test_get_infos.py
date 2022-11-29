import unittest
import configparser

from get_infos import memorylist, whoami, list_process

config = configparser.RawConfigParser() 
config.read("config.txt")
username = config['settings']['username']


class get_infos_Test_Case(unittest.TestCase):
    # Test de la connexion avec whoami
    def test_connexion(self):
        self.assertEqual(whoami,username)

    def test_memory(self):
        self.assertEqual(len(memorylist),6)
        for i in range(6):
            self.assertNotEqual(memorylist[i],0)
    
    def test_process(self):
        for i in range(len(list_process)):
            self.assertNotEqual(list_process[i].user,'')
            self.assertNotEqual(list_process[i].memory,0)
            self.assertNotEqual(list_process[i].pid, 0)
            self.assertNotEqual(list_process[i].start_time, "")
            self.assertNotEqual(list_process[i].command, "")
