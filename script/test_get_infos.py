import unittest
import configparser

from get_infos import memorylist, whoami

config = configparser.RawConfigParser() 
config.read("config.txt")
username = config['settings']['username']


class get_infos_Test_Case(unittest.TestCase):
    # Test de la connexion avec whoami
    def test_connexion(self):
        self.assertEqual(whoami,username)

    def test_memory(self):
        self.assertEqual(len(memorylist),6)
        i=0
        while(i<6):
            self.assertNotEqual(memorylist[i],0)
            i+=1
