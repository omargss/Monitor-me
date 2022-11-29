import unittest
import configparser

#TODO : changer processList (adapter à ce que mathys à fait)

from get_infos import memorylist, whoami, processList

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
    
    def test_process(self):
        i=0
        while(i<len(processList)):
            self.assertNotEqual(processList[i].name,'')
            self.assertNotEqual(processList[i].memory,0)
            self.assertNotEqual(processList[i].pid, "")
